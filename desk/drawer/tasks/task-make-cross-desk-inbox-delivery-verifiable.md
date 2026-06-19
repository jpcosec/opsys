# Make cross-desk inbox delivery verifiable and actionable

ID: task-make-cross-desk-inbox-delivery-verifiable
Status: deferred
Priority: high

## Goal

Make cross-desk inbox communication operationally useful by ensuring the sender, target, delivery result, and follow-up path are explicit across project desks.

## Scope

- define what successful cross-desk inbox delivery must prove
- require clear sender and target identity instead of inferred ambiguity
- decide how recipients discover, acknowledge, or pull pending cross-desk updates
- design a reply or follow-up path so inbox notes do not become write-only dead drops
- identify the minimum implementation slice needed before inbox can be treated as a real horizontal coordination surface

## Done When

- Cross-desk inbox behavior has an explicit contract for sender identity, target identity, delivery evidence, and recipient follow-up.
- The design explains how inbox notes become actionable across desks instead of isolated local files.
- The task yields a scoped implementation slice or sibling-repo routing plan for the missing coordination surfaces.

## Related Issues

- `desk/drawer/issues/issue-fix-inbox-sender-project-resolution.md`
- `desk/drawer/issues/issue-add-desk-update-sync-command.md`
- `desk/drawer/issues/issue-establish-canonical-repository-identity-through-sldb.md`

## Suggested Pills

- `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`
- `desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
