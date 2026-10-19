---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T21:37:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Corrida candidata de la suite SLDB_1 (spec2viz tools/suite-check.sh --fr

_Describe the incoming message with enough evidence to triage._

Corrida candidata de la suite SLDB_1 (spec2viz tools/suite-check.sh --fresh --from-origin --pythons 3.10,3.12,3.13, 2026-10-18, deskops origin/main@63b36df): con Python 3.10.18 (uv) la suite de deskops no colecciona, 42 errors, todos 'ImportError: cannot import name StrEnum from enum' (enum.StrEnum existe desde 3.11). Comando: cd <clon de deskops> && <venv 3.10>/bin/python -m pytest tests -q. Con 3.12 y 3.13 pasa entera. Inconsistencia: pyproject declara requires-python >= 3.10 pero el codigo necesita 3.11; pron, spec2viz y graph_ui ya declaran >= 3.11 y sldb (>= 3.10) si pasa en 3.10. Arreglo probable: requires-python >= 3.11 en deskops, o reemplazar StrEnum por (str, Enum). Log: /tmp/suite-candidate/py3.10/suite-deskops.log
