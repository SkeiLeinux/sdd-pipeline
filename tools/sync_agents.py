#!/usr/bin/env python3
"""Copy the canonical skills from .agents/skills/ to tool folders that do not read .agents/.

    python tools/sync_agents.py          copy
    python tools/sync_agents.py --check  report differences, exit 1 if any

.agents/skills/ is the single source of truth. Claude Code reads skills from
.claude/skills/, so the copies there are generated - edit .agents/skills/ and re-run.
Kilo, OpenCode and Codex read .agents/skills/ directly.
"""

import argparse
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".agents", "skills")
TARGETS = [os.path.join(ROOT, ".claude", "skills")]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    skills = sorted(d for d in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, d, "SKILL.md")))
    diffs = []
    for target in TARGETS:
        for name in skills:
            src = os.path.join(SRC, name, "SKILL.md")
            dst = os.path.join(target, name, "SKILL.md")
            if os.path.isfile(dst) and read(dst) == read(src):
                continue
            diffs.append(os.path.relpath(dst, ROOT))
            if not args.check:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
        if os.path.isdir(target):
            for name in sorted(os.listdir(target)):
                if name not in skills:
                    diffs.append(os.path.relpath(os.path.join(target, name), ROOT) + " (not in .agents/skills)")
                    if not args.check:
                        shutil.rmtree(os.path.join(target, name))
    if args.check:
        for d in diffs:
            print("out of sync: " + d)
        print("Skills: %d, out of sync: %d." % (len(skills), len(diffs)))
        return 1 if diffs else 0
    print("Skills: %d, updated: %d." % (len(skills), len(diffs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
