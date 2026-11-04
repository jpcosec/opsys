---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-04T18:06:58'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Cambios solo de desk van directo en el checkout principal, nunca en un worktree

_Describe the incoming message with enough evidence to triage._

JP (04-11-2026, desde MEPU): crear una tarea, mandar notas al inbox, editar un campo o hacer un closeout se hace con deskops en el checkout principal del repo, sobre su rama de integración (p. ej. dev): ponerse al día con el remoto, git add solo de los archivos de desk/ que tocó deskops (nunca git add -A: otras sesiones pueden tener cambios sin commitear ahí), commit con [skip ci] y push. Los worktrees son para cambios de código que pasan por PR; armar un worktree para documentar una tarea es ceremonia. Ya quedó en ~/.claude/CLAUDE.md y en la skill deskops-workflow (~/.claude/skills). Propuesta: llevarlo a la guía del propio deskops (use-deskops / deskops-task-lifecycle) y, si aplica, que deskops avise cuando se corre dentro de un worktree secundario.
