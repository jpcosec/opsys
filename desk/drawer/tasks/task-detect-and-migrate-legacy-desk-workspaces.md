# Detect and migrate legacy desk workspaces

ID: task-detect-and-migrate-legacy-desk-workspaces
Status: deferred
Priority: high

## Goal

Make deskops detect legacy or hand-rolled desk layouts explicitly and provide a safe adaptation path into the current modeled workspace contract.

## Scope

- detect legacy `desk/` layouts whose board, task, pill, or ritual docs do not satisfy current deskops models
- distinguish empty/fresh desks from incompatible/legacy desks
- report which current modeled surfaces are missing or malformed
- define a migration or adoption path for legacy boards, tasks, pills, and contexts
- preserve user-authored legacy content instead of overwriting it blindly
- clarify how this interacts with per-project config and desk/version contracts

## Done When

- deskops can identify a legacy desk workspace and explain why it is not compatible with current modeled commands.
- Operators get an explicit adaptation path instead of silent empty listings or generic validation failures.
- The work defines how legacy desks move toward current BoardDoc/TaskDoc-compatible surfaces without losing authored history.

## Suggested Pills

- `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md`
- `desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md`
- `desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md`
