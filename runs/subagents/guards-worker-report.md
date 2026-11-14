# Worker: quita las guardas H2 de deskops con sldb H1-H3 corregido

## Perfil y entorno

- Worker de scion/pi (DeepSeek) en la rama `wt/guardas-h1h3`, worktree
  `/mnt/ssd/proyectos/SLDB_1/deskops-wt-guardas`, desde `deskops main 9b3bb95a`.
- Precondición comprobada antes de tocar código: `sldb-runtime` está en
  `b51e9667` (origin/main, con H1-H3, H11 y H47) y su código trae el hallazgo
  `store/doc-invalid` (`src/sldb/api/stores/store_findings.py`).
- venv no editable en `/tmp/venv`; tests con
  `PYTHONPATH=<worktree>:/mnt/ssd/proyectos/SLDB_1/sldb-runtime/src`.

## Cambios (g1-g5)

- **g1**: `ClosureService.close_retired` y `_record_closing_status` (supersede y
  resolved-by) ya no consultan `_other_invalid_tasks`; las dos funciones
  `_other_invalid_tasks` y `_blocked_by_invalid_tasks` se borraron. La escritura
  por frontmatter de una tarea que el modelo rechaza se conserva.
- **g2**: la rama `store_check_error` de `desk update` desapareció. Con informe
  de `stores check` (aunque liste `store/doc-invalid`) `--apply` hace todas las
  reparaciones; sin JSON y con rc distinto de 0 se mantiene
  `DeskopsEnvironmentError`.
- **g3**: `doctor_findings.invalid_document_findings` lee los errores
  `store/doc-invalid` y los mapea a la ruta relativa del documento. El informe
  de `desk update` (`- Invalid documents (not written)`) y `doctor`
  (`- Invalid desk document: ...`) los suman al listado por frontmatter,
  dejando fuera las tareas que ese listado ya nombra. La nota `doc_invalid` de
  `stores check` ya no se lista por nota ni entra en `docs.store_errors`, para
  no duplicar; `inspect_desk` tampoco la convierte en superficie legacy.
- **g4**: fixture `sldb_cache` en `tests/conftest.py`, parametrizado `warm`/`cold`
  (borra `.sldb_cache` y deja `XDG_CACHE_HOME` vacío en frío). Retire, supersede
  y resolved-by tienen tests que cierran una de dos tareas inválidas del mismo
  modelo, comprueban que `stores check` deja el hallazgo de la que queda, y
  cierran la segunda. `desk update --apply` repara estructura e índices con un
  documento inválido. `test_cli.py::test_doctor_reports_invalid_documents` se
  adaptó al hallazgo (antes esperaba el crash de sldb).
- **g5**: `docs/operator-manual.md` (doctor y estados heredados),
  `docs/workflow-policy-reference.md` y `CHANGELOG.md`.

## Tests (uno por archivo)

Comandos, desde el worktree, con `TMPDIR=/tmp` y `python -m pytest -q
-p no:cacheprovider <archivo>`:

- `tests/test_legacy_task_states.py`: 42 passed (incluye warm y cold).
- `tests/test_task_lifecycle_validator.py`: 38 passed.
- `tests/test_closeout.py`: 59 passed.
- `tests/test_closeout_resolved_by.py`: 20 passed.
- `tests/test_closeout_resolved_by_xrepo.py`: 12 passed.
- `tests/test_retire_cli.py`: 13 passed.
- `tests/test_doctor_alerts.py`: 5 passed.
- `tests/test_doctor_unmodeled_surfaces.py`: 4 passed.
- `tests/test_doctor_model_registration.py`: 8 passed.
- `tests/test_doc_readability.py`: 6 passed.
- `tests/test_desk_sync.py`: 8 passed.
- `tests/test_lifecycle_seed_drift.py`: 8 passed.
- `tests/test_operator_manual.py`: 1 passed.
- `tests/test_cli.py` (con el test adaptado, desde /dev/shm): 101 passed.

Suite completa de a un archivo desde `/dev/shm/deskops-suite`, contra
`/dev/shm/sldb` extraído de `sldb b51e9667` (99 archivos, logs en
`/dev/shm/suite-logs/`): **97 archivos rc=0**, `test_cli.py` falló solo por la
aserción vieja y se re-ejecutó completa después de adaptarla (**101 passed**),
y `test_domain_tree.py` tiene 2 fallos preexistentes (ver hallazgos).

## Mediciones

- `test_legacy_task_states.py`: 186,86 s con 42 tests (warm+cold).
- `test_task_lifecycle_validator.py`: 37,82 s.
- Suite completa desde /dev/shm: ~62 min de reloj, un pytest a la vez; los
  archivos más lentos fueron `test_output_goldens.py` (349 s),
  `test_operator_manual.py` (198 s) y `test_view.py` (163 s).
- No se midió rendimiento de producto: el cambio no toca rutas calientes.

## Hallazgos

- **Preexistente, fuera de alcance**: con sldb `b51e9667` (H47 q2: `track` evalúa
  `on_write`), `tests/test_domain_tree.py::test_validate_all_reports_atoms_hanging_from_unwritten_paths`
  y `::test_an_atom_with_an_undeclared_namespace_is_an_sldb_finding` fallan porque
  `desk update --apply` ya no puede trackear un átomo inválido (sldb lanza
  `SLDBRuleViolationError` por `builtin:tag_namespace`). Se reprodujo igual en un
  checkout limpio de `deskops main 9b3bb95a` (`/tmp/deskops-main`) con el mismo
  sldb, así que no lo introduce este cambio. No se tocó esa superficie.
- Para g3 hubo que excluir la nota `doc_invalid` de las rutas de nota
  (`read_store_check`, `inspect_desk`): si no, doctor repetía el documento como
  nota, como `store_errors` y como hallazgo, y marcaba el desk como legacy.
- La rama `store_check_error` quedó inalcanzable con el sldb corregido; el test
  de `desk update --apply` con documento inválido valida las reparaciones, no la
  rama eliminada.

## Dudas

- El CI de 4 pasos lo corre el coordinador. La suite completa no queda 100 %
  verde solo por los dos fallos preexistentes de `test_domain_tree.py` con H47;
  el resto, incluidos todos los tests de closeout y estados heredados, pasa.
