# Doctor confunde superficies no modeladas con untracked en sldb

ID: task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260811-011208-suggestion-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb.md`.

## Scope

En el repo sldb, tras corregir data_mutation y sincronizar los docs modelados, deskops status --root . sigue reportando como 'Untracked desk documents' superficies que no deberían forzarse a estar trackeadas por SLDB: desk/drawer/features/*.md, desk/issues/*.md y desk/METHODOLOGY.md. En la práctica, el doctor está mezclando 'docs no modelados' con 'estado roto'. Sería mejor excluir esas superficies no modeladas del chequeo de untracked, o distinguirlas explícitamente de los documentos que sí deben estar registrados en .sldb. Evidencia: en tools/sldb ya no quedan data_mutation; sólo esos paths siguen apareciendo en Doctor Findings.

## Source

- `desk/inbox/20260811-011208-suggestion-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb.md`

## Done When

- The message is resolved, answered, or promoted into active work.
