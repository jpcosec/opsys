REFORMULACION
Nodo hoja ejecutable. Propósito: borrar `deskops/doc_io.py` y hacer que toda escritura pase por `sldb.api.transaction` con `expected_source_hash`, de modo que una operación compuesta revierta entera si falla a mitad. Resultado: grep `doc_io/DocTransaction` vacío; fallo inyectado revierte átomo, referrers e índice; update con hash viejo da el mensaje de conflicto; goldens idénticos; tests verdes; doctor limpio en 6 desks; CHANGELOG. Repo: deskops, worktree por nodo en robocop2. Límites: fuera selectores (CC35b), referencias entrantes (CC35c), tags/reemplazo (CC35d), escrituras en sldb, formato del desk y gramática del CLI; no crear módulo que repita `doc_io`; `bootstrap.py` (P4) solo import y llamada.

AMBIGUEDADES
1. «sldb lo da en el estado o la referencia del documento» (a4) frente a «doc_status no lo trae» y «sldb.api no tiene un accesor público para leerlo» (b3): obliga a inventar cuál es cierta y la vía de lectura.
2. «en P4 solo se cambia el import y la llamada» (a3) frente a las 8 referencias de a1: obliga a inventar si se cambian todas o una.
3. «sin rollback manual» (a7) frente a «Warning: delivered ... could not track it» (message.py): obliga a inventar si un tracking fallido revierte la nota.
4. «en lifecycle.py (advance)» (b4) frente a `advance`, que muta el payload y devuelve sin escribir: obliga a inventar dónde vive la escritura y la guarda.
5. «El worker elige el mecanismo... o reindexar ese documento antes de la guarda» (b3): obliga a inventar el mecanismo y qué módulo interno de sldb usar.

DRY-RUN
Lecturas: TaskDoc, ritual, `doc_io.py`, `doc_access.py`, `message.py`, `desk.py`, `repo.py`, `scion.py`, `lifecycle.py`, `workspace.py`, `bootstrap.py`, CHANGELOG y tests nombrados. Cambios: borrar `doc_io.py`; sustituir cada envoltorio por `sldb.api` (`transaction/create/update/delete/track/untrack/register_model`) en los módulos listados; concentrar en `doc_access` la lectura del hash y la traducción de `ConflictError` al texto de a5; envolver send/ack; ajustar el test de atoms merge al punto b2; reescribir/borrar `test_doc_io` y añadir tests de conflicto y transacción. Dependencias: `sldb.api.transaction/apply_batch`, `ConflictError`, acceso al hash, CC30/CC36/CC38 en main. Validaciones futuras: grep vacío, fallo inyectado, conflicto a5, message, pytest uno a uno, doctor en 6 desks con cwd neutro, `wc -l`, CHANGELOG.

FUTURO
CC35b, CC35c y CC35d siguen el agregado; el coordinador fija worktree y correcciones; el supervisor corre la suite completa; sldb puede recibir la hipótesis de un accesor público del hash; el humano decide promoción y disposición de revisiones.
