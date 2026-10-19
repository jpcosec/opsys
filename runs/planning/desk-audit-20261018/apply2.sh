#!/usr/bin/env bash
set -euo pipefail

ROOT=${ROOT:-/tmp/rw/wt/apply2}
D() { PYTHONPATH=${DESKOPS_PY:-/tmp/rw/wt/apply2} python -m deskops "$@" --root "$ROOT"; }

# ---------------------------------------------------------------- atoms
old=$(cat <<'EOF'
  multi_example:
    do_not_use_when: not
    examples:
    - multi_example:ex1
    - multi_example:ex2
    - multi_example:ex3
    meaning: test
    use_when: testing
EOF
)
D desk replace desk/atoms/tag-namespaces.yaml --old "
$old" --new ""

old=$(cat <<'EOF'
  testex:
    do_not_use_when: no examples needed
    examples:
    - testex:foo
    - testex:bar
    meaning: test examples
    use_when: testing example flag
EOF
)
D desk replace desk/atoms/tag-namespaces.yaml --old "
$old" --new ""

old=$(cat <<'EOF'
  testns:
    do_not_use_when: not testing
    examples: []
    meaning: test
    use_when: testing
EOF
)
D desk replace desk/atoms/tag-namespaces.yaml --old "
$old" --new ""

old=$(cat <<'EOF'
  valid_underscore:
    do_not_use_when: x
    examples: []
    meaning: x
    use_when: x
EOF
)
D desk replace desk/atoms/tag-namespaces.yaml --old "
$old" --new ""

# ---------------------------------------------------------------- roles
D desk replace desk/roles/deskops-supervisor.md \
  --old '- `fireworks/accounts/fireworks/models/kimi-k3` (paid API; routing and review need long context and reliable instruction-following).' \
  --new '- anthropic/claude-opus-4-8 (canonical; routing and review need long context and reliable instruction-following). Fallback: openai-codex/gpt-5.4.'

# ---------------------------------------------------------------- drawer README
D desk replace desk/drawer/README.md \
  --old 'or decomposed into routines and hooks.' \
  --new 'or implemented as CLI operations.'

D desk replace desk/drawer/README.md \
  --old '- `desk/drawer/features/` holds deferred feature documents.' \
  --new '- `desk/drawer/features/` holds deferred feature documents.
- `desk/drawer/issues/` holds deferred issues and closed routing records.
- `desk/drawer/use-cases/` holds user interaction narratives before they become specs or tests.
- `desk/drawer/stress-tests/` holds scripted UX stress-tests derived from the use cases.'

# ---------------------------------------------------------------- features
D desk replace desk/drawer/features/feature-agent-role-models.md \
  --old 'Merged on 2026-09-24. These three arrived as models imported from paper_IEEE. Supervisor and executor are now real RoleDocs (`desk/roles/deskops-supervisor.md`, `desk/roles/deskops-executor.md`, plus a tester) that are tracked and materialize the installed agent files, so what is recorded here is the modelling intent. The router role has no RoleDoc yet.' \
  --new 'Supervisor, executor, and tester are RoleDocs under `desk/roles/`; the router role has no RoleDoc. The imported bodies below are historical: `desk/agents/` is deleted and retirement is `deskops closeout commit`, not file deletion.'

D desk replace desk/drawer/features/feature-runtime-and-launcher.md \
  --old 'Implemented and merged into working tree, uncommitted.' \
  --new 'Implemented and committed on main.'

D desk replace desk/drawer/features/feature-runtime-and-launcher.md \
  --old '`feature-adhoc-subagent-launcher-tmux-multi-cli.md` and its ready-to-promote drawer task cover substantially this same ground, over tmux + `codex`/`agy`/`pi`. Its already-resolved operator principles (context compiled via sldb from tracked RoleDocs, minimal bundle per profile, one launch = one task = one run dir, everything persisted to disk) apply unchanged here and should be inherited, not restated.' \
  --new '`task-adhoc-subagent-launcher-tmux-multi-cli.md` covers substantially this same ground, over tmux + `codex`/`agy`/`pi`, retargeted onto Herdr. Its already-resolved operator principles (context compiled via sldb from tracked RoleDocs, minimal bundle per profile, one launch = one task = one run dir, everything persisted to disk) apply unchanged here and should be inherited, not restated.'

# ---------------------------------------------------------------- issues
D desk replace desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md \
  --old 'feature-herdr-supervised-execution-runtime.md' \
  --new 'feature-runtime-and-launcher.md'

