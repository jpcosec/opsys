---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-20T14:13:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:05:16'
---

# sldb: cómo declarar anchors a código desde atoms, tasks y docs (CodeAnchorDoc, anchors record|check)

_Describe the incoming message with enough evidence to triage._

Desde sldb, 2026-10-20, commit 52f63690 en main: el anclaje a código ya existe (docs/architecture/anchoring.md y code-anchoring.md). Cómo declarar anchors desde atoms, tasks y docs:

1. Qué es. Un anchor fundamenta una afirmación en un símbolo de código y guarda lo que vio: `CodeAnchorDoc` (sldb.models.code_anchor_doc:CodeAnchorDoc), autoridad `theorem`. Campos: ref `code:<ruta>::<qualified_name>` (ruta relativa al proyecto; nombre léxico `Clase.metodo`, vacío para el módulo), kind, seen (fingerprints de firma, forma, docstring y cuerpo), normalization, recorded_with, history y claim (lo que se afirma). Requiere el extra `pip install "structuredLanguageDB[code]"` (tree-sitter).

2. Registrar el modelo en tu store: `sldb models add sldb.models.code_anchor_doc:CodeAnchorDoc --store .sldb`. En store.yaml queda como modelo por referencia (sin path), igual que RelationDoc.

3. Crear un anchor desde un atom, una task o un doc:
   sldb anchors record code:deskops/cli/commands/doctor.py::run --write desk/anchors/doctor-run.md --claim "deskops doctor delega la integridad del store a sldb stores check" --store .sldb
   Eso crea y trackea el CodeAnchorDoc firmado (bloque sldb: by, at, via=create_document, authority=theorem). Sin --write solo imprime el bloque. Para enlazar el atom/task/doc con su anchor, usa lo que ya tienes: un RelationDoc (p.ej. relación `grounded_by` de atom → anchor) o la referencia `[[doctor-run]]` en el cuerpo; sldb no inventa un campo nuevo en tus modelos.

4. Comprobar: `sldb anchors check --store .sldb` (solo lee). Estados: intact (ok); changed(signature|docstring|body), reconnected (X -> Y), lost, renormalize son ALERTAS (exit 0, siempre visibles: texto, JSON errors/alerts, warnings del envelope, ::warning en CI); unparseable, invalid y unavailable son ERRORES (exit 1). `--record` es lo único que escribe: registra las reconexiones (ref nuevo, firma y forma del nombre nuevo, entrada en history). Aceptar un cambio es regrabar: `anchors record <ref> --write <mismo archivo>` conserva claim e history.

5. Política: los códigos son anchors/changed, anchors/lost, etc.; puedes declarar en store.yaml `CodeAnchorDoc: {changed: "hook: deskops message send ..."}` y correrlo con `stores check --apply` cuando los hallazgos de anchors pasen por stores check (hoy anchors check es un comando aparte; su JSON trae errors y alerts con la misma forma).

6. Sugerencia de uso en el desk: un anchor por cada claim de un atom que cite código; `anchors check` como gate junto a `stores check` en tu CI (exit solo por errores).
