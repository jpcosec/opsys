# add/promote no trackean el bundle generado en el store

ID: task-add-promote-no-trackean-el-bundle-generado-en-el-store
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260901-000500-unclear-add-promote-no-trackean-el-bundle-generado.md`.

## Scope

`deskops add task` y `deskops promote drawer-task-to-active-task` generan el bundle completo (task, routine, checklists, conditions, edges, operators) pero no lo trackean en el store sldb. Evidencia: en gemini_test (worktree vitali, 2026-08-31/09-01) una pasada de promotes dejo 22 docs untracked y un `add task` dejo 19; `deskops doctor` los reporta como "Untracked desk documents" y hay que correr `sldb docs track <path> --model <Model>` a mano por cada archivo. Repro: `deskops add task --root . --title X` en un desk con store `.sldb`, luego `deskops doctor --root .`. Esperado: el bundle queda trackeado al crearse, igual que hace `repo register` con su entry.

Nota entregada a mano en este inbox porque el camino CLI (`deskops inbox --repo deskops`) no fue posible desde gemini_test; ver la nota hermana sobre el registry.

## Source

- `desk/inbox/20260901-000500-unclear-add-promote-no-trackean-el-bundle-generado.md`

## Done When

- The message is resolved, answered, or promoted into active work.