# ---------------------------------------------------------------- questions README
old=$(cat <<'EOF'
## Files

- `workflow-questions.md` - open questions grouped by surface and 5WH1+.
- `workflow-question-map.md` - diagram of the currently suspected connections and unresolved edges.

EOF
)
D desk replace desk/drawer/questions/README.md --old "$old" --new ''

D desk replace desk/drawer/questions/README.md \
  --old '- a ritual/routine/hook, when the answer changes operational process' \
  --new '- a ritual, when the answer changes operational process'

D desk replace desk/drawer/questions/README.md \
  --old '### Task And Routine Semantics' \
  --new '### Task Lifecycle Semantics'

D desk replace desk/drawer/questions/README.md \
  --old '- How does `deskops advance task` evaluate routine progress?' \
  --new '- How does the sldb ritual graph evaluate transition conditions?'

D desk replace desk/drawer/questions/README.md \
  --old '- atom-kgdb-owns-relations-between-knowledge-surfaces' \
  --new '- atom-sldb-semantics-are-graph-inputs' \
  --count 2

D desk replace desk/drawer/questions/README.md \
  --old '- What owns relations? -> `atom-kgdb-owns-relations-between-knowledge-surfaces`, `atom-kgdb-should-parallel-sldb-not-compete`' \
  --new '- What owns relations? -> `atom-sldb-semantics-are-graph-inputs`, `atom-knowledge-graph-connects-desk-and-source-files`'

D desk replace desk/drawer/questions/README.md \
  --old '- What does KGDB provide? -> `atom-kgdb-is-graph-substrate-not-reasoner`, `atom-networkx-is-first-graph-runtime`' \
  --new '- What do sldb graph contracts provide? -> `atom-sldb-semantics-are-graph-inputs`'

D desk replace desk/drawer/questions/README.md \
  --old '        routines["Routines/hooks/gates\nstructured or automatic process"]
' \
  --new ''

old=$(cat <<'EOF'
    rituals -->|decompose when stable?| routines
    routines -->|advance/check/block?| tasks
    routines -->|audit/delete?| pills
EOF
)
D desk replace desk/drawer/questions/README.md --old "$old
" --new ''

# ---------------------------------------------------------------- questions herdr
D desk replace desk/drawer/questions/question-herdr-runtime-open-decisions.md \
  --old '`desk/drawer/features/feature-herdr-supervised-execution-runtime.md`' \
  --new '`desk/drawer/features/feature-runtime-and-launcher.md`'

D desk replace desk/drawer/questions/question-herdr-runtime-open-decisions.md \
  --old '## Blocked Surface' \
  --new '## Resolved'

D desk replace desk/drawer/questions/question-herdr-runtime-open-decisions.md \
  --old '`deskops inbox` cannot record these notes today. The command aborts with `Duplicate repository root` because `desk/registry/` holds nine repo documents pointing at this same root — `described-repo`, `repo-deskops-alt`, `deskops-dir`, `deskops`, `my-repo`, `myrepo`, `pythonpath-repo`, `store-test`, `tagged-repo`. All but `deskops` look like stress-test leftovers. Passing `--sender` does not bypass it. Until the registry is deduplicated, coordination intake is unavailable and notes like this one have to live in the drawer.' \
  --new 'Resolved: the registry was deduplicated and `deskops message send`, `list`, `read`, `ack` works; duplicate roots are rejected by `deskops/identity.py`.'

# ---------------------------------------------------------------- drawer ritual
D desk replace desk/drawer/rituals/knowledge-distillation-pass.md \
  --old 'KGDB query state' \
  --new 'sldb graph state'

D desk replace desk/drawer/rituals/knowledge-distillation-pass.md \
  --old '## KGDB Tools Used' \
  --new '## Graph checks'

old=$(cat <<'EOF'
- KGDB runtime output written by `deskops graph build` under `.sldb/runtime/knowledge_graph.kg.json` and `.sldb/runtime/knowledge_graph.nx.json`.
- KGDB node identity conventions such as `atom:<id>` and `question:<path>` through the deskops graph vocabulary.
- KGDB edge queries exposed by `deskops graph neighbors` to verify relation direction and provenance at the deskops level.
EOF
)
D desk replace desk/drawer/rituals/knowledge-distillation-pass.md --old "$old" --new '- Graph runtime output written by `deskops graph build` under `.sldb/runtime/graphs/deskops.kg.json`.
- Node identity conventions such as `atom:<id>` and `question:<path>` through the deskops graph vocabulary.
- Edge queries exposed by `deskops graph build`, `deskops graph missing`, and `deskops graph neighbors` to verify relation direction and provenance at the deskops level.'

