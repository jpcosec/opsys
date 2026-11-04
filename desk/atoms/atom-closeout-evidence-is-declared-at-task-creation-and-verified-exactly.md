---
id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
title: Closeout evidence is declared at task creation and verified exactly
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
- topic:tasks
---

# Closeout evidence is declared at task creation and verified exactly

## Answer

Owner decision, 2026-10-29: the evidence that closes a task is declared when the task is created, and closeout verifies exactly that; the same evidence cannot be demanded of every task. A task states closeout_evidence, a list in a closed vocabulary: tests, commit, atom, materialization, document, external. Pass it with deskops add task --evidence <kind>...; when absent it is filled from --task-type (code, implementation or test: tests + commit + atom|materialization; docs, spec or design: commit + document; external: external). With neither --evidence nor --task-type, add task fails and says how to declare it. deskops closeout verify and deskops closeout commit check only what was declared: tests needs a resolvable test file reference, commit a resolvable ancestor commit id, atom/materialization an atom reference or a changed-file link (either one satisfies it), document an existing document file in references or files, external an http(s) URL in references. A task that lives outside the repository (for example in Linear) declares external, records its URL in references, and closes with deskops closeout commit --no-run --reason. The gate always prints 'esta tarea declaró X; encontré Y'. If the changed files include .py and the task did not declare tests, closeout does not block but prints a visible alert, never silently. A task created before the field existed has no closeout_evidence and is gated as code (tests, commit, atom|materialization), with an alert telling its owner to declare the evidence. Do not demand tests, atom or commit evidence from a docs, spec or external task, and do not leave evidence undeclared on a new task. In a desk without local atom documents (a missing, empty, or README-only desk/atoms/) the atom|materialization gate is exempt and the report says so; the other declared gates still apply.
