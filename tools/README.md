# Tools

Python 3.8+, standard library only. Run from the repository root. Agents run them through the subagents `sdd-source` and `sdd-check`; people can run them directly.

```
python tools/snapshot.py <input.md> features/<ID>-<slug>/source [--number] [--force] [--origin "..."]
python tools/slices.py features/<ID>-<slug> [--domain <name>] [--check]
python tools/check.py [features/<ID>-<slug> | files...] [--gate contracts|ready] [--trace] [--next]
python tools/sync_agents.py [--check]
python -m unittest discover -s tools/tests
```

| Script | What it does |
|---|---|
| `snapshot.py` | immutable numbered snapshot of a Markdown document, section index with checksums; with `--force` - `changes.md` against the previous snapshot |
| `slices.py` | per-domain slices of the snapshot from the Read lists of `analysis.md` |
| `check.py` | form, references, coverage, gates, traceability matrix, next free IDs |
| `sync_agents.py` | copies `.agents/skills/` to `.claude/skills/` |
| `sddlib.py` | shared parsing helpers |

Exit codes: 0 - fine, 1 - problems found, 2 - usage error. Rule codes are listed in [docs/artifacts.md](../docs/artifacts.md#checker-rule-codes).
