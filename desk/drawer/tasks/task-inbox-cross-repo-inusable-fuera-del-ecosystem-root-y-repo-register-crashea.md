# inbox cross-repo inusable fuera del ecosystem root y repo register crashea

ID: task-inbox-cross-repo-inusable-fuera-del-ecosystem-root-y-repo-register-crashea
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260901-000600-unclear-inbox-cross-repo-inusable-fuera-del-ecosystem-root.md`.

## Scope

Dos bloqueos encadenados al intentar `deskops inbox "<nota>" --repo deskops` desde gemini_test (worktree en /home/jp/proyectos/_worktrees/vitali, fuera del ecosystem root):

1. El registry se resuelve contra `ecosystem_root/desk/registry` derivado del store local, asi que un repo que vive fuera del arbol del ecosistema no encuentra a `deskops` ("Repository id 'deskops' not found in registry"), y el registry del ecosistema (/home/jp/proyectos/hum-ecosystem/desk/registry/) tampoco tiene entry para el propio deskops.
2. Workaround intentado: `deskops repo register` local con path absoluto para deskops (funciona) y luego registrar el repo actual para pasar el check de identidad (`resolve_canonical_project_identity` exige el repo actual en el mismo registry). Ese segundo register crashea: `Unexpected: 'RegisteredRepository' object has no attribute 'models_index'`.

Esperado: poder enviar notas a repos hermanos desde cualquier checkout/worktree, o al menos un mensaje que indique el camino soportado. Esta nota y su hermana se entregaron escribiendo el archivo a mano en desk/inbox/ con el formato de las notas precedentes.

## Source

- `desk/inbox/20260901-000600-unclear-inbox-cross-repo-inusable-fuera-del-ecosystem-root.md`

## Done When

- The message is resolved, answered, or promoted into active work.
