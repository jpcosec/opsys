# Store migration — 2026-10-18 (apply)

Authorized by the owner on 2026-10-18. Run by task-rw-f6-apply-store-migration in three passes over the 40 stores of the dry-run. A backup of each repo's desk/, knowledge/ and .sldb/ was taken first: /tmp/rw/mig/backup/NN-<repo>.tgz.

## Final state per store

stores check | edges check | edges unresolved --local | legacy rituals archived | repo

- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/chatbot/Chatbot_Infra
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/chatbot/ChatbotsKnowledgeBases
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/chatbot/psp_chatbot
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/chatbot/shared_llm-gateway
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/grifo/Chatbot_Infra
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/grifo/grifo_chatbot
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/grifo/shared_llm-gateway
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/manifest
- FAIL | Edges OK | 3 unresolved reference(s) | legacy:0 | AntonIA/repos/mepu/mepu_ocs_dev
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway
- ? | Edges OK | 0 unresolved reference(s) | legacy:3 | Upla/paper_IEEE
- ? | Edges OK | 0 unresolved reference(s) | legacy:0 | Upla/tutor_apoe
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | audiomedia_lodge/legacy/implementacion
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/SLDB_1/UIs/graph_ui
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/SLDB_1/UIs/marcado-ui
- PASS | Edges OK | 46 unresolved reference(s) | legacy:0 | proyectos/SLDB_1/deskops
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/SLDB_1/sldb
- PASS | Edges OK | 3 unresolved reference(s) | legacy:0 | proyectos/SLDB_1/spec2viz
- FAIL | Edges OK | 21 unresolved reference(s) | legacy:1 | proyectos/TraderBot
- ? | 0 error(s), 3 stale | 0 unresolved reference(s) | legacy:3 | proyectos/kimun/docs/archive/architecture/spec2viz
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/legacy/hum-core
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/legacy/hum-ecosystem
- PASS | Edges OK | 3 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem/core/code2specyaml
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem/core/knowledge
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem/core/specyaml
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem/core/turn_extractor
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem/pilots/repopackage-core
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem-worktrees/pm-surface/hum
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/legacy/hum-ecosystem-worktrees/sldb-ui/hum
- ? | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/legacy/hum-scrapper
- PASS | Edges OK | 9 unresolved reference(s) | legacy:0 | proyectos/legacy/ontology
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/office/humble
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/office/humble/Cotizador
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/office/humble/humble-framework
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/wittgenstein/Matrix/Matrix
- PASS | Edges OK | 3 unresolved reference(s) | legacy:0 | proyectos/wittgenstein/Matrix/paper_v2
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/wittgenstein/Matrix/review
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | proyectos/wittgenstein/matrix-shrdlu-spec/matrix
- PASS | Edges OK | 0 unresolved reference(s) | legacy:3 | proyectos/wittgenstein/tractatusIR
- PASS | Edges OK | 0 unresolved reference(s) | legacy:0 | setup

## Stores still failing stores check (owner data, not the migration)

- Upla/paper_IEEE: an AtomDoc has provenance as a list of objects; AtomDoc.provenance is text. No inbox note: its desk has no project_identity.
- Upla/tutor_apoe: atoms in desk/atoms/branches/ lack five_wh_one_plus, with uncommitted owner edits. Note sent to its inbox.
- kimun/docs/archive/architecture/spec2viz: an archived TaskDoc has no id or status. Note sent asking whether the archive should be excluded.
- AntonIA/repos/mepu/mepu_ocs_dev: a tracked inbox note was deleted from disk (the desk was already migrated). Note sent.
- proyectos/TraderBot: its own models (SelfDeclaration is not importable, legacy contract hashes, a StrategyRule data_mutation). No inbox note: the sender is not in its registry.
- proyectos/legacy/hum-scrapper: a TaskDoc has no id or status. Note sent.

## Pass 1 output