D desk replace desk/drawer/rituals/knowledge-distillation-pass.md \
  --old '## Routine Steps' \
  --new '## Steps'

D desk replace desk/drawer/rituals/knowledge-distillation-pass.md \
  --old 'This ritual is deferred until it is converted into an active `desk/rituals/` document or decomposed into routines, hooks, and gates.' \
  --new 'This ritual is deferred until it is promoted into an active `desk/rituals/` document.'

D desk replace desk/drawer/rituals/knowledge-distillation-pass.md \
  --old '- system:kgdb
' \
  --new ''

# ---------------------------------------------------------------- stress tests
D desk replace desk/drawer/stress-tests/README.md \
  --old '- `desk/drawer/issues/issue-stress-test-fix-backlog.md` — what is left to fix,
  with Phase 0 re-verified against the current CLI
- `desk/drawer/issues/issue-empty-selector-validation-error.md` — the one Phase 0
  item still reproducible' \
  --new '- `desk/drawer/issues/issue-stress-test-fix-backlog.md` — closed; all Phase 0 items are fixed, including empty selectors (`d42a3e3`).'

D desk replace desk/drawer/stress-tests/st-01-fresh-start-orientation.md \
  --old 'deskops graph neighbors atom-deskops' \
  --new 'deskops graph neighbors atom:atom-deskops'

old=$(cat <<'EOF'
# 1. Capture simple
deskops inbox "we should auto-tag atoms by content"

# 2. Capture con urgencia (medio escribiendo)
deskops inbox "el grafo no esta mostrando"

# 3. Ver lo capturado
deskops inbox --list

# 4. Ver detalle
deskops inbox --show <selector>
EOF
)
D desk replace desk/drawer/stress-tests/st-02-inbox-capture.md --old "$old" --new '# 1. Capture simple
deskops message send "we should auto-tag atoms by content"

# 2. Capture con urgencia (medio escribiendo)
deskops message send "el grafo no esta mostrando"

# 3. Ver lo capturado
deskops message list

# 4. Leer y confirmar
deskops message read <selector>
deskops message ack <selector>'

D desk replace desk/drawer/stress-tests/st-03-graph-traceability.md \
  --old 'deskops graph neighbors atom-materialization-contracts-bind-source-output-validation' \
  --new 'deskops graph neighbors atom:atom-materialization-contracts-bind-source-output-validation'

D desk replace desk/drawer/stress-tests/st-03-graph-traceability.md \
  --old 'deskops graph neighbors atom-specs-formalize-atoms-as-contracts' \
  --new 'deskops graph neighbors atom:atom-specs-formalize-atoms-as-contracts'

D desk replace desk/drawer/stress-tests/st-03-graph-traceability.md \
  --old 'deskops graph neighbors atom-orphaned-idea' \
  --new 'deskops graph neighbors atom:atom-orphaned-idea'

old=$(cat <<'EOF'
# 1. Ver tablero
deskops list

# 2. Ver detalle de una tarea
deskops show desk-042

# 3. Avanzar tarea por fases
deskops advance desk-042 --to in_progress

# 4. Saltarse una fase (intencional)
deskops advance desk-042 --to done
# ¿debería dejar? ¿tiene phase gates?

# 5. Avanzar tarea inexistente
deskops advance desk-999 --to in_progress

# 6. Estado después de todo
deskops list
EOF
)
D desk replace desk/drawer/stress-tests/st-05-task-lifecycle.md --old "$old" --new '# 1. Ver tareas
deskops list tasks

# 2. Ver detalle de una tarea
deskops show task <id>

# 3. Ver la siguiente accion
deskops next <id>

# 4. Avanzar tarea (transicion valida)
deskops advance task <id>

# 5. Verificar closeout
deskops closeout verify --task <id>

# 6. Cerrar con commit
deskops closeout commit --task <id> --no-run --reason "..."

# 7. Avanzar tarea inexistente
deskops advance task desk-999'

D desk replace desk/drawer/stress-tests/st-05-task-lifecycle.md \
  --old '| `advance` sin fase actual | ¿Asume una fase default o falla? |
| `advance --to done` saltándose review | ¿El phase gate lo bloquea con un mensaje claro? |' \
  --new '| `advance` sin transición válida | ¿Asume una transición default o falla? |
| `advance` con transición inválida | ¿La validación de transición lo bloquea con un mensaje claro? |'

