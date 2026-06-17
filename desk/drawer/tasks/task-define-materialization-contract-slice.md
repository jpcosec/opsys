# Define materialization contract slice (deskops surface)

ID: task-define-materialization-contract-slice
Status: deferred
Priority: medium

## Goal

Implement the deskops CLI and contract definition surface for materialization.

## Scope

- source atom references
- target artifact identity/path
- materialization intent model
- validation checks
- generated/projection metadata

KGDB relation extraction for materialization is routed to the sibling `kgdb` repo's inbox. This task assumes the extraction API exists.

## Done When

- A materialization contract can be declared via deskops CLI or model
- Contract validates source existence and target path
- Contract metadata (intent, projection, validation rules) is queryable
