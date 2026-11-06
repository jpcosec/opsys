---
id: materialization-mc-fixtures-model-contract-hashes-json
title: mc fixtures model_contract_hashes.json
source_atoms:
- atom-un-cambio-de-contrato-de-un-modelo-se-registra-a-propósito-en-el-snapshot-y-en-el-store
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
validation:
- pytest -q tests/fixtures/model_contract_hashes.json
tags:
- system:deskops
- topic:model-contracts
---

# mc fixtures model_contract_hashes.json

## Intent

materializa atom-un-cambio-de-contrato-de-un-modelo-se-registra-a-propósito-en-el-snapshot-y-en-el-store en tests/fixtures/model_contract_hashes.json
