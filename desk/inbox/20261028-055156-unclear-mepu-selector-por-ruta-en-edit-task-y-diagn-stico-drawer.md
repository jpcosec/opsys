---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: mepu_ocs_dev
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-28T05:51:56'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# MEPU: selector por ruta en edit task y diagnóstico drawer

_Describe the incoming message with enough evidence to triage._

Para equipo deskops, desde MEPU (coordinador repos-9f). Fricción observada, no reparada aquí:
deskops edit task desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md scope '<contenido>' --root .
Error: No artifact.task file found for selector 'desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md'
deskops desk replace desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md --old '<Scope anterior>' --new '<Scope con evidencia>' --root .
Error: archivo modelado; use deskops edit task <selector> <field> <value>.
Diagnóstico: edit task SÍ soporta drawer/tasks. El selector admite basename/stem/prefijo, no ruta. Repetir con el stem funcionó. Mejora solicitada: error que explique la diferencia o aceptar rutas contenidas en desk; ejemplo drawer en help. No presentar como bug de soporte de drawer.
Además promote retira inbox origen y conserva su referencia junto a placeholders en el Scope, aunque copia el cuerpo completo. Mejorar legibilidad para no parecer vacío o perdido.
Envío inicial --to deskops falló: Repository id 'deskops' not found in registry at '/home/jp/AntonIA/repos/legacy/mepu/mepu/desk/registry' (found: none). Se usa destino explícito --desk-root; no se cambia registro global.
Sin cambios de código, commit ni reparación.
