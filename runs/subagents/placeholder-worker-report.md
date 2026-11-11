# placeholder-worker: deskops edit no guarda el placeholder de la plantilla como contenido

Plan `deskops-como-config`, worker `placeholder-worker`, rama `wt/placeholder` (base `9035ca60`).
TaskDoc: `task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com` (task.debug).

## Causa raíz

Confirmada en deskops, no en sldb.

1. La plantilla de cada modelo con secciones (`TaskDoc`, `InboxNoteDoc`, …) pone un párrafo literal en
   cursiva antes del marcador del campo (`_Outline the expected implementation route or affected surface._`
   y luego `⸢rev•implementation_path⸥`). Para sldb ese párrafo es un recipe `paragraph` sin props con
   `anchor: True`: el render lo escribe siempre y extract lo consume como ancla (sldb 9dcabd9a: solo
   ancla un párrafo con ese texto exacto), así que el campo nunca lo contiene.
2. `deskops edit <subject> <sel> <campo> <valor>` pasa por `DeskopsOperations.edit_artifact_field` →
   `doc_access.edit_artifact_field`, que asigna `payload[campo] = _parse_field_value(...)` con el texto
   tal cual (para un campo `str` el valor crudo, sin tocar) y llama a `write_doc`, que renderiza.
3. Si el valor ya trae el párrafo placeholder (el caso 3 de la reproducción: el texto crudo de la sección,
   que lo incluye, más el texto nuevo; es lo que hizo la corrida scion de CC33c, 4305c7d9), el render
   escribe el ancla de la plantilla y después el valor, que lo repite: dos copias. Extract consume solo la
   primera como ancla y devuelve la segunda como contenido, así que cada edición de este tipo suma una
   (reproducción: [1, 2, 3]).
4. Los casos 1 y 2 de la reproducción son estables porque su valor no trae el párrafo (valor limpio, o el
   que extract ya devolvió sin el ancla).

No hay nada que corregir en sldb: render y extract son simétricos para cualquier payload que no traiga el
literal; lo que falta es que la escritura de deskops normalice la entrada con el mismo criterio con que
extract la lee. El único normalizador existente es `_TASK_SECTION_PLACEHOLDERS` en
`deskops/cli/commands/promote.py`, una lista a mano de los placeholders de TaskDoc que usa solo
`_parse_task_sections` (promote desde una nota de inbox), no la escritura de edit.

Arreglo (r1-r2): un helper en `deskops/doc_access.py` que lee los placeholders de la plantilla del propio
modelo (los recipes de sldb: párrafo literal ancla seguido del recipe del campo string) y quita del valor
los párrafos de nivel superior que son exactamente ese texto; `edit_artifact_field` lo llama antes de
escribir. promote.py pasa a leer de la misma fuente.
