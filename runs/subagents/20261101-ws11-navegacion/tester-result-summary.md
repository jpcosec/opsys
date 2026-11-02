## LECTURA PROPIA (no ejecuté nada)

### 1. Alcance del diff

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| `fix-diff.txt` toca solo §4 | Propia | `fix-diff.txt:4-15`: un único hunk `@@ -117,7 +117,7 @@` sobre `navegacion.md:120` | PASS |

### 2. Cobertura de la enumeración (línea 120)

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| Enumeración completa en `SL/cli/serve/` | Propia | grep `read_text|read_bytes`: `serve/document_routes.py:62`, `serve/sections_routes.py:46`. Ambas listadas. Ningún `read_bytes` | PASS |
| Enumeración completa en `SL/api/documents/` | Propia | `document_ast.py:22`, `document_serialization.py:20`, `payload_save.py:54`, `track_document_file.py:47`, `:48`, `:68`, `provenance_stamp.py:31`. Las 7 listadas en la cita | PASS |
| Sin lecturas fuera de `read_text/read_bytes` | Propia | grep `open\(|\.read\(|encode\(` en `SL/api/documents/`: 0 coincidencias; en `SL/cli/serve/` solo `auth.py:35`, `responses.py:23,43,44` (petición/respuesta, no archivo de documento) | PASS |
| Etiquetas de las citas correctas | Propia | `:47/:48` = `refuse_structural_noise`/`refuse_undeclared_frontmatter`; `:68` = `validate_model_input_roundtrip` → «validación al registrar»; `:31` = `previous = path.read_text(...)` → «texto previo al estampar» | PASS |
| Ninguna devuelve el texto crudo | Propia | `document_routes.py:62-63`→`build_document_ir_json` (IR); `sections_routes.py:46-48`→IR+secciones; `document_ast.py:22-23`→IR; `document_serialization.py:20`→bloque `provenance`; `payload_save.py:54-55`→payload extraído; `track_document_file.py:47,48,68`→validación, retorna `DocumentReference` (`:49`); `provenance_stamp.py:31-32`→devuelve el `text` argumento (renderizado), no el del archivo | PASS |
| «No hay operación pública que devuelva bytes» | Propia | `stamped_file` (`provenance_stamp.py:29`) es el único retorno de texto y solo lo usan escrituras (`payload_save_steps.py:74`, `model_drafts/backfill.py:66`, `edges/builtin_relation_writes.py:28,55`); `render_routes.py:59` devuelve markdown del payload, ya excluido en la cita | PASS |

## DATO DEL SUPERVISOR (no verificado por mí)
- `tester-v3-facts.log`: HEAD deskops `4d710c02`; sha256 `ca537c71…`; `build_plan --check`, `validate_plan --check`, `context_review status` exit 0. No los ejecuté.

## No pude verificar
- Estado de git / árbol limpio: sin acceso a git.
- Que `surface` reconstruya el texto íntegro: el contrato lo declara no verificado y no lo afirma.

RESULTADO: PASS
