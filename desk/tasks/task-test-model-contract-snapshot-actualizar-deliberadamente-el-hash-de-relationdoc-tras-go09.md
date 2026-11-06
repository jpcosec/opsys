---
id: task-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_model_contract_snapshot.py
- tests/test_model_contract_snapshot.py
- 30eb97d40e458d342f68aacb1dac4c7ee6f5a4e8
- desk/atoms/atom-un-cambio-de-contrato-de-un-modelo-se-registra-a-propósito-en-el-snapshot-y-en-el-store.md
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
depends_on: []
pills: []
files:
- tests/fixtures/model_contract_hashes.json
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09.md
---

# test_model_contract_snapshot: actualizar deliberadamente el hash de RelationDoc tras GO09

## Rationale

_Explain why this task exists or the business driver behind it._

Hallado en la suite completa de deskops (f0a4a476, repetido con sldb 88f19ac8): tests/test_model_contract_snapshot.py falla con 'Model contract changed for: RelationDoc'. Causa: GO09 de sldb (transiciones como datos de la arista; código 33b3c7a0, closeout d39bf915) cambió el contrato de RelationDoc (validador de attributes sets/terminal). Decisión del overlord, 2026-11-06; alcance acordado con el coordinador de proyecto el mismo día. Inbox 20261106-180227, promovido al drawer.

## Goal

_Describe the concrete result this task must produce._

tests/fixtures/model_contract_hashes.json registra deliberadamente el contrato nuevo de RelationDoc (a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6) citando GO09, y test_model_contract_snapshot.py pasa; la migración del store de deskops ya está hecha en main (09b5075c: .sldb/core/models/RelationDoc.yaml con ese contract_hash).

## Scope

_State what is in scope and what is out of scope._

En alcance: tests/fixtures/model_contract_hashes.json (solo la entrada RelationDoc) y CHANGELOG.md (una línea en Unreleased / Changed que cita GO09 y la migración 09b5075c). Fuera: los otros 5 desks: sldb ya lo migró el coordinador de proyecto (96bcc5dd, stores update por CLI); spec2viz, scion, pron y graph_ui siguen con el contrato viejo (e2dd…) y los repara el coordinador de proyecto en su tarea de reparar desks con desk update --apply / stores update en cada repo; scripts/migrate_desk_stores.py (no migra RelationDoc, que es modelo de sldb: su dry-run da 'models to update: none'); .sldb/ y desk/; cualquier otro hash.

## Implementation Path

_Outline the expected implementation route or affected surface._

Estado verificado por el coordinador en main: test_model_contract_snapshot falla solo por RelationDoc (1 failed, 1 passed). El hash actual de sldb.models.relation_doc:RelationDoc (hash_model_contract) es a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6 y el snapshot tiene e2ddf0393e197450a26cf048bdfac1d41f049d00983a9c252b9901f4afe9d516. En main, .sldb/core/models/RelationDoc.yaml de deskops ya tiene contract_hash a71cc045 (lo escribió sldb stores update en 09b5075c).
1) Cambiar solo el valor de RelationDoc en tests/fixtures/model_contract_hashes.json por a71cc045..., sin reordenar ni tocar otras claves. Se toma de la salida 'New hashes' del test y se comprueba que coincide con el contract_hash de .sldb/core/models/RelationDoc.yaml.
2) No editar el mensaje FIXTURE_UPDATE del test.
3) CHANGELOG, en Unreleased / Changed, una línea con este texto: «`tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.»
4) Si el test falla por un modelo distinto de RelationDoc, parar y avisar al coordinador: no se actualiza ningún otro hash.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-06):
t1 (desks): quedan pendientes cuatro desks, spec2viz, scion, pron y graph_ui, y los repara el coordinador de proyecto. sldb ya está migrado (96bcc5dd). Este nodo no toca ninguno.
t2 (hash distinto): si el hash de RelationDoc en la salida 'New hashes' no es a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6, o no coincide con el contract_hash de .sldb/core/models/RelationDoc.yaml del worktree, el worker no escribe nada y avisa al coordinador.
t3 (base): el worker trabaja en el worktree que le asigna el coordinador (rama wt/model-contract, creada desde origin/main). Verifica que la migración esté en su base con git merge-base --is-ancestor 09b5075c HEAD (exit 0) y que .sldb/core/models/RelationDoc.yaml tenga contract_hash a71cc045...
t4 (CHANGELOG): «## [Unreleased]» ya tiene «### Changed». La línea va al final de esa lista, antes de la siguiente cabecera. No se crean secciones.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_model_contract_snapshot.py verde (2 passed)
- grep RelationDoc tests/fixtures/model_contract_hashes.json = a71cc045… = contract_hash de .sldb/core/models/RelationDoc.yaml
- git diff --stat contra git merge-base HEAD origin/main limitado a tests/fixtures/model_contract_hashes.json y CHANGELOG.md, una línea cambiada en el fixture
- RESULTADO (coordinador de proyecto, 2026-11-06, squash 30eb97d4 sobre origin/main): test_model_contract_snapshot 2 passed. Solo la entrada RelationDoc del fixture pasa a a71cc045, que es el contract_hash del store de deskops migrado en 09b5075c y el de sldb migrado en 96bcc5dd. CHANGELOG cita GO09 (33b3c7a0/d39bf915). La migración F6 (scripts/migrate_desk_stores.py) no migra RelationDoc porque es modelo de sldb; el equivalente vigente es sldb stores update. Los desks de spec2viz, scion, pron y graph_ui quedan para la tarea de reparación de desks del coordinador de proyecto.

## Done When

_Name the observable condition that makes the task complete._

test_model_contract_snapshot verde con el hash de RelationDoc de GO09 registrado deliberadamente, igual al del store de deskops migrado en 09b5075c; CHANGELOG cita GO09; los cuatro desks pendientes (spec2viz, scion, pron, graph_ui) quedan para la tarea del coordinador de proyecto (sldb ya migrado en 96bcc5dd).
