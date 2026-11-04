#!/usr/bin/env python3
"""Check the form and traceability of a feature's artifacts.

    python tools/check.py                              all features (features/, examples/)
    python tools/check.py features/<ID>                one feature
    python tools/check.py features/<ID>/specs/SPEC-03-x.md   one file (the feature is still read whole)
    python tools/check.py features/<ID> --gate contracts     ready to plan the spec set
    python tools/check.py features/<ID> --gate ready         spec set ready for delivery
    python tools/check.py features/<ID> --trace        write traceability.md
    python tools/check.py features/<ID> --next         next free IDs

Output: "E|W path[:line] - [code] message", then a summary. E - error, W - warning.
How strict a rule is depends on the feature status in its passport: a check that
belongs to a later stage is a warning before that stage and an error after it.
Gates raise the stage. Exit code: 0 - no errors, 1 - errors, 2 - usage error.

The checker sees form, not meaning: a pass means "nothing is visibly missing or
inconsistent", never "the specs are right". Meaning is checked by people.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sddlib  # noqa: E402
from sddlib import STAGES, ID_PATTERNS  # noqa: E402

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CYR_ID = re.compile(r"(?<![\w-])([A-Za-zЀ-ӿ]{1,6})-(\d{2,})(?![\w])")
PLACEHOLDER = re.compile(r"<(?!!--)(?!/?(?:br|b|i|u|s|em|strong|sup|sub|details|summary|kbd|a|img|p|div|span|code|pre)\b)"
                         r"[^<>\n]{1,80}>")
SPEC_STATUSES = ["draft", "review", "approved", "superseded"]
CONTRACT_STATUSES = ["draft", "review", "approved"]
Q_STATUSES = ["open", "answered", "deferred"]
DECISION_KINDS = ["business", "technical", "external"]
MANUAL_TYPES = ["decision", "edit", "approval", "rejection"]


class Report:
    def __init__(self, root, only=None):
        self.root = root
        self.only = [os.path.abspath(p) for p in only] if only else None
        self.items = []
        self.outside = 0

    def add(self, sev, path, code, msg, line=None):
        if self.only:
            ap = os.path.abspath(path)
            if not any(ap == o or ap.startswith(o + os.sep) for o in self.only):
                self.outside += 1
                return
        self.items.append((sev, sddlib.rel(path, self.root), line, code, msg))

    @property
    def errors(self):
        return sum(1 for i in self.items if i[0] == "E")

    @property
    def warnings(self):
        return sum(1 for i in self.items if i[0] == "W")

    def print(self):
        for sev, path, line, code, msg in self.items:
            where = "%s:%d" % (path, line + 1) if line is not None else path
            print("%s %s - [%s] %s" % (sev, where, code, msg))


class Feature:
    def __init__(self, fdir, root, cfg, report):
        self.dir = fdir
        self.root = root
        self.cfg = cfg
        self.r = report
        self.scope_in = cfg["scope"]["in"]
        self.scope_out = cfg["scope"]["out"]
        self.stage = 0
        self.gate = None
        self.meta = {}
        self.id = os.path.basename(fdir)
        self.src_secs = []
        self.src_lines = []
        self.nums = []
        self.analysis = None
        self.reqs = {}
        self.inactive = {}
        self.questions = {}
        self.decisions = {}
        self.manual = {}
        self.cards = {}
        self.registry = {}
        self.registry_meta = None
        self.registry_groups = {}
        self.no_contract = {}
        self.plan = {}
        self.specs = {}

    # ------------------------------------------------------------ helpers

    def p(self, *parts):
        return os.path.join(self.dir, *parts)

    def sev(self, stage):
        return "E" if self.stage >= STAGES.index(stage) else "W"

    def add(self, sev, path, code, msg, line=None):
        self.r.add(sev, path, code, msg, line)

    def active(self, rid):
        return rid in self.reqs and rid not in self.inactive

    def in_scope(self, rid):
        return self.active(rid) and self.reqs[rid]["scope"] == self.scope_in

    def md_files(self):
        out = []
        for base, dirs, files in os.walk(self.dir):
            relp = os.path.relpath(base, self.dir).replace("\\", "/")
            if relp == "source/import" or relp.startswith("source/import/"):
                dirs[:] = []
                continue
            for f in sorted(files):
                if f.endswith(".md"):
                    out.append(os.path.join(base, f))
        return sorted(out)

    def is_source(self, path):
        relp = os.path.relpath(path, self.dir).replace("\\", "/")
        return relp.startswith("source/")


# ====================================================================== loading

def load(F):
    readme = F.p("README.md")
    lines = sddlib.read_lines(readme)
    meta, _ = sddlib.parse_frontmatter(lines)
    F.meta = meta or {}
    status = F.meta.get("status", "")
    if status in STAGES:
        F.stage = STAGES.index(status)
    elif status in ("hold", "cancelled"):
        F.stage = 1
    F.id = F.meta.get("id") or F.id

    src = F.p("source", "source.md")
    if os.path.isfile(src):
        F.src_lines, F.src_secs = sddlib.parse_source(src)
        F.nums = [s["num"] for s in F.src_secs]
    if os.path.isfile(F.p("analysis.md")):
        F.analysis = sddlib.parse_analysis(F.p("analysis.md"))


# ====================================================================== checks: files

def check_files(F):
    cfg = F.cfg
    fchars = cfg["style"].get("forbidden_chars") or {}
    fwords = cfg["style"].get("forbidden_words") or {}
    for path in F.md_files():
        lines = sddlib.read_lines(path)
        meta, body = sddlib.parse_frontmatter(lines)
        if meta is None:
            F.add("E", path, "fm-none", "no frontmatter (--- type: ... ---) at the top of the file")
            continue
        if not meta.get("type"):
            F.add("E", path, "fm-type", "frontmatter has no 'type'")
        upd = meta.get("updated")
        if upd and not DATE.match(str(upd)):
            F.add("E", path, "fm-date", "updated: '%s' - use YYYY-MM-DD" % upd)
        if F.is_source(path):
            continue
        cm = sddlib.code_mask(lines)
        for i, line in enumerate(lines):
            for m in CYR_ID.finditer(line):
                prefix = m.group(1)
                if re.search(r"[Ѐ-ӿ]", prefix) and _looks_like_id(prefix):
                    F.add("E", path, "id-cyrillic", "ID '%s' contains Cyrillic letters - IDs are Latin only"
                          % m.group(0), i)
            if cm[i]:
                continue
            for ch, hint in fchars.items():
                if ch in line:
                    F.add("W", path, "style-char", "'%s' is not allowed by sdd.config.json: %s" % (ch, hint), i)
            for word, hint in fwords.items():
                if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", sddlib.strip_inline_code(line), re.I):
                    F.add("W", path, "style-word", "'%s': %s" % (word, hint), i)


def _looks_like_id(prefix):
    """True when a prefix with Cyrillic look-alike letters reads as one of our ID prefixes."""
    trans = str.maketrans("АВЕКМНОРСТХЅаеорсхѕ", "ABEKMHOPCTXSaeopcxs")
    return prefix.translate(trans).upper() in ("REQ", "Q", "M", "CON", "SPEC")


# ====================================================================== checks: passport

def check_passport(F):
    path = F.p("README.md")
    m = F.meta
    for key in ("id", "title", "status", "source", "owner", "updated"):
        if not m.get(key):
            F.add("E", path, "fm-missing", "passport: no '%s'" % key)
    if m.get("status") and m["status"] not in sddlib.FEATURE_STATUSES:
        F.add("E", path, "fm-status", "status '%s' - allowed: %s" % (m["status"], ", ".join(sddlib.FEATURE_STATUSES)))
    if m.get("id"):
        if not re.match(F.cfg["feature_id_pattern"], m["id"]):
            F.add("E", path, "fm-id", "feature id '%s' does not match feature_id_pattern" % m["id"])
        folder = os.path.basename(F.dir)
        if folder != m["id"] and not folder.startswith(m["id"] + "-"):
            F.add("E", path, "fm-id", "folder '%s' must be '<id>' or '<id>-<slug>'" % folder)


# ====================================================================== checks: source and domain map

def check_map(F):
    src = F.p("source", "source.md")
    if not os.path.isfile(src):
        if F.stage >= 1:
            F.add(F.sev("analysis"), F.p("README.md"), "source-missing",
                  "no snapshot source/source.md - run tools/snapshot.py")
        return
    ana = F.p("analysis.md")
    a = F.analysis
    if a is None:
        if F.stage >= 1:
            F.add(F.sev("contracts"), F.p("README.md"), "analysis-missing", "no analysis.md with the domain map")
        return
    sev = F.sev("contracts")
    ui = F.cfg["ui_domain_prefix"]

    if not a["order"]:
        F.add(sev, ana, "domain-map", "section 'Domains' has no table 'Domain | Kind | ...' with rows")
    seen = set()
    for ln, name, cells in a["domain_rows"]:
        if name in seen:
            F.add("E", ana, "domain-dup", "domain %s is listed twice" % name, ln)
        seen.add(name)
        if not sddlib.DOMAIN_NAME.match(name):
            F.add("E", ana, "domain-name", "domain '%s' - use lowercase kebab-case" % name, ln)
        if cells[1].strip().lower() not in ("node", "edge"):
            F.add("E", ana, "domain-kind", "domain %s: kind '%s' - node or edge" % (name, cells[1]), ln)

    read_sets = {}
    slice_dir = F.p("source", "domains")
    for name in a["order"]:
        sl = a["slices"].get(name)
        if not sl or sl["items"] is None:
            F.add(sev, ana, "domain-read", "domain %s: no subsection with a 'Read:' list in 'Source slices'" % name,
                  a["domains"][name]["line"])
            continue
        text, errors = sddlib.build_slice(F.id, name, sl["items"], F.src_lines, F.src_secs)
        for ln, e in errors:
            F.add("E", ana, "domain-read", "domain %s: %s" % (name, e), ln)
        picked = set()
        for _, refs, _ in sl["items"]:
            picked |= sddlib.resolve_refs(refs, F.nums)[0]
        read_sets[name] = picked
        spath = os.path.join(slice_dir, name + ".md")
        if not os.path.isfile(spath):
            F.add(sev, ana, "domain-slice", "domain %s: slice source/domains/%s.md is missing - run tools/slices.py"
                  % (name, name), sl["line"])
        elif "\n".join(sddlib.read_lines(spath)) + "\n" != text:
            F.add(sev, spath, "domain-slice", "slice is stale (Read list or snapshot changed) - run tools/slices.py")
    for name in a["slices"]:
        if name not in a["domains"]:
            F.add("W", ana, "domain-read", "slice subsection '%s' has no domain in 'Domains'" % name,
                  a["slices"][name]["line"])
    if os.path.isdir(slice_dir):
        for f in sorted(os.listdir(slice_dir)):
            if f.endswith(".md") and f[:-3] not in a["domains"]:
                F.add("W", os.path.join(slice_dir, f), "domain-slice", "slice of a domain that is not in the map")

    listed = {}
    for ln, num, doms in a["index_rows"]:
        if num not in F.nums:
            F.add("E", ana, "domain-index", "section %s is not in the snapshot" % num, ln)
            continue
        listed[num] = (ln, doms)
        for d in doms:
            if d != "*" and d not in a["domains"]:
                F.add("E", ana, "domain-index", "section %s: unknown domain '%s'" % (num, d), ln)
    missing = [n for n in F.nums if n not in listed]
    if missing:
        F.add(sev, ana, "domain-index", "sections not in 'Sections by domain': %s" % ", ".join(missing[:20])
              + (" and %d more" % (len(missing) - 20) if len(missing) > 20 else ""))
    for name, picked in read_sets.items():
        for num in sorted(picked, key=F.nums.index):
            if num in listed and listed[num][1] != ["*"] and name not in listed[num][1]:
                F.add("W", ana, "domain-index", "section %s is in the Read list of %s but its row does not name it"
                      % (num, name), listed[num][0])
    for num, (ln, doms) in listed.items():
        for d in doms:
            if d in read_sets and num not in read_sets[d]:
                F.add("W", ana, "domain-index", "section %s names %s, but it is not in that domain's Read list"
                      % (num, d), ln)

    req_dir = F.p("requirements")
    for name in a["order"]:
        rp = os.path.join(req_dir, name + ".md")
        if not os.path.isfile(rp):
            F.add(sev, ana, "domain-file", "domain %s has no requirements/%s.md" % (name, name),
                  a["domains"][name]["line"])
            continue
        if name.startswith(ui):
            lines = sddlib.read_lines(rp)
            rng = sddlib.section(lines, "Screen fields", 2)
            rows = []
            if rng:
                for t in sddlib.tables(lines, rng[0], rng[1]):
                    rows += t["rows"]
            if not rows:
                F.add(sev, rp, "domain-ui", "UI domain needs a 'Screen fields' table: field or action -> source rule"
                      " -> operation")
        fnd = a["findings"].get(name)
        if fnd and fnd["pending"] and not fnd["applied"]:
            F.add(sev, ana, "domain-finding", "findings for %s are not marked 'Applied <date> in <file>'" % name,
                  fnd["line"])
    if os.path.isdir(req_dir):
        for f in sorted(os.listdir(req_dir)):
            if f.endswith(".md") and f not in ("README.md", "dispositions.md") and f[:-3] not in a["domains"]:
                F.add("E", os.path.join(req_dir, f), "domain-file",
                      "requirements file of a domain that is not in the map ('Domains' in analysis.md)")


# ====================================================================== checks: requirements

def check_requirements(F):
    req_dir = F.p("requirements")
    if not os.path.isdir(req_dir):
        if F.stage >= 2:
            F.add("E", F.p("README.md"), "req-missing", "no requirements/ folder")
        return
    if not os.path.isfile(os.path.join(req_dir, "README.md")):
        F.add("W", req_dir, "req-index", "requirements/README.md (index of domain files) is missing")
    types = F.cfg["requirement_types"]
    scopes = (F.scope_in, F.scope_out)
    for f in sorted(os.listdir(req_dir)):
        if not f.endswith(".md") or f in ("README.md", "dispositions.md"):
            continue
        path = os.path.join(req_dir, f)
        lines = sddlib.read_lines(path)
        meta, _ = sddlib.parse_frontmatter(lines)
        if meta and meta.get("type") != "requirements":
            F.add("E", path, "fm-type", "type must be 'requirements'")
        domain = f[:-3]
        for t in sddlib.tables(lines):
            if not t["header"] or t["header"][0] != "ID":
                continue
            for ln, cells in t["rows"]:
                rid = cells[0].strip()
                if not re.fullmatch(ID_PATTERNS["REQ"], rid):
                    if rid:
                        F.add("E", path, "req-id", "'%s' is not a requirement ID (REQ-NNN)" % rid, ln)
                    continue
                if len(cells) != 7:
                    F.add("E", path, "req-cols", "%s: %d columns, need 7: ID | Requirement | Source | Scenario | "
                          "Type | Scope | Note" % (rid, len(cells)), ln)
                    continue
                if rid in F.reqs:
                    F.add("E", path, "req-dup", "%s is also in %s" % (rid, sddlib.rel(F.reqs[rid]["path"], F.root)), ln)
                    continue
                refs = [x.strip() for x in cells[2].split(",") if x.strip()]
                F.reqs[rid] = {"path": path, "line": ln, "domain": domain, "text": cells[1], "source": cells[2],
                               "type": cells[4], "scope": cells[5], "note": cells[6]}
                if not cells[1]:
                    F.add("E", path, "req-text", "%s: empty requirement" % rid, ln)
                if not refs:
                    F.add("E", path, "req-source", "%s: no source section - every requirement cites the source" % rid,
                          ln)
                for ref in refs:
                    if F.nums and ref not in F.nums:
                        F.add("E", path, "req-source", "%s: source section %s is not in the snapshot" % (rid, ref), ln)
                if cells[4] not in types:
                    F.add("E", path, "req-type", "%s: type '%s' - allowed: %s" % (rid, cells[4], ", ".join(types)), ln)
                if cells[5] not in scopes:
                    F.add("E", path, "req-scope", "%s: scope '%s' - allowed: %s" % (rid, cells[5], ", ".join(scopes)),
                          ln)

    disp = os.path.join(req_dir, "dispositions.md")
    if os.path.isfile(disp):
        lines = sddlib.read_lines(disp)
        for t in sddlib.tables(lines):
            for ln, cells in t["rows"]:
                rid = cells[0].strip()
                if not re.fullmatch(ID_PATTERNS["REQ"], rid):
                    continue
                if len(cells) != 5:
                    F.add("E", disp, "req-disposition", "%s: need 5 columns: Requirement | State | Reason | Decision |"
                          " Replacement" % rid, ln)
                    continue
                state, reason, decision, repl = cells[1], cells[2], cells[3], cells[4]
                if rid not in F.reqs:
                    F.add("E", disp, "req-disposition", "%s is not in any requirements file" % rid, ln)
                if state not in ("excluded", "superseded"):
                    F.add("E", disp, "req-disposition", "%s: state '%s' - excluded or superseded" % (rid, state), ln)
                if not reason or reason == "-" or not decision or decision == "-":
                    F.add("E", disp, "req-disposition", "%s: reason and decision are required" % rid, ln)
                repls = sddlib.ids_in(repl, "REQ")
                if state == "superseded" and not repls:
                    F.add("E", disp, "req-disposition", "%s: superseded needs active replacement IDs" % rid, ln)
                F.inactive[rid] = {"state": state, "replacement": repls, "line": ln}
        for rid, d in F.inactive.items():
            for x in d["replacement"]:
                if x not in F.reqs or x in F.inactive:
                    F.add("E", disp, "req-disposition", "%s: replacement %s is not an active requirement" % (rid, x),
                          d["line"])


# ====================================================================== checks: questions and decisions

def _blocks(lines, prefix):
    out = []
    hs = sddlib.headings(lines)
    for idx, (ln, lv, t) in enumerate(hs):
        m = re.match(r"^(" + ID_PATTERNS[prefix] + r")\b\s*(.*)$", t)
        if lv != 3 or not m:
            continue
        end = hs[idx + 1][0] if idx + 1 < len(hs) else len(lines)
        out.append((ln, m.group(1), m.group(2), sddlib.bullet_fields(lines, ln + 1, end)))
    return out


def check_decisions(F):
    d = F.p("decisions")
    if not os.path.isdir(d):
        if F.stage >= 1:
            F.add("W", F.p("README.md"), "q-file", "no decisions/ folder (questions.md, decisions.md, manual.md)")
        return
    qp, dp, mp = (os.path.join(d, x) for x in ("questions.md", "decisions.md", "manual.md"))
    if os.path.isfile(qp):
        for ln, qid, title, fields in _blocks(sddlib.read_lines(qp), "Q"):
            if qid in F.questions:
                F.add("E", qp, "q-dup", "%s repeats" % qid, ln)
                continue
            F.questions[qid] = {"line": ln, "title": title, "fields": fields, "path": qp}
            for key in ("to", "status", "question"):
                if not fields.get(key, ("", 0))[0]:
                    F.add("E", qp, "q-field", "%s: field '%s' is empty or missing" % (qid, key.capitalize()), ln)
            st = fields.get("status", ("", 0))[0]
            if st and st not in Q_STATUSES:
                F.add("E", qp, "q-status", "%s: status '%s' - allowed: %s (a decided question moves to decisions.md)"
                      % (qid, st, ", ".join(Q_STATUSES)), fields["status"][1])
    if os.path.isfile(dp):
        for ln, qid, title, fields in _blocks(sddlib.read_lines(dp), "Q"):
            if qid in F.decisions:
                F.add("E", dp, "q-dup", "%s repeats" % qid, ln)
                continue
            if qid in F.questions:
                F.add("E", dp, "q-dup", "%s is both open (questions.md) and decided (decisions.md)" % qid, ln)
            F.decisions[qid] = {"line": ln, "title": title, "fields": fields, "path": dp}
            for key in ("status", "kind", "question", "decision", "decided"):
                if not fields.get(key, ("", 0))[0]:
                    F.add("E", dp, "q-field", "%s: field '%s' is empty or missing" % (qid, key.capitalize()), ln)
            st = fields.get("status", ("", 0))[0]
            if st and st != "active" and not re.fullmatch(r"superseded by " + ID_PATTERNS["Q"], st):
                F.add("E", dp, "q-status", "%s: status '%s' - active or 'superseded by Q-NNN'" % (qid, st), ln)
            kind = fields.get("kind", ("", 0))[0]
            if kind and kind not in DECISION_KINDS:
                F.add("E", dp, "q-kind", "%s: kind '%s' - allowed: %s" % (qid, kind, ", ".join(DECISION_KINDS)), ln)
    if os.path.isfile(mp):
        for ln, mid, title, fields in _blocks(sddlib.read_lines(mp), "M"):
            if mid in F.manual:
                F.add("E", mp, "m-dup", "%s repeats" % mid, ln)
                continue
            F.manual[mid] = fields
            tp = fields.get("type", ("", 0))[0]
            if tp not in MANUAL_TYPES:
                F.add("E", mp, "m-type", "%s: type '%s' - allowed: %s" % (mid, tp, ", ".join(MANUAL_TYPES)), ln)
            for key in ("what", "who and when"):
                if not fields.get(key, ("", 0))[0]:
                    F.add("E", mp, "m-field", "%s: field '%s' is empty or missing" % (mid, key.capitalize()), ln)


# ====================================================================== checks: references and markers

def check_links(F):
    for path in F.md_files():
        if F.is_source(path) or os.path.basename(path) == "traceability.md":
            continue
        lines = sddlib.read_lines(path)
        relp = os.path.relpath(path, F.dir).replace("\\", "/")
        is_spec = relp.startswith("specs/")
        approved = False
        if is_spec:
            meta, _ = sddlib.parse_frontmatter(lines)
            approved = (meta or {}).get("status") == "approved"
        for i, line in enumerate(lines):
            for qid in re.findall(r"\[\?(" + ID_PATTERNS["Q"] + r")\]", line):
                if qid in F.decisions:
                    F.add("E", path, "marker-closed", "[?%s]: the question is decided - apply the decision and remove "
                          "the marker" % qid, i)
                elif qid not in F.questions:
                    F.add("E", path, "link-q", "[?%s]: no such question in decisions/questions.md" % qid, i)
                if approved:
                    F.add("E", path, "marker-approved", "[?%s] in an approved spec" % qid, i)
            for rid in sddlib.ids_in(line, "REQ"):
                if rid not in F.reqs and F.reqs:
                    F.add("E", path, "link-req", "%s is not in requirements/" % rid, i)
            for cid in sddlib.ids_in(line, "CON"):
                if cid not in F.cards and (F.cards or F.registry):
                    F.add("E", path, "link-con", "%s has no card in contracts/" % cid, i)
            for qid in sddlib.ids_in(line, "Q"):
                if qid not in F.questions and qid not in F.decisions and (F.questions or F.decisions):
                    F.add("E", path, "link-q", "%s is not in decisions/" % qid, i)
            for sid in sddlib.ids_in(line, "SPEC"):
                if F.plan and sid not in F.plan:
                    F.add("W", path, "link-spec", "%s is not in the spec plan" % sid, i)


# ====================================================================== checks: contracts

CONTRACT_KEYS = ("id", "title", "feature", "domain", "kind", "provider", "consumers", "scope", "mode", "status",
                 "version", "requirements", "updated")


def _template_sections(F, name):
    path = os.path.join(F.root, "templates", name)
    if not os.path.isfile(path):
        return []
    lines = sddlib.read_lines(path)
    return [t for _, lv, t in sddlib.headings(lines) if lv == 2]


def _template_comments(F, name):
    path = os.path.join(F.root, "templates", name)
    if not os.path.isfile(path):
        return set()
    return {c for _, c in sddlib.html_comments(sddlib.read_lines(path))}


def _check_body(F, path, lines, template):
    have = {t.lower() for _, lv, t in sddlib.headings(lines) if lv == 2}
    for sec in _template_sections(F, template):
        if sec.lower() not in have:
            F.add("E", path, "section", "section '## %s' from templates/%s is missing (write 'Not applicable: <why>'"
                  " if it does not apply)" % (sec, template))
    tcom = _template_comments(F, template)
    for ln, c in sddlib.html_comments(lines):
        if c in tcom:
            F.add("W", path, "template-comment", "template hint left in the document - remove it", ln)
    cm = sddlib.code_mask(lines)
    hm = sddlib.comment_mask(lines, cm)
    _, body = sddlib.parse_frontmatter(lines)
    for i in range(body, len(lines)):
        if cm[i] or hm[i]:
            continue
        m = PLACEHOLDER.search(sddlib.strip_inline_code(lines[i]))
        if m:
            F.add("W", path, "placeholder", "placeholder %s - fill it in or mark it [?Q-NNN]" % m.group(0), i)


def check_contracts(F):
    cdir = F.p("contracts")
    reg = os.path.join(cdir, "README.md")
    a = F.analysis
    edges = [n for n in (a["order"] if a else []) if a["domains"][n]["kind"] == "edge"]
    if not os.path.isfile(reg):
        if F.stage >= 2:
            F.add(F.sev("plan"), F.p("README.md"), "contract-registry", "no contracts/README.md (contract registry)")
        return
    lines = sddlib.read_lines(reg)
    F.registry_meta, _ = sddlib.parse_frontmatter(lines)
    meta = F.registry_meta or {}
    if meta.get("status") not in CONTRACT_STATUSES:
        F.add("E", reg, "fm-status", "registry status '%s' - allowed: %s" % (meta.get("status"),
                                                                           ", ".join(CONTRACT_STATUSES)))
    cm = sddlib.code_mask(lines)
    rng = sddlib.section(lines, "Registry", 2, cm)
    if not rng:
        F.add("E", reg, "contract-table", "no section '## Registry'")
    else:
        for ln, title, b, e in sddlib.subsections(lines, rng[0], rng[1], 3, cm):
            group = title.split(" - ", 1)[0].strip().strip("`")
            no_change = any(re.match(r"^no changes:", lines[i].strip(), re.I) for i in range(b, e))
            F.registry_groups[group] = {"line": ln, "no_change": no_change, "rows": 0}
            if a and group not in a["domains"]:
                F.add("W", reg, "contract-group", "group '%s' is not a domain of the map" % group, ln)
            elif a and a["domains"][group]["kind"] != "edge":
                F.add("W", reg, "contract-group", "group '%s' is a node; contracts are grouped by edges" % group, ln)
            for t in sddlib.tables(lines, b, e, cm):
                if not t["header"] or t["header"][0].lower() != "contract":
                    continue
                for rl, cells in t["rows"]:
                    ids = sddlib.ids_in(cells[0], "CON")
                    if not ids:
                        continue
                    cid = ids[0]
                    if len(cells) != 8:
                        F.add("E", reg, "contract-table", "%s: %d columns, need 8: Contract | Kind | Provider | "
                              "Consumers | Mode | Operation | Requirements | Status" % (cid, len(cells)), rl)
                        continue
                    if cid in F.registry:
                        F.add("E", reg, "contract-dup", "%s is listed twice" % cid, rl)
                        continue
                    link = re.search(r"\]\(([^)]+)\)", cells[0])
                    F.registry[cid] = {"line": rl, "group": group, "kind": cells[1], "mode": cells[4],
                                       "reqs": set(sddlib.ids_in(cells[6], "REQ")), "status": cells[7],
                                       "link": link.group(1) if link else None}
                    F.registry_groups[group]["rows"] += 1
                    if not link:
                        F.add("E", reg, "contract-table", "%s: link the card: [%s](%s-<slug>.md)" % (cid, cid, cid), rl)
                    elif not os.path.isfile(os.path.join(cdir, link.group(1))):
                        F.add("E", reg, "link-con", "%s: card %s not found" % (cid, link.group(1)), rl)
    rng = sddlib.section(lines, "Requirements without contracts", 2, cm)
    if rng:
        for t in sddlib.tables(lines, rng[0], rng[1], cm):
            for rl, cells in t["rows"]:
                for rid in sddlib.ids_in(cells[0], "REQ"):
                    F.no_contract[rid] = rl
                    if len(cells) < 2 or not cells[1] or cells[1] == "-":
                        F.add("E", reg, "contract-coverage", "%s: say why no contract is needed" % rid, rl)

    for f in sorted(os.listdir(cdir)):
        m = re.match(r"^(" + ID_PATTERNS["CON"] + r")-[a-z0-9-]+\.md$", f)
        if f == "README.md":
            continue
        path = os.path.join(cdir, f)
        if not m:
            F.add("E", path, "fm-filename", "contract card file name: CON-NNN-<slug>.md")
            continue
        cl = sddlib.read_lines(path)
        cmeta, _ = sddlib.parse_frontmatter(cl)
        cmeta = cmeta or {}
        cid = m.group(1)
        F.cards[cid] = {"path": path, "meta": cmeta}
        for key in CONTRACT_KEYS:
            if key not in cmeta or cmeta[key] in ("", None):
                F.add("E", path, "fm-missing", "contract: no '%s'" % key)
        if cmeta.get("type") != "contract":
            F.add("E", path, "fm-type", "type must be 'contract'")
        if cmeta.get("id") and cmeta["id"] != cid:
            F.add("E", path, "fm-id", "id '%s' does not match the file name" % cmeta["id"])
        if cmeta.get("kind") and cmeta["kind"] not in F.cfg["contract_kinds"]:
            F.add("E", path, "contract-field", "kind '%s' - allowed: %s" % (cmeta["kind"], ", ".join(F.cfg["contract_kinds"])))
        if cmeta.get("mode") and cmeta["mode"] not in F.cfg["contract_modes"]:
            F.add("E", path, "contract-field", "mode '%s' - allowed: %s" % (cmeta["mode"], ", ".join(F.cfg["contract_modes"])))
        if cmeta.get("scope") and cmeta["scope"] not in (F.scope_in, F.scope_out):
            F.add("E", path, "contract-field", "scope '%s' - %s or %s" % (cmeta["scope"], F.scope_in, F.scope_out))
        if cmeta.get("status") and cmeta["status"] not in CONTRACT_STATUSES:
            F.add("E", path, "fm-status", "status '%s' - allowed: %s" % (cmeta["status"], ", ".join(CONTRACT_STATUSES)))
        reqs = cmeta.get("requirements") or []
        if not isinstance(reqs, list):
            reqs = sddlib.ids_in(str(reqs), "REQ")
        for rid in reqs:
            if rid not in F.reqs:
                F.add("E", path, "link-req", "%s is not in requirements/" % rid)
            elif rid in F.inactive:
                F.add("E", path, "req-inactive", "%s is %s - use the active requirement" % (rid, F.inactive[rid]["state"]))
        _check_body(F, path, cl, "feature/contract.md")
        row = F.registry.get(cid)
        if not row:
            F.add("E", path, "contract-registry", "%s is not in contracts/README.md" % cid)
            continue
        for key, rkey in (("kind", "kind"), ("mode", "mode"), ("status", "status")):
            if cmeta.get(key) and cmeta[key] != row[rkey]:
                F.add("E", reg, "contract-mismatch", "%s: %s '%s' in the registry, '%s' in the card"
                      % (cid, key, row[rkey], cmeta[key]), row["line"])
        if set(reqs) != row["reqs"]:
            F.add("E", reg, "contract-mismatch", "%s: requirements differ between the registry and the card" % cid,
                  row["line"])
        if cmeta.get("domain") and cmeta["domain"] != row["group"]:
            F.add("W", path, "contract-mismatch", "domain '%s' but the registry group is '%s'" % (cmeta["domain"], row["group"]))
    for cid, row in F.registry.items():
        if cid not in F.cards and row["link"] and os.path.isfile(os.path.join(cdir, row["link"])):
            F.add("E", reg, "fm-filename", "%s: card file name must start with %s-" % (cid, cid), row["line"])

    sev = F.sev("plan")
    for e in edges:
        g = F.registry_groups.get(e)
        if not g:
            F.add(sev, reg, "domain-edge", "edge domain %s has no group '### %s - ...' in the registry" % (e, e))
        elif not g["rows"] and not g["no_change"]:
            F.add(sev, reg, "domain-edge", "group %s: add contracts or a line 'No changes: <why>'" % e, g["line"])
    covered = set()
    for c in F.cards.values():
        reqs = c["meta"].get("requirements") or []
        covered |= set(reqs if isinstance(reqs, list) else [])
    F.contract_uncovered = [r for r in F.reqs if F.in_scope(r) and r not in covered and r not in F.no_contract]
    for rid in F.contract_uncovered:
        F.add(sev, reg, "contract-coverage", "%s is not linked to a contract and not in 'Requirements without "
              "contracts'" % rid)


# ====================================================================== checks: plan

def check_plan(F):
    path = F.p("README.md")
    lines = sddlib.read_lines(path)
    cm = sddlib.code_mask(lines)
    rng = sddlib.section(lines, "Spec plan", 2, cm)
    types = F.cfg["unit_types"]
    if rng:
        for t in sddlib.tables(lines, rng[0], rng[1], cm):
            if not t["header"] or t["header"][0].lower() != "spec":
                continue
            for ln, cells in t["rows"]:
                ids = sddlib.ids_in(cells[0], "SPEC")
                if not ids:
                    continue
                sid = ids[0]
                if len(cells) != 7:
                    F.add("E", path, "plan-table", "%s: %d columns, need 7: Spec | Type | Title | Component | "
                          "Requirements | Contracts | Status" % (sid, len(cells)), ln)
                    continue
                if sid in F.plan:
                    F.add("E", path, "plan-dup", "%s is planned twice" % sid, ln)
                    continue
                link = re.search(r"\]\(([^)]+)\)", cells[0])
                row = {"line": ln, "type": cells[1], "title": cells[2], "reqs": sddlib.ids_in(cells[4], "REQ"),
                       "cons": sddlib.ids_in(cells[5], "CON"), "status": cells[6],
                       "link": link.group(1) if link else None}
                F.plan[sid] = row
                if not link:
                    F.add("E", path, "plan-table", "%s: link the file: [%s](specs/%s-<slug>.md)" % (sid, sid, sid), ln)
                elif not re.match(r"^specs/" + sid + r"-[a-z0-9-]+\.md$", link.group(1)):
                    F.add("E", path, "plan-table", "%s: file must be specs/%s-<kebab-slug>.md" % (sid, sid), ln)
                if cells[1] not in types:
                    F.add("E", path, "plan-type", "%s: type '%s' - allowed: %s" % (sid, cells[1], ", ".join(types)), ln)
                if not row["reqs"]:
                    F.add("E", path, "plan-req", "%s covers no requirements" % sid, ln)
                for rid in row["reqs"]:
                    if rid not in F.reqs:
                        F.add("E", path, "link-req", "%s: %s is not in requirements/" % (sid, rid), ln)
                    elif rid in F.inactive:
                        F.add("E", path, "req-inactive", "%s: %s is %s" % (sid, rid, F.inactive[rid]["state"]), ln)
                    elif not F.in_scope(rid):
                        F.add("E", path, "plan-scope", "%s: %s is out of scope - no specs for it" % (sid, rid), ln)
                for cid in row["cons"]:
                    if cid not in F.cards:
                        F.add("E", path, "link-con", "%s: %s has no card" % (sid, cid), ln)
                if cells[1] == F.cfg["api_unit_type"]:
                    good = len(row["cons"]) == 1 and row["cons"][0] in F.cards and \
                        F.cards[row["cons"][0]]["meta"].get("kind") == "api" and \
                        F.cards[row["cons"][0]]["meta"].get("scope") == F.scope_in
                    if not good:
                        F.add("E", path, "plan-contracts", "%s: an %s unit describes exactly one in-scope api contract"
                              % (sid, cells[1]), ln)
                if cells[6] not in SPEC_STATUSES:
                    F.add("E", path, "plan-status", "%s: status '%s' - allowed: %s" % (sid, cells[6],
                                                                                      ", ".join(SPEC_STATUSES)), ln)
    elif F.stage >= 3:
        F.add(F.sev("spec"), path, "plan-table", "no section '## Spec plan' in the passport")
    if F.stage < 3:
        return
    sev = F.sev("spec")
    planned = set()
    for row in F.plan.values():
        planned |= set(row["reqs"])
    for rid in F.reqs:
        if F.in_scope(rid) and rid not in planned:
            F.add(sev, path, "plan-coverage", "%s (in scope) is not covered by any planned spec" % rid)
    planned_cons = set()
    for row in F.plan.values():
        planned_cons |= set(row["cons"])
    for cid, c in F.cards.items():
        m = c["meta"]
        if m.get("scope") == F.scope_in and m.get("mode") in ("new", "change") and cid not in planned_cons:
            F.add(sev, path, "plan-contracts", "%s (new or changed, in scope) is not described by any planned spec"
                  % cid)


# ====================================================================== checks: specs

SPEC_KEYS = ("id", "type", "title", "feature", "component", "mode", "status", "version", "requirements",
             "contracts", "depends", "updated")


def check_specs(F):
    sdir = F.p("specs")
    files = sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []
    for f in files:
        if not f.endswith(".md"):
            continue
        path = os.path.join(sdir, f)
        m = re.match(r"^(" + ID_PATTERNS["SPEC"] + r")-[a-z0-9-]+\.md$", f)
        if not m:
            F.add("E", path, "fm-filename", "spec file name: SPEC-NN-<kebab-slug>.md")
            continue
        sid = m.group(1)
        lines = sddlib.read_lines(path)
        meta, body = sddlib.parse_frontmatter(lines)
        meta = meta or {}
        F.specs[sid] = {"path": path, "meta": meta}
        for key in SPEC_KEYS:
            if key not in meta:
                F.add("E", path, "fm-missing", "spec: no '%s'" % key)
        if meta.get("id") and meta["id"] != sid:
            F.add("E", path, "fm-id", "id '%s' does not match the file name" % meta["id"])
        tp = meta.get("type")
        if tp and tp not in F.cfg["unit_types"]:
            F.add("E", path, "fm-type", "type '%s' - allowed: %s" % (tp, ", ".join(F.cfg["unit_types"])))
        if meta.get("status") and meta["status"] not in SPEC_STATUSES:
            F.add("E", path, "fm-status", "status '%s' - allowed: %s" % (meta["status"], ", ".join(SPEC_STATUSES)))
        if meta.get("mode") and meta["mode"] not in ("new", "change"):
            F.add("E", path, "fm-mode", "mode '%s' - new or change" % meta["mode"])
        reqs = meta.get("requirements") if isinstance(meta.get("requirements"), list) else []
        cons = meta.get("contracts") if isinstance(meta.get("contracts"), list) else []
        deps = meta.get("depends") if isinstance(meta.get("depends"), list) else []
        if not reqs:
            F.add("E", path, "fm-missing", "requirements: [] - a spec covers at least one requirement")
        for rid in reqs:
            if rid not in F.reqs:
                F.add("E", path, "link-req", "%s is not in requirements/" % rid)
            elif rid in F.inactive:
                F.add("E", path, "req-inactive", "%s is %s" % (rid, F.inactive[rid]["state"]))
            elif not F.in_scope(rid):
                F.add("W", path, "zone-outside", "%s is out of scope - remove it from the spec" % rid)
        for cid in cons:
            if cid not in F.cards:
                F.add("E", path, "link-con", "%s has no card in contracts/" % cid)
        for dep in deps:
            if dep not in F.plan:
                F.add("E", path, "link-dep", "depends: %s is not in the spec plan" % dep)
        row = F.plan.get(sid)
        if not row:
            F.add("E", path, "spec-plan", "%s is not in the spec plan (passport, '## Spec plan')" % sid)
        else:
            if row["type"] != tp:
                F.add("E", path, "spec-plan", "type '%s' but the plan says '%s'" % (tp, row["type"]))
            if set(row["reqs"]) != set(reqs):
                F.add("E", path, "spec-plan", "requirements differ from the plan row")
            if set(row["cons"]) != set(cons):
                F.add("E", path, "spec-plan", "contracts differ from the plan row")
            if row["status"] != meta.get("status"):
                F.add("W", F.p("README.md"), "plan-status", "%s: status '%s' in the plan, '%s' in the file"
                      % (sid, row["status"], meta.get("status")), row["line"])
            if row["link"] and os.path.normpath(row["link"]) != os.path.normpath("specs/" + f):
                F.add("E", F.p("README.md"), "plan-table", "%s: link %s, file is specs/%s" % (sid, row["link"], f),
                      row["line"])
        if tp:
            _check_body(F, path, lines, "spec/%s.md" % tp)
        text = "\n".join(lines[body:])
        for rid in reqs:
            if text.count(rid) == 0:
                F.add("W", path, "spec-req", "%s from the header is not mentioned in the text or acceptance criteria"
                      % rid)
        if tp == F.cfg["data_model_unit_type"]:
            _check_data_model(F, path, lines)
        if tp == F.cfg["api_unit_type"] and F.cfg.get("api_response_required_keys"):
            _check_envelope(F, path, lines)
    for sid, row in F.plan.items():
        if sid not in F.specs:
            F.add(F.sev("ready"), F.p("README.md"), "link-spec", "%s is planned but %s is not written yet"
                  % (sid, row["link"] or "the file"), row["line"])


def _check_data_model(F, path, lines):
    dm = F.cfg["data_model"]
    cols = dm["columns"]
    chg = dm.get("change_column")
    types = set(dm["types"])
    for t in sddlib.tables(lines):
        h = t["header"]
        if not h or h[0] != cols[0]:
            continue
        if h != cols and h != cols + [chg]:
            F.add("E", path, "dm-cols", "data model columns: %s (optional '%s' for mode: change)"
                  % (" | ".join(cols), chg), t["line"])
            continue
        for ln, cells in t["rows"]:
            if len(cells) < 2:
                continue
            raw = cells[1].strip().strip("`").lower()
            base = re.match(r"[a-z][a-z-]*", raw)
            if not base or base.group(0) not in types:
                F.add("E", path, "dm-type", "type '%s' - use a logical type: %s" % (cells[1], ", ".join(sorted(types))),
                      ln)


def _check_envelope(F, path, lines):
    """JSON examples under '## Response...' headings must contain every configured top-level key."""
    keys = F.cfg["api_response_required_keys"]
    current, start = "", None
    for i, line in enumerate(lines):
        s = line.lstrip()
        if start is None:
            if s.startswith(("```", "~~~")):
                start = i
                continue
            m = sddlib.ANY_HEADING.match(line)
            if m and len(m.group(1)) == 2:
                current = m.group(2).strip().lower()
        elif s.startswith(("```", "~~~")):
            if current.startswith("response") and "json" in lines[start].lower():
                text = "\n".join(lines[start:i])
                missing = [k for k in keys if '"%s"' % k not in text]
                if missing:
                    F.add("E", path, "api-envelope", "response example lacks required keys: %s "
                          "(api_response_required_keys in sdd.config.json)" % ", ".join(missing), start)
            start = None


# ====================================================================== gates

def check_gate(F, gate):
    if gate == "contracts":
        st = (F.registry_meta or {}).get("status")
        if st not in ("review", "approved"):
            F.add("E", F.p("contracts", "README.md"), "gate", "registry status must be review or approved before "
                  "planning (now: %s)" % st)
        return
    if (F.registry_meta or {}).get("status") != "approved":
        F.add("E", F.p("contracts", "README.md"), "gate", "contract registry is not approved")
    used = set()
    for sid, row in F.plan.items():
        s = F.specs.get(sid)
        if s and s["meta"].get("status") != "approved":
            F.add("E", s["path"], "gate", "%s is %s, not approved" % (sid, s["meta"].get("status")))
        used |= set(row["cons"])
    for cid in sorted(used):
        c = F.cards.get(cid)
        if c and c["meta"].get("status") != "approved":
            F.add("E", c["path"], "gate", "%s is %s, not approved" % (cid, c["meta"].get("status")))
    for qid, q in F.questions.items():
        st = q["fields"].get("status", ("", 0))[0]
        blocks = q["fields"].get("blocks", ("-", 0))[0]
        if st in ("open", "answered") and blocks not in ("", "-"):
            F.add("E", q["path"], "gate", "%s is %s and blocks %s" % (qid, st, blocks), q["line"])
    for folder in ("specs", "contracts"):
        d = F.p(folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                for i, line in enumerate(sddlib.read_lines(os.path.join(d, f))):
                    for qid in re.findall(r"\[\?(" + ID_PATTERNS["Q"] + r")\]", line):
                        F.add("E", os.path.join(d, f), "gate", "open marker [?%s]" % qid, i)


# ====================================================================== trace and next IDs

def write_trace(F):
    order = {"draft": 0, "review": 1, "approved": 2, "superseded": -1}
    rows = []
    stats = {"in": 0, "no_contract": 0, "no_spec": 0, "approved": 0}
    con_by_req, spec_by_req = {}, {}
    for cid, c in F.cards.items():
        for rid in c["meta"].get("requirements") or []:
            con_by_req.setdefault(rid, []).append(cid)
    for sid, row in F.plan.items():
        for rid in row["reqs"]:
            spec_by_req.setdefault(rid, []).append(sid)
    for rid in sorted(F.reqs, key=lambda x: int(x.split("-")[1])):
        r = F.reqs[rid]
        cons = sorted(con_by_req.get(rid, []))
        specs = sorted(spec_by_req.get(rid, []))
        if rid in F.inactive:
            state = F.inactive[rid]["state"]
        elif r["scope"] != F.scope_in:
            state = "out of scope"
        else:
            stats["in"] += 1
            if not cons and rid not in F.no_contract:
                stats["no_contract"] += 1
            if not specs:
                state = "not planned"
                stats["no_spec"] += 1
            else:
                sts = [F.specs[s]["meta"].get("status") if s in F.specs else None for s in specs]
                if None in sts:
                    state = "planned"
                else:
                    state = min(sts, key=lambda s: order.get(s, 0))
                    if state == "approved":
                        stats["approved"] += 1
        con_cell = ", ".join(cons) or ("not needed" if rid in F.no_contract else "-")
        rows.append("| %s | %s | %s | %s | %s | %s | %s |" % (rid, r["domain"], r["source"], r["scope"], con_cell,
                                                            ", ".join(specs) or "-", state))
    out = ["---", "type: traceability", "feature: %s" % F.id, "generated: true", "---", "",
           "# Traceability %s" % F.id, "",
           "<!-- Generated by tools/check.py --trace. Do not edit. -->", "",
           "In-scope active requirements: %d. Without a contract or a reason: %d. Not planned: %d. "
           "Covered by approved specs: %d." % (stats["in"], stats["no_contract"], stats["no_spec"], stats["approved"]),
           "", "| Requirement | Domain | Source | Scope | Contracts | Specs | State |", "|---|---|---|---|---|---|---|"]
    out += rows
    sddlib.write_text(F.p("traceability.md"), "\n".join(out) + "\n")
    return stats


def next_ids(F):
    def nxt(ids, width):
        nums = [int(x.split("-")[1]) for x in ids]
        return "%0*d" % (width, (max(nums) if nums else 0) + 1)
    return "REQ-%s, Q-%s, M-%s, CON-%s, SPEC-%s" % (
        nxt(list(F.reqs) + list(F.inactive), 3), nxt(list(F.questions) + list(F.decisions), 3),
        nxt(list(F.manual), 3), nxt(list(F.cards) + list(F.registry), 3), nxt(list(F.plan) + list(F.specs), 2))


# ====================================================================== driver

def check_feature(fdir, root, cfg, report, gate=None):
    F = Feature(fdir, root, cfg, report)
    if not os.path.isfile(F.p("README.md")):
        report.add("E", fdir, "feature-passport", "no README.md (feature passport)")
        return F
    load(F)
    if gate:
        F.gate = gate
        F.stage = max(F.stage, STAGES.index("plan" if gate == "contracts" else "ready"))
    F.contract_uncovered = []
    check_passport(F)
    check_files(F)
    check_map(F)
    check_requirements(F)
    check_decisions(F)
    check_contracts(F)
    check_plan(F)
    check_specs(F)
    check_links(F)
    if gate:
        check_gate(F, gate)
    return F


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Check SDD pipeline artifacts.")
    ap.add_argument("paths", nargs="*", help="feature folders or files (default: all features)")
    ap.add_argument("--gate", choices=["contracts", "ready"], help="check a stage gate")
    ap.add_argument("--trace", action="store_true", help="write traceability.md")
    ap.add_argument("--next", action="store_true", help="print the next free IDs")
    ap.add_argument("--root", default=sddlib.ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    cfg = sddlib.load_config(root)

    targets = {}
    only = []
    if not args.paths:
        for f in sddlib.find_features(root):
            targets[f] = True
    for p in args.paths:
        if not os.path.exists(p):
            print("E %s - [scope] path not found" % p)
            return 2
        fdir = sddlib.feature_of(p)
        if not fdir:
            print("E %s - [scope] not inside a feature folder (README.md with type: feature)" % p)
            return 2
        targets[fdir] = True
        if os.path.abspath(p) != fdir:
            only.append(p)
    if not targets:
        print("No features found.")
        return 0
    report = Report(root, only or None)
    for fdir in targets:
        F = check_feature(fdir, root, cfg, report, args.gate)
        if args.next:
            print("%s: next free IDs: %s" % (F.id, next_ids(F)))
            continue
        if args.trace:
            st = write_trace(F)
            print("%s: traceability.md written. In scope %d, not planned %d, approved %d."
                  % (F.id, st["in"], st["no_spec"], st["approved"]))
    if args.next:
        return 0
    report.print()
    tail = " (outside the given files: %d)" % report.outside if report.outside else ""
    print("Total: errors %d, warnings %d%s." % (report.errors, report.warnings, tail))
    if args.gate:
        print("Gate %s: %s" % (args.gate, "PASSED" if report.errors == 0 else "NOT PASSED"))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
