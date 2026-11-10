---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-09T21:53:46'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Decisión revisable por JP: review record firma preflight/bundle humano, contradice pill-zero-context-preflight-precedes-executor

_Describe the incoming message with enough evidence to triage._

Decidido por el coordinador de proyecto el 2026-11-09, revisable por JP (DO4 en decisiones.md de deskops-como-config). Para dejar main en verde (fallos 1-3 de e2e_agent del run 42694709414), deskops review record acepta también kind preflight y bundle con evidencia del operador. Desde CC32, task.code exige esos recibos y sin modelo no hay otra vía CLI. Esto CONTRADICE la pill pill-zero-context-preflight-precedes-executor: la aprobación de un experto no sustituye a la revisión barata sin contexto. Condiciones del overlord: (a) el recibo deja visibles engine human, el operador y el motivo 'no model available'; (c) solo se usa en el quickstart y los e2e del CI, y no para activar tareas reales en ningún desk hasta que JP confirme. Alternativas descartadas: task.aggregate en el quickstart, recibos por la API en el escenario (rompe el modo agente) y un runtime determinista (choca con anti-mock).
