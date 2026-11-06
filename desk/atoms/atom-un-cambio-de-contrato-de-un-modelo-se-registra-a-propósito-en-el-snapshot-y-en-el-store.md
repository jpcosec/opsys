---
id: atom-un-cambio-de-contrato-de-un-modelo-se-registra-a-propósito-en-el-snapshot-y-en-el-store
title: Un cambio de contrato de un modelo se registra a propósito en el snapshot y
  en el store
five_wh_one_plus: what
tags:
- system:deskops
- topic:model-contracts
---

# Un cambio de contrato de un modelo se registra a propósito en el snapshot y en el store

## Answer

tests/fixtures/model_contract_hashes.json guarda el hash de contrato de cada modelo que deskops usa. Cuando un modelo cambia de contrato (sus campos o su template), test_model_contract_snapshot falla a propósito: el cambio se acepta actualizando el fixture solo junto con la migración de los stores que trackean ese modelo, y con una entrada de CHANGELOG que nombra el cambio de origen. Para un modelo de sldb, como RelationDoc tras GO09, la migración es recalcular el contrato con sldb stores update (o desk update --apply) en cada desk; scripts/migrate_desk_stores.py solo migra modelos de deskops.
