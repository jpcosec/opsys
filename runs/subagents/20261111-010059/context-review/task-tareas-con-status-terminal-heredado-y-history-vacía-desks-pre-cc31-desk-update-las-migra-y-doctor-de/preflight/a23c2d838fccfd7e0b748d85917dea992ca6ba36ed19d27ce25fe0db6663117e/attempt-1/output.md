## REFORMULACION

Propósito: corregir deskops para desks pre-CC31 con tareas de status terminal heredado y `history` vacía. Resultado: `desk update --apply` (o subcomando) migra según tabla y reporta las indecidibles; `doctor` y `desk update` aíslan documentos inválidos sin abortar; `closeout retire` retira también superseded/cancelled/deferred/candidate heredadas. Repo: deskops, superficies listadas (`task_lifecycle.py`, `desk.py`, `workspace.py`, `closure.py`, `closeout.py`, `doctor_findings.py`, tests, docs, CHANGELOG). Límites: no relajar el validador salvo `cancelled` en `LEGACY_RESOLVED_STATUSES`; no tocar desks de AntonIA; no cambiar gramática CLI salvo ayuda de retire; no editar a mano `desk/`/`.sldb/`; no `git add -A`; tests aislados con TMPDIR y guarda pgrep. El nodo es una tarea, no un agregado ejecutable.

## AMBIGUEDADES

1. "desk update --apply (o un subcomando de migración con dry-run)" y "Si en el código resulta más claro, puede ser un subcomando propio": obliga a elegir superficie CLI, nombre y goldens.
2. "'cancelled' se suma a LEGACY_RESOLVED_STATUSES" frente a "OUTSIDE_LIFECYCLE_STATUSES (con cancelled sumado)": no queda claro si `cancelled` entra en ambos conjuntos; obliga a inventar la constante.
3. "retire acepta además superseded, cancelled y deferred (y candidate)": el paréntesis no aclara si `candidate` es aceptado o solo mencionado; obliga a decidir la lista.
4. "los de salida, salvo los mensajes nuevos con golden propio": no identifica qué mensajes exactos requieren golden; obliga a inventar el inventario.

## DRY-RUN

Lecturas: tarea, código citado, tests/goldens, docs y CHANGELOG. Cambios previstos: constantes de ciclo de vida; lectura por frontmatter y validación por documento en doctor/update; migración idempotente y dry-run; retire con estados heredados; ayuda/golden de retire; fixtures de 7 tareas; doc, CHANGELOG e informe. Dependencias: `TaskDoc`, `desk_transaction`/`sldb replace_text`, goldens, pytest con TMPDIR y guarda pgrep. Validaciones futuras: reproducción antes/después, segunda corrida idempotente, doctor continúa ante inválido, ayuda intacta, copia del gateway con `stores check` rc 0 y 4 pasos en clon limpio.

## FUTURO

El coordinador corre los 4 pasos en clon limpio y abre la nota a sldb; el overlord/coordinador confirma decisiones revisables (cancelled, subcomando); autoriza el golden de ayuda; los dueños de otros desks ejecutan la migración; el revisor acepta el informe.
