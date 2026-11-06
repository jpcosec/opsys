---
id: materialization-gi-tests-test-gitignore-policy
title: gi tests test_gitignore_policy
source_atoms:
- atom-en-deskops-el-store-de-sldb-se-versiona-entero-y-solo-la-caché-se-ignora
target_kind: test
target_identity: tests/test_gitignore_policy.py
validation:
- pytest -q tests/test_gitignore_policy.py
tags:
- system:deskops
- topic:store-layout
---

# gi tests test_gitignore_policy

## Intent

materializa atom-en-deskops-el-store-de-sldb-se-versiona-entero-y-solo-la-caché-se-ignora en tests/test_gitignore_policy.py
