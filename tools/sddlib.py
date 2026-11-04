"""Shared helpers for the SDD pipeline tools.

Standard library only: the tools must run anywhere Python 3.8+ is available,
including closed networks without package mirrors.
"""

import copy
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CONFIG = {
    "artifact_language": "en",
    "feature_id_pattern": r"^[A-Z][A-Z0-9]*-[0-9]+$",
    "scope": {"in": "in", "out": "out"},
    "requirement_types": ["FR", "NFR", "BR", "IR"],
    "ui_domain_prefix": "ui-",
    "unit_types": ["component", "data-model", "integration", "job", "api-method", "scenario", "ui", "config"],
    "api_unit_type": "api-method",
    "data_model_unit_type": "data-model",
    "contract_kinds": ["api", "message", "file", "other"],
    "contract_modes": ["new", "change", "reuse", "external"],
    "api_response_required_keys": [],
    "data_model": {
        "columns": ["Name", "Type", "Comment", "Constraint"],
        "change_column": "Change",
        "types": ["uuid", "string", "text", "int", "bigint", "decimal", "boolean",
                  "date", "date-time", "time", "json", "binary", "enum"],
    },
    "style": {"forbidden_chars": {}, "forbidden_words": {}},
}

STAGES = ["intake", "analysis", "contracts", "plan", "spec", "ready"]
FEATURE_STATUSES = STAGES + ["hold", "cancelled"]

ID_PATTERNS = {
    "REQ": r"REQ-\d{3,}",
    "Q": r"Q-\d{3,}",
    "M": r"M-\d{3,}",
    "CON": r"CON-\d{3,}",
    "SPEC": r"SPEC-\d{2,}",
}

SECTION_NUM = r"\d+(?:\.\d+)*"
SRC_HEADING = re.compile(r"^(#{2,6})\s+(" + SECTION_NUM + r")\s+(.*?)\s*$")
ANY_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


# ---------------------------------------------------------------- config

def load_config(root=ROOT):
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    path = os.path.join(root, "sdd.config.json")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            user = json.load(f)
        for key, value in user.items():
            if key.startswith("_"):
                continue
            if isinstance(value, dict) and isinstance(cfg.get(key), dict):
                cfg[key].update(value)
            else:
                cfg[key] = value
    return cfg


# ---------------------------------------------------------------- files

