# Store migration, pass 2 — 2026-10-18

Run by task-second-migration-pass-deskfaqdoc-and-ritual-prose after c468749 (FAQDoc renamed to DeskFAQDoc) and e60cdb3 (RitualDoc steps are prose). Same 40 stores as pass 1. Each repo's desk/, knowledge/ and .sldb/ was backed up first to /tmp/rw/mig2/backup/NN-<repo>.tgz.

## What the pass did

- In 35 stores: `sldb models update RitualDoc` (the contract moved), then `deskops desk update --apply`.
- Moved any store that still registered `deskops.models:FAQDoc` as FAQDoc to DeskFAQDoc. sldb's own `docs.models:FAQDoc` was left untouched.
- Seven stores failed on data_mutation that came from sldb's extraction fixes (9dcabd9a, d31180e4), not from deskops. The text did not change; sldb now extracts more of it. Following sldb's own advice ("safe to run: sldb models update <Model>"), only the affected models were re-extracted:
  - code2specyaml, ontology and humble-framework: TaskDoc
  - Matrix: InboxNoteDoc
  - matrix-shrdlu-spec: InboxNoteDoc and PillDoc
  - setup: RepositoryDoc
  - hum-ecosystem: AtomDoc
- In sldb, only desk/ and .sldb/ were committed (86f9be0b), and sldb-04 verified it and pushed it.

## Final state

stores check | edges check | edges unresolved --local | uncommitted desk/.sldb paths | repo

- PASS | Edges OK | 0 unresolved reference(s) | changed:5305 | AntonIA/repos/chatbot/Chatbot_Infra
- PASS | Edges OK | 0 unresolved reference(s) | changed:157 | AntonIA/repos/chatbot/ChatbotsKnowledgeBases
- PASS | Edges OK | 0 unresolved reference(s) | changed:747 | AntonIA/repos/chatbot/psp_chatbot
- PASS | Edges OK | 0 unresolved reference(s) | changed:826 | AntonIA/repos/chatbot/shared_llm-gateway
- PASS | Edges OK | 0 unresolved reference(s) | changed:3879 | AntonIA/repos/grifo/Chatbot_Infra
- PASS | Edges OK | 0 unresolved reference(s) | changed:77 | AntonIA/repos/grifo/grifo_chatbot
- PASS | Edges OK | 0 unresolved reference(s) | changed:826 | AntonIA/repos/grifo/shared_llm-gateway
- PASS | Edges OK | 0 unresolved reference(s) | changed:56 | AntonIA/repos/manifest
- PASS | Edges OK | 3 unresolved reference(s) | changed:0 | AntonIA/repos/mepu/mepu_ocs_dev
- PASS | Edges OK | 0 unresolved reference(s) | changed:14 | AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway
- ? | Edges OK | 0 unresolved reference(s) | changed:633 | Upla/paper_IEEE
- ? | Edges OK | 0 unresolved reference(s) | changed:402 | Upla/tutor_apoe
- PASS | Edges OK | 0 unresolved reference(s) | changed:43 | audiomedia_lodge/legacy/implementacion
- PASS | Edges OK | 0 unresolved reference(s) | changed:0 | proyectos/SLDB_1/UIs/graph_ui
- PASS | Edges OK | 0 unresolved reference(s) | changed:193 | proyectos/SLDB_1/UIs/marcado-ui
- PASS | Edges OK | 0 unresolved reference(s) | changed:0 | proyectos/SLDB_1/deskops
- PASS | Edges OK | 0 unresolved reference(s) | changed:0 | proyectos/SLDB_1/sldb
- PASS | Edges OK | 3 unresolved reference(s) | changed:0 | proyectos/SLDB_1/spec2viz
- FAIL | Edges OK | 1 unresolved reference(s) | changed:517 | proyectos/TraderBot
- ? | 0 error(s), 7 stale | 0 unresolved reference(s) | changed:41 | proyectos/kimun/docs/archive/architecture/spec2viz
- PASS | Edges OK | 0 unresolved reference(s) | changed:27 | proyectos/legacy/hum-core
- PASS | Edges OK | 0 unresolved reference(s) | changed:103 | proyectos/legacy/hum-ecosystem
- PASS | Edges OK | 3 unresolved reference(s) | changed:12 | proyectos/legacy/hum-ecosystem/core/code2specyaml
- PASS | Edges OK | 0 unresolved reference(s) | changed:2 | proyectos/legacy/hum-ecosystem/core/knowledge
- PASS | Edges OK | 0 unresolved reference(s) | changed:8 | proyectos/legacy/hum-ecosystem/core/specyaml
- PASS | Edges OK | 0 unresolved reference(s) | changed:2 | proyectos/legacy/hum-ecosystem/core/turn_extractor
- PASS | Edges OK | 0 unresolved reference(s) | changed:2 | proyectos/legacy/hum-ecosystem/pilots/repopackage-core
- PASS | Edges OK | 0 unresolved reference(s) | changed:26 | proyectos/legacy/hum-ecosystem-worktrees/pm-surface/hum
- PASS | Edges OK | 0 unresolved reference(s) | changed:26 | proyectos/legacy/hum-ecosystem-worktrees/sldb-ui/hum
- ? | Edges OK | 0 unresolved reference(s) | changed:106 | proyectos/legacy/hum-scrapper
- PASS | Edges OK | 9 unresolved reference(s) | changed:13 | proyectos/legacy/ontology
- PASS | Edges OK | 0 unresolved reference(s) | changed:21 | proyectos/office/humble
- PASS | Edges OK | 0 unresolved reference(s) | changed:789 | proyectos/office/humble/Cotizador
- PASS | Edges OK | 0 unresolved reference(s) | changed:79 | proyectos/office/humble/humble-framework
- PASS | Edges OK | 0 unresolved reference(s) | changed:773 | proyectos/wittgenstein/Matrix/Matrix
- PASS | Edges OK | 3 unresolved reference(s) | changed:195 | proyectos/wittgenstein/Matrix/paper_v2
- PASS | Edges OK | 0 unresolved reference(s) | changed:40 | proyectos/wittgenstein/Matrix/review
- PASS | Edges OK | 0 unresolved reference(s) | changed:822 | proyectos/wittgenstein/matrix-shrdlu-spec/matrix
- PASS | Edges OK | 0 unresolved reference(s) | changed:2 | proyectos/wittgenstein/tractatusIR
- PASS | Edges OK | 0 unresolved reference(s) | changed:21 | setup

