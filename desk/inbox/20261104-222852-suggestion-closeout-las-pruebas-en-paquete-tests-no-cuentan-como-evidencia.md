---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-04T22:28:52'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout: las pruebas en <paquete>/tests no cuentan como evidencia

_Describe the incoming message with enough evidence to triage._

En heyantonia/Chatbot_Infra las pruebas viven en ops/tests, runtime/*/tests y paquetes/*/tests, no en <root>/tests. reference_points_to_test (services/closeout_gates.py) solo acepta archivos bajo <root>/tests, así que una tarea de código con tests declarados no puede cerrar aunque cite ops/tests/test_wiki_desk.py. Propuesta: aceptar cualquier test_*.py existente dentro del repo (o las testpaths de pytest del pyproject). Hoy se cerraron tres tareas de la wiki declarando commit+document.
