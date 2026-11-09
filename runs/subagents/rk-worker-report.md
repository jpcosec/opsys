# rk-worker: review record (reproduction, goldens, owner sin modelo; seguimiento de CC32)

Rama `wt/review-record`, base `a865bbcf`. Contrato: `desk/tasks/task-review-record-recibos-reproduction-goldens-y-owner-sin-modelo-seguimiento-de-cc32.md` (r1-r8, b1-b4).
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/rk/`.

## Commits

- `983853b2`: el comando `deskops review record`, con su servicio, la CLI y el registry; también el test, el manual y el CHANGELOG.
- `36cbb5d6`: los goldens de ayuda de review y el pin del subject tras dispose.
- este informe.

## Qué se hizo

- `deskops/services/review.py`:
  - `RECORD_KINDS = ("reproduction", "goldens", "owner")`.
  - Método nuevo `record_receipt(task_id, kind, evidence, reason)`. Llama a `_task_path`, `_task_model` y `_write_review` tal como están (r6).
  - El recibo sale con `engine: human` (b2), `actor` de `_identity()` (b2), `run_dir` vacío, `output_sha256` vacío, `verdict: pending` y `reason` el texto dado.
  - `input_sha256` cumple b1: las rutas van POSIX y relativas al root, ordenadas y sin repetir (una misma ruta dada en relativo y en absoluto cuenta una vez). El hash es sha256 de `<ruta>\n<contenido>\n` concatenado, y queda vacío sin evidencia.
  - `summary` es `<kind> receipt recorded by <actor>; evidence: <rutas>` (b4), o `(none)` si no hay evidencia.
  - Evidencia inexistente, fuera del root (`..`, ruta absoluta externa o symlink que sale) o que no es un archivo (un directorio): `DomainError` → `Error: evidence not found: <ruta>`, exit 1. Todo se valida antes de escribir, así que no se escribe nada (r3).
  - `reproduction` o `goldens` sin evidencia: `UsageError`, exit 2. `owner` acepta ir sin evidencia.
- `deskops/cli/commands/review.py`: despacho de `record` y formato de texto del resultado.
- `deskops/cli/registry.py`:
  - Comando `review record` con `--kind {reproduction,goldens,owner}` obligatorio, `--evidence` repetible, `--reason` obligatorio, `--root` y `--format`.
  - argparse rechaza `--kind preflight|bundle|node` con exit 2 (r1).
  - En la ayuda de `review` solo cambian el ejemplo y el párrafo final. Su línea `help` no se tocó, así que el golden `deskops.txt` no cambia.
- `docs/operator-manual.md` (b3): un párrafo y un bloque ilustrativo, no `runnable`, en «Cold context reviews», y `record` en la tabla de verbos.
- `CHANGELOG.md`: una entrada en `## [Unreleased]` / `### Added`.

## Aceptación

1. **`tests/test_review_record.py` cubre r8.** 17 tests, verdes (log `review_record.log`):
   - reproduction con evidencia, pending y bien formado (comprueba todos los campos, el hash b1 y el summary, sin `runs/subagents` ni llamada a `pi`): `test_reproduction_with_evidence_writes_a_pending_well_formed_receipt`;
   - preflight rechazado (también bundle y node), sin escritura ni modelo: `test_model_kinds_are_refused_and_nothing_is_written[preflight|bundle|node]`;
   - evidencia inexistente, sin escritura: `test_missing_evidence_fails_without_writing`;
   - evidencia fuera del root o que no es archivo, sin escritura: `test_evidence_outside_the_root_or_not_a_file_fails_without_writing[dotdot|absolute|symlink|directory]`;
   - owner sin evidencia: `test_owner_without_evidence_records_the_reason_alone`;
   - dispose → accepted: `test_dispose_accepts_a_recorded_receipt`;
   - subject con `@sha256`, ancla intacta según `sldb.api.check_doc_anchors`: `test_subject_is_pinned_and_the_anchor_is_intact` (ver el comportamiento documentado más abajo);
   - extras: `test_goldens_with_evidence_is_numbered_by_its_kind`, `test_reproduction_and_goldens_require_evidence[reproduction|goldens]`, `test_record_requires_a_reason` y `test_json_output_reports_the_receipt`.