def read_lines(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read().splitlines()


def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def rel(path, root):
    try:
        return os.path.relpath(path, root).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


# ---------------------------------------------------------------- frontmatter

def _value(raw):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [_unquote(x.strip()) for x in inner.split(",") if x.strip()] if inner else []
    return _unquote(raw)


def _unquote(s):
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def parse_frontmatter(lines):
    """Return (meta, body_start). meta is None when there is no frontmatter."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    meta = {}
    for i in range(1, len(lines)):
        s = lines[i].strip()
        if s == "---":
            return meta, i + 1
        if not s or s.startswith("#") or ":" not in s:
            continue
        key, value = s.split(":", 1)
        meta[key.strip()] = _value(value)
    return None, 0


# ---------------------------------------------------------------- markdown structure

def code_mask(lines):
    """True for lines inside fenced code blocks (fence lines included)."""
    mask = [False] * len(lines)
    fence = None
    for i, line in enumerate(lines):
        s = line.lstrip()
        if fence:
            mask[i] = True
            if s.startswith(fence):
                fence = None
            continue
        m = re.match(r"(`{3,}|~{3,})", s)
        if m:
            fence = m.group(1)[:3]
            mask[i] = True
    return mask


def comment_mask(lines, cmask=None):
    """True for lines that are fully or partly inside HTML comments."""
    mask = [False] * len(lines)
    inside = False
    for i, line in enumerate(lines):
        if cmask and cmask[i]:
            continue
        if inside:
            mask[i] = True
            if "-->" in line:
                inside = False
            continue
        if "<!--" in line:
            mask[i] = True
            if "-->" not in line[line.index("<!--"):]:
                inside = True
    return mask


def html_comments(lines):
    """Return list of (line, normalized text) for HTML comments outside code."""
    cm = code_mask(lines)
    text = "\n".join("" if cm[i] else l for i, l in enumerate(lines))
    out = []
    for m in re.finditer(r"<!--(.*?)-->", text, re.S):
        line = text.count("\n", 0, m.start())
        out.append((line, " ".join(m.group(1).split())))
    return out


def headings(lines, cmask=None):
    cmask = cmask or code_mask(lines)
    out = []
    for i, line in enumerate(lines):
        if cmask[i]:
            continue
        m = ANY_HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def section(lines, title, level=2, cmask=None, begin=0, end=None):
    """Body range (b, e) of the first heading of `level` whose title equals `title`."""
    end = len(lines) if end is None else end
    hs = [h for h in headings(lines, cmask) if begin <= h[0] < end]
    for idx, (ln, lv, t) in enumerate(hs):
        if lv == level and t.lower() == title.lower():
            stop = end
            for ln2, lv2, _ in hs[idx + 1:]:
                if lv2 <= level:
                    stop = ln2
                    break
            return ln + 1, stop
    return None


def subsections(lines, begin, end, level=3, cmask=None):
    """List of (heading_line, title, body_begin, body_end) for headings of `level` in range."""
    hs = [h for h in headings(lines, cmask) if begin <= h[0] < end]
    out = []
    for idx, (ln, lv, t) in enumerate(hs):
        if lv != level:
            continue
        stop = end
        for ln2, lv2, _ in hs[idx + 1:]:
            if lv2 <= level:
                stop = ln2
                break
        out.append((ln, t, ln + 1, stop))
    return out


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def tables(lines, begin=0, end=None, cmask=None):
    """Markdown tables in range: dicts with line, header, rows [(line, cells)]."""
    cmask = cmask or code_mask(lines)
    end = len(lines) if end is None else end
    res = []
    i = begin
    while i < end:
        if not cmask[i] and lines[i].lstrip().startswith("|"):
            j = i
            while j < end and not cmask[j] and lines[j].lstrip().startswith("|"):
                j += 1
            if j - i >= 2 and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
                res.append({
                    "line": i,
                    "header": split_row(lines[i]),
                    "rows": [(k, split_row(lines[k])) for k in range(i + 2, j)],
                })
            i = j
        else:
            i += 1
    return res


def bullet_fields(lines, begin, end):
    """'- Key: value' bullets in range -> {key_lower: (value, line)}."""
    out = {}
    for i in range(begin, end):
        m = re.match(r"^\s*-\s+([^:]{1,40}):\s*(.*)$", lines[i])
        if m:
            out.setdefault(m.group(1).strip().lower(), (m.group(2).strip(), i))
    return out


def ids_in(text, kind):
    return re.findall(r"(?<![A-Za-z0-9-])" + ID_PATTERNS[kind] + r"(?![0-9])", text)


def strip_inline_code(line):
    return re.sub(r"`[^`]*`", "", line)


# ---------------------------------------------------------------- source snapshot

def section_hash(body_lines):
    text = "\n".join(l.rstrip() for l in body_lines).strip()
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def parse_source(path):
    """Sections of a normalized snapshot, in document order.

    Each section: num, title, level, start (heading line), end (exclusive end of own text).
    """
    lines = read_lines(path)
    cm = code_mask(lines)
    secs = []
    for i, line in enumerate(lines):
        if cm[i] or not ANY_HEADING.match(line):
            continue
        if secs and secs[-1]["end"] is None:
            secs[-1]["end"] = i
        m = SRC_HEADING.match(line)
        if m:
            secs.append({"num": m.group(2), "title": m.group(3), "level": len(m.group(1)),
                         "start": i, "end": None})
    if secs and secs[-1]["end"] is None:
        secs[-1]["end"] = len(lines)
    for s in secs:
        s["hash"] = section_hash(lines[s["start"] + 1:s["end"]])
    return lines, secs


def is_within(num, parent):
    return num == parent or num.startswith(parent + ".")


def resolve_refs(text, nums):
    """Resolve a Read reference list ('2, 3.1-3.4, 5 (intro)') against section numbers.

    N          section N with all its subsections
    N-M        from N through the end of M's subtree, in document order
    N (intro)  only the own text of N, without subsections
    """
    picked = []
    errors = []
    index = {n: i for i, n in enumerate(nums)}

    def subtree_end(n):
        j = index[n]
        while j + 1 < len(nums) and is_within(nums[j + 1], n):
            j += 1
        return j

    for tok in [t.strip() for t in text.split(",") if t.strip()]:
        m_intro = re.match(r"^(" + SECTION_NUM + r")\s*\(intro\)$", tok)
        m_range = re.match(r"^(" + SECTION_NUM + r")-(" + SECTION_NUM + r")$", tok)
        m_one = re.match(r"^(" + SECTION_NUM + r")$", tok)
        if m_intro:
            n = m_intro.group(1)
            if n not in index:
                errors.append("section %s is not in the snapshot" % n)
            else:
                picked.append(n)
        elif m_range:
            a, b = m_range.group(1), m_range.group(2)
            missing = [x for x in (a, b) if x not in index]
            if missing:
                errors.append("section %s is not in the snapshot" % ", ".join(missing))
            elif index[a] > index[b]:
                errors.append("range %s: %s comes after %s" % (tok, a, b))
            else:
                picked.extend(nums[index[a]:subtree_end(b) + 1])
        elif m_one:
            n = m_one.group(1)
            if n not in index:
                errors.append("section %s is not in the snapshot" % n)
            else:
                picked.extend(nums[index[n]:subtree_end(n) + 1])
        else:
            errors.append("cannot read reference '%s' (use N, N-M or N (intro))" % tok)
    return set(picked), errors


# ---------------------------------------------------------------- analysis.md (domain map)

DOMAIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _clean(cell):
    return cell.strip().strip("`").strip()


def parse_read_list(lines, begin, end):
    """Items of the 'Read:' list in range -> [(line, refs, what)], or None without 'Read:'."""
    for i in range(begin, end):
        if lines[i].strip().lower() == "read:":
            items = []
            j = i + 1
            while j < end and not lines[j].strip():
                j += 1
            while j < end and re.match(r"^\s*-\s+", lines[j]):
                body = re.sub(r"^\s*-\s+", "", lines[j]).strip()
                if " - " in body:
                    refs, what = body.split(" - ", 1)
                else:
                    refs, what = body, ""
                items.append((j, refs.strip().rstrip("."), what.strip()))
                j += 1
            return items
    return None


def parse_analysis(path):
    lines = read_lines(path)
    cm = code_mask(lines)
    a = {"path": path, "lines": lines, "domains": {}, "order": [], "domain_rows": [],
         "slices": {}, "index_rows": [], "findings": {}, "scenarios": []}

    rng = section(lines, "Domains", 2, cm)
    if rng:
        for t in tables(lines, rng[0], rng[1], cm):
            if t["header"] and t["header"][0].lower() == "domain":
                for ln, cells in t["rows"]:
                    if len(cells) < 2:
                        continue
                    name = _clean(cells[0])
                    a["domain_rows"].append((ln, name, cells))
                    if name not in a["domains"]:
                        a["order"].append(name)
                        a["domains"][name] = {"kind": cells[1].strip().lower(), "line": ln,
                                              "component": cells[2] if len(cells) > 2 else ""}

    rng = section(lines, "Source slices", 2, cm)
    if rng:
        for ln, title, b, e in subsections(lines, rng[0], rng[1], 3, cm):
            name = _clean(title.split(" - ", 1)[0])
            a["slices"][name] = {"line": ln, "items": parse_read_list(lines, b, e)}

    rng = section(lines, "Sections by domain", 2, cm)
    if rng:
        for t in tables(lines, rng[0], rng[1], cm):
            if t["header"] and t["header"][0].lower() == "section":
                for ln, cells in t["rows"]:
                    m = re.match(r"^(" + SECTION_NUM + r")\b", cells[0].strip())
                    if not m:
                        continue
                    raw = cells[1].strip() if len(cells) > 1 else ""
                    if raw in ("", "-"):
                        doms = []
                    elif raw.lower() in ("all", "all domains"):
                        doms = ["*"]
                    else:
                        doms = [_clean(x) for x in raw.split(",") if x.strip()]
                    a["index_rows"].append((ln, m.group(1), doms))

    rng = section(lines, "Findings for domains", 2, cm)
    if rng:
        for ln, title, b, e in subsections(lines, rng[0], rng[1], 3, cm):
            name = _clean(title.split(" - ", 1)[0])
            pending, applied = 0, False
            for i in range(b, e):
                s = lines[i].strip()
                if re.match(r"^-\s+applied\b", s, re.I):
                    applied = True
                elif s.startswith("- "):
                    pending += 1
            a["findings"][name] = {"line": ln, "pending": pending, "applied": applied}

    rng = section(lines, "Scenarios", 2, cm)
    if rng:
        for t in tables(lines, rng[0], rng[1], cm):
            for ln, cells in t["rows"]:
                a["scenarios"].append((ln, cells))
    return a


def build_slice(feature_id, domain, items, src_lines, secs):
    nums = [s["num"] for s in secs]
    picked, errors = set(), []
    for ln, refs, _ in items:
        p, errs = resolve_refs(refs, nums)
        picked |= p
        errors.extend((ln, e) for e in errs)
    out = ["---", "type: slice", "feature: %s" % feature_id, "domain: %s" % domain, "generated: true", "---", "",
           "# Source slice: %s" % domain, "",
           "<!-- Generated by tools/slices.py from source/source.md and the Read list in analysis.md. "
           "Do not edit: change the Read list and rebuild. -->", "", "What to look for:", ""]
    for _, refs, what in items:
        out.append("- %s - %s" % (refs, what) if what else "- %s" % refs)
    out.append("")
    for s in secs:
        if s["num"] in picked:
            chunk = src_lines[s["start"]:s["end"]]
            while chunk and not chunk[-1].strip():
                chunk = chunk[:-1]
            out.extend(chunk)
            out.append("")
    return "\n".join(out).rstrip() + "\n", errors


def find_features(root):
    out = []
    for top in ("features", "examples"):
        base = os.path.join(root, top)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            d = os.path.join(base, name)
            if os.path.isfile(os.path.join(d, "README.md")):
                meta, _ = parse_frontmatter(read_lines(os.path.join(d, "README.md")))
                if meta and meta.get("type") == "feature":
                    out.append(d)
    return out


def feature_of(path):
    """Nearest ancestor folder (or the folder itself) whose README.md is a feature passport."""
    d = os.path.abspath(path if os.path.isdir(path) else os.path.dirname(path))
    while True:
        readme = os.path.join(d, "README.md")
        if os.path.isfile(readme):
            meta, _ = parse_frontmatter(read_lines(readme))
            if meta and meta.get("type") == "feature":
                return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
