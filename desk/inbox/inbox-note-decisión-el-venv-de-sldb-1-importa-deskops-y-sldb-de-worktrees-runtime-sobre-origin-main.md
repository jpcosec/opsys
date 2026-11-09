---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-09T13:49:29'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Decisión: el venv de SLDB_1 importa deskops y sldb de worktrees runtime sobre origin/main

_Describe the incoming message with enough evidence to triage._

Decidido por el overlord el 2026-11-09, revisable. ~/proyectos/SLDB_1/.venv tiene deskops y structuredLanguageDB instalados en modo editable desde ~/proyectos/SLDB_1/deskops-runtime y ~/proyectos/SLDB_1/sldb-runtime: worktrees limpios, con --detach sobre origin/main, que el coordinador de proyecto avanza después de cada integración. Antes apuntaba a los checkouts compartidos ~/proyectos/SLDB_1/deskops y ~/proyectos/SLDB_1/sldb, que iban 65 y 39 commits detrás y tenían cambios ajenos sin commitear. IMPORTANTE: los cambios sin commitear de esos checkouts compartidos YA NO tienen efecto a través del venv. Quien dependa de ellos tiene que commitearlos o usar su propio PYTHONPATH. Rollback exacto: .venv/bin/pip install --no-deps -e ~/proyectos/SLDB_1/sldb && .venv/bin/pip install --no-deps -e ~/proyectos/SLDB_1/deskops. Detalle en reports/coordinador-proyecto.md y en reports/venv-runtime-20261109/.
