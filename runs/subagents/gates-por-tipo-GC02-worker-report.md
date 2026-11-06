# Informe del worker GC02 (gates-por-tipo)

Worktree: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`).
No hice commit, `git add` ni push. No toqué el repo `sldb` ni ningún checkout suyo. No escribí a mano en `desk/` ni en `.sldb/`; el único cambio en `.sldb/` lo hizo el CLI `python -m sldb models add "deskops.models:ReviewDoc" --store .sldb --pythonpath .`, como en GC01.

## 1. Archivos cambiados y creados

Creados:

- `deskops/models/review.py` — `ReviewDoc` completo (campos, vocabularios cerrados, patrones, `__doc_anchors__ = ["subject"]`, `__references__ = []`, plantilla con `## Summary` y `## Disposition`, validaciones).
- `.sldb/core/models/ReviewDoc.yaml` — índice del modelo creado por `sldb models add` en el store dueño.
- `tests/test_review_doc.py` — 14 tests: roundtrip, vocabularios, subject/subject_ref, tracking en desk temporal, `desk/reviews/` en init y `desk update`, xfail de `sldb edges show`, y rechazo de `edit review`.
- `tests/fixtures/golden/help/deskops_edit_review.txt`
- `tests/fixtures/golden/help/deskops_list_reviews.txt`
- `tests/fixtures/golden/help/deskops_show_review.txt`

Cambiados:

- `deskops/models/__init__.py` — exporta `ReviewDoc` (entra en `MODEL_REFS` por `__all__`).
- `deskops/workspace.py` — `scaffold_desk` crea `desk/reviews/` (lo usan `init`, `desk migrate` y `ensure_workspace`).
- `deskops/cli/commands/desk.py` — `desk update` detecta `desk/reviews/` ausente y lo scaffoldea (fuera de la lista `files`, justificado en §5).
- `deskops/operations.py` — `artifact.review` en `ARTIFACT_MODELS`/`ARTIFACT_PATHS`/`ARTIFACT_SUBJECTS`, patrón de glob `*.md`, resolución del selector por el `id` del frontmatter (ruta física `<kind>-<n>.md`, precisión 4) y rechazo de `verdict`/`reason`/`disposed_at`/`disposed_by` en `edit review`.
- `deskops/cli/registry.py` — el sujeto `review` no genera `add review` (GC02 no escribe recibos; GC03 los produce). `edit review`, `show review` y `list reviews` sí se generan.
- `.sldb/core/store_index.yaml` — alta de `ReviewDoc` + `store_hash` actualizado por el CLI de sldb.
- `tests/fixtures/model_contract_hashes.json` — regenerado con las funciones de `tests/test_model_contract_snapshot.py` (no a ojo); única línea añadida: `ReviewDoc`.
- `tests/fixtures/golden/help/deskops_{edit,list,show}.txt` — regenerados con `pytest tests/test_output_goldens.py::test_help_goldens --update-golden`.
- `tests/test_cli_help_examples.py` — `ADD_KINDS` excluye sujetos con `create: False` (review no tiene `add review`).
- `tests/test_command_registry.py` — `("edit", "review")` declarado como mutating.
- `CHANGELOG.md` — entrada de `ReviewDoc`, `desk/reviews/` y `edit review`.

## 2. Done When → test

| Línea de Done When | Test (archivo::nombre) | Pasa |
|---|---|---|
| ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo | `tests/test_review_doc.py::test_review_doc_roundtrips_a_payload` | sí |
| un kind fuera del vocabulario falla al validar | `tests/test_review_doc.py::test_review_kind_outside_the_closed_vocabulary_fails` | sí |
| verdict accepted sin reason falla | `tests/test_review_doc.py::test_review_accepted_without_reason_fails` | sí |
| subject `task-x` (sin `doc:`) falla | `tests/test_review_doc.py::test_review_subject_without_the_doc_prefix_fails` | sí |
| subject `doc:TaskCodeDoc:task-x` valida | `tests/test_review_doc.py::test_review_subject_with_doc_prefix_validates` | sí |
| subject y subject_ref mutuamente excluyentes / subject_ref de nodo de plan (precisión 2) | `tests/test_review_doc.py::test_review_plan_node_subject_ref_is_the_alternative_to_subject` | sí |
| ReviewDoc guardado con deskops (`doc_io`) queda tracked como `ReviewDoc:<id>` | `tests/test_review_doc.py::test_review_doc_is_tracked_as_review_doc_in_a_temporary_desk` | sí |
| `sldb edges show` lo enlaza a la tarea por subject, xfail hasta GO07 | `tests/test_review_doc.py::test_sldb_edges_show_links_the_review_to_the_task_by_subject` (marcado `xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07")`) | xfail esperado (falla hoy en la ausencia de la arista `references` sobre `subject`; con `--runxfail` se comprobó que falla exactamente ahí) |
| edit review verdict falla con el mensaje que remite a review dispose (y también reason/disposed_at/disposed_by, precisión 3) | `tests/test_review_doc.py::test_edit_review_refuses_the_disposition_fields[verdict|reason|disposed_at|disposed_by]` | sí |
| `desk/reviews/` creado por init y por desk update | `tests/test_review_doc.py::test_init_creates_the_reviews_directory` y `::test_desk_update_recreates_the_reviews_directory` | sí |
| `tests/fixtures/model_contract_hashes.json` actualizado | `tests/test_model_contract_snapshot.py::test_snapshot_covers_the_registered_model_set` y `::test_model_contract_hashes_match_the_snapshot` | sí |
| CHANGELOG | (documento, sin test) | — |

## 3. Línea final de pytest de cada corrida

