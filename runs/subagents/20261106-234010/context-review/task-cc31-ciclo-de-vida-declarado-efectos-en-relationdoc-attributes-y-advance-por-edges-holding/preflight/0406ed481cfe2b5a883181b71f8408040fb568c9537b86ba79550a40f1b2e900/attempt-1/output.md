REFORMULACION
Propósito: ejecutar CC31 del plan `deskops-como-config`, rehaciendo GC04 sobre la API general de sldb. Resultado: ciclo de vida como grafo con efectos; RelationDoc de `desk/lifecycle/` con `attributes.sets.status` y `terminal`, declarados como semillas managed; `advance` usa `edges_holding` y `apply_effects`; `task_lifecycle.yaml` sin `transitions`; se eliminan `sets_status`, `terminal` y `LifecycleSpec.effect`; `lifecycle.py` se reduce a cargar configuración, llamar a sldb y escribir `history`; pruebas, docs y CHANGELOG. Repo: deskops. Límites: no tocar doc_io/transacción, gates de activación, cierre, escrituras en sldb, formato del desk salvo `desk/lifecycle/` ni gramática del CLI; no escribir a mano en `desk/`.

AMBIGUEDADES
1. “advance toma la primera arista de edges_holding en el orden de los RelationDoc (campo order en attributes si hace falta desempatar…)” frente a k4: “No se agrega attributes.order. Si al implementar aparece más de una arista que se cumple a la vez desde un mismo nodo, el worker para y avisa.” Obliga a inventar si se añade orden o se detiene el worker.
2. “task_lifecycle.yaml queda solo con states (next_actions, advance_when) para el comando next”: “solo con states” contradice incluir `next_actions`/`advance_when`; obliga a inventar la estructura exacta.
3. “lifecycle.py queda en: cargar la configuración, llamar a sldb y escribir history; objetivo < 150 líneas” frente a k6, que conserva condicionalmente “lifecycle.py :228-298”; obliga a decidir si la migración es excepción al objetivo.
4. “reemplaza ensure_lifecycle_graph, lifecycle.py:275-374” frente a k2: “ensure_lifecycle_graph :299-400”; obliga a elegir la referencia vigente.

DRY-RUN
Lecturas: TaskDoc, archivos listados, contrato del DAG, APIs de sldb (`edges_holding`, `apply_effects`), mecanismo de CC36 (`scaffold_store`, `apply_includes`) y tests/goldens. Cambios previstos: semillas managed y declaración/include; RelationDoc con attributes; `task_lifecycle.yaml`; `lifecycle.py`; llamadas a `ensure_lifecycle_graph`; tests, docs y CHANGELOG; evidencia k6 en copias de los 6 desks. Dependencias: CC30 y CC36 en main; sldb main editable; G_GO09 y G_GD26 satisfied. Validaciones futuras, sin ejecutar: pytest seleccionado con `TMPDIR=/dev/shm`; idempotencia de `desk update --apply`; cambio de `sets` vía API de sldb; greps; goldens; `deskops doctor` en los 6 desks; `wc -l`.

FUTURO
El supervisor decide revisiones en frío, worktree y suite completa. CC35a, CC32 y CC33 cubren doc_io/transacción, gates y cierre. Si sldb no expresa una regla, se anota hipótesis y se avisa a sldb.
