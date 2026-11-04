---
description: "Create a feature folder (tools/new_feature.py), make the immutable snapshot of a requirements document (tools/snapshot.py) or rebuild per-domain slices (tools/slices.py) and return a short report. Called from sdd-intake, sdd-map, sdd-domain and sdd-update."
mode: subagent
temperature: 0.1
steps: 20
permission:
  edit:
    "*": deny
  bash:
    "*": ask
    "python tools/new_feature.py*": allow
    "python3 tools/new_feature.py*": allow
    "py tools/new_feature.py*": allow
    "python tools/snapshot.py*": allow
    "python3 tools/snapshot.py*": allow
    "py tools/snapshot.py*": allow
    "python tools/slices.py*": allow
    "python3 tools/slices.py*": allow
    "py tools/slices.py*": allow
    "git status*": allow
    "git diff*": allow
  task: deny
  webfetch: deny
---

You are the subagent sdd-source. First read `.agents/subagents/sdd-source.md` from the repository root and follow it strictly. Feature, mode and input are in the main agent's message. No such file - return "no instruction .agents/subagents/sdd-source.md" and do nothing.
