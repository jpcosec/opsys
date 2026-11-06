REFORMULACION
Propósito: limpieza previa CC30 (hijo de PF1, plan deskops-como-config) para dejar `operations.py` como fachada y eliminar los spec YAML duplicados sin cambio de comportamiento. Resultado: helpers privados en `deskops/doc_access.py` o en su servicio dueño; ningún servicio construye `DeskopsOperations`; `_normalize_task_payload` y `compile_task_spec` unificadas; `task_lifecycle.yaml` solo vía `lifecycle.load_lifecycle_spec`; borrados `spec/artifacts/`, `spec/fields/`, `SpecRegistry` y `specs/mermaid.py` si solo lo usan tests; `id_pattern`, `status_default` y `tags` como atributo de clase del modelo. Repo: deskops, worktree por nodo en robocop2; base main dc1d2834; no se escribe en sldb. Límites: fuera `task_lifecycle.yaml` (CC31), la vista de `desk_view.py` (CC34), graph_ui, formato del desk y gramática del CLI; goldens de ayuda y salida idénticos.

AMBIGUEDADES
1. "G_P0: ... (pending); G_GATES_FROZEN: ... (pending)" — no aclara si el ejecutor puede arrancar; obligaría a inventar si se bloquea o se procede.
2. "pasan a un módulo deskops/doc_access.py ... o al servicio dueño" — obligaría a inventar el destino de cada helper.
3. "un atributo de clase de cada modelo (p. ej. __artifact__)" — obligaría a inventar el nombre real del atributo.
4. "specs/mermaid.py si solo lo usan tests" — obligaría a decidir/inventar el criterio del borrado.
5. "y los demás que el grep delate" — conjunto abierto; obligaría a inventar el inventario completo.
6. q2: "doc_access o la fachada recibida por parámetro" — obligaría a inventar el mecanismo para `desk_view.py:66` y `retire.py:200`.
7. "lista final en esta sección al cerrar" — el conjunto de tests no está fijado ahora.

DRY-RUN
Leería `operations.py`, `doc_access.py`, `services/` (tasks, atoms, closure, retire, desk_view), `specs/`, `spec/artifacts`, `spec/fields`, `cli/model_introspection.py`, `models/`, `workflow/next_actions.py`, tests citados y `CHANGELOG.md`. Cambios previstos: mover helpers, alias marcados CC34 en la fachada, unificar funciones, borrar YAML/registry/mermaid, añadir atributo de clase, adaptar tests y CHANGELOG. Dependencias: gates satisfechos y main dc1d2834. Validaciones futuras: pytest goldens sin `--update-golden`, test_specs/extension_points/desk_view, greps vacíos o de definición única, `wc -l` antes/después, `deskops doctor` y `view board` en los 6 desks. Sin ejecutar nada.

FUTURO
El supervisor marca G_P0/G_GATES_FROZEN y promueve el nodo; CC31 reduce `task_lifecycle.yaml`; CC34 reemplaza la vista y retira los alias de graph_ui; CC38 recoge los chequeos DK6; la suite completa la corre el supervisor sobre el resultado integrado.
