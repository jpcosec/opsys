---
sldb:
  by: agent
  at: '2026-11-11T08:50:21Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-11T08:50:19Z'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# una task.code no puede cerrar en un desk cuando su código vive en otro repo

_Describe the incoming message with enough evidence to triage._

Caso de AntonIA (2026-11-11): task-el-almacén-sellado-del-kit-no-guarda-lotes-de-más-de-9300-filas vive en el desk de Governance y su código en Chatbot_Infra (#400, 87671716). advance se frena en task_hands_to_closeout (nonempty(validation)); closeout verify da missing_tests_evidence y missing_commit_evidence porque ni el commit ni el test existen en el repo del desk; resolved-by exige un commit ancestro local y un test .py del repo. Vía actual (decisión del coordinador, revisable): tarea espejo en el desk del repo del código cerrada con resolved-by, supersede en el desk coordinador apuntando a ella, y task.external para lo que viene. Falta en deskops: (a) que desk update o add task sugiera task.external cuando files o references apuntan a otro repo; (b) o que la evidencia commit/tests acepte referencias calificadas por repo (repo:sha, repo:path) verificadas contra un repo registrado (deskops repo register).
