# Decide SLDB KGDB operational boundaries

ID: question-sldb-kgdb-operational-boundaries
Status: deferred

## Question

Which operations should deskops perform through SLDB APIs, KGDB APIs, shell commands, or its own CLI wrappers?

## Why It Matters

The workflow depends on SLDB for modeled documents and semantic indexes, and KGDB for relations and traversal. Deskops should not duplicate either layer, but it must provide a coherent user path.

## Needs Answer Before

- graph trace commands
- closeout knowledge gates
- drift checks
- init/bootstrap repair behavior