2. **Goldens de ayuda.** Se corrió `pytest tests/test_output_goldens.py::test_help_goldens --update-golden`. `git status` mostró solo `M deskops_review.txt` y `?? deskops_review_record.txt`; ningún otro golden cambió. Diff de `deskops_review.txt`:

   ```diff
   -usage: deskops review [-h] {node,preflight,bundle,status,dispose} ...
   +usage: deskops review [-h] {node,preflight,bundle,status,dispose,record} ...
   -  {node,preflight,bundle,status,dispose}
   +  {node,preflight,bundle,status,dispose,record}
   +    record              Record a reproduction, goldens, or owner receipt from
   +                        operator evidence (no model call).
   +  deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
   -caps good attempts per key unless --force --reason.
   +caps good attempts per key unless --force --reason. `record` writes a reproduction, goldens or owner
   +receipt from evidence the operator names, without calling the model; `dispose` gives it the verdict.
   ```

   `deskops_review_record.txt` es nuevo, con 28 líneas.
3. **Tests de a uno**, con TMPDIR=/dev/shm, systemd-run MemoryMax=2G y la guarda pgrep:

   | archivo | resultado | log |
   |---|---|---|
   | test_review_record | 17 passed | review_record.log |
   | test_review_command | 12 passed | review_command.log |
   | test_review_doc | 13 passed, 1 xfailed | review_doc.log |
   | test_output_goldens | 7 passed | output_goldens.log |
   | test_cli_help_examples | 11 passed | cli_help_examples.log |
   | test_operator_manual | **1 failed, falla igual en la base** | operator_manual.log, operator_manual_base.log |
   | test_cli (copia `/dev/shm/deskops-rk` de HEAD `36cbb5d6`, `worktree remove --force` al terminar) | 101 passed | cli.log |

   `test_operator_manual` falla en el bloque runnable 29: `deskops add atom` con `--answer` que trae headings `###`, y sldb lo rechaza con `SLDBValidationError: ruido estructural`. Ese fallo ya existía antes de este nodo: corrido sobre la base `a865bbcf` en `/dev/shm/deskops-rk-base` (ya borrada), falla con el mismo bloque y el mismo error. El bloque nuevo de `record` no es `bash runnable`, así que el test no lo ejecuta.
4. **`wc -l`, antes y después:**

   | archivo | antes | después |
   |---|---|---|
   | deskops/services/review.py | 860 | 923 |
   | deskops/cli/commands/review.py | 118 | 136 |
   | deskops/cli/registry.py | 1838 | 1873 |
   | tests/test_review_record.py | (no existía) | 282 |
   | tests/fixtures/golden/help/deskops_review.txt | 30 | 34 |
   | tests/fixtures/golden/help/deskops_review_record.txt | (no existía) | 28 |
   | docs/operator-manual.md | 909 | 929 |
   | CHANGELOG.md | 162 | 163 |

5. **CHANGELOG y manual:** hechos, ver la sección anterior.

## Desvíos y comportamiento documentado

- **`_write_review` gana `summary: str | None = None`.** Con `None` (el valor por defecto) el summary es el de siempre, así que preflight, bundle y node no cambian. Sin este argumento, el summary de r2/b4 obligaba a escribir el documento dos veces. Ni `_task_path` ni `_resolve_review_path` se tocaron (r6).
- **Pin del subject (H-CC32-2, decidido por coord2):** el `create_document` de sldb no pinnea `__doc_anchors__`; solo lo hace `save_document_payload` (`sldb-runtime/src/sldb/api/documents/payload_save.py:46`). Por eso el recibo **pending queda sin `@sha256`**, igual que los recibos preflight y bundle, y el **accepted queda con `@sha256`**, porque el pin llega en la escritura de `review dispose`. Esa escritura es la que mira la regla de activación de CC32. El test lo verifica en las dos fases y comprueba que, después de dispose, `check_doc_anchors` no da alertas para el recibo. No hay reescritura no-op en `record_receipt`. La brecha va a sldb en la nota de G_CONSUMER (coord2).
- **Exit codes:** `--kind` fuera de la lista y `reproduction` o `goldens` sin evidencia dan exit 2 (uso). La evidencia inválida da exit 1 con el mensaje de r3.
- **Guarda pgrep:** el patrón `pgrep -f "python -m pytest"` dentro de un script lanzado con `bash -c` se encontraba a sí mismo y la espera no terminaba nunca. Se usó `pgrep -f '^(\S*/)?python[0-9.]* -m pytest'`, de acuerdo con coord2.
- No se tocó nada en `desk/`, `.sldb/` ni sldb, y no se hizo push.
