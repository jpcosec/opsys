# Add knowledge drift check routine

## Kind

feature

## Status

open

## Problem

There is no routine that checks whether a change made atoms stale, made materializations stale, or made implementation violate known atoms/specs.

## Desired Outcome

Add a routine or checklist used during testing and closeout that asks which knowledge surface changed and what must be updated or routed.

## Questions

- Should this start as a ritual checklist or a CLI command?
- Which file changes should trigger atom/materialization review?
- Should drift checks block closeout or only create follow-up issues?

## Related Atoms

- atom-drift-checks-compare-atoms-materializations-implementation
- atom-closeout-validates-knowledge-surfaces
- atom-phase-gates-prevent-agent-skipping
