# Audit apply summary

Script: `/tmp/rw/audit/apply.sh` (exit 0, validated end-to-end on fresh worktrees `/tmp/rw/base2`, `/tmp/rw/base3`, `/tmp/rw/base4`).

## Edits (UPDATE rows applied via `deskops edit`)

45 documents edited with 64 commands:

| folder | documents | commands |
|---|---:|---:|
| `desk/atoms/` (top-level, excluding `tag-namespaces.yaml`) | 11 | 11 |
| `desk/atoms/knowledge-model/` | 4 | 5 |
| `desk/atoms/workflow-model/` | 20 | 32 |
| `desk/contexts/` | 5 | 6 |
| `desk/rituals/` | 1 | 2 |
| `desk/registry/` | 2 | 2 |
| `desk/tasks/` | 1 | 2 |
| `desk/drawer/tasks/` | 1 | 4 |
| **total** | **45** | **64** |

37 UPDATE rows are no-verb and listed in `/tmp/rw/audit/no-verb.md`.

## Retirements (RETIRE rows)

19 items retired:

| folder | count | items |
|---|---:|---|
| `desk/atoms/` | 4 | anti-pattern-monolithic, hook-automation, kgdb-is-graph-substrate, kgdb-should-parallel |
| `desk/contexts/` | 1 | pill-operator-manual-follows-stable-runnable-slices |
| `desk/rituals/` | 1 | ritual-deployment-ritual |
| `desk/steps/` | 2 | step-build, step-document-the-cli |
| `desk/faq/` | 3 | faq-how-to-deploy, faq-how-to-test, faq-how-to-test-comprehensively |
| `desk/features/` | 1 | feature-atom-model-kinds-and-question-facets |
| `desk/models/` | 1 | `__init__.py` (leftover of removed package) |
| `desk/drawer/features/` | 2 | workflow-execution-engine, feature-materialization-pipeline |
| `desk/drawer/stress-tests/` | 2 | st-06-spec-pipeline, st-10-materialization |
| `desk/drawer/use-cases/` | 1 | uc-06-spec-to-artifact-pipeline |
| `desk/inbox/` | 1 | 20260827-165024 (empty closed note) |
| **total** | **19** | |

No files existed under `desk/__pycache__`, `desk/drawer/__pycache__`, `desk/cli/`, `desk/materializers/`, or `desk/primitives/` in this worktree; the leftover loop was exercised with synthetic `__pycache__` files in `/tmp/rw/base6` and removed them all.

## Failed commands and fixes

- First run: four health atoms lost their unmodeled trailing sections (`## Boundary Rationale`, `## Delegation Pattern`, `## Diagnostic Surface`, `## Repairability`, `## Owned Operations`) because the AtomDoc `answer` field extracts everything after `## Answer`. Fix: pass the preserved tail inside the `answer` value, with the stale runtime-deletion lines removed and the diagnostic/repair sections updated, so the CLI write keeps them.
- First run: closeout ritual kept the old "Untrack the task" and "Delete the resolved task file" steps and appended the replacement at the end. Cause: extracted step values carry a `1. ` prefix, so the filters did not match. Fix: normalize `^\d+\.\s*` before matching, dedupe any prior replacement, and insert the replacement before the supersede step.
- Leftover `desk/drawer/__pycache__` files cannot go through `deskops retire` (it refuses every `desk/drawer/` path as having a dedicated verb), so the leftover loop removes those with `deskops drawer remove <path>`; all other leftover paths use `deskops retire`.
- `deskops retire` used `--force` only where the remaining reference has no edit verb or is a historical archive: pill-operator-manual (drawer Board pills list), the empty inbox note (historical drawer issue mention), and step-document-the-cli (`desk/drawer/stress-tests/findings-archive.md`, an allowed historical archive). Drawer removals ran without `--force`.

## No-verb list

See `/tmp/rw/audit/no-verb.md` (37 files: `tag-namespaces.yaml`, the supervisor role body, and 35 drawer README/feature/issue/question/ritual/stress-test/task-board/use-case files).

## Final checks (`ROOT=/tmp/rw/wt/apply`)

`python -m sldb stores check --store .sldb` (exit 1, same as HEAD baseline):

```
FAIL: store integrity — 215 documents in 17 models — 2 damaged
```

`python -m deskops doctor --root .` (exit 1, same as HEAD baseline):

```
Doctor Findings:
- Legacy desk detected: sldb stores check failed
- Invalid desk documents: desk/inbox/20261018-213734-unclear-corrida-candidata-de-la-suite-sldb-1-spec2viz-tools-suite-check-sh-fr.md (missing), desk/inbox/20261018-214355-suggestion-faltan-verbos-para-retirar-pills-y-notas-cerradas-del-inbox.md (missing)
```

`python -m deskops graph missing --root .` (exit 1; baseline HEAD had 6 missing):

```
2 missing, 136 informational
```

The three failures are pre-existing at HEAD `2ec128a` (verified in `/tmp/rw/base`), not caused by the applied edits/retirements.
