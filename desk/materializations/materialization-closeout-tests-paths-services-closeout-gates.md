---
id: materialization-closeout-tests-paths-services-closeout-gates
title: closeout-tests-paths services closeout_gates
source_atoms:
- atom-el-gate-de-tests-del-closeout-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files
target_kind: code
target_identity: deskops/services/closeout_gates.py
validation:
- pytest -q tests/test_closeout_test_paths.py
tags:
- system:deskops
- topic:closeout
---

# closeout-tests-paths services closeout_gates

## Intent

materializa atom-el-gate-de-tests-del-closeout-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files en deskops/services/closeout_gates.py