- `tests/test_review_doc.py` → `13 passed, 1 xfailed, 1 warning in 93.10s`
- `tests/test_review_doc.py::test_sldb_edges_show_links_the_review_to_the_task_by_subject --runxfail` → `1 failed` (la aserción de la arista `references`; es el fallo que el xfail estricto documenta)
- `tests/test_model_contract_snapshot.py tests/test_federated_models.py tests/test_model_templates.py` → `18 passed, 1 warning in 83.95s`
- `tests/test_cli.py` → `101 passed, 1 warning in 833.09s`
- `tests/test_cli_help_examples.py tests/test_command_registry.py tests/test_cli_contract.py tests/test_cli_grammar.py` → `1 failed, 23 passed` en la primera pasada; tras declarar `("edit", "review")` como mutating, `tests/test_command_registry.py` → `3 passed, 1 warning in 0.92s`
- `tests/test_task_types.py` → `15 passed, 1 warning in 307.43s`
- `tests/test_output_goldens.py --update-golden` (solo `test_help_goldens`) → `1 passed, 1 warning in 174.92s`
- `tests/test_output_goldens.py` → `7 passed, 1 warning in 335.21s`
- `tests/test_desk_sync.py tests/test_desk_replace.py tests/test_extension_points.py tests/test_doctor_unmodeled_surfaces.py tests/test_doctor_alerts.py tests/test_doctor_model_registration.py tests/test_doc_readability.py` → `42 passed, 1 warning in 934.55s`
- `tests/test_packaging.py tests/test_doc_io.py tests/test_model_contract_snapshot.py` → `15 passed, 1 warning in 93.67s`

Verificación directa de CLI:

```
python -m deskops edit review --help   # exit 0
python -m deskops list reviews --help  # exit 0
python -m deskops --help               # exit 0
python -m deskops faq                  # exit 0
```

## 4. Hipótesis y evidencia

**Hipótesis de la precisión 1 (sldb no resuelve `doc:Model:name` en `__references__`) → CONFIRMADA por código.**
`sldb/store/edge_index/declared_references.py:84` (`is_export_id`) acepta cualquier valor con `:`, y `_target` lo convierte en `doc_node_id("doc:TaskCodeDoc:task-x")`; el store `doc` no existe, así que la referencia queda sin resolver. Por eso `ReviewDoc` declara `__doc_anchors__ = ["subject"]` y deja `__references__ = []`. No hay Python que fabrique la arista.

**Evidencia del xfail.** En un desk temporal con la tarea `TaskCodeDoc:task-x` y el recibo `ReviewDoc:review-task-x-preflight-1` tracked, `sldb edges show ReviewDoc:review-task-x-preflight-1 --store .sldb` devuelve aristas estructurales (`has_field`, `tagged_as`, etc.) pero ninguna `references` con `field: subject` hacia `sldb://document/TaskCodeDoc:task-x`. El test xfail estricto se vuelve rojo (XPASS) en cuanto GO07 agregue esa arista, que es la señal pedida para quitar la marca.

**Evidencia de resolución por id.** El archivo físico es `desk/reviews/task-x/preflight-1.md`, así que `resolve_selector` por nombre/stem no encontraba `review-task-x-preflight-1`. Añadí un fallback solo para `artifact.review` que compara el `id` del frontmatter, sin parsear el id desde la ruta (precisión 4). `edit review` y `show review` funcionan con el id.

**Evidencia de tracking.** En un desk temporal, tras `doc_io.track(root, path, ReviewDoc, name=<id>)`, `doc_status(store, "ReviewDoc/review-task-x-preflight-1")` existe con modelo `ReviewDoc`, y `sldb find ... --format json` devuelve `("review-task-x-preflight-1", "ReviewDoc")`.

## 5. Lo que no hice y por qué

- **No corrí la suite completa** (`pytest` entero), como pide el brief; corrí el archivo nuevo, los vecinos enumerados y los de `edit`/`desk update` encontrados con grep.
- **`deskops/cli/commands/desk.py` no está en `files` del TaskDoc.** Fue necesario: `desk update --apply` decide si scaffoldea mirando su propia lista de estructura faltante; sin añadir `desk/reviews/` allí, un desk existente nunca obtendría el directorio. La lógica de creación sigue en `workspace.py` (sí en `files`); `desk.py` solo la invoca.
- **`tests/test_cli_help_examples.py` y `tests/test_command_registry.py`** no están nombrados en `files`, pero `tests/` sí está en la lista. Eran obligatorios: el primero habría intentado ejecutar un `add review` inexistente y el segundo exige declarar todo comando mutating.
- **No generé `add review`.** GC02 no escribe recibos desde ningún comando (eso es GC03). Para conservar `edit review`/`show review`/`list reviews` sin abrir una vía de creación, marqué el sujeto con `create: False` en `ARTIFACT_SUBJECTS`; el registry y el test de ayuda lo respetan.
- **No toqué `desk/` del worktree ni corrí `deskops` contra él.** Toda la validación con escritura se hizo en desks temporales de pytest.
- **No modifiqué sldb.** La falta de la arista `doc:` queda registrada como `xfail(strict=True)` con el gate `G_SLDB_ANCHORS: sldb GO07`.
- **No añadí `reviews` a `_MODELED_DESK_TOP_LEVEL_DIRS`.** El id no se deduce de la ruta y el tracking lo hace GC03 con `doc_io`; incluirlo haría que `doctor`/`desk update` intentaran trackear `preflight-1.md` con el nombre equivocado. Si un nodo posterior quiere auto-reparar reviews, debe resolver el nombre desde el `id` del frontmatter.
- **`sldb stores check --store .sldb`** reporta hallazgos preexistentes del desk del worktree (inbox notes missing / data mutations) ajenos a GC02; `ReviewDoc` no aparece con finding.
