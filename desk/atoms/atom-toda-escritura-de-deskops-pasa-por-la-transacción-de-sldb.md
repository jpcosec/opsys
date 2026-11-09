---
id: atom-toda-escritura-de-deskops-pasa-por-la-transacción-de-sldb
title: Toda escritura de deskops pasa por la transacción de sldb
five_wh_one_plus: what
tags:
- system:deskops
- topic:transaction
---

# Toda escritura de deskops pasa por la transacción de sldb

## Answer

deskops no tiene escritor propio: cada creación, edición, borrado o tracking de documentos del desk pasa por sldb.api.transaction (doc_access.desk_transaction), con expected_source_hash en los updates; un documento reescrito entre lectura y escritura se rechaza y la transacción completa se revierte. Los documentos quedan con el bloque de proveniencia sldb: en el frontmatter (DO1).
