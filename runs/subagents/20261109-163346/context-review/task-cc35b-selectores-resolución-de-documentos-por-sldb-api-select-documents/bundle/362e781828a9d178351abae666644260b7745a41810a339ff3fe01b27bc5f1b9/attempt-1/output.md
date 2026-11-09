REFORMULACION
El nodo es una hoja ejecutable (`task.code`), no un agregado. Propósito: sustituir la resolución propia de selectores de documentos trackeados de deskops por `sldb.api.select_documents` (GD23), conservando la regla exacto > prefijo único y los mensajes. Resultado: `doc_access` y sus callers resuelven por sldb; desaparecen `resolve_selector` y `_tracked_task_paths` de las superficies trackeadas, salvo los usos de drawer/issues marcados CC35b-a3 y los alias de graph_ui marcados CC34; tests y CHANGELOG actualizados. Repo: deskops, worktree por nodo en robocop2, base CC35a squash `8d0e23fe`. Límites: fuera escritura (CC35a), referencias entrantes (CC35c), tags/reemplazo (CC35d), `lifecycle.py`/`cli/commands/` y lo de CC32, la forma del desk y `docs/`.

AMBIGUEDADES
1. «issues.find_issue/list_issues y drawer.resolve_drawer_source/_resolve_unique pasan a sldb.api.select_documents» frente a «El drawer y los issues, que no están trackeados, quedan fuera del cambio». b1 manda a3, pero el SCOPE del dag sigue incluido; sin aplicar b1 habría que inventar si se migran.
2. «cuando lo conoce, el model (ARTIFACT_MODELS)» frente a que las tareas se guardan bajo su tipo (`TaskCodeDoc`, etc.). Obligaría a inventar si se pasa `TaskDoc`, el tipo registrado o ningún modelo.
3. «Donde hoy se compara contra el stem del archivo y el name trackeado difiere del stem (...) los dos selectores tienen que seguir funcionando» no fija si se consulta con `expect="many"` y se filtra localmente o se hacen dos consultas. Obligaría a elegir la estrategia.

DRY-RUN
Leería el TaskDoc, el ritual enrutado y los archivos nombrados (`desk_paths.py`, `doc_access.py`, `operations.py`, `services/`, tests, CHANGELOG), más la firma de `sldb.api.select_documents`. Cambios previstos: reemplazar resoluciones trackeadas por `select_documents` con `path_glob`/model/expect; armar los mensajes con candidatos relativos a `desk/`; borrar `_tracked_task_paths` y fallbacks por frontmatter si quedan sin uso; conservar `resolve_selector` solo para drawer/issues con marca; marcar alias; adaptar fixtures con sldb.api. Dependencias: CC35a, GD23 y el tracking declarado. Validaciones futuras: grep de aceptación, goldens de ayuda/salida, pytest uno a uno, `deskops doctor` en 6 desks con cwd neutro, tabla `wc -l`, CHANGELOG. Sin ejecutar nada.

FUTURO
CC34 eliminará los alias; CC35c/CC35d cubrirán referencias y tags; el dueño decidirá si trackea drawer/issues; sldb aclarará `select_documents` sobre no trackeados; el supervisor correrá la suite completa y el coordinador integrará CC32 y aceptará el informe.
