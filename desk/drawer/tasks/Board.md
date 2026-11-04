# Drawer Board

This board routes deferred work only.

## Remaining

- `tasks/task-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a.md` — Chatbot_Infra: indexar las citas código→atom de los docstrings en el grafo (y huecos de atoms vistos en la auditoría)
- `tasks/task-closeout-commit-reference-points-to-test-solo-acepta-root-tests-py.md` — closeout commit: reference_points_to_test solo acepta <root>/tests/*.py;
- `tasks/task-closeout-la-compuerta-tests-missing-tests-evidence-bloquea-tareas-que.md` — closeout: la compuerta tests (missing_tests_evidence) bloquea tareas que
- `tasks/task-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references.md` — closeout verify ignora el campo atoms de la tarea y solo lee references
- `tasks/task-closeout-verify-no-ve-materializaciones-de-archivos-fuera-del-desk-en-repos-con-src.md` — closeout verify no ve materializaciones de archivos fuera del desk en repos con src/
- `tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md` — Correlacionar intentos Scion con RunDoc y closeout
- `tasks/task-mepu-selector-por-ruta-en-edit-task-y-diagn-stico-drawer.md` — MEPU: selector por ruta en edit task y diagnóstico drawer
- `tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md` — Release deskops 0.2.0 pendiente hasta que la suite completa funcione junta
- `tasks/task-requisitos-d4-d6-de-governance-pr-en-taskdoc-alertas-en-el-inbox-y-rundoc.md` — Requisitos D4–D6 de Governance: PR en TaskDoc, alertas en el inbox y RunDoc
- `tasks/task-sldb-en-main-procedencia-por-documento-pol-tica-por-store-y-alertas-que-no-fallan.md` — sldb en main: procedencia por documento, política por store y alertas que no fallan

## Retired

The covered use-cases, stress-tests (the CI gap closed by task-test-ci-knowledge-integrity-flow, which added scripts/ci-knowledge-check.sh and tests/test_ci_integration.py), findings archive, answered questions, drawer rituals, attention review, and obsolete feature outlines were retired on 2026-10-19. The runtime-and-launcher feature and the tmux launcher task were retired the same day by the coordinator's decision: `deskops runtime supervise` plus the external harness (Herdr) cover what the tmux launcher would have done. Each retirement commit names the test or replacement that covers it, and git history is the durable record.

## Rule

Nothing in `desk/drawer/` executes. When an item is ready, author a full task with `deskops add task --from-drawer <item>` and remove the drawer item by hand once that task supersedes it; there is no drawer-to-task promotion.
