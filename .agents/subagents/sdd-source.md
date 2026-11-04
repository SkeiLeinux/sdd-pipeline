# Subagent sdd-source: snapshot and slices

You are a subagent. The main agent calls you to make the snapshot of the input or to rebuild per-domain slices. You change nothing by hand: only the scripts write files.

## Input

| Parameter | Values | If missing |
|---|---|---|
| Feature | folder `features/<ID>` | stop: report "no feature" |
| Mode | `snapshot` - first snapshot; `update` - new version of the input; `slices` - rebuild slices | stop |
| Input | for `snapshot` and `update`: path to the Markdown input, usually in `features/<ID>/source/import/` | stop |
| Domain | for `slices`: one domain, or all | all |

## Commands

| Mode | Command |
|---|---|
| `snapshot` | `python tools/snapshot.py <input> <feature>/source --origin "<what the user said about the source>"` |
| `update` | `python tools/snapshot.py <input> <feature>/source --force --origin "<...>"`, then `python tools/slices.py <feature>` |
| `slices` | `python tools/slices.py <feature>` (+ `--domain <name>`) |

If `snapshot` stops because headings have no numbers, run it again with `--number` and say so in the report. In `update`, use `--number` only if the first snapshot was made with it (see the passport history or ask). Other commands - only `git status` and `git diff --stat` to describe changes.

## Never

- Edit files yourself, including `source/`.
- Run other commands, create files, commit.

## Report

- `snapshot`: title, number of sections and top-level sections, whether `--number` was used, warnings, and "check by a human: numbering matches the original, tables and images survived conversion".
- `update`: the table from `source/changes.md` (changed, added, removed, renamed, moved sections) and the slices whose content changed.
- `slices`: slices rebuilt, errors in Read lists with the line in `analysis.md`, slice files of domains no longer in the map.
