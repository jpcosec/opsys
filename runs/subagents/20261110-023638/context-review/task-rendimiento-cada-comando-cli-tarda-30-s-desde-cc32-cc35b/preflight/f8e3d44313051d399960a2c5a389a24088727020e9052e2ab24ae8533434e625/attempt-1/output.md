## REFORMULACION

Propósito: diagnosticar y corregir la regresión de rendimiento (~30 s por comando CLI de deskops) atribuida a CC32 (`6afc78b0`) y CC35b (`5328b664`).

Resultado: informe con medición por comando (`show task`, `next`, `advance task` bloqueada y con recibos, `add task`), con tiempo total, tiempo de import y top-15 pstats; causa raíz escrita con evidencia (función, llamadas por comando, lecturas de disco); arreglo aplicado si vive en deskops; tabla «antes de CC32 | main hoy | con el arreglo»; `test_activation_rules` y `test_lifecycle_end_to_end` por debajo de ~90 s cada uno.

Repo: deskops (`deskops/`, `tests/`, `CHANGELOG.md`), con mediciones en desks temporales creados con `deskops init` en `/dev/shm` y copias detached de main.

Límites: no cambiar semántica de reglas CC32, selectores CC35b ni transacción CC35a; no duplicar el trabajo de main-en-verde; si la causa está en sldb, parar y avisar al coordinador; sin cachés en deskops que oculten problemas de sldb.

## AMBIGUEDADES

1. «~30 s» y «por debajo de ~90 s»: umbral aproximado; obliga a inventar tolerancia exacta.
2. «se arregla donde viva» frente a «el worker para y avisa»: la frontera deskops/sldb (p. ej. registro de modelo invocado desde `desk update`) no está definida; obliga a inventar criterio de atribución.
3. «Nada de cachés en deskops que escondan un problema de sldb (regla 7)»: la regla no está incluida; obliga a inventar su contenido.
4. «como el de dirty.json»: precedente externo no descrito; obliga a inventar el procedimiento.
5. «main hoy»: no se fija commit exacto para esa columna; obliga a elegir uno.
6. «el coordinador del plan abre la tarea en el desk de sldb»: rol y protocolo no definidos en el input.

## DRY-RUN

Lecturas: TaskDoc, `dag.yaml` de origen, `git show/log` de `6afc78b0` y `5328b664`, código CLI de deskops, los tests citados.

Cambios previstos: scripts de medición temporales, informe de resultados, posible parche en deskops (una llamada por comando, registro de modelo), nota en `CHANGELOG.md`.

Dependencias: git, `python -X importtime`, `cProfile`/`pstats`, espacio en `/dev/shm`, `deskops init`, copias detached.

Validaciones futuras: tabla p4; cada test entero, de a uno, desde `/dev/shm`, bajo ~90 s; `test_activation_rules`, `test_tracked_selector_resolution`, `test_transaction`, `test_cli` y `test_output_goldens` verdes sin `--update-golden`; si la causa es de sldb, tarea abierta y despachada.

## FUTURO

Deciden humano/coordinador: apertura y despacho de la tarea en el desk de sldb, coordinación con main-en-verde, y aceptación del commit/PR.