35 stores pass stores check. The 5 that don't (paper_IEEE, tutor_apoe, the kimun archive, hum-scrapper, TraderBot) fail on their owners' own data, the same as in pass 1, and each has an inbox note. The coordinator decided not to touch their data.

## Pass output

```
[/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 97 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 97 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/ChatbotsKnowledgeBases/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 25 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 25 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 41 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 41 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 36 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 81 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 81 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/grifo_chatbot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 27 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 27 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 36 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/manifest/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 24 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 49 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 49 documents in 17 models
  result: PASS
[/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 36 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 36 documents in 17 models
  result: PASS
[/home/jp/Upla/paper_IEEE/.sldb]
  before: FAIL (exit 1)
  PASS (exit 0) — Updated 'RitualDoc'
  FAIL (exit 3) — - removed FAQDoc
  result: FAIL
[/home/jp/Upla/tutor_apoe/.sldb]
  before: FAIL (exit 1)
  PASS (exit 0) — Updated 'RitualDoc'
  FAIL (exit 3) — - removed FAQDoc
  result: FAIL
[/home/jp/audiomedia_lodge/legacy/implementacion/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 24 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Could not guess model for desk/atoms/detalle/atom-compra-mixer-arcoiris.md.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 319 documents in 17 models
  PASS (exit 0) — Desk is up to date.
  PASS (exit 0) — PASS: store integrity — 319 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/UIs/marcado-ui/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 24 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/deskops/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 226 documents in 17 models
  PASS (exit 0) — Desk is up to date.
  PASS (exit 0) — PASS: store integrity — 226 documents in 17 models
  result: PASS
[/home/jp/proyectos/SLDB_1/sldb/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 2798 documents in 33 models
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 2798 documents in 34 models
  result: PASS
[/home/jp/proyectos/SLDB_1/spec2viz/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 462 documents in 22 models
  PASS (exit 0) — Desk is up to date.
  PASS (exit 0) — PASS: store integrity — 462 documents in 22 models
  result: PASS
[/home/jp/proyectos/TraderBot/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 169 documents in 30 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 169 documents in 30 models
  result: PASS
[/home/jp/proyectos/kimun/docs/archive/architecture/spec2viz/.sldb]
  before: FAIL (exit 1)
  FAIL (exit 1)
  result: FAIL
[/home/jp/proyectos/legacy/hum-core/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 19 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 19 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 128 documents in 29 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 128 documents in 30 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/code2specyaml/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 31 documents in 17 models — 2 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 31 documents in 17 models — 2 damaged
  result: FAIL
[/home/jp/proyectos/legacy/hum-ecosystem/core/knowledge/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/specyaml/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/core/turn_extractor/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem/pilots/repopackage-core/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/pm-surface/hum/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-ecosystem-worktrees/sldb-ui/hum/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/hum-scrapper/.sldb]
  before: PASS (exit 0) — PASS: store integrity — 92 documents in 17 models
  PASS (exit 0) — Could not guess model for desk/atoms/05-portals/Portals.md.
  PASS (exit 0) — PASS: store integrity — 92 documents in 17 models
  result: PASS
[/home/jp/proyectos/legacy/ontology/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 30 documents in 17 models — 6 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 30 documents in 17 models — 6 damaged
  result: FAIL
[/home/jp/proyectos/office/humble/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 24 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/Cotizador/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 224 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 224 documents in 17 models
  result: PASS
[/home/jp/proyectos/office/humble/humble-framework/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 41 documents in 17 models — 16 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 41 documents in 17 models — 16 damaged
  result: FAIL
[/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 33 documents in 17 models — 2 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 33 documents in 17 models — 2 damaged
  result: FAIL
[/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 62 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 62 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/Matrix/review/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 24 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 24 documents in 17 models
  result: PASS
[/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 35 documents in 17 models — 3 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 35 documents in 17 models — 3 damaged
  result: FAIL
[/home/jp/proyectos/wittgenstein/tractatusIR/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 29 documents in 17 models — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Registered missing models and converted copied deskops models.
  PASS (exit 0) — PASS: store integrity — 29 documents in 17 models
  result: PASS
[/home/jp/setup/.sldb]
  before: FAIL (exit 1) — FAIL: store integrity — 155 documents in 19 models — 17 damaged — 1 contract moved
  PASS (exit 0) — Updated 'RitualDoc'
  PASS (exit 0) — Updated store derived indexes.
  FAIL (exit 1) — FAIL: store integrity — 155 documents in 19 models — 17 damaged
  result: FAIL
Summary: 31/40 PASS
Log: /home/jp/proyectos/SLDB_1/deskops/runs/planning/store-migration-20261018.md
```
