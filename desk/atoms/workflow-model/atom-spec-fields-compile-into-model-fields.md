---
id: atom-spec-fields-compile-into-model-fields
title: Spec fields describe model fields
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:fields
- topic:specs
---

# Spec fields describe model fields

## Answer

Spec field YAML defines reusable field vocabulary used by artifact specs and structure diagrams. The Pydantic model for each artifact owns its fields, and concrete values belong inside the artifact payload rather than in separate desk field documents.
