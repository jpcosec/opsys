---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-27T20:02:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout: la compuerta tests (missing_tests_evidence) bloquea tareas que

_Describe the incoming message with enough evidence to triage._

closeout: la compuerta tests (missing_tests_evidence) bloquea tareas que solo cambian specs o docs. Caso: MEPU SPEC-2 (task-spec-2-spec-de-ingesta-..., PR #101, 1130d14b) cambió solo specs/etl/ingesta.yml, su render y el catálogo; no hay test que lo cubra y citar uno ajeno sería falso. Se cerró con 'deskops advance task --to closed' (override) el 2026-10-27; la compuerta de átomo sí pasó con átomos reales. Pedido: que closeout commit/verify acepten una tarea sin tests cuando los archivos cambiados son solo specs/docs/rendered (o un --no-tests --reason explícito que quede en el trailer, como Closeout-Mode: manual), en vez de obligar a forzar la transición, que no deja commit de cierre ni índice.
