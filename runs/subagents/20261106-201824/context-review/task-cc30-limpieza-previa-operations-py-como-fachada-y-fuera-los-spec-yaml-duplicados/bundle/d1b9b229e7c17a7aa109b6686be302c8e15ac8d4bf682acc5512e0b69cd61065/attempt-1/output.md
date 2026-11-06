REFORMULACION
Propósito: ejecutar CC30 del plan deskops-como-config (hijo de PF1, task.refactor) para dejar operations.py como fachada y retirar los spec YAML duplicados sin cambiar comportamiento. Resultado: helpers privados movidos a deskops/doc_access.py o al servicio dueño; ningún servicio construye DeskopsOperations; _normalize_task_payload y compile_task_spec unificadas; task_lifecycle.yaml cargado solo por lifecycle.load_lifecycle_spec; spec/artifacts y spec/fields borrados; id_pattern, status_default y tags en __artifact__ de cada modelo; goldens de ayuda/salida idénticos. Repo: deskops, worktree robocop2, base main dc1d2834. Límites: no ejecutar; no arrancar con G_P0/G_GATES_FROZEN pending; sin escrituras en sldb; desk, gramática CLI y vista de desk_view intactos (CC31/CC34); alias privados de graph_ui hasta CC34.

AMBIGUEDADES
1. "specs/loader.py (SpecRegistry) ... borrados" frente a "compile_task_spec (specs/compiler.py:25-61)" y "tests/test_specs.py ... se adaptan": obliga a inventar la firma sustituta y si el registro desaparece o queda mínimo.
2. "_normalize_task_payload (operations.py:537-567) y compile_task_spec (specs/compiler.py:25-61) quedan en una sola función" pero q6 manda "_normalize_task_payload ... a ese servicio" y compile_task_spec al compiler: inventar nombre, módulo y firma de la función única.
3. "id_pattern, status_default y tags por artefacto pasan a un atributo de clase de cada modelo (p. ej. __artifact__)": _ARTIFACT_DEFAULTS no incluye artifact.task y compiler lee artifact["data"]["doc"]; inventar el __artifact__ de TaskDoc.
4. "task_lifecycle.yaml se carga solo por lifecycle.load_lifecycle_spec": el input solo muestra next_actions.load_task_lifecycle_spec; inventar si se crea, renombra o ya existe.
5. "si algo de deskops/ lo importa, se conserva y se registra aquí": "aquí" no define destino ni qué pasa si solo lo importan tests; inventar dónde se registra.
6. "ningún método con más de una llamada a servicio más el armado de argumentos": inventar cómo clasificar métodos con snapshot, validación o registro (create_task_bundle, verify_task_closeout).

DRY-RUN
Lecturas: TaskDoc, servicios, specs, model_introspection, next_actions, tests y CHANGELOG; greps de q7 antes/después sobre main dc1d2834. Cambios: crear doc_access.py; editar services/tasks, atoms, closure, retire, desk_view; añadir __artifact__ a modelos; borrar _ARTIFACT_DEFAULTS, loader/mermaid (según grep) y spec/artifacts|fields; adaptar compiler, next_actions y tests; CHANGELOG. Dependencias: gates satisfechos, lifecycle.load_lifecycle_spec, graph_ui externo. Validaciones futuras: goldens sin --update-golden, greps de aceptación, wc -l, lista pytest q11 contra fallas previas, doctor y view board en 6 desks.

FUTURO
El supervisor marca G_P0/G_GATES_FROZEN y despacha; CC31 reduce task_lifecycle.yaml; CC34 elimina desk_view y los alias de graph_ui; CC38 recoge el inventario DK6; el supervisor corre la suite completa integrada.
