#!/usr/bin/env python3
"""Build per-domain slices of the source snapshot from the domain map.

    python tools/slices.py features/<ID>                 rebuild all slices
    python tools/slices.py features/<ID> --domain <name>  rebuild one slice
    python tools/slices.py features/<ID> --check          only report stale slices

A slice is a copy of the snapshot sections listed in the domain's "Read:" list in
analysis.md (section "Source slices"). The text is copied verbatim, never retold, so
an agent working on one domain reads only what it needs, and a section needed by
several domains lands in each of their slices.

Exit codes: 0 - done, 1 - errors in Read lists or stale slices (--check), 2 - usage error.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sddlib  # noqa: E402


def plan(fdir):
    """Return (feature_id, {domain: (text, errors)}, problems)."""
    readme = os.path.join(fdir, "README.md")
    meta, _ = sddlib.parse_frontmatter(sddlib.read_lines(readme)) if os.path.isfile(readme) else (None, 0)
    fid = (meta or {}).get("id") or os.path.basename(fdir)
    src = os.path.join(fdir, "source", "source.md")
    ana = os.path.join(fdir, "analysis.md")
    problems = []
    if not os.path.isfile(src):
        problems.append("no snapshot source/source.md (run tools/snapshot.py)")
    if not os.path.isfile(ana):
        problems.append("no analysis.md with the domain map")
    if problems:
        return fid, {}, problems
    src_lines, secs = sddlib.parse_source(src)
    a = sddlib.parse_analysis(ana)
    result = {}
    for name in a["order"]:
        sl = a["slices"].get(name)
        if not sl or sl["items"] is None:
            problems.append("domain %s: no 'Read:' list in section 'Source slices'" % name)
            continue
        if not sl["items"]:
            problems.append("domain %s: 'Read:' list is empty" % name)
            continue
        result[name] = sddlib.build_slice(fid, name, sl["items"], src_lines, secs)
    return fid, result, problems


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Build per-domain slices of the source snapshot.")
    ap.add_argument("feature", help="feature folder")
    ap.add_argument("--domain", help="rebuild only this domain")
    ap.add_argument("--check", action="store_true", help="do not write, report stale or missing slices")
    args = ap.parse_args(argv)
    fdir = os.path.abspath(args.feature)
    if not os.path.isdir(fdir):
        print("error: folder not found: %s" % args.feature)
        return 2

    _, result, problems = plan(fdir)
    out_dir = os.path.join(fdir, "source", "domains")
    bad = 0
    for p in problems:
        print("error: " + p)
        bad += 1
    names = [args.domain] if args.domain else sorted(result)
    if args.domain and args.domain not in result:
        if not problems:
            print("error: domain %s is not in the domain map" % args.domain)
        return 1
    written, stale = [], []
    for name in names:
        text, errors = result[name]
        for ln, e in errors:
            print("error: analysis.md:%d: domain %s: %s" % (ln + 1, name, e))
            bad += 1
        path = os.path.join(out_dir, name + ".md")
        current = "\n".join(sddlib.read_lines(path)) + "\n" if os.path.isfile(path) else None
        if current == text:
            continue
        if args.check:
            stale.append(name)
        elif not errors:
            sddlib.write_text(path, text)
            written.append(name)
    if not args.domain and os.path.isdir(out_dir):
        for f in sorted(os.listdir(out_dir)):
            if f.endswith(".md") and f[:-3] not in result:
                print("warning: source/domains/%s is not in the domain map; delete it if the domain was removed" % f)
    if args.check:
        for name in stale:
            print("stale: source/domains/%s.md" % name)
        print("Slices: %d, stale or missing: %d, errors: %d." % (len(names), len(stale), bad))
        return 1 if (stale or bad) else 0
    print("Slices: %d, rebuilt: %d (%s), already up to date: %d, errors: %d." % (
        len(names), len(written), ", ".join(written) or "-", max(0, len(names) - len(written) - bad), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
