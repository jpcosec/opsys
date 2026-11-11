## REFORMULACION
Encargo ejecutable (no agregado) del nodo CC35c: en el repo deskops, sustituir las búsquedas y reescrituras propias de referencias entrantes por `referrers` y `rewrite_references` de sldb, dentro de la misma transacción que la escritura principal, para `atoms delete/split/merge`, `retire`, `drawer remove` y `closeout`. Debe comprobar que las menciones `atom:<id>` en prosa y los bullets del drawer se detectan mediante `MentionPattern`, añadir el patrón que falte o registrar hipótesis si sldb no lo admite. Resultado: código viejo borrado, pruebas, docs y CHANGELOG. Límites: solo `deskops/services/`, `deskops/atom_references.py`, `deskops/graph/desk_graph.py`, `tests/`, `docs/`, `CHANGELOG.md`; fuera la API de tags (CC35d/DO7) y vistas (CC34); no cambian formato del desk ni goldens de CLI; nada manual en `desk/` ni `.sldb/`; sin dos caminos simultáneos.

## AMBIGUEDADES
1. “drawer remove y closeout”: no fija comandos ni flujos concretos; obligaría a decidir qué vías cuentan y si deben reescribir referencias o solo documentarse.
2. “el MentionPattern que falte se suma ahí; si sldb no admite el caso, hipótesis y nota a sldb”: exige juzgar qué patrón falta y cuándo sldb “no admite” el caso; sin criterio explícito, se podría inventar la hipótesis.
3. “líneas antes y después”: no indica dónde ni con qué formato registrar el conteo.
4. “retire de una pill… (o el comando que retire pills hoy)”: el comando exacto queda a descubrimiento del ejecutor.

## DRY-RUN
Leería el TaskDoc, `dag.yaml`, `alcance.md`, `a1`–`a8`, `services/atoms.py`, `services/retire.py`, `atom_references.py`, `graph/desk_graph.py`, tests, docs y CHANGELOG. Localizaría helpers por nombre, no por línea. Cambiaría llamadas a `sldb.api.edges.referrers/rewrite_references` dentro de `desk_transaction`; borraría `_find_inbound_atom_references`, `_rewrite_inbound_atom_references`, `_inbound_references`; ajustaría `MentionPattern`; añadiría test `tmp_path` de pill ligada al Board y dos tareas, incluyendo fallo forzado; actualizaría docs/CHANGELOG. Dependencias: CC35a y CC33c en main, sldb GD22, `ProjectGraph(root, desk_graph_config())`. Validaría con grep, pytest por archivo, goldens, `deskops doctor` en 6 desks, líneas antes/después, `stores build`, `--check` y `ci-knowledge-check`. Sin ejecutar.

## FUTURO
El coordinador fija worktree, corre los 4 pasos en clon limpio y la suite integrada; el supervisor decide revisiones frías y promoción; quien opera dispone hallazgos como correcciones y resume en `coordinator-status.md`. CC35d/CC34 quedan para otros nodos.
