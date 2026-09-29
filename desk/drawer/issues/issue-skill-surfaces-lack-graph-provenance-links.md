# Issue: agent-facing skill surfaces have no graph provenance links

## Kind

issue

## Status

open

## Evidence

`deskops closeout verify` for task-sync-pi-skills (2026-09-29) reported
`missing_changed_file_link` for every changed skill surface
(`.pi/skills/use-deskops/SKILL.md`, `.pi/skills/deskops-task-lifecycle/SKILL.md`)
and for the new guard test: changed files with no atom/materialization link in
the graph, coverable only by a routed follow-up reference.

## Problem

Skill docs (especially under the gitignored `.pi/`) and test files carry no
declared atom/materialization provenance, so closeout cannot prove their
knowledge links per changed file; the gap recurs on every skill-touching task.

## Candidate fixes

- Declare `source_atoms`/provenance metadata for skill docs where the
  materialization contract applies, or
- teach the closeout link gate to accept a matching drift-guard test as the
  link surface for gitignored skill trees (see
  atom-git-ignored-skill-trees-need-tracked-drift-guards).

## Notes

Routed from closeout verify per the closeout ritual; do not close skill tasks
by weakening the gate silently.
