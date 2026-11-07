## REFORMULACION

**Propósito:** eliminar `deskops/doc_io.py` y hacer que toda escritura de deskops pase por `sldb.api.transaction` (GD24), con `expected_source_hash` en los updates y sin rollback manual. **Resultado:** grep de `doc_io|DocTransaction` vacío; operaciones compuestas atómicas —un fallo inyectado en atoms merge revierte átomo, referrers e índice—; conflicto de hash con el mensaje de a5; `message send/ack` transaccional; goldens y `deskops doctor` sin cambios; tests verdes; CHANGELOG. **Repo:** deskops, worktree en robocop2 sobre main con CC30, CC36 y CC38 integrados. **Límites:** no cambia selectores, referencias entrantes, tags/reemplazo, escrituras en sldb, formato del desk ni gramática del CLI; `bootstrap.py` en P4 solo cambia import y llamada; no se crea un módulo sustituto de `doc_io`; a2 permite lógica propia en `doc_access.py`. Nodo ejecutable, no agregado; no hay hijos que recorrer.

## AMBIGUEDADES

1. «Error: <ruta relativa> changed since deskops read it» no fija la base de la ruta relativa (raíz del desk, raíz del repo o cwd); obliga a inventar la base y la expectativa exacta del test.
2. «monkeypatch de una llamada que ocurre a mitad del merge» no nombra la llamada ni el punto de importación; obliga a elegir el seam exacto que se intercepta.
3. «sldb lo da en el estado o la referencia del documento» ofrece dos fuentes para el source hash; obliga a decidir cuál API y forma usar.
4. El Goal dice «expected_source_hash en los updates», pero a4 lo limita a «cada lectura-modificación-escritura ... en los servicios»; obliga a decidir si los updates fuera de servicios también llevan guarda.

## DRY-RUN

**Lecturas:** TaskDoc, contrato CC35a del dag, `alcance.md`, `doc_io.py`, sus 16 callers, API `sldb.api.transaction/apply_batch`, tests y goldens, plantilla `n7c.sh`. **Cambios previstos:** borrar `doc_io.py`; sustituir `DocTransaction`, `_RootTransaction` y envoltorios por llamadas directas a `sldb.api`; actualizar `doc_access.py`, `services/`, CLI, `lifecycle.py`, `workspace.py`, `bootstrap.py` (solo import/llamada); escribir `message send/ack` dentro de transacción; añadir guardas y traducir `ConflictError`; reescribir o borrar `test_doc_io`; CHANGELOG y docs/rituales. **Dependencias:** CC30/CC36/CC38 en main; gate G_GD24; `sldb.api.transaction`, `apply_batch` y conflicto; copias de los 6 desks; cwd neutro. **Validaciones futuras:** grep, tests listados, fallo inyectado con hashes y `sldb stores check`, conflicto de hash, `message`, goldens, doctor en 6 desks, `wc -l`.

## FUTURO

El coordinador fija worktree y promueve con `deskops add task --from-drawer`; el supervisor decide revisiones en frío y corre la suite completa sobre lo integrado. CC35b/c/d cubren selectores, referencias entrantes y tags/reemplazo. sldb debe proveer la transacción, `apply_batch`, el source hash y `ConflictError`.
