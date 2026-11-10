## REFORMULACION

**Propósito:** fijar el encargo que un ejecutor leería solo desde este TaskDoc: corregir en deskops dos defectos sobre tareas heredadas pre-CC31 (estado terminal con `history` vacía): d1, falta de migración; d2, doctor y `desk update` abortan ante el primer documento inválido.

**Resultado:** `deskops desk update --apply` migra según la tabla de d1 y reporta lo indecidible; doctor y `desk update` reportan inválidos uno por uno sin caer, registrando modelos; tests de reproducción, doc y CHANGELOG.

**Repo:** deskops (rutas `deskops/...`, `tests/`, `docs/`, `CHANGELOG.md`).

**Límites:** no relajar el validador salvo `cancelled` en `LEGACY_RESOLVED_STATUSES`; no tocar desks de AntonIA; no cambiar gramática del CLI; nada manual en `desk/` ni `.sldb/`; nunca `git add -A`; tests con `TMPDIR=/dev/shm` y guarda pgrep.

Este nodo es de revisión (no ejecutable, sin hijos); el encargo descrito sí es ejecutable por un worker futuro.

## AMBIGUEDADES

1. «el arreglo sugerido (deskops advance o closeout según el caso)»: no hay correspondencia caso→comando; obligaría a inventar la regla de elección.
2. «4 pasos del workflow de deskops en clon limpio»: no se enumeran; obligaría a inventar el pipeline y sus comandos.
3. «la guarda de pgrep anclada»: no se da patrón ni forma de anclaje; obligaría a inventar el mecanismo.
4. «archivo, estado anterior y estado nuevo»: para `superseded` el status y `current_node` no cambian; obligaría a inventar qué se registra como “estado nuevo”.
5. «Se deja como hipótesis con nota a sldb»: no se define el canal de la nota; obligaría a inventar issue/documento/comentario.

## DRY-RUN

**Lecturas:** TaskDoc, `models/task_lifecycle.py`, `cli/commands/desk.py`, `workspace.py`, `services/closure.py`, `cli/commands/closeout.py`, `doctor_findings.py`, tests, docs, CHANGELOG; `CLOSEOUT_STATES` y `LEGACY_RESOLVED_STATUSES`.

**Cambios previstos:** añadir `cancelled` a `LEGACY_RESOLVED_STATUSES`; migrador en `desk update --apply` leyendo/escribiendo por ruta de documentos, idempotente; reporte por línea; tolerancia a inválidos en doctor/update; tests, docs y CHANGELOG.

**Dependencias:** validador TaskDoc, comportamiento de `sldb stores check`, registro de modelos.

**Validaciones futuras:** test de las cinco formas, segunda corrida idempotente, doctor continúa, goldens, copia del gateway con stores check rc 0, 4 pasos en clon limpio. Sin ejecutar.

## FUTURO

El worker implementa y entrega `runs/subagents/<worker>-report.md`; el coordinador corre los 4 pasos en clon limpio; los dueños de desks ejecutan `--apply`; un humano decide si `cancelled` se mantiene en `LEGACY_RESOLVED_STATUSES` y cómo se eleva la nota a sldb.
