# Issue: `deskops desk install` requires a pre-existing target directory

## Kind

issue

## Status

open

## Evidence

Found during the sandbox proof of task-sync-pi-skills (2026-09-29, executor
evidence in `runs/subagents/20260929-task-sync-pi-skills/validation.log`):

```
$ python -m deskops desk install .tmp/deskops-cli-test
```

fails when the target directory does not exist; the operator must run
`mkdir -p .tmp/deskops-cli-test` first. With the dir present, install
scaffolds `desk/` correctly (tasks, contexts, ...).

## Problem

`desk install` is a bootstrap/repair surface; requiring a pre-existing target
dir is a small but avoidable operator friction, especially for the documented
first-use flow `deskops init`/`deskops desk install .` on fresh roots.

## Candidate fix

Auto-create the target directory (and parents) in `deskops desk install`, or
emit a clear "target dir does not exist; create it first" error instead of the
current failure mode.

## Notes

Minor: not a documented-path failure, but per pill-cli-gaps-become-tracked-work
it is routed here instead of staying in session memory.
