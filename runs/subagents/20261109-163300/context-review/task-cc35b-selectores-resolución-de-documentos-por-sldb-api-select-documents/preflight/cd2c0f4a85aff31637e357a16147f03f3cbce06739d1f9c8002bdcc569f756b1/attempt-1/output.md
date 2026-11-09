## REFORMULACION
Propósito: nodo CC35b del plan `deskops-como-config` (dag rev 3), parte (2) selectores del agregado CC35. Resultado: la resolución de selectores de documentos trackeados de deskops pasa a `sldb.api.select_documents` (GD23), misma regla exacto > prefijo único y mismos mensajes; `resolve_selector` y `_tracked_task_paths` desaparecen de las superficies trackeadas; los alias privados de graph_ui se conservan marcados CC34. Repo: deskops (`desk_paths.py`, `doc_access.py`, `services/`, `operations.py`, `tests/`, `CHANGELOG.md`). Límites: fuera escritura (CC35a), referencias entrantes (CC35c), tags/reemplazo (CC35d), lo que CC32 toca en `lifecycle.py`/`tasks.py`/`operations.py` y la forma del desk; drawer e issues no trackeados quedan fuera (a3). Es un nodo ejecutable, no un agregado.

## AMBIGUEDADES
1. Contradicción: "issues.find_issue/list_issues y drawer.resolve_drawer_source/_resolve_unique pasan a sldb.api.select_documents" vs a3: "siguen leyendo el disco como hoy, sin cambiar su regla". Obliga a inventar cuál prevalece.
2. "las superficies trackeadas (tasks, reviews, rituals, inbox, pills, atoms, registry y las demás del include)": a2 solo mide tasks, inbox, rituals, reviews. Obliga a inventar qué más está trackeado y con qué `path_glob`/model.
3. "marcados CC34" / "marcados CC35b-a3": el formato de la marca no se define (comentario, tag, texto). Obliga a inventarlo.
4. Regla común 5 exige "doc en `docs/`", pero OUTPUT_SCOPE y `files` no listan `docs/`. Obliga a decidir si se toca.
5. "wc -l antes y después" sin umbral ni destino del registro. Obliga a inventar el criterio.
6. a7: "trackeándolas con sldb.api en su fixture" sin nombrar la llamada. Obliga a inventar la API.

## DRY-RUN
Lecturas: TaskDoc, `dag.yaml` rev 3 (contrato), `alcance.md`, `desk_declaration.yaml` (include), líneas citadas de a1 (`desk_paths.py:24`, `doc_access.py:551-675`, `operations.py:261-270`, `issues.py:96,356`, `drawer.py:49,224`), callers en `services/`, goldens help/output, `doctor6.sh`. Cambios previstos: sustituir `resolve_glob`/`resolve_artifact_selector[_multi]`/`resolve_ritual_selector`/`_tracked_task_paths` por `select_documents` (`expect="one"/"many"`) rearmando mensajes con los candidatos; reducir `resolve_selector` a drawer/issues; conservar alias; adaptar tests; CHANGELOG. Dependencias: CC35a (8d0e23fe), sldb GD23, CC32 en paralelo, 6 desks. Validaciones futuras: grep de aceptación, goldens idénticos, `pytest -q` por archivo en `/dev/shm`, `deskops doctor` en 6 desks con cwd neutro, `wc -l`. Nada ejecutado.

## FUTURO
Decisión del dueño sobre a3 (declarar drawer/issues en el include, como seguimiento); hipótesis a sldb sobre archivos no trackeados; integración de CC32; CC35c (referencias) y CC35d (tags/reemplazo); el supervisor corre la suite completa; captura previa de goldens (regla 4).