old=$(cat <<'EOF'
# 1. Drift check completo
deskops drift check

# 2. Drift check por area
deskops drift check --scope graph
deskops drift check --scope materialization

# 3. Drift check con --verbose
deskops drift check --verbose

# 4. Ver detalle de un drift item especifico
deskops drift show drift-003

# 5. Acknowledge drift (aceptar que existe sin arreglarlo)
deskops drift acknowledge drift-003 --reason "will fix in next sprint"

# 6. Re-check despues de acknowledge
deskops drift check
EOF
)
D desk replace desk/drawer/stress-tests/st-07-drift-check.md --old "$old" --new '# 1. Drift check completo
deskops drift check --root .

# 2. Drift check con salida a un directorio
deskops drift check --out <dir>'

D desk replace desk/drawer/stress-tests/st-07-drift-check.md \
  --old '| `--scope` | ¿Filtra correctamente o siempre corre todo? |
| `drift acknowledge` | ¿El acknowledge persiste entre runs? ¿O hay que repetirlo siempre? |
' \
  --new ''

old=$(cat <<'EOF'
# 1. Closeout completo
deskops closeout

# 2. Closeout con fase especifica
deskops closeout --phase graph-building

# 3. Closeout falla — ver que falta
deskops closeout --verbose

# 4. Corregir lo que falta y re-ejecutar
# (various fixes)
deskops closeout
EOF
)
D desk replace desk/drawer/stress-tests/st-08-closeout-ritual.md --old "$old" --new '# 1. Verificar closeout
deskops closeout verify --task <id>

# 2. Corregir lo que falta y re-ejecutar
deskops closeout verify --task <id>

# 3. Commit de cierre
deskops closeout commit --task <id> --no-run --reason "..."'

D desk replace desk/drawer/stress-tests/st-08-closeout-ritual.md \
  --old '| Detalle de fallo | ¿Cada fallo dice qué cheque se ejecutó, qué esperaba, y qué encontró? |
| Fase específica | ¿Corre solo los checks relevantes a esa fase, o es un alias para correr todo? |
' \
  --new ''

old=$(cat <<'EOF'
# 3. Reflection detallada
deskops graph reflect --verbose

# 4. Reflection por tipo de hallazgo
deskops graph reflect --kind orphans
deskops graph reflect --kind cycles
EOF
)
D desk replace desk/drawer/stress-tests/st-09-self-reflection.md --old "$old" --new ''

D desk replace desk/drawer/stress-tests/st-09-self-reflection.md \
  --old '| `--verbose` | ¿Agrega información útil o solo ruido? |
| `--kind` | ¿Filtra bien? ¿Muestra kinds válidos si se pasa uno inválido? |
' \
  --new ''

D desk replace desk/drawer/stress-tests/st-11-atom-scaffold-validate.md \
  --old 'deskops atoms new "Why we use pydantic over dataclasses"' \
  --new 'deskops add atom --title "Why we use pydantic over dataclasses" --five-wh-one-plus what --answer "..."'

D desk replace desk/drawer/stress-tests/st-11-atom-scaffold-validate.md \
  --old 'deskops atoms new ""' \
  --new 'deskops add atom --title "" --five-wh-one-plus what --answer "..."'

D desk replace desk/drawer/stress-tests/st-11-atom-scaffold-validate.md \
  --old 'deskops atoms new "a"  # demasiado corto' \
  --new 'deskops add atom --title "a" --five-wh-one-plus what --answer "..."  # demasiado corto'

D desk replace desk/drawer/stress-tests/st-11-atom-scaffold-validate.md \
  --old 'deskops atoms new "a"$'"'"'\n'"'"'"b"  # multilinea' \
  --new 'deskops add atom --title "a"$'"'"'\n'"'"'"b" --five-wh-one-plus what --answer "..."  # multilinea'

D desk replace desk/drawer/stress-tests/st-11-atom-scaffold-validate.md \
  --old '| `atoms new` |' \
  --new '| `add atom` |'

old=$(cat <<'EOF'
# 1. Health check
deskops status

# 2. Auto-fix
deskops status --fix

# 3. Re-check después del fix
deskops status

# 4. Repair manual guiado
deskops status --guide
EOF
)
D desk replace desk/drawer/stress-tests/st-12-desk-health-recovery.md --old "$old" --new '# 1. Health check
deskops doctor --root .

# 2. Auto-fix
deskops doctor --repair

# 3. Re-check después del fix
deskops doctor --root .'

D desk replace desk/drawer/stress-tests/st-12-desk-health-recovery.md \
  --old '| `status` con archivo faltante | ¿Detecta que falta un atomo referenciado? |
| `status` con .sldb corrupto | ¿El error es "can'"'"'t parse .sldb/core/something.yaml: line 1" o "something went wrong"? |
| `status` con desk sano | ¿El output es "✓ all good" o no imprime nada? |' \
  --new '| `doctor` con archivo faltante | ¿Detecta que falta un atomo referenciado? |
