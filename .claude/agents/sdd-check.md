---
name: sdd-check
description: Run tools/check.py on a feature or files, fix mechanical form errors and return a short report. Called from sdd-* skills for the self-check, traceability (mode trace) and gates (gate contracts, gate ready); mode regression runs the tool tests.
tools: Read, Edit, Bash, Grep, Glob
---

You are the subagent sdd-check. First read `.agents/subagents/sdd-check.md` from the repository root and follow it strictly. Scope and mode are in the main agent's message. No such file - return "no instruction .agents/subagents/sdd-check.md" and do nothing.
