---
sldb:
  by: agent
  at: '2026-11-09T18:21:21Z'
  authority: generated
  via: save_document_payload
id: task-review-record-recibos-reproduction-goldens-y-owner-sin-modelo-seguimiento-de-cc32
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_review_record.py
- pytest tests/test_review_command.py
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
- 293c4dc7ee97c6a156d5ae1c6f608804bb7589da
- desk/atoms/atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo.md
depends_on: []
pills: []
files:
- deskops/services/review.py
- deskops/cli/commands/review.py
- deskops/cli/registry.py
- tests/test_review_record.py
- tests/fixtures/golden/help/deskops_review.txt
- tests/fixtures/golden/help/deskops_review_record.txt
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# review record: recibos reproduction, goldens y owner sin modelo (seguimiento de CC32)

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de CC32 (gates de activación por tipo como RuleDoc), decidido por el overlord el 2026-11-09 (revisable por el dueño). Las reglas de activación de CC32 exigen recibos reproduction (task.debug), goldens (task.refactor) y owner (task.decision), pero deskops review solo produce preflight, bundle y node. Sin esta vía, esas tareas no se pueden activar en un desk real (TaskDoc de CC32, a9). No depende del código de CC32, solo de CC35a (escritura por sldb.api.transaction, que pinnea el ancla del recibo).

## Goal

_Describe the concrete result this task must produce._

deskops review record <task> --kind reproduction|goldens|owner escribe un recibo ReviewDoc de ese kind sobre la tarea, con la evidencia que el operador nombra y verdict pending. deskops review dispose le da el veredicto, como a los demás recibos. Con el recibo accepted e intacto, la regla de activación de CC32 lo cuenta.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/review.py (solo un método nuevo record_receipt, que reusa _write_review), deskops/cli/commands/review.py (el despacho del subcomando), deskops/cli/registry.py (el comando review record), los goldens de ayuda nuevos o cambiados de review (tests/fixtures/golden/help/deskops_review.txt y deskops_review_record.txt), tests/test_review_record.py (nuevo), docs (la sección de review de docs/workflow-policy-reference.md o la referencia del CLI donde se documenta review) y CHANGELOG.md. Fuera: la resolución de documentos de review.py (CC35b la cambia en paralelo), las reglas de CC32 y los kinds preflight, bundle y node (siguen con su comando, que llama al modelo).

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (base CC35a squash 8d0e23fe): deskops/services/review.py (860 líneas). _write_review (:562) arma el payload del ReviewDoc (id review-<task>-<kind>-<n>, subject, engine, run_dir, input/output sha, verdict, reason) y lo crea con doc_access.create_doc. dispose (:616) solo acepta recibos pending. ReviewKind (models/review.py:33) ya tiene reproduction, goldens y owner. CLI: cli/commands/review.py (118 líneas) y registry.py :744-850 (review, node, preflight, bundle, status, dispose).