| `doctor` con .sldb corrupto | ¿El error es "can'"'"'t parse .sldb/core/something.yaml: line 1" o "something went wrong"? |
| `doctor` con desk sano | ¿El output es "✓ all good" o no imprime nada? |'

D desk replace desk/drawer/stress-tests/st-12-desk-health-recovery.md \
  --old '| `--fix` | ¿Qué porcentaje de los issues se puede auto-fixear? ¿El resto da instrucciones? |
| `--guide` | ¿Las instrucciones son accionables ("run: deskops atoms restore atom-X") o vagas? |' \
  --new '| `--repair` | ¿Qué porcentaje de los issues se puede auto-fixear? ¿El resto da instrucciones? |'

D desk replace desk/drawer/stress-tests/st-12-desk-health-recovery.md \
  --old '- `status` es otro nombre para `graph missing` — no cubre otras dimensiones
- `status` siempre dice "ok" aunque el desk esté roto (checks no implementados)
- `--fix` empeora las cosas (ej: regenerate snapshot vacío que sobreescribe el bueno)
- No hay `status --backup` antes del fix para poder revertir
- Las guías de reparación son párrafos de documentación en vez de comandos para copiar-pegar
- `status` es lento porque corre todos los checks secuencialmente' \
  --new '- `doctor` es otro nombre para `graph missing` — no cubre otras dimensiones
- `doctor` siempre dice "ok" aunque el desk esté roto (checks no implementados)
- `--repair` empeora las cosas (ej: regenerate snapshot vacío que sobreescribe el bueno)
- No hay `doctor --backup` antes del fix para poder revertir
- Las guías de reparación son párrafos de documentación en vez de comandos para copiar-pegar
- `doctor` es lento porque corre todos los checks secuencialmente'

old=$(cat <<'EOF'
# 1. Registrar repos
deskops repo register ~/projects/hum-ecosystem/tools/deskops
deskops repo register ~/projects/hum-ecosystem/tools/another-tool

# 2. Listar repos registrados
deskops repo list

# 3. Switch context
deskops repo switch tools/another-tool
deskops atoms list  # deberia mostrar atoms de another-tool

# 4. Switch back
deskops repo switch tools/deskops
deskops atoms list

# 5. Ver repo activo actual
deskops repo current

# 6. Unregister
deskops repo unregister tools/another-tool
EOF
)
D desk replace desk/drawer/stress-tests/st-13-multi-repo-context.md --old "$old" --new '# 1. Registrar repos
deskops repo register ~/projects/hum-ecosystem/tools/deskops
deskops repo register ~/projects/hum-ecosystem/tools/another-tool

# 2. Ver repo activo actual
deskops repo whoami

# 3. Ver los repos registrados: ls desk/registry/

# 4. Remover repo
deskops repo remove <selector>'

D desk replace desk/drawer/stress-tests/st-13-multi-repo-context.md \
  --old '| `repo switch` a repo no registrado | ¿Error claro o KeyError? |
| `atoms list` después de switch | ¿Efectivamente cambió el contexto? ¿O el estado es global? |
| `repo current` | ¿El output es un path completo o un alias corto? |' \
  --new '| `repo remove` de un repo no registrado | ¿Error claro o KeyError? |
| `repo whoami` | ¿El output es un path completo o un alias corto? |'

D desk replace desk/drawer/stress-tests/st-13-multi-repo-context.md \
  --old '`repo unregister` borra el repo' \
  --new '`repo remove` borra el repo'

D desk replace desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md \
  --old=--at \
  --new=--into \
  --count 3

D desk replace desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md \
  --old 'deskops atoms deprecate atom-old-idea --reason "superseded by atom-new-idea"' \
  --new 'deskops atoms delete atom-old-idea'

old=$(cat <<'EOF'
# 5. Listar incluyendo deprecados
deskops atoms list --include-deprecated

# 6. Validar grafo post-operacion
EOF
)
D desk replace desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md --old "$old" --new '# 5. Validar grafo post-operacion
'

D desk replace desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md \
  --old '| `atoms deprecate` | ¿El atomo desaparece del `list` normal o aparece con marca? |' \
  --new '| `atoms delete` | ¿El atomo desaparece del `list` y del grafo? |'

D desk replace desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md \
  --old '- deprecate borra el archivo en vez de marcarlo — no hay vuelta atrás' \
  --new '- delete borra el archivo sin confirmación — no hay vuelta atrás'

