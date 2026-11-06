REFORMULACION
Propósito: rehacer GC04 sobre la API general de sldb, declarando el ciclo de vida como grafo con efectos en los attributes de cada RelationDoc. Resultado: RelationDoc/RelationTypeDoc seed managed con attributes {sets:{status}, terminal}; advance por edges_holding y apply_effects; task_lifecycle.yaml sin transitions; lifecycle.py delgado; migración legada decidida por evidencia; tests, goldens, docs y CHANGELOG. Repo: deskops, worktree por nodo. Límites: fuera doc_io/transacción (CC35a), gates de activación (CC32), cierre y _add_closeout_facts (CC33), escrituras en sldb, formato del desk salvo desk/lifecycle/, gramática CLI.

AMBIGUEDADES
1. "o en un archivo hermano de deskops/data/lifecycle/ que la declaración incluye": no fija ubicación; obligaría a inventar archivo e include.
2. "aplica apply_effects(payload, effects, modelo del tipo de la tarea)": no aporta el contrato de sldb (parámetros, retorno); obligaría a inventar su semántica.
3. "en el orden que devuelve sldb": no garantiza orden estable; obligaría a inventar desempate.
4. "un RelationDoc de la versión anterior (sin attributes)": no acota cuáles; obligaría a inventar si reescribe cualquiera o solo los tres conocidos.
5. "mientras algún desk de los 6 la necesite (lo dice desk update en dry-run)": no define la señal exacta; obligaría a inventar el criterio.
6. "history la sigue escribiendo deskops": no reparte la responsabilidad frente a apply_effects; obligaría a inventar quién escribe history.
7. "sin hallazgos nuevos en los 6 desks": no define baseline ni copias; obligaría a inventar el método.

DRY-RUN
Leería TaskDoc, Board/rituales enrutados, pills/átomos ligados y los archivos nombrados. Cambiaría: seeds managed con attributes en desk_declaration.yaml; rewrite reportado en desk update --apply; effects/edges_holding en lifecycle.py; quitar sets_status, terminal y LifecycleSpec.effect; adaptar tests; docs y CHANGELOG. Depende de GO09/GD26 y CC30/CC36; k6 decide migración. Validaría con pytest listado uno a uno (TMPDIR=/dev/shm), greps, dry-run de 6 desks, doctor, wc -l y goldens.

FUTURO
CC32 aporta gates de activación; CC33, cierre y _add_closeout_facts; CC35a, doc_io/transacción. sldb mantiene GO09/GD26. El supervisor corre la suite completa, integra y decide promoción/cierre; el humano decide producto y alcance.
