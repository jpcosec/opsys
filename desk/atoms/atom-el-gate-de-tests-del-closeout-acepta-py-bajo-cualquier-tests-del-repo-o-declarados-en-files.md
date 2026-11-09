---
id: atom-el-gate-de-tests-del-closeout-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files
title: El gate de tests del closeout acepta .py bajo cualquier tests/ del repo o declarados
  en files
five_wh_one_plus: what
tags:
- system:deskops
- topic:closeout
---

# El gate de tests del closeout acepta .py bajo cualquier tests/ del repo o declarados en files

## Answer

La evidencia de tests del closeout es un .py existente dentro del root del repo cuya ruta pasa por un directorio tests (en cualquier nivel, p. ej. runtime/<x>/tests/) o que está declarado en files del TaskDoc evaluado; se rechazan rutas absolutas o que salen del root (incluidos symlinks), inexistentes, sufijos distintos de .py, lo que esté bajo .venv, site-packages o node_modules, y cadenas que solo parecen evidencia. El gate no recorre el disco.
