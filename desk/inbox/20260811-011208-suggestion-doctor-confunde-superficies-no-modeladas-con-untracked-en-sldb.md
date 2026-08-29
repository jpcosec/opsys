---
kind: suggestion
sender_project: sldb
created_at: 2026-08-11T01:12:08
status: open
---

# Doctor confunde superficies no modeladas con untracked en sldb

En el repo sldb, tras corregir data_mutation y sincronizar los docs modelados, deskops status --root . sigue reportando como 'Untracked desk documents' superficies que no deberían forzarse a estar trackeadas por SLDB: desk/drawer/features/*.md, desk/issues/*.md y desk/METHODOLOGY.md. En la práctica, el doctor está mezclando 'docs no modelados' con 'estado roto'. Sería mejor excluir esas superficies no modeladas del chequeo de untracked, o distinguirlas explícitamente de los documentos que sí deben estar registrados en .sldb. Evidencia: en tools/sldb ya no quedan data_mutation; sólo esos paths siguen apareciendo en Doctor Findings.
