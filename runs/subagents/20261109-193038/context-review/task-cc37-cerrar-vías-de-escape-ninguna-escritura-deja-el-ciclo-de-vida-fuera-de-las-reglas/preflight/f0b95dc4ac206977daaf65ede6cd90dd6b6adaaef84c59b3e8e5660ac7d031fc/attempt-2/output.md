## REFORMULACION
El encargo es ejecutar CC37 en el repo **deskops**, en un worktree: cerrar las vías de escritura que dejan una `TaskDoc` con ciclo de vida inconsistente. Debe producir un validador del modelo `TaskDoc` que exija coherencia entre `status`, `current_node`, `history` y `task_type` según la tabla derivada de las `RelationDoc` de CC31; hacer que sldb lo aplique en toda escritura; verificar que las escrituras internas de deskops pasan solo por `advance` y `closeout`; dejar el inventario de vías en el `TaskDoc`; y añadir pruebas y `CHANGELOG`. Límites: solo `deskops/models/`, `deskops/data/rules/`, `deskops/services/`, `deskops/lifecycle.py`, `deskops/cli/commands/desk.py`, `tests/` y `CHANGELOG.md`; quedan fuera el campo «solo por transición» de sldb, reglas de cierre, selectores, closeout resolved-by y la forma del desk. El nodo es ejecutable, no agregado.

## AMBIGUEDADES
1. «sldb lo aplica en toda escritura (roundtrip en sldb api/documents/payload_save_steps.py:62)»: el scope no incluye sldb; obliga a inventar cómo se integra el validador en sldb sin tocar ese repo.
2. «más los status que hoy escriben add task y promote (el worker los inventaría; por ejemplo «active» si compile_task_spec lo pone)»: no enumera el conjunto exacto; obliga a inventar o inferir los status de entrada.
3. «lo que solo se puede ver entre documentos queda como RuleDoc»: no define qué comprobaciones, con qué modelo ni dónde; obliga a inventar el `RuleDoc`.
4. «inventario en el TaskDoc (vía disposición)»: no indica campo ni formato; obliga a inventar dónde y cómo registrarlo.
5. «el validador acepta las dos formas» respecto de cierre/resolved-by: no concreta las formas; obliga a inventar la representación aceptada.

## DRY-RUN
Lecturas previstas: TaskDoc, `dag.yaml`, `alcance.md`, `deskops/data/lifecycle/`, `models/task.py`, `specs/compiler.py`, `lifecycle.py`, `closure.py`, `api/documents/payload_save_steps.py` y tests citados. Cambios previstos: validador en `models/` alimentado por la tabla de `deskops/data/lifecycle/`; ajustes mínimos en `services/`, `lifecycle.py` o `desk.py` si el grep los exige; pruebas por caso de a2/a4; inventario y `CHANGELOG`. Dependencias: CC31, CC32 y CC38 en main; GC06 ya retiró `advance --to`; CC35b y closeout resolved-by en paralelo. Validaciones futuras: `pytest` de los archivos listados, grep de a5, copias de los 6 desks con `desk update --apply`, y rechazo por sldb de payloads inconsistentes. No se ejecuta nada.

## FUTURO
CC31 aporta las `RelationDoc`; CC38 el mecanismo de validador; GC06 lo ya retirado. CC35b y closeout resolved-by pueden afectar `services/` y `closure.py`. El supervisor corre la suite completa y decide revisiones en frío; el operador del desk dispone hallazgos y promueve. Si sldb debe cambiar fuera del scope, lo decide un humano o ese repo.