old=$(cat <<'EOF'
# Simular lo que correria en CI

# 1. Build graph
deskops graph build --ci

# 2. Missing check (exit non-zero si hay missing)
deskops graph missing --ci

# 3. Drift check (exit non-zero si hay drift)
deskops drift check --ci

# 4. Closeout (exit non-zero si no pasa)
deskops closeout --ci-mode

# 5. Ver exit codes
echo $?
EOF
)
D desk replace desk/drawer/stress-tests/st-15-ci-integration.md --old "$old" --new '# Simular lo que correria en CI

# 1. Tests
python -m pytest tests -q

# 2. Missing check (exit non-zero si hay missing)
deskops graph missing

# 3. Drift check (exit non-zero si hay drift)
deskops drift check

# 4. Closeout (exit non-zero si no pasa)
deskops closeout verify --task <id>

# 5. Ver exit codes
echo $?'

D desk replace desk/drawer/stress-tests/st-15-ci-integration.md \
  --old '| `--ci` flag | ¿Cambia el output (menos verbose, más parseable)? ¿O es igual que local? |
' \
  --new ''

# ---------------------------------------------------------------- drawer tasks Board
D desk replace desk/drawer/tasks/Board.md \
  --old '- `issues/` — 28 files:' \
  --new '- `issues/` — 29 files:'

D desk replace desk/drawer/tasks/Board.md \
  --old '  - `workflow-execution-engine.md` — hooks, state machines, condition evaluators, gated pipeline
' \
  --new ''

D desk replace desk/drawer/tasks/Board.md \
  --old '  - `feature-materialization-pipeline.md` — documents from atoms, artifacts for agents
' \
  --new ''

D desk replace desk/drawer/tasks/Board.md \
  --old '- `features/` — six deferred design documents:' \
  --new '- `features/` — four deferred design documents:'

D desk replace desk/drawer/tasks/Board.md \
  --old '- `task-adhoc-subagent-launcher-tmux-multi-cli` — deskops launch: tmux + codex/agy/pi, sldb-compiled per-role context, tool limits by profile, disk-persisted output, deskops-mediated signals (ambiguities resolved; ready to promote)' \
  --new '- `task-adhoc-subagent-launcher-tmux-multi-cli` — deskops launch: tmux + codex/agy/pi, sldb-compiled per-role context, tool limits by profile, disk-persisted output, deskops-mediated signals (ambiguities resolved; ready to promote)
- `task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta` — release 0.2.0, pending until the full suite works together'

D desk replace desk/drawer/tasks/Board.md \
  --old 'Promoted to active desk tasks:' \
  --new 'Promoted to active desk tasks (historical):'

old=$(cat <<'EOF'
KGDB inbox (`tools/kgdb/desk/inbox/`):
- `20260614-000000` — stabilize graph snapshot validation
- `20260614-000001` — stabilize relation serialization
- `20260614-000002` — add graph trace query surface

EOF
)
D desk replace desk/drawer/tasks/Board.md --old "$old" --new 'KGDB was merged into sldb; its inbox no longer exists.

'

old=$(cat <<'EOF'
### Attention (desk/drawer/attention/)

Items triaged into `desk/drawer/attention/` for human review before promotion:

- `20260621-034212-suggestion-clarify-atoms-vs-pills-and-knowledge-flow-in-deskops-docs.md` — epistemic flow documentation gap (overlaps drawer issue)
- `20260621-034342-unclear-clarify-inbox-model-for-inter-project-communication.md` — inter-project inbox model (overlaps drawer issue)
- `20260621-113406-note-tmux-usage-for-development-and-testing-only.md` — tmux boundary: external orchestration only, not runtime logic
- `20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md` — closeout gate: commit boundary required before retirement
- `20260621-160450-note-workflow-summary-so-far.md` — comprehensive workflow model documentation
- `20260621-160930-note-current-workflow-invariants.md` — 13 concise workflow invariants
- `20260621-164028-note-subagent-ready-task-standard-checklist.md` — 100% subagent-ready task checklist (13 sections)

EOF
)
D desk replace desk/drawer/tasks/Board.md --old "$old" --new ''

D desk replace desk/drawer/tasks/Board.md \
  --old '- `desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md`
' \
  --new ''

D desk replace desk/drawer/tasks/Board.md \
  --old '`issue-deskops-init-spawns-one-process-per-model.md` are both resolved.' \
  --new '`issue-deskops-init-spawns-one-process-per-model.md` are both resolved.

Audited 2026-10-19: removed retired drawer references, recorded that KGDB was merged into sldb, and added the pending 0.2.0 release task.'

