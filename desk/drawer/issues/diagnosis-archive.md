# Deskops architectural diagnosis (2026-08, archived 2026-09-24)

A structured diagnosis of the deskops/SLDB stack that broke its findings into atom-shaped
documents across fifteen families (SLDB underuse and composition-first workflow, hook runtime,
workspace health, cross-desk identity, CLI surface, atom mutation and provenance, multi-surface
drift, stack-level core realignment). It was never promoted.

Six of its documents became atoms, current as of this review:

- `desk/atoms/atom-deskops-still-reads-workflow-surfaces-as-files-where-it-could-compose-them.md`
- `desk/atoms/atom-deskops-should-read-through-sldb-compositions.md`
- `desk/atoms/atom-materializations-are-projections-not-read-surfaces.md`
- `desk/atoms/atom-do-not-atomize-a-coherent-deliverable-into-disconnected-tasks.md`
- `desk/atoms/atom-hook-automation-can-be-powerful-but-opaque.md`
- `desk/atoms/atom-multi-surface-drift-is-a-core-workflow-failure-mode.md`

The rest is kept verbatim below. Most of it is either a process note ("X needs its own
diagnosis line"), a workline (a candidate implementation slice), or a stack observation written
when KGDB and HUM were separate substrates, so it is history rather than backlog. The open
issues it fed are listed in `desk/drawer/tasks/Board.md`.


---

### 01-summary/atom-diagnosis-deskops-subutilizes-sldb

---
id: atom-diagnosis-deskops-subutilizes-sldb
title: Deskops subutilizes SLDB as its operational reading layer
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:workflow-model
type: atom
description: Architectural diagnosis summary for the current deskops workflow.
---

### Deskops subutilizes SLDB as its operational reading layer

#### Answer

The current workflow still treats too many structured workflow surfaces as Markdown files to read directly instead of as structured documents to query, compose, and render through SLDB. That weakens the intended architecture where deskops should sit on top of SLDB and expose workflow operations over compositions rather than raw file reads.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `README.md` — declares that deskops is built on top of `sldb` and that `sldb` owns structured document infrastructure.
- `.skills/sldb/SKILL.md` — describes the intended SLDB-first path for structured document reads, writes, field queries, and model operations.
- `deskops/operations.py` — still contains multiple direct file/path resolution and document-loading paths in the deskops runtime.


---

### 02-observed-problems/atom-deskops-still-operates-too-directly-on-files

---
id: atom-deskops-still-operates-too-directly-on-files
title: Deskops still operates too directly on files
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:workflow-model
type: atom
description: Observed problem in how deskops consumes workflow surfaces.
---

### Deskops still operates too directly on files

#### Answer

Deskops still relies too often on direct file-shaped surfaces such as task Markdown, atom Markdown, and materialized docs instead of consistently routing those reads through SLDB-backed queries and compositions. This keeps deskops too close to document storage and too far from the structured domain layer it is meant to provide.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

#### Evidence

- `deskops/operations.py` — uses `_resolve_glob`, `_read_doc`, direct task paths, and board file paths throughout operational flows.
- `deskops/workflow/next_actions.py` — reads workflow YAML directly from `spec/workflows/task_lifecycle.yaml` and matches states by current node.
- `README.md` — says deskops should sit on top of SLDB rather than duplicate document infrastructure behavior.


---

### 02-observed-problems/atom-hooks-are-modeled-but-not-a-general-runtime

---
id: atom-hooks-are-modeled-but-not-a-general-runtime
title: Hooks are modeled but not a general runtime
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:hooks
type: atom
description: Observed problem in the current hook layer.
---

### Hooks are modeled but not a general runtime

#### Answer

Deskops already models hooks as workflow artifacts, but it does not yet expose a general runtime that resolves events, evaluates hook conditions, and dispatches hook targets consistently. As a result, some automatic behavior exists only as specialized code paths instead of as reusable hook-driven workflow automation.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `deskops/models/hook.py` — defines hook documents as first-class modeled workflow artifacts.
- `deskops/cli/parser.py` and `deskops/cli/commands/operations.py` — expose add/show/list surfaces for hooks.
- `deskops/operations.py` — contains specific automation like `_auto_commit_task_closure()` but no general hook dispatcher that resolves hook docs by event and runs targets.


---

### 02-observed-problems/atom-reading-atoms-through-markdown-bypasses-sldb-composition

---
id: atom-reading-atoms-through-markdown-bypasses-sldb-composition
title: Reading atoms through Markdown bypasses SLDB composition
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:atoms
type: atom
description: Observed problem in the current reading path for atoms.
---

### Reading atoms through Markdown bypasses SLDB composition

#### Answer

When an atom is consumed primarily by opening its `.md` file, the operational reading path bypasses SLDB's document model, field access, and composition capabilities. That makes the materialized file behave like the primary interface instead of a projection over structured knowledge.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-drift-check-review-loop.md`

#### Evidence

- `README.md` — states that docs are human-facing materializations and that SLDB should be the structured read/write/edit surface.
- `.skills/sldb/SKILL.md` — describes field/query/compose operations that should be preferred over ad hoc file reads.
- `docs/diagrams/workflow/workflow-model.md` — says docs should be materialized from atoms, which implies the projection should not become the primary operational read path.


---

### 02-observed-problems/atom-tasks-are-not-yet-atomized-to-execution-actions

---
id: atom-tasks-are-not-yet-atomized-to-execution-actions
title: Tasks are not yet atomized to execution actions
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Observed problem in the current task execution model.
---

### Tasks are not yet atomized to execution actions

#### Answer

Current tasks usually capture goal, scope, files, and validation, but they do not yet consistently decompose execution into concrete edit-oriented actions such as replacing a pattern, introducing a method from an existing example, or applying a named refactor to a specific surface. That leaves too much semantic improvisation to the executor lane.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `spec/artifacts/task.yaml` — task artifacts are modeled at the current task-document layer rather than as detailed edit-action bundles.
- `deskops/operations.py` — normalized task payloads focus on title, goal, scope, references, files, validation, and routine linkage.
- `/home/jp/.pi/agent/agents/deskops-executor.md` — still frames execution mainly as reading task scope and then implementing, not as consuming a compiled edit-plan composition.


---

### 03-evidence-and-symptoms/atom-documentation-growth-compensates-for-weak-semantic-access

---
id: atom-documentation-growth-compensates-for-weak-semantic-access
title: Documentation growth compensates for weak semantic access
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:documentation
type: atom
description: Symptom connecting document growth with architectural underuse of SLDB.
---

### Documentation growth compensates for weak semantic access

#### Answer

When structured knowledge is not easy to recover through queries and compositions, projects tend to add more explanatory docs, diagrams, summaries, and operational prompts to compensate. Some of the current documentation pressure likely comes from this missing semantic access path rather than from an intrinsic need for more prose.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

#### Evidence

- `docs/diagrams/` — the repo already carries many explanatory workflow diagrams across multiple subtrees.
- `AGENTS.md`, `README.md`, `docs/faq.md`, `desk/rituals/*.md`, and `.agents/skills/*.md` — together show a large amount of compensating operational prose.
- `.skills/sldb/SKILL.md` and `README.md` — indicate the intended structured access path that could reduce the need for some compensating prose if used more directly.


---

### 03-evidence-and-symptoms/atom-frontmatter-becomes-reading-noise-when-sldb-is-underused

---
id: atom-frontmatter-becomes-reading-noise-when-sldb-is-underused
title: Frontmatter becomes reading noise when SLDB is underused
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:symptoms
type: atom
description: Symptom explaining why the current reading path feels heavy.
---

### Frontmatter becomes reading noise when SLDB is underused

#### Answer

Frontmatter is valuable as structured metadata for indexing, validation, and field access, but it becomes reading noise when the operational path repeatedly consumes whole Markdown files instead of retrieving only the needed fields or a composed view. This symptom indicates the structured layer is not acting as the primary interface.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `spec/artifacts/atom.yaml` — atom docs carry structured fields like title, five_wh_one_plus, and answer in a modeled document format.
- `.skills/sldb/SKILL.md` — suggests those fields should be queried or composed structurally instead of always reading whole Markdown files.
- Current atom materializations under `desk/atoms/` expose frontmatter plus rendered body, which is useful for humans but heavy as the default operational read path.


---

### 04-expected-model/atom-deskops-should-read-through-sldb-compositions

---
id: atom-deskops-should-read-through-sldb-compositions
title: Deskops should read through SLDB compositions
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:composition
type: atom
description: Expected model for reading workflow knowledge.
---

### Deskops should read through SLDB compositions

#### Answer

Deskops should treat SLDB as the primary read/query/compose layer for structured workflow knowledge. Reading an atom, task, or materialization should usually mean resolving a structured document and asking SLDB for the appropriate composition or field view, not opening the materialized Markdown file as the default operational path.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

#### Evidence

- `README.md` — defines the SLDB boundary and says SLDB owns structured Markdown operations while deskops owns the workflow domain on top of that infrastructure.
- `.skills/sldb/SKILL.md` — lists the exact SLDB query, field, model, and composition commands that form the intended structured access path.
- `desk/atoms/workflow-model/atom-sldb-is-read-write-edit-surface.md` — names SLDB as the preferred structured document surface for these operations.


---

### 04-expected-model/atom-materializations-are-projections-not-primary-read-surfaces

---
id: atom-materializations-are-projections-not-primary-read-surfaces
title: Materializations are projections not primary read surfaces
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:materialization
type: atom
description: Expected model for docs and rendered workflow surfaces.
---

### Materializations are projections not primary read surfaces

#### Answer

Materialized docs, diagrams, and similar rendered surfaces should primarily act as human-facing projections over structured knowledge. They should not be the default operational input path for deskops when a structured query or composition can provide the needed information more precisely.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `docs/diagrams/README.md` — explicitly says diagrams are human-facing materializations.
- `docs/diagrams/workflow/workflow-model.md` — describes docs as materialized from atoms.
- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md` and `atom-rendered-diagrams-are-projections.md` — express the same architectural direction.


---

### 04-expected-model/atom-tasks-should-compile-to-execution-compositions

---
id: atom-tasks-should-compile-to-execution-compositions
title: Tasks should compile to execution compositions
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Expected model for making tasks more executable.
---

### Tasks should compile to execution compositions

#### Answer

A task should not stop at human-readable intent. Deskops should be able to compile a task into an execution composition that includes the exact surfaces to touch, relevant patterns or examples, intended edits, validation targets, and anti-patterns. That would reduce executor improvisation and make subagent lanes more deterministic.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md` — pushes tasks toward bounded autonomous execution.
- `desk/rituals/execution.md` — requires explicit scope, touched files, and validation targets before implementation.
- `.agents/skills/subagent-execution/SKILL.md` and `/home/jp/.pi/agent/agents/deskops-executor.md` — already assume the need for bounded execution bundles and evidence, which points toward a compiled execution composition.


---

### 05-gaps/atom-gap-between-current-file-reading-and-composed-reading

---
id: atom-gap-between-current-file-reading-and-composed-reading
title: Gap between current file reading and composed reading
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:gaps
type: atom
description: Main architectural gap between current and target workflow behavior.
---

### Gap between current file reading and composed reading

#### Answer

The main gap is that deskops has not yet fully turned SLDB queries and compositions into its normal operational interface. Until that happens, agents and humans will keep falling back to direct file reads, and the intended separation between structured source, composition, and materialization will remain incomplete.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-add-drift-check-review-loop.md`

#### Evidence

- `README.md` and `.skills/sldb/SKILL.md` — define the intended SLDB-first architecture.
- `deskops/operations.py` and `deskops/workflow/next_actions.py` — show the current runtime still operating heavily through file-shaped document access.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` — now records this mismatch between intended architecture and current operational behavior.


---

### 06-worklines/atom-workline-activate-a-general-hook-runtime

---
id: atom-workline-activate-a-general-hook-runtime
title: Activate a general hook runtime
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:hooks
type: atom
description: Workline for turning modeled hooks into reusable runtime automation.
---

### Activate a general hook runtime

#### Answer

Deskops should move from merely modeling hooks to running them through a general event-driven mechanism. A minimal runtime should resolve hook documents for an event, evaluate conditions, support dry-run visibility, persist evidence, and dispatch targets such as closeout automation or executor-lane launch.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`
- `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md`

#### Evidence

- `deskops/models/hook.py` and hook CLI surfaces show that hooks already exist as modeled documents.
- `deskops/operations.py` already contains narrow automatic behavior like auto-closeout commit, suggesting a candidate target for generalization into hook runtime behavior.
- `docs/diagrams/process/rituals-routines-hooks-workflow.md` and `llm-tasks-vs-automatic-routines.md` describe the intended role of hooks and automatic routines.


---

### 06-worklines/atom-workline-add-execution-plan-to-task-model

---
id: atom-workline-add-execution-plan-to-task-model
title: Add an execution plan to the task model
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagnosis
- topic:tasks
type: atom
description: Workline for making tasks more executable by subagents.
---

### Add an execution plan to the task model

#### Answer

The task model should gain a field or composition layer for execution plans that describe concrete edit actions. These plans can name target files, replacement patterns, insertion points, donor examples, refactor shapes, and validation obligations so the executor lane receives a bounded operational recipe rather than only a semantic goal.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `deskops/operations.py` current task normalization and bundle creation show the present task contract and where an execution-plan layer could attach.
- `desk/rituals/execution.md` requires explicit touched files and validation, which aligns with a more concrete execution-plan field or composition.
- `/home/jp/.pi/agent/agents/deskops-executor.md` describes the need for exact touched surfaces and bounded action, which an execution plan could encode directly.


---

### 06-worklines/atom-workline-introduce-deskops-compose-operations

---
id: atom-workline-introduce-deskops-compose-operations
title: Introduce deskops compose operations
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:worklines
type: atom
description: Workline for making deskops consume SLDB compositions directly.
---

### Introduce deskops compose operations

#### Answer

Deskops should expose first-class compose operations for structured workflow artifacts such as atoms, tasks, and materializations. These operations should resolve documents through SLDB and return fit-for-purpose views such as minimal field bundles, execution bundles, review bundles, or human-facing composed summaries.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

#### Evidence

- `.skills/sldb/SKILL.md` — provides the underlying query/compose/document operations that deskops can build on.
- `README.md` — says deskops should not duplicate document infrastructure behavior owned by SLDB.
- Existing `deskops next` behavior in `deskops/operations.py` already hints at higher-level composed views and can serve as a stepping stone.


---

### 07-priority-use-cases/atom-use-case-auto-dispatch-executor-on-execution-ready

---
id: atom-use-case-auto-dispatch-executor-on-execution-ready
title: Auto-dispatch an executor when a task becomes execution-ready
five_wh_one_plus: when
tags:
- system:deskops
- topic:diagnosis
- topic:use-cases
type: atom
description: Priority use case for hook-driven workflow automation.
---

### Auto-dispatch an executor when a task becomes execution-ready

#### Answer

When a task satisfies execution-ready conditions, deskops should be able to compose the bounded execution bundle, create the run evidence directory, and dispatch the executor lane automatically or in a reviewable dry-run mode. This use case would prove that hooks can drive real workflow automation rather than remain passive documentation artifacts.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `spec/workflows/task_lifecycle.yaml` defines the execution gate and next actions conceptually.
- `deskops/operations.py` can already detect task state transitions and create runtime artifacts for task lifecycle handling.
- `.agents/skills/subagent-execution/SKILL.md` defines the run-evidence bundle that an automatic dispatch path would need to create.


---

### 07-priority-use-cases/atom-use-case-read-atom-without-reading-full-markdown

---
id: atom-use-case-read-atom-without-reading-full-markdown
title: Read an atom without reading full Markdown
five_wh_one_plus: when
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:use-cases
type: atom
description: Priority use case for the compose/query path.
---

### Read an atom without reading full Markdown

#### Answer

A common workflow should allow deskops to retrieve just the relevant structured answer or a composed view of an atom without forcing the operator to read raw frontmatter and the whole materialized file. This use case is a direct test of whether deskops is really mounted over SLDB rather than merely coexisting beside it.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

#### Evidence

- `spec/artifacts/atom.yaml` models atoms with structured fields that should support partial retrieval.
- `.skills/sldb/SKILL.md` provides commands for field-level and document-level structured access.
- Current atom files under `desk/atoms/` remain the human-facing materialization that this use case tries to avoid reading by default.


---

### 08-risks/atom-hook-automation-can-be-powerful-but-opaque

---
id: atom-hook-automation-can-be-powerful-but-opaque
title: Hook automation can be powerful but opaque
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:diagnosis
- topic:risks
type: atom
description: Risk to control when activating automatic hooks.
---

### Hook automation can be powerful but opaque

#### Answer

Hook automation should not become an invisible side-effect machine. If hooks begin dispatching executors or creating commits automatically, deskops must also provide clear event logs, dry-run inspection, condition visibility, and evidence capture so operators can understand why automation fired and what it changed.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`

#### Evidence

- `_auto_commit_task_closure()` in `deskops/operations.py` shows how impactful automatic workflow side effects can already be.
- `docs/diagrams/process/llm-tasks-vs-automatic-routines.md` says automatic routines should block or return work rather than invent semantic decisions.
- `/home/jp/.pi/agent/agents/deskops-supervisor.md` emphasizes evidence review and truthful routing, which opaque automation could undermine.


---

### 08-risks/atom-over-atomized-tasks-can-fragment-coherent-work

---
id: atom-over-atomized-tasks-can-fragment-coherent-work
title: Over-atomized tasks can fragment coherent work
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:diagnosis
- topic:risks
type: atom
description: Risk to control when making tasks more execution-oriented.
---

### Over-atomized tasks can fragment coherent work

#### Answer

Task atomization should reduce improvisation, not destroy coherent deliverables. If execution plans become too granular or too rigid, the workflow may fragment one meaningful change into excessive micro-actions that are expensive to author, review, and maintain.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `AGENTS.md` and `desk/rituals/execution.md` both insist on one coherent deliverable per task.
- `desk/atoms/workflow-model/atom-task-board-phases.md` and related workflow atoms frame tasks as atomic but still meaningful execution units.
- This sets a boundary against turning execution plans into excessive micro-fragmentation.


---

### 09-advancement-criteria/atom-criterion-deskops-uses-sldb-as-primary-read-path

---
id: atom-criterion-deskops-uses-sldb-as-primary-read-path
title: Deskops uses SLDB as its primary read path
five_wh_one_plus: done_when
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:criteria
type: atom
description: Advancement criterion for this diagnosis line.
---

### Deskops uses SLDB as its primary read path

#### Answer

This diagnosis line starts to resolve when deskops can serve common reads of atoms, tasks, and materializations through SLDB-backed queries and compositions by default, while raw Markdown reads become an exception instead of the main operational habit.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

#### Evidence

- `README.md` and `.skills/sldb/SKILL.md` describe the target architecture this criterion is measuring against.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` records the current hybrid state, which gives a baseline for improvement.
- Future deskops compose operations and reduced raw Markdown dependency would provide the direct evidence that this criterion is being met.


---

### 10-workspace-health/atom-dirty-worktree-and-stale-board-state-come-from-mixed-lanes-and-diverged-truth-surfaces

---
id: atom-dirty-worktree-and-stale-board-state-come-from-mixed-lanes-and-diverged-truth-surfaces
title: Dirty worktree and stale board state come from mixed lanes and diverged truth surfaces
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
- topic:drift
- topic:routing
type: atom
description: Diagnosis of why dirty git state and stale board/task routing accumulated together.
---

### Dirty worktree and stale board state come from mixed lanes and diverged truth surfaces

#### Answer

The dirty git state accumulated because execution stopped respecting single-lane cleanup boundaries. The evidence bundle shows multiple unrelated strands living in the same worktree at once: active `doctor` implementation work, bulk atom/template mutation residue, operational agent/tooling additions, diagnosis drafting, inbox intake, run artifacts, and generated scratch files. That mix left unreverted or generated residue in place, so later work started on top of an already-dirty tree instead of first isolating or cleaning the earlier lane.

The stale board and task state accumulated because deskops currently lets several sources of truth drift independently: board frontmatter routing, board prose notes, task-file frontmatter such as `status`, task runtime state such as `current_node`, and the actual commit history. The evidence bundle shows all of those disagreeing at once. `desk/tasks/Board.md` routes one set of task files in frontmatter, its prose notes still advertise additional `[active]` work, some task files still read as `status: active` even when `current_node: complete`, and git history already contains commits that look like closeout points for some of those surfaces. `deskops list tasks` makes that drift more visible because it currently scans `desk/tasks/task-*.md` directly rather than only the board-routed task set, so any lingering task file can still appear active even when board routing and commit history say something else.

This is not only a documentation inconsistency. It is a workflow failure mode that sits directly between desk health and recovery, drift review, task lifecycle execution, and the eventual operator manual/routing contract. Until those tasks define one authoritative routing and cleanup model, the repo can keep recreating dirty worktrees and stale board state even after individual fixes land.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

#### Evidence

- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/git-status.txt` — shows a mixed dirty worktree with tracked modifications plus untracked agent/tooling, diagnosis, inbox, and run-evidence residue.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/git-triage-report.md` — groups the dirt into multiple unrelated execution lanes and calls out unreverted/generated residue plus incomplete cleanup boundaries.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/cleanup-result-summary.md` — shows that even after targeted cleanup, the remaining tree still had several separate lanes, proving the cleanup contract was only partial.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/board.txt` — shows divergence between board frontmatter task routing and prose notes, including prose-only active items.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/list-tasks.txt` — shows `deskops list tasks` reporting `task-enrich-templates-with-instructional-text | active | complete`, which is not a board-routed active task.
- `deskops/operations.py` — `list_tasks` iterates `desk/tasks/task-*.md`, so file presence currently drives task listing more than board routing does.
- `desk/tasks/task-enrich-templates-with-instructional-text.md` — still says `status: active` while `current_node: complete`, showing task-file state can remain stale on its own.
- `desk/tasks/Board.md` and the commit history summarized in `git-triage-report.md` — show that board prose, routed task references, and landed closeout-style commits can tell different stories at the same time.


---

### 10-workspace-health/atom-legacy-and-versioned-desk-state-remain-fragile

---
id: atom-legacy-and-versioned-desk-state-remain-fragile
title: Legacy and versioned desk state remain fragile
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
type: atom
description: Diagnosis of why desk recovery and migration work keeps appearing.
---

### Legacy and versioned desk state remain fragile

#### Answer

Desk state remains fragile because the project still depends on conventions that can drift across modeled docs, runtime files, legacy layouts, and version expectations. Without a stronger workspace contract and explicit recovery surface, deskops cannot reliably distinguish healthy desks, fresh desks, stale desks, and incompatible desks.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md`
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md`
- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`

#### Evidence

- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md` — scope includes malformed current surfaces and migration/adoption paths.
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md` — scope includes explicit desk format and workflow expectation versions.
- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md` — scope includes stale runtime state and invalid desk documents.


---

### 10-workspace-health/atom-workspace-health-and-recovery-need-explicit-diagnosis

---
id: atom-workspace-health-and-recovery-need-explicit-diagnosis
title: Workspace health and recovery need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
type: atom
description: Summary diagnosis for workspace health, recovery, and migration concerns.
---

### Workspace health and recovery need explicit diagnosis

#### Answer

The active board already treats desk health, recovery, legacy migration, and per-project version/config contracts as important work, but the diagnosis tree does not yet capture them as a first-class architectural problem family. That leaves a gap between implementation pressure and explicit understanding of why workspace state remains fragile.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`
- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md`
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md`

#### Evidence

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md` — targets broken desk states, invalid modeled documents, and stale runtime files.
- `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md` — targets incompatible and hand-rolled desk layouts.
- `desk/tasks/task-add-per-project-desk-config-and-version-contract.md` — targets explicit version/config contracts for safe per-project behavior.


---

### 11-cross-desk-identity/atom-cross-desk-identity-and-transport-need-explicit-diagnosis

---
id: atom-cross-desk-identity-and-transport-need-explicit-diagnosis
title: Cross-desk identity and transport need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:cross-desk
type: atom
description: Summary diagnosis for horizontal desk identity and inbox transport gaps.
---

### Cross-desk identity and transport need explicit diagnosis

#### Answer

The active board already treats cross-repo identity resolution and inbox delivery as core workflow concerns, but the current diagnosis tree does not isolate them as their own architectural problem family. This hides how much multi-repo workflow reliability depends on canonical identity and verifiable transport behavior.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md`
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md`

#### Evidence

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md` — focuses on reliable self and sibling desk discovery.
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md` — focuses on sender, target, delivery result, and follow-up path.
- `desk/drawer/issues/issue-establish-canonical-repository-identity-through-sldb.md` — records the underlying repository identity ambiguity.


---

### 11-cross-desk-identity/atom-horizontal-operations-need-canonical-identity-and-verifiable-transport

---
id: atom-horizontal-operations-need-canonical-identity-and-verifiable-transport
title: Horizontal operations need canonical identity and verifiable transport
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:cross-desk
type: atom
description: Diagnosis of why cross-desk workflow remains unreliable.
---

### Horizontal operations need canonical identity and verifiable transport

#### Answer

Cross-desk workflow remains unreliable when desk identity can be inferred ambiguously and inbox delivery behaves like a write-only drop rather than a verifiable transport. Canonical identity and explicit delivery semantics are prerequisites for treating multi-repo workflow as an operational surface instead of a best-effort convention.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md`
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md`

#### Evidence

- `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md` — requires reliable answers to “who am I?” and “where is that repo's desk?”.
- `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md` — requires sender/target identity and recipient follow-up semantics.
- `desk/drawer/issues/issue-fix-inbox-sender-project-resolution.md` — captures a concrete sender-identity failure mode.


---

### 12-cli-surface/atom-cli-surface-and-scriptability-need-explicit-diagnosis

---
id: atom-cli-surface-and-scriptability-need-explicit-diagnosis
title: CLI surface and scriptability need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:cli-surface
type: atom
description: Summary diagnosis for CLI grammar and machine-readable output gaps.
---

### CLI surface and scriptability need explicit diagnosis

#### Answer

The active board already treats command grammar and JSON output as active work, which shows the current CLI surface is not yet fully aligned with spoken workflow language or machine-composable usage. The diagnosis tree should capture this as its own problem family rather than only as a side effect of other architectural concerns.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-design-operational-cli-grammar.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`

#### Evidence

- `desk/tasks/task-design-operational-cli-grammar.md` — targets a clearer workflow-oriented command language.
- `desk/tasks/task-add-json-output-for-modeled-documents.md` — targets scriptable output for modeled surfaces.
- `docs/faq.md` and `README.md` — already spend significant effort explaining command usage and boundaries.


---

### 12-cli-surface/atom-current-cli-still-exposes-internal-structure-too-directly

---
id: atom-current-cli-still-exposes-internal-structure-too-directly
title: Current CLI still exposes internal structure too directly
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:cli-surface
type: atom
description: Diagnosis of why CLI simplification and output shaping remain active work.
---

### Current CLI still exposes internal structure too directly

#### Answer

The current CLI still reflects internal artifact and implementation structure more directly than an operator-facing workflow language should. That makes both human use and machine composition harder than necessary, and it increases the amount of explanatory documentation needed around command behavior.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-design-operational-cli-grammar.md`
- `desk/tasks/task-add-json-output-for-modeled-documents.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`

#### Evidence

- `desk/tasks/task-design-operational-cli-grammar.md` — explicitly aims to align commands with spoken workflow nouns and user intent.
- `desk/tasks/task-add-json-output-for-modeled-documents.md` — explicitly aims to make list/show surfaces scriptable.
- `desk/drawer/issues/issue-make-deskops-easy-to-use.md` — notes that the model is powerful but concept-heavy for first use.


---

### 13-atom-mutation-provenance/atom-atom-mutation-and-provenance-need-explicit-diagnosis

---
id: atom-atom-mutation-and-provenance-need-explicit-diagnosis
title: Atom mutation and provenance need explicit diagnosis
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:atom-lifecycle
type: atom
description: Summary diagnosis for atom lifecycle mutation and provenance concerns.
---

### Atom mutation and provenance need explicit diagnosis

#### Answer

The active board already treats atom lifecycle operations, closeout knowledge gates, and pill graduation as first-class work, but the diagnosis tree does not yet isolate durable-knowledge mutation as its own problem family. That leaves atom evolution pressure under-described even though it strongly shapes closeout and workflow trustworthiness.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-atom-lifecycle-operations.md`
- `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `desk/tasks/task-define-atom-lifecycle-operations.md` — scope includes create, validate, split, merge, delete, and traceability operations.
- `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md` — scope includes atom updates from durable pill residue.
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md` — scope includes atom/materialization links and closeout evidence.


---

### 13-atom-mutation-provenance/atom-durable-knowledge-mutation-needs-safer-provenance-contracts

---
id: atom-durable-knowledge-mutation-needs-safer-provenance-contracts
title: Durable knowledge mutation needs safer provenance contracts
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:atom-lifecycle
type: atom
description: Diagnosis of why atom lifecycle and knowledge closeout still need deeper contracts.
---

### Durable knowledge mutation needs safer provenance contracts

#### Answer

Durable knowledge mutation needs safer provenance contracts because atoms are not static notes: they are created, split, merged, linked to materializations, and updated from workflow discoveries. Without stronger mutation and provenance rules, closeout cannot reliably prove that durable knowledge changed safely rather than merely changed somehow.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-define-atom-lifecycle-operations.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`
- `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md`

#### Evidence

- `desk/tasks/task-define-atom-lifecycle-operations.md` — includes split/merge/delete rules and relation to provenance.
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md` — requires knowledge-surface checks before work leaves the active desk.
- `desk/drawer/issues/issue-atom-validation-and-traceability.md` — identifies missing project-level validation and composed-usage traceability.


---

### 14-drift/atom-drift-needs-its-own-diagnosis-line

---
id: atom-drift-needs-its-own-diagnosis-line
title: Drift needs its own diagnosis line
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:drift
type: atom
description: Summary diagnosis for drift as a first-class workflow problem.
---

### Drift needs its own diagnosis line

#### Answer

The active board already treats drift review as explicit work, but the current diagnosis tree only mentions drift as a symptom of weak semantic access. Drift should be diagnosed as its own first-class workflow problem because it spans atoms, materializations, graphs, tests, diagrams, and implementation surfaces at once.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `desk/tasks/task-add-drift-check-review-loop.md` — directly targets review-only comparison across atoms, materializations, graph links, tests, diagrams, and implementation surfaces.
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md` — requires knowledge-surface checks during closeout.
- `desk/drawer/issues/issue-add-knowledge-drift-check-routine.md` — frames drift checks as a missing routine/checklist concern.


---

### 14-drift/atom-multi-surface-drift-is-a-core-workflow-failure-mode

---
id: atom-multi-surface-drift-is-a-core-workflow-failure-mode
title: Multi-surface drift is a core workflow failure mode
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:drift
type: atom
description: Diagnosis of why drift deserves direct workflow treatment.
---

### Multi-surface drift is a core workflow failure mode

#### Answer

Multi-surface drift is a core workflow failure mode because deskops intentionally spreads truth across structured knowledge, materializations, operational docs, tests, graphs, and implementation. If those surfaces evolve out of sync, the workflow starts lying about itself even when each individual file still looks locally reasonable.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- `desk/tasks/task-add-drift-check-review-loop.md` — defines the cross-surface comparison target directly.
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md` — tries to consolidate a methodology that is otherwise spread across many surfaces.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` — shows the breadth of surfaces involved in the current workflow.


---

### 15-core-realignment/atom-deskops-absorbed-missing-composition-and-runtime-layers

---
id: atom-deskops-absorbed-missing-composition-and-runtime-layers
title: Deskops absorbed missing composition and runtime layers
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:core-realignment
type: atom
description: Diagnosis of why deskops has been mutating beyond its original workflow-doc role.
---

### Deskops absorbed missing composition and runtime layers

#### Answer

Deskops has been mutating beyond a workflow-document layer because it has had to absorb two missing capabilities at once: a stronger composition layer over structured knowledge and a stronger runtime layer for execution orchestration. As those missing layers failed to crystallize elsewhere, deskops became the place where knowledge operations, composition pressure, and workflow runtime concerns converged.

#### Related tasks (as of 2026-08, not live references)

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

#### Evidence

- Active tasks already mix materialization contracts, task lifecycle runtime, closeout automation, and knowledge-surface checks.
- `docs/diagrams/process/current-agent-workflow-and-automation.md` shows deskops spanning discovery, composition-like reads, runtime progression, and automatic closeout behavior.
- The diagnosis tree itself now spans SLDB usage, hook runtime, task execution composition, drift, provenance, and cross-desk transport, showing how much has accumulated in deskops.


---

### 15-core-realignment/atom-hum-needs-a-wiki-native-knowledge-runtime-not-only-chat-context

---
id: atom-hum-needs-a-wiki-native-knowledge-runtime-not-only-chat-context
title: HUM needs a wiki native knowledge runtime not only chat context
five_wh_one_plus: for_whom
tags:
- system:hum
- system:deskops
- topic:diagnosis
- topic:core-realignment
type: atom
description: Diagnosis connecting the stack redesign to the original hum or wikipu direction.
---

### HUM needs a wiki native knowledge runtime not only chat context

#### Answer

If HUM is meant to be an autopoietic agent operating through persistent knowledge surfaces rather than transient chat turns alone, then the stack needs a wiki-native knowledge runtime with composable nuclei, durable views, and execution surfaces grounded in persistent structure. That requirement pushes the architecture beyond simple markdown workflow docs and toward a more explicit separation between knowledge substrate, composition, and orchestration.

#### Evidence

- Project discussion in this session explicitly reconnects the current architecture drift to the earlier HUM or Wikipu direction.
- The existing deskops workflow already depends heavily on persistent knowledge surfaces such as atoms, pills, tasks, rituals, diagnosis trees, and materializations.
- `.agents/skills/*` and `runs/subagents/` show that agent operation here is already structured around persistent repo state more than around free chat memory.


---

### 15-core-realignment/atom-kgdb-never-realized-the-knowledge-nuclei-layer

---
id: atom-kgdb-never-realized-the-knowledge-nuclei-layer
title: KGDB never realized the knowledge nuclei layer
five_wh_one_plus: what
tags:
- system:kgdb
- system:deskops
- topic:diagnosis
- topic:core-realignment
type: atom
description: Diagnosis of the missing compositional knowledge layer originally associated with KGDB.
---

### KGDB never realized the knowledge nuclei layer

#### Answer

KGDB did not become the active layer that identifies knowledge nuclei across code and documents and composes them into a navigable semantic structure. Because that layer never fully materialized, composition, provenance, and cross-surface semantic linkage have been reappearing indirectly inside atoms, diagrams, issues, tasks, and deskops runtime design.

#### Evidence

- `AGENTS.md` in this repo routes `use-kgdb` for graph contracts and runtime validation, but active board work shows almost no KGDB-centered execution path today.
- `desk/drawer/issues/issue-integrate-kgdb-for-desk-source-knowledge-graph.md` — frames KGDB integration as still-missing work.
- The diagnosis tree under `desk/drawer/issues/diagnosis/` now carries many composition/provenance concerns that a realized knowledge-nuclei layer might have absorbed more centrally.


---

### 15-core-realignment/atom-sldb-became-more-format-standardizer-than-document-ast-runtime

---
id: atom-sldb-became-more-format-standardizer-than-document-ast-runtime
title: SLDB became more format standardizer than document AST runtime
five_wh_one_plus: what
tags:
- system:sldb
- system:deskops
- topic:diagnosis
- topic:core-realignment
type: atom
description: Diagnosis of how SLDB evolved relative to its stronger AST-oriented ambition.
---

### SLDB became more format standardizer than document AST runtime

#### Answer

SLDB currently provides strong value as a structured Markdown contract, store, field, and query layer, but it has not yet become a broadly used document AST runtime that deskops can treat as its normal operational substrate. This gap matters because composition, structural editing, and semantically precise document access were expected to be deeper than frontmatter extraction and document normalization alone.

#### Evidence

- `README.md` — defines SLDB as the structured document infrastructure beneath deskops.
- `.skills/sldb/SKILL.md` — emphasizes fields, tracked docs, queries, and structured operations, but current repo usage still falls back frequently to file-level operational behavior.
- `desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md` — explicitly references AST-driven templates and markdown hooks as upstream missing capabilities.


---

### 15-core-realignment/atom-the-stack-needs-a-new-core-boundary

---
id: atom-the-stack-needs-a-new-core-boundary
title: The stack needs a new core boundary
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- system:kgdb
- system:hum
- topic:diagnosis
- topic:core-realignment
type: atom
description: Expected direction for reordering the current stack around its real emerging responsibilities.
---

### The stack needs a new core boundary

#### Answer

The current stack likely needs a new boundary that distinguishes at least four layers: document infrastructure, knowledge nuclei and composition, workflow or execution orchestration, and agent interface or cognition. Without that realignment, deskops will continue to accumulate responsibilities that conceptually belong to a stronger document AST layer, a stronger knowledge graph or composition layer, or a HUM-facing persistent knowledge runtime.

#### Evidence

- `README.md` still describes deskops mainly as a workflow-domain instance built on top of SLDB.
- The active board and diagnosis tree now cover concerns that go beyond a narrow workflow-domain layer: composition, provenance, runtime automation, drift, and cross-surface orchestration.
- `desk/drawer/issues/issue-integrate-kgdb-for-desk-source-knowledge-graph.md` and `issue-refactor-primitives-to-ast-driven-task-nodes.md` point to missing layers beneath the current deskops pressure.


---

### diagnosis/TASK_TRACEABILITY

### Task traceability for diagnosis tree

This note maps the diagnosis atoms under `desk/drawer/issues/diagnosis/` back to active tasks and identifies task themes that still suggest missing diagnosis coverage.

#### Diagnosis atoms supported by active tasks

| Diagnosis atom | Related active tasks |
|---|---|
| `atom-diagnosis-deskops-subutilizes-sldb` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-define-materialization-contract-slice-deskops-surface`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-reading-atoms-through-markdown-bypasses-sldb-composition` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-drift-check-review-loop` |
| `atom-deskops-still-operates-too-directly-on-files` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-define-materialization-contract-slice-deskops-surface`, `task-design-operational-cli-grammar` |
| `atom-hooks-are-modeled-but-not-a-general-runtime` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates` |
| `atom-tasks-are-not-yet-atomized-to-execution-actions` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-frontmatter-becomes-reading-noise-when-sldb-is-underused` | `task-define-materialization-contract-slice-deskops-surface`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-documentation-growth-compensates-for-weak-semantic-access` | `task-write-end-to-end-deskops-operator-manual`, `task-add-drift-check-review-loop`, `task-design-operational-cli-grammar` |
| `atom-deskops-should-read-through-sldb-compositions` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents` |
| `atom-materializations-are-projections-not-primary-read-surfaces` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-drift-check-review-loop`, `task-wire-closeout-to-knowledge-gates` |
| `atom-tasks-should-compile-to-execution-compositions` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-gap-between-current-file-reading-and-composed-reading` | `task-define-materialization-contract-slice-deskops-surface`, `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-add-drift-check-review-loop` |
| `atom-workline-introduce-deskops-compose-operations` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents`, `task-design-operational-cli-grammar` |
| `atom-workline-activate-a-general-hook-runtime` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates`, `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout` |
| `atom-workline-add-execution-plan-to-task-model` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-use-case-read-atom-without-reading-full-markdown` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents` |
| `atom-use-case-auto-dispatch-executor-on-execution-ready` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates` |
| `atom-hook-automation-can-be-powerful-but-opaque` | `task-wire-closeout-to-knowledge-gates`, `task-make-task-lifecycle-runnable-from-intake-to-closeout` |
| `atom-over-atomized-tasks-can-fragment-coherent-work` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-criterion-deskops-uses-sldb-as-primary-read-path` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents`, `task-design-operational-cli-grammar` |

#### Active tasks that suggest diagnosis themes not yet captured in this tree

These active tasks point to additional diagnosis lines that are either missing or only weakly implied by the current diagnosis atoms.

##### 1. Desk health, recovery, and migration surfaces

Related tasks:

- `task-add-desk-health-and-recovery-surface-deskops-slice`
- `task-detect-and-migrate-legacy-desk-workspaces`
- `task-add-per-project-desk-config-and-version-contract`

Likely missing diagnosis themes:

- deskops lacks a strong diagnosis model for workspace health and recoverability
- the current workspace contract is still fragile across legacy desks, stale runtime state, and mixed-version surfaces
- per-project desk identity/config/version rules are not yet explicit enough to support safe recovery and migration

##### 2. Cross-desk identity and transport diagnosis

Related tasks:

- `task-establish-horizontal-desk-discovery-and-canonical-identity`
- `task-make-cross-desk-inbox-delivery-verifiable-and-actionable`

Likely missing diagnosis themes:

- horizontal desk identity is not yet canonical enough for reliable cross-repo operations
- cross-desk delivery and acknowledgment are not yet modeled as a trustworthy operational transport
- deskops still lacks a clean diagnosis subtree for multi-repo coordination contracts

##### 3. CLI surface and scriptability diagnosis

Related tasks:

- `task-design-operational-cli-grammar`
- `task-add-json-output-for-modeled-documents`

Likely missing diagnosis themes:

- the current CLI surface still exposes internal architecture too directly instead of a spoken workflow language
- modeled document output is not yet shaped enough for scriptable and composable machine use
- compose/query-first deskops usage may require a broader diagnosis about command surface design, not only about SLDB reading path

##### 4. Atom lifecycle and provenance diagnosis beyond reading path

Related tasks:

- `task-define-atom-lifecycle-operations`
- `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout`
- `task-wire-closeout-to-knowledge-gates`

Likely missing diagnosis themes:

- atom lifecycle operations still need a more explicit diagnosis around provenance preservation, mutation safety, and reversible atom evolution
- closeout knowledge gates imply a broader diagnosis about how durable knowledge mutates under workflow pressure, not just how it is read

##### 5. Drift review as its own diagnosis line

Related tasks:

- `task-add-drift-check-review-loop`

Likely missing diagnosis themes:

- the system lacks a unified diagnosis of multi-surface drift across atoms, materializations, tests, diagrams, and implementation
- drift is currently present in the tree as a symptom, but not yet as a first-class diagnosis/workline cluster

#### Interpretation

The current diagnosis tree explains the SLDB-composition, hook-runtime, and execution-composition direction fairly well. But the active board also suggests at least five additional diagnosis families:

1. workspace health and migration
2. cross-desk identity and transport
3. CLI grammar and machine-readable output
4. atom lifecycle mutation and provenance
5. drift detection and reconciliation

Those can either become new diagnosis subtrees or be attached to the current tree through additional atoms if this issue is meant to stay broader.

#### Follow-up status

These missing diagnosis families have now been scaffolded under:

- `10-workspace-health/`
- `11-cross-desk-identity/`
- `12-cli-surface/`
- `13-atom-mutation-provenance/`
- `14-drift/`
