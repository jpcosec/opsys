---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T17:19:08'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# tests: fixture autouse que limpia los caches globales de sldb después de cada test

_Describe the incoming message with enough evidence to triage._

La suite completa de deskops en UN proceso crece a 3-6 GB: los caches de sldb son globales del proceso (sldb.store.runtime_cache _STORES/_DOCS, sldb.store.built_cache, sldb.cli.alert_sink._KEPT) y tests/conftest.py no los limpia. Con MemoryMax=2G la suite muere por OOM a la mitad, y hoy se corre un proceso por archivo como paliativo. Propuesta: una fixture autouse en tests/conftest.py que, después de cada test, llame a sldb.store.runtime_cache.invalidate_runtime_cache(), sldb.store.io.invalidate_index_cache(), sldb.store.built_cache.clear() y sldb.cli.alert_sink.forget(). Aceptación: la suite completa en un solo proceso termina bajo MemoryMax=2G. Pedido del overlord (sldb-1-9e) por el coordinador de proyecto SLDB_1, 2026-11-06.
