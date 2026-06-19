# Establish horizontal desk discovery and canonical identity

ID: task-establish-horizontal-desk-discovery-and-identity
Status: deferred
Priority: high

## Goal

Make desks discoverable to each other through one canonical per-project identity path, so cross-repo workflow commands can resolve sibling desks without ambiguous local heuristics.

## Scope

- define the minimal per-project desk identity contract
- decide how local desk identity relates to SLDB-backed ecosystem registration
- make repo self-discovery answer "who am I?" reliably at the current root
- make sibling desk discovery answer "where is that repo's desk?" reliably from canonical identity
- route duplicate-root and duplicate-id ambiguity into explicit failure instead of first-match guessing

## Done When

- There is one documented canonical identity path for the current repo and one lookup path for sibling repos.
- Cross-desk routing no longer depends on scanning arbitrary `desk/registry/*.md` files and taking the first match.
- The work produces explicit follow-up implementation notes for `deskops inbox`, repo targeting, and future desk federation.

## Related Issues

- `desk/drawer/issues/issue-establish-canonical-repository-identity-through-sldb.md`
- `desk/drawer/issues/issue-add-repo-self-identity-document.md`
- `desk/drawer/issues/issue-fix-inbox-sender-project-resolution.md`

## Suggested Pills

- `desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md`
- `desk/contexts/pill-004-opsys-boundary.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
