## REFORMULACION

Encargo: nodo CC37 (leaf, ejecutable) del plan deskops-como-config, en el repo deskops, worktree por nodo. Propósito: que ninguna vía de escritura deje una TaskDoc con ciclo de vida incoherente. Resultado: un `model_validator` de pydantic en `deskops/models/` (TaskDoc o base) que exige coherencia entre `status`, `current_node`, `history` y `task_type` según la tabla derivada de los `RelationDoc` de `deskops/data/lifecycle/`; sldb lo aplica en `fields update`, `docs update`, `/save` y transacción (roundtrip ya existente, sin tocar sldb); las escrituras internas de deskops pasan solo por `lifecycle.advance` y closeout; inventario de vías en el TaskDoc; tests y CHANGELOG. Límites: no cambia el formato del desk ni la gramática del CLI/goldens; fuera de alcance el campo «solo por transición» (DA6), CC33, CC35b, closeout resolved-by y la forma del desk.

## AMBIGUEDADES

1. Conjunto de status de entrada. a2(i): «el worker los inventaría; por ejemplo «active» si compile_task_spec lo pone»; b2: «el conjunto de entrada es {"draft"} … más cada status que el inventario de a6 encuentre en tareas existentes». ¿Se deriva del código o de los datos de los 6 desks? Obliga a inventar cuál prevalece.
2. Cierre por `closed`. a2(iii)/b5: «history que termina en la arista terminal task_completes (lo que escribe advance/closeout commit)», pero el CHANGELOG dice que la transición terminal «is still not persisted from advance». Obliga a inventar qué history real lleva una tarea cerrada.
3. Alcance del grep a5. «filtrado a los payloads de TaskDoc» no define el filtro; obliga a inventar qué hits cuentan.
4. Resultado en los 6 desks. a6: «pasa el validador, o desk update la reporta como inconsistente sin escribirla»: ¿basta reportar o debe pasar? Ambigüedad de aceptación.
5. `task_type` genérico. a2(iv): «TaskDoc genérico acepta task_type vacío o legacy (d4 de CC31)» remite a una decisión externa no incluida.

## DRY-RUN

Lecturas: `deskops/models/task.py`, `task_types.py`, `validation.py`, `lifecycle.py`, `services/closure.py`, `specs/compiler.py`, `services/tasks.py`, `sldb api/documents/payload_save_steps.py`, `UIs/graph_ui`. Cambios previstos: validador y constantes (entrada, cierre) en `deskops/models/`; tests por caso a2 y por vía sldb (copia de desk temporal); CHANGELOG. No se prevé tocar `data/rules/` (b3) ni sldb. Dependencias: tabla de CC31, mecanismo de CC38, roundtrip de sldb, rama resolved-by. Validaciones futuras: grep a5; `pytest -q` uno a uno (lista de a8) con `TMPDIR=/dev/shm`; `desk update --apply` sobre copias de los 6 desks con `doctor6.sh`.

## FUTURO

El worker entrega el inventario en el informe; el coordinador lo copia al TaskDoc con `deskops edit task` (b4) y fija el conjunto de entrada (b2). La rama closeout resolved-by y CC35b aportan sus formas; el supervisor corre la suite completa integrada.