DECISIONES (coordinador del plan, 2026-11-09; REVISABLES por el dueño):
r1 (forma del comando): deskops review record <task> --kind {reproduction,goldens,owner} --evidence <ruta> [--evidence <ruta> ...] --reason "<texto>" --root <r>. No llama al modelo: el recibo lo escribe quien opera el desk con la evidencia que verificó. preflight, bundle y node no se aceptan en --kind, porque esos los produce la revisión en frío con su comando.
r2 (qué escribe): un ReviewDoc nuevo por _write_review, con kind el pedido, subject el ancla de la tarea igual que en preflight/bundle (doc:<Modelo>:<task>), engine «operator», run_dir vacío, input_sha256 el sha256 de la concatenación ordenada de los archivos de evidencia (ruta + contenido), output_sha256 vacío, verdict «pending», reason el texto dado y summary «<kind> receipt recorded by <actor>; evidence: <rutas>». La evidencia va también en un campo existente del modelo si alguno la admite (references o evidence). Si no hay ninguno, va en summary. No se cambia el modelo ReviewDoc.
r3 (evidencia): cada --evidence es una ruta existente dentro del repo (relativa al root, sin salir con ..). Si no, el comando falla con «Error: evidence not found: <ruta>», exit 1, y no escribe nada. owner admite --evidence opcional (puede ser solo --reason); reproduction y goldens exigen al menos una.
r4 (veredicto): review record no da veredicto. El veredicto lo pone review dispose <review-id> --verdict accepted --reason ..., igual que con preflight/bundle. Así el ciclo pending → disposed es uno solo.
r5 (goldens de ayuda): cambian solo deskops_review.txt (lista el subcomando nuevo) y se agrega deskops_review_record.txt, generados con --update-golden solo para esos dos y revisados en el diff. Ningún otro golden cambia; test_output_goldens y test_cli_help_examples verdes.
r6 (conflicto con CC35b): CC35b cambia en paralelo la resolución de documentos en services/ (incluye _task_path y _resolve_review_path de review.py). Este nodo no toca esas funciones: el método nuevo las llama tal como están. El rebase lo resuelve el coordinador.
r7 (prueba de extremo a extremo con CC32 fuera de este nodo): este nodo prueba que el recibo se escribe, se trackea con subject pinneado (anchor_state intact vía sldb, tras CC35a) y se dispone. Que la regla de activación de CC32 lo cuente se prueba al integrar CC32, no aquí: CC32 no está en main.
r8 (tests): tests/test_review_record.py nuevo. Cubre: un recibo reproduction con evidencia se escribe pending y bien formado; el kind preflight se rechaza; evidencia inexistente o fuera del root falla sin escribir nada; owner sin evidencia funciona; dispose lo pasa a accepted; el subject queda con @sha256 (anchor intact según sldb). Además, de a uno: test_review_command, test_review_doc, test_cli_help_examples y test_output_goldens; test_cli desde una copia en /dev/shm.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-09):
b1 (hash de la evidencia): las rutas de --evidence se normalizan a POSIX relativas al root y se ordenan alfabéticamente, sin repetidas. input_sha256 es el sha256 de los bytes «<ruta>\n<contenido>\n» de cada archivo, concatenados en ese orden. Sin evidencia (owner), input_sha256 queda vacío.
b2 (actor y engine): actor sale de self._identity() (deskops/identity.py), igual que en los demás recibos. engine es «human», como dice la descripción del campo en ReviewDoc (models/review.py:105), y no «operator»: esto corrige r2.
b3 (doc destino): docs/operator-manual.md, que es donde ya se documenta deskops review. Reemplaza a docs/workflow-policy-reference.md en files. Si test_operator_manual verifica el manual contra el CLI, entra en la validación.
b4 (dónde va la evidencia): ReviewDoc no tiene campo references ni evidence (models/review.py:88-121). Las rutas van en summary con el formato de r2; el modelo no se cambia.

## Validation

_List the checks required before this task can close._

- tests/test_review_record.py nuevo (r8)
- Solo cambian deskops_review.txt y deskops_review_record.txt (nuevo) en goldens de ayuda; test_output_goldens y test_cli_help_examples verdes
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_review_command, test_review_doc; test_cli desde copia en /dev/shm
- wc -l antes y después
- CHANGELOG y doc
- Resultado (coordinador de proyecto, squash 293c4dc7): de a uno desde /dev/shm, review_record 17, review_command 12, review_doc 13 (+1 xfail), cli_help_examples 11, cli 101, output_goldens 7 (sin --update-golden). Goldens de ayuda: cambia deskops_review.txt y se agrega deskops_review_record.txt.

## Done When

_Name the observable condition that makes the task complete._

deskops review record escribe recibos reproduction, goldens y owner con evidencia verificada y verdict pending, con subject pinneado; review dispose los acepta; preflight, bundle y node quedan rechazados en --kind. tests/test_review_record.py verde. Solo cambian los goldens de ayuda deskops_review.txt y deskops_review_record.txt (nuevo). test_review_command, test_review_doc, test_cli, test_output_goldens y test_cli_help_examples verdes. CHANGELOG y doc al día.