```
[/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 1063 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 97 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/ChatbotsKnowledgeBases/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 19 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 25 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 144 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 41 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 156 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 777 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 81 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/grifo_chatbot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 26 documents in 14 models — 2 contract moved
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Updated store derived indexes.
  PASS (exit 0) — PASS: store integrity — 27 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 156 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/manifest/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 0 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 50 documents in 17 models
  PASS (exit 0) — Desk is up to date.
  PASS (exit 0) — PASS: store integrity — 50 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 156 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/Upla/paper_IEEE/.sldb]
  before: FAIL (exit 1)
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/Upla/tutor_apoe/.sldb]
  before: FAIL (exit 1)
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — - updated store indexes
  result: FAIL
[/home/jp/audiomedia_lodge/legacy/implementacion/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 71 documents in 9 models — 71 damaged — 8 roster-only
  FAIL (exit 1)
  result: FAIL
[/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 314 documents in 17 models
  PASS (exit 0) — Desk is up to date.
  PASS (exit 0) — PASS: store integrity — 314 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/UIs/marcado-ui/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 0 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/deskops/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 221 documents in 17 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 221 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/sldb/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 1595 documents in 35 models — 1 contract moved
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Tracked desk/tasks/task-congelar-journal-autoridad-arbol.md as TaskDoc.
  PASS (exit 0) — PASS: store integrity — 1533 documents in 33 models
  result: PASS
[/home/jp/proyectos/TraderBot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 523 documents in 30 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/kimun/docs/archive/architecture/spec2viz/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 0 documents in 9 models — 9 roster-only
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-core/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 1 documents in 3 models — 1 damaged — 2 roster-only
  FAIL (exit 1) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 113 documents in 29 models — 9 damaged — 3 contract moved
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Updated store derived indexes.
  PASS (exit 0) — PASS: store integrity — 128 documents in 29 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/code2specyaml/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 7 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/core/knowledge/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/core/specyaml/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/core/turn_extractor/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/pilots/repopackage-core/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/pm-surface/hum/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/sldb-ui/hum/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/legacy/hum-scrapper/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 95 documents in 17 models — 25 damaged
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated store derived indexes.
  PASS (exit 0) — PASS: store integrity — 91 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/ontology/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 6 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 30 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 0 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/office/humble/Cotizador/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 931 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 224 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/humble-framework/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 18 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 135 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 33 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 191 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 62 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/Matrix/review/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 0 documents in 9 models — 9 roster-only
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Lifecycle graph: tracked desk/lifecycle/closeout-task_completes.md
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 147 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 35 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/tractatusIR/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 5 documents in 17 models — 4 contract moved
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'CrossroadDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'ProtoAtomDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  FAIL (exit 3) — Migrating the task lifecycle to the desk's sldb graph...
  result: FAIL
[/home/jp/setup/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 129 documents in 17 models — 2 damaged — 15 roster-only
  PASS (exit 0) — Updated 'AtomDoc'
  PASS (exit 0) — Updated 'BoardDoc'
  PASS (exit 0) — Updated 'FAQDoc'
  PASS (exit 0) — Updated 'InboxNoteDoc'
  PASS (exit 0) — Updated 'PillDoc'
  PASS (exit 0) — Updated 'RepositoryDoc'
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated 'RoleDoc'
  PASS (exit 0) — Updated 'StepDoc'
  PASS (exit 0) — Updated 'TaskDoc'
  PASS (exit 0) — Updated store derived indexes.
  PASS (exit 0) — PASS: store integrity — 155 documents in 19 models
  result: PASS
Summary: 23/39 PASS
Log: /home/jp/proyectos/SLDB_1/deskops/runs/planning/store-migration-20261018.md
```

## Pass 2 output

```
[/home/jp/Upla/paper_IEEE/.sldb]
  before: FAIL (exit 1)
  FAIL (exit 3) — - updated store indexes
  result: FAIL
[/home/jp/Upla/tutor_apoe/.sldb]
  before: FAIL (exit 1)
  FAIL (exit 3)
  result: FAIL
[/home/jp/audiomedia_lodge/legacy/implementacion/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  PASS (exit 0) — Could not guess model for desk/atoms/detalle/atom-milestone-data-chinook.md.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/TraderBot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 160 documents in 27 models — 21 damaged
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 169 documents in 30 models
  result: PASS
[/home/jp/proyectos/kimun/docs/archive/architecture/spec2viz/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 15 documents in 11 models
  PASS (exit 0) — For further information visit https://errors.pydantic.dev/2.13/v/missing
  FAIL (exit 1)
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/core/code2specyaml/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 22 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 31 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/knowledge/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/specyaml/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/turn_extractor/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/pilots/repopackage-core/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/pm-surface/hum/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/sldb-ui/hum/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 15 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/humble-framework/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 32 documents in 14 models
  PASS (exit 0) — Could not guess model for desk/atoms/workflow/atom-desk-lifecycle.md.
  PASS (exit 0) — PASS: store integrity — 41 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/tractatusIR/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 20 documents in 14 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
Summary: 12/15 PASS
Log: /home/jp/proyectos/SLDB_1/deskops/runs/planning/store-migration-20261018.md
```

## Pass 3 output

```
[/home/jp/proyectos/SLDB_1/spec2viz/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 458 documents in 19 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 458 documents in 22 models
  result: PASS
Summary: 1/1 PASS
Log: /home/jp/proyectos/SLDB_1/deskops/runs/planning/store-migration-20261018.md
```