# ---------------------------------------------------------------- use cases
D desk replace desk/drawer/use-cases/README.md \
  --old '| UC-05 | Routine work — ticking off tasks | add, list, show, advance |' \
  --new '| UC-05 | Task lifecycle | list, show, next, advance, closeout |'

D desk replace desk/drawer/use-cases/README.md \
  --old '| UC-06 | Spec to artifact pipeline | specs, materialization |
' \
  --new ''

D desk replace desk/drawer/use-cases/README.md \
  --old '| UC-15 | Deskops as a CI step | CI integration |' \
  --new '| UC-15 | Deskops as a CI step | CI via pytest and graph/drift checks |'

D desk replace desk/drawer/use-cases/doc-pattern-crawl4ai-analysis.md \
  --old '│   ├── Rituals & Routines' \
  --new '│   ├── Rituals (lifecycle states)'

D desk replace desk/drawer/use-cases/doc-pattern-crawl4ai-analysis.md \
  --old '│   ├── Primitives (conditions, operators, checklists, edges)' \
  --new '│   ├── Workflow model (tasks, atoms, graph)'

D desk replace desk/drawer/use-cases/uc-01-fresh-start-getting-oriented.md \
  --old 'deskops graph neighbors atom-deskops' \
  --new 'deskops graph neighbors atom:atom-deskops'

old=$(cat <<'EOF'
1. `deskops inbox add "we should have a way to auto-tag atoms based on their content"` → saved
2. Later: `deskops inbox list` → sees the idea sitting there
3. `deskops inbox show 1` → reads the full note
EOF
)
D desk replace desk/drawer/use-cases/uc-02-spark-of-an-idea-capture-it.md --old "$old" --new '1. `deskops message send "..."` → saved
2. Later: `deskops message list` → sees the idea sitting there
3. `deskops message read <selector>` → reads the full note'

D desk replace desk/drawer/use-cases/uc-03-where-does-this-atom-touch.md \
  --old 'deskops graph neighbors atom-materialization-contracts-bind-source-output-validation' \
  --new 'deskops graph neighbors atom:atom-materialization-contracts-bind-source-output-validation'

D desk replace desk/drawer/use-cases/uc-03-where-does-this-atom-touch.md \
  --old '`deskops atoms show atom-specs-formalize-atoms-as-contracts`' \
  --new '`deskops atoms show atom:atom-specs-formalize-atoms-as-contracts`'

D desk replace desk/drawer/use-cases/uc-05-routine-work-ticking-off-tasks.md \
  --old '# UC-05: Routine work — ticking off tasks' \
  --new '# UC-05: Task lifecycle — moving through rituals'

old=$(cat <<'EOF'
1. `deskops list` → sees available tasks with status and phase
2. `deskops show desk-042` → reads the task details
3. Starts working: `deskops advance desk-042 --to in_progress`
4. Finishes implementation: commits, then `deskops advance desk-042 --to review`
5. After review passes: `deskops advance desk-042 --to done`
EOF
)
D desk replace desk/drawer/use-cases/uc-05-routine-work-ticking-off-tasks.md --old "$old" --new '1. `deskops list tasks` → sees available tasks with status and phase
2. `deskops show task <id>` → reads the task details
3. `deskops next <id>` → sees the next valid action
4. Starts working: `deskops advance task <id>`
5. Finishes implementation: `deskops closeout verify --task <id>`
6. After verification passes: `deskops closeout commit --task <id> --no-run --reason "..."`'

old=$(cat <<'EOF'
1. `deskops drift check` → compares atom claims against implementation
2. Gets a report:
   - **Green**: claims match implementation
   - **Yellow**: claims exist but can't be verified automatically
   - **Red**: claims contradict implementation
3. User drills into a red item → sees what the atom says vs what the code does
4. Decides: update the atom, update the code, or acknowledge drift
EOF
)
D desk replace desk/drawer/use-cases/uc-07-the-drift-check.md --old "$old" --new '1. `deskops drift check --root .` → compares atom claims against implementation
2. Reads the findings: each one names the check, the expected claim, and what was found
3. Decides: update the atom or update the code'

D desk replace desk/drawer/use-cases/uc-08-closeout-wrapping-up.md \
  --old '1. Run `deskops closeout` — or some named ritual' \
  --new '1. Run `deskops closeout verify --task <id>`'

D desk replace desk/drawer/use-cases/uc-08-closeout-wrapping-up.md \
  --old '4. If pass: marks the phase as truly done' \
  --new '4. If pass: `deskops closeout commit --task <id> --no-run --reason "..."`'

