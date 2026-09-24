# Decide SLDB KGDB operational boundaries

ID: question-sldb-kgdb-operational-boundaries
Status: resolved (2026-09-24)

## Question

Which operations should deskops perform through SLDB APIs, KGDB APIs, shell commands, or its own CLI wrappers?

## Why It Matters

The workflow depends on SLDB for modeled documents and semantic indexes, and KGDB for relations and traversal. Deskops should not duplicate either layer, but it must provide a coherent user path.

## Needs Answer Before

- graph trace commands
- closeout knowledge gates
- drift checks
- init/bootstrap repair behavior

---

## Answer (2026-09-24)

The question assumed two sibling substrates and a deskops choice between their
APIs. There is only one now: the graph contracts live in sldb, and `kgdb` is no
longer a separate operational surface.

The boundary in force:

- **sldb owns documents**: model contracts, stores, tracked documents, field
  operations, semantic and section indexes. deskops reaches it through a small
  API surface (`sldb.api.documents.track_document_file`, `untrack_document`,
  `sldb.api.stores.init_store`) and nothing else.
- **deskops owns the graph projection**: it extracts nodes and edges from the
  desk and writes its own snapshot under `.sldb/runtime/graphs/`. There is no
  kgdb ingest step to call.
- **deskops owns its CLI**: every workflow verb is deskops', wrapping those two
  layers rather than duplicating them.
- A sldb path that fails becomes an inbox note to sldb, not a workaround here.

Recorded in `README.md` (SLDB boundary) and `AGENTS.md` (core boundaries), which
is where an agent will actually look for it.
