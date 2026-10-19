---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T22:12:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Limpieza del desk de sldb: cinco huecos del CLI de deskops

_Describe the incoming message with enough evidence to triage._

Gracias por deskops retire: con eso retiré en sldb 18 notas del inbox y 15 pills. En la limpieza aparecieron estos huecos, todos reproducibles en sldb (main, 53735294):

1. deskops add pill no trackea la pill que crea: el archivo queda en desk/contexts/ y doctor lo marca 'Untracked desk documents' hasta correr sldb docs track --model PillDoc. doctor --repair tampoco lo arregla ('Manual repair required').
2. deskops add pill --from-yaml no alcanza: argparse sigue exigiendo --what/--why/--when/--where/--how/--how-not.
3. deskops retire de una pill no la saca de la lista pills: del Board, ni sin --force ni con --force; hubo que hacer deskops edit board Board pills a mano.
4. No hay deskops edit issue: tres issues abiertas de sldb (stable-section-ids, sections-have-no-own-hash, one-way-composition-no-edit-through) citan en related_tasks tasks y pills que ya no existen, y no hay verbo para corregirlo.
5. Una task del drawer en el formato viejo, sin frontmatter (desk/drawer/tasks/task-atom-como-field-tipado-composicion-por-field.md), no se puede editar: deskops edit task falla con 'id Field required', y desk migrate no la adopta. La única salida hoy es add task --from-drawer, que la promueve a activa.

Aparte, una observación sobre el template: todos los documentos renderizados (pills, tasks, Board, registry, notas) llevan las pistas en itálica ('_Explain why..._') encima del contenido real. Si es a propósito, está bien; si no, el lugar para arreglarlo es el template.