D desk replace desk/drawer/use-cases/uc-10-i-want-to-share-this-insight.md \
  --old '2. `deskops materialize` → generates human-friendly documents from atoms' \
  --new '2. Write or update the atom materialization doc under `docs/` (see `MaterializationContractDoc`)'

D desk replace desk/drawer/use-cases/uc-11-ritual-new-atom-from-scratch.md \
  --old '1. `deskops atoms new "Why we use pydantic over dataclasses"` → scaffolds a new atom file' \
  --new '1. `deskops add atom --title "..." --five-wh-one-plus what --answer "..."` → scaffolds a new atom file'

D desk replace desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md \
  --old '1. `deskops status` → health check of the desk workspace' \
  --new '1. `deskops doctor --root .` → health check of the desk workspace'

D desk replace desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md \
  --old '3. `deskops status --fix` → auto-fixes what it can' \
  --new '3. `deskops doctor --repair` → auto-fixes what it can'

D desk replace desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md \
  --old '5. User follows instructions, re-runs `status`, desk is healthy again' \
  --new '5. User follows instructions, re-runs `doctor`, desk is healthy again'

D desk replace desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md \
  --old '- `status` says "everything fine" when things are obviously broken' \
  --new '- `doctor` says "everything fine" when things are obviously broken'

old=$(cat <<'EOF'
1. `deskops repo register ~/projects/hum-ecosystem/tools/deskops` → registers a desk
2. `deskops repo list` → sees all registered desks
3. `deskops repo switch tools/deskops` → active desk context changes
4. Now `deskops atoms list` shows atoms for that project
5. `deskops repo switch tools/another-tool` → context switches
EOF
)
D desk replace desk/drawer/use-cases/uc-13-multi-repo-ecosystem.md --old "$old" --new '1. `deskops repo register ~/projects/hum-ecosystem/tools/deskops` → registers a desk
2. `deskops repo whoami` → confirms which desk the current root resolves to
3. `ls desk/registry/` → sees all registered desks
4. `deskops repo remove <selector>` → unregisters a desk'

D desk replace desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md \
  --old '# UC-14: Atom evolution — splitting, merging, deprecating' \
  --new '# UC-14: Atom evolution — splitting, merging, deleting'

D desk replace desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md \
  --old=--at \
  --new=--into \
  --count 2

D desk replace desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md \
  --old '3. `deskops atoms deprecate atom-old-idea --reason "superseded by atom-new-idea"` → marks as deprecated' \
  --new '3. `deskops atoms delete atom-old-idea` → removes the obsolete atom'

old=$(cat <<'EOF'
4. `deskops graph build && deskops graph missing` → validates the refactored graph
5. Old atoms show deprecated status in `atoms list` and `graph neighbors`
EOF
)
D desk replace desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md --old "$old" --new '4. `deskops graph build && deskops graph missing` → validates the refactored graph'

old=$(cat <<'EOF'
2. CI runs: `deskops graph build && deskops graph missing`
3. CI runs: `deskops drift check`
4. CI runs: `deskops closeout --ci-mode`
5. If any fail → PR is blocked with a clear report
6. Developer sees in CI logs: "2 missing references, 1 drift item"
7. Fixes issues, pushes, CI passes
EOF
)
D desk replace desk/drawer/use-cases/uc-15-deskops-as-a-ci-step.md --old "$old" --new '2. CI runs: `python -m pytest tests -q`
3. CI runs: `deskops graph missing`
4. CI runs: `deskops drift check`
5. CI runs: `deskops closeout verify --task <id>`
6. If any fail → PR is blocked with a clear report
7. Developer sees in CI logs: "2 missing references, 1 drift item"
8. Fixes issues, pushes, CI passes'

# ---------------------------------------------------------------- whitespace cleanup
D desk replace desk/drawer/questions/README.md \
  --old $'\n\n\n\n## Promotion Rule' \
  --new $'\n\n## Promotion Rule'

D desk replace desk/drawer/tasks/Board.md \
  --old $'KGDB was merged into sldb; its inbox no longer exists.\n\n\n\nRemoved' \
  --new $'KGDB was merged into sldb; its inbox no longer exists.\n\nRemoved'

D desk replace desk/drawer/tasks/Board.md \
  --old $'`paper_IEEE`.\n\n\n\n### Features' \
  --new $'`paper_IEEE`.\n\n### Features'

D desk replace desk/drawer/stress-tests/st-09-self-reflection.md \
  --old $'deskops graph reflect\n\n\n' \
  --new $'deskops graph reflect\n\n'

echo "apply2: all replacements applied"
