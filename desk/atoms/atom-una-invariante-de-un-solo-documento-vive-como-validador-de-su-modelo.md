---
id: atom-una-invariante-de-un-solo-documento-vive-como-validador-de-su-modelo
title: Una invariante de un solo documento vive como validador de su modelo
five_wh_one_plus: what
tags:
- system:deskops
- topic:models
- topic:invariants
---

# Una invariante de un solo documento vive como validador de su modelo

## Answer

En deskops, una invariante que se puede comprobar mirando un solo documento (la convención de slug del id de AtomDoc y ProtoAtomDoc, la forma de CrossroadDoc, el título de TaskDoc no vacío) es un validador pydantic del modelo, no un chequeo del CLI. Así sldb la aplica en toda escritura, venga de deskops, de sldb fields update o de sldb docs update, y un test prueba el rechazo por cada ruta. Las invariantes que cruzan documentos van como RuleDoc (CC32 y CC33). Principio del dueño DK6; implementado en CC38 (plan deskops-como-config).
