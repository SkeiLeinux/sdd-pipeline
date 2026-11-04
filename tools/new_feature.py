#!/usr/bin/env python3
"""Create the folder of a new feature from the templates.

    python tools/new_feature.py <ID> <slug> --title "<title>" [--owner "<name>"] [--source "<origin>"] [--input <file.md>]

Creates features/<ID>-<slug>/ with source/import/, the passport and empty decisions files.
With --input, copies the Markdown input into source/import/. Then make the snapshot:

    python tools/snapshot.py features/<ID>-<slug>/source/import/<file.md> features/<ID>-<slug>/source

Exit codes: 0 - created, 1 - the folder exists or a value is invalid, 2 - usage error.
"""

import argparse
import datetime
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sddlib  # noqa: E402


def fill(text, values):
    for key, value in values.items():
        text = text.replace(key, value)
    return text


def without_blocks(text):
    """Template text up to the first example block '### ' - the file starts empty."""
    head = text.split("\n### ", 1)[0]
    return head.rstrip() + "\n"


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Create a new feature folder from the templates.")
    ap.add_argument("id", help="feature ID, e.g. PAY-42")
    ap.add_argument("slug", help="short Latin kebab-case name, e.g. refunds")
    ap.add_argument("--title", required=True)
    ap.add_argument("--owner", default="<Analyst>")
    ap.add_argument("--source", default="<Where the input came from: document name, link, version>")
    ap.add_argument("--input", help="Markdown input to copy into source/import/")
    ap.add_argument("--root", default=sddlib.ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    cfg = sddlib.load_config(args.root)
    if not re.match(cfg["feature_id_pattern"], args.id):
        print("error: ID '%s' does not match feature_id_pattern %s" % (args.id, cfg["feature_id_pattern"]))
        return 1
    if not sddlib.DOMAIN_NAME.match(args.slug):
        print("error: slug '%s' - use lowercase Latin kebab-case" % args.slug)
        return 1
    if args.input and not os.path.isfile(args.input):
        print("error: input not found: %s" % args.input)
        return 1
    fdir = os.path.join(args.root, "features", "%s-%s" % (args.id, args.slug))
    if os.path.exists(fdir):
        print("error: %s already exists" % sddlib.rel(fdir, args.root))
        return 1

    today = datetime.date.today().isoformat()
    values = {"<ID>": args.id, "<Short feature title>": args.title, "<Analyst>": args.owner,
              "<Where the input came from: document name, link, version>": args.source, "YYYY-MM-DD": today}
    tdir = os.path.join(args.root, "templates", "feature")

    def template(name):
        with open(os.path.join(tdir, name), encoding="utf-8") as f:
            return f.read()

    os.makedirs(os.path.join(fdir, "source", "import"))
    passport = template("passport.md").replace("| YYYY-MM-DD | Input accepted, version <N> |",
                                               "| YYYY-MM-DD | Feature created |")
    passport = fill(passport, values)
    sddlib.write_text(os.path.join(fdir, "README.md"), passport)
    sddlib.write_text(os.path.join(fdir, "decisions", "questions.md"), without_blocks(fill(template("questions.md"), values)))
    sddlib.write_text(os.path.join(fdir, "decisions", "decisions.md"), without_blocks(fill(template("decisions.md"), values)))
    sddlib.write_text(os.path.join(fdir, "decisions", "manual.md"), fill(template("manual.md"), values))
    copied = None
    if args.input:
        copied = os.path.join(fdir, "source", "import", os.path.basename(args.input))
        shutil.copyfile(args.input, copied)

    rel = sddlib.rel(fdir, args.root)
    print("Created %s: README.md, decisions/, source/import/." % rel)
    if copied:
        print("Input copied: %s" % sddlib.rel(copied, args.root))
        print("Next: python tools/snapshot.py %s %s/source" % (sddlib.rel(copied, args.root), rel))
    else:
        print("Next: put the Markdown input into %s/source/import/ and run tools/snapshot.py" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
