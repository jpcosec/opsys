REFORMULACION
Propósito: inventariar el estado real de graph_ui (Board, tareas, código y sesiones activas) y reconciliarlo con los nodos de este plan que afecten a graph_ui, incluido el SPEC externo. Resultado: `auditoria/ui.md` con correspondencias, solapamientos y evidencia por path/hash/commit. Repo dueño: deskops; lectura principal: `../UIs/graph_ui` y `/home/jp/proyectos/softfactory_spec/SPEC.md`. Límites: no cambiar tareas ni sesiones ajenas, no ejecutar producto, no aceptar deltas ni producir autorización de implementación.

AMBIGUEDADES
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui» frente a «Tabla de mapeo para cada nodo graph_ui». No queda fijado si «nodo graph_ui» significa solo `owner_repo: graph_ui` o también nodos de otros repos que producen contratos/validaciones para graph_ui (WS11, WS12, WS16). Obligaría a inventar el criterio de inclusión y el tamaño de la tabla.
2. «reconciliar también el SPEC externo (...) con path y hash» y `SPEC externo = /home/jp/proyectos/softfactory_spec/SPEC.md`. No se define qué hacer si ese archivo no existe, no es legible o cambia durante la ejecución; obligaría a inventar si detener, registrar ausencia o continuar sin reconciliación.
3. «Cada tarea externa con path, estado observado, hash» y «Hash = SHA256 del archivo de tarea», pero el alcance admite «tarea o entrada del Board». Para una entrada del Board sin archivo de tarea no hay hash definido; obligaría a inventar el identificador o la evidencia exigida.

DRY-RUN
Un ejecutor futuro leería el brief/glosario de WS01, el Board y tareas de graph_ui, `git status`/historial y paneles herdr, los commits citados y el SPEC; después escribiría únicamente `auditoria/ui.md`. Consumiría WS01 como prerrequisito y no tendría gates propios. Ante archivo de tarea, SPEC o panel ausente, registraría el hueco sin sustituirlo. Validaría: una fila por nodo incluido, path/símbolo, commit si procede, hash SHA256 cuando exista archivo, solapamientos y categorías del SPEC; finalmente comprobaría que no modificó tareas ni sesiones.

FUTURO
WS06 consume esta matriz para proponer correspondencias por repo; WS11/WS12 solo enlazan contratos y actas existentes. La promoción de WS04 requiere preflight de tarea y autorización humana; este nodo no ejecuta ni acepta deltas.
