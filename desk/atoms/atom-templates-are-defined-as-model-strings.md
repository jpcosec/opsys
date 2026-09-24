---
id: atom-templates-are-defined-as-model-strings
title: Templates are defined as model strings
five_wh_one_plus: where
tags:
- system:sldb
- topic:templates
---

# Templates are defined as model strings

## Answer

Each StructuredNLDoc subclass carries its __template__ as a multiline string, next to the fields it renders; in this repository that means deskops/models/*.py. The store tracks the resulting documents, not the template.
