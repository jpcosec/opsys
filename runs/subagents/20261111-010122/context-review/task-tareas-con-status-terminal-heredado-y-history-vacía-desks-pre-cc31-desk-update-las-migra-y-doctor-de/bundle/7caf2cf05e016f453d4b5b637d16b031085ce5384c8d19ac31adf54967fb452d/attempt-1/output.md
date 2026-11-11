## REFORMULACION

Nodo ejecutable `task.debug` (no agregado): corregir deskops para desks pre‑CC31 con tareas de status terminal heredado y `history` vacía. Resultado: `deskops desk update` (dry‑run/`--apply`) migra según la tabla d1 o reporta lo indecidible; `doctor` y `desk update` reportan documentos inválidos uno por uno sin caer; `closeout retire` retira `superseded`, `cancelled` y `deferred` heredadas. Repo: deskops (`deskops/models/task_lifecycle.py`, `cli/commands/desk.py`, `workspace.py`, `services/closure.py`, `cli/commands/closeout.py`, `doctor_findings.py`, `tests/`, `docs/`, `CHANGELOG.md`). Límites: no relajar el validador salvo `cancelled` en `LEGACY_RESOLVED_STATUSES`; no tocar desks de AntonIA; no cambiar la gramática del CLI; no escribir en desks reales.

## AMBIGUEDADES

1. “Goldens de ayuda idénticos” frente a “La ayuda y su golden se actualizan solo en la lista de status aceptados; ese golden de ayuda es el único que cambia, con autorización.” Obliga a inventar qué golden prevalece y quién autoriza.
2. “Test de reproducción sobre tmp_path con las cinco formas” frente a “las 5 tareas … más una cancelled y una closed”. Obliga a inventar si son cinco o siete fixtures y si `candidate` entra.
3. “retire acepta además superseded, cancelled y deferred (y candidate) con history vacía.” Obliga a inventar si `candidate` es obligatorio, opcional o solo ejemplo.
4. “Si en el código resulta más claro, puede ser un subcomando propio”. Obliga a inventar el criterio de claridad y el contrato exacto de ese subcomando.

## DRY-RUN

Lecturas: input, TaskDoc y validador, CLI `desk update`, `workspace.py`, `closure.py`, `closeout.py`, `doctor_findings.py`, tests/docs/CHANGELOG y log de reproducción. Cambios previstos: migración por frontmatter con tabla d1, reporte por campo, hallazgos por documento, `retire` ampliado, tests de reproducción, doc y CHANGELOG. Dependencias: comportamiento de `sldb stores check`, escritura vía `desk_transaction`/`replace_text`, fixtures en `/dev/shm`, guardas de pytest. Validaciones futuras: tests de reproducción e idempotencia; doctor continúa tras inválido; goldens; copia del gateway con `stores check` rc 0; cuatro pasos del workflow.

## FUTURO

El coordinador corre los cuatro pasos en clon limpio y abre la nota a sldb. Los dueños de AntonIA ejecutan `desk update --apply`. Un humano autoriza el golden de ayuda y las decisiones revisables; sldb puede corregir el aborto de `stores check`.
