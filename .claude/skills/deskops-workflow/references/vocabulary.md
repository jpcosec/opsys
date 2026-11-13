# deskops + spec2viz vocabulary

Precise definitions for the nouns these tools use. Consult this when a command's *purpose*, not
just its flags, is unclear — for example, before deciding whether something belongs in a pill or
an atom, or whether a diagram spec or its rendered output is the thing to edit.

## Layering

- **sldb** owns structured-Markdown infrastructure in general: modeled document contracts,
  reversible templates, field-level query/update/append/clean/create/remove, section ownership,
  semantic + physical search, store integrity. It has no opinion on workflow or diagrams.
- **deskops** is the workflow-domain instance built on sldb: tasks, routines, pills, atoms,
  drawer, board, rituals, hooks. It owns *what work is happening and why*.
- **spec2viz** is the diagram-domain mirror of the same idea: a diagram's YAML spec plus its
  contract compiles to a rendered visual artifact, exactly as an sldb model plus a template
  compiles to a Markdown document. It owns *what things look like*.

Both exist to keep a human-facing surface (a Markdown doc, a rendered diagram) from drifting
silently away from its structured source. The fix for a wrong output is always upstream: the
model/field for docs, the YAML spec/renderer for diagrams — never the generated file itself.

## Tasks, routines, phases, board

- A **task** (`desk/tasks/task-*.md`) is one unit of routed work: title, goal, scope,
  implementation path, done-when rule, validation command(s), optional dependencies and bound
  atoms/pills.
- A **routine** is the directed graph of checklists, operators, conditions, and edges that gates a
  task's progress. `deskops advance task` walks the task through this graph; it is the only
  supported way to change a task's runtime status.
- A **phase** is *not* a standalone document — it is a horizontal dependency layer of the task
  graph inside the board: tasks whose prerequisites are already satisfied and whose planned
  changes do not operationally overlap, so they can run in parallel. Phases have execution
  meaning, not business meaning.
- The **board** (`desk/tasks/Board.md`) routes active work; it is the entry point for "what should
  happen next," ahead of inventing new scope.

## Drawer, inbox, promotion

- The **inbox** is coordination intake: external needs, unclear requests, suggestions
  (`deskops inbox`). It routes toward work; it is not itself work.
- The **drawer** (`desk/drawer/`) holds future, uncertain, or loosely shaped work — features,
  issues, questions — that is deliberately *not* active. It only becomes active execution when
  explicitly authored as a routed task: there is no drawer-to-task promotion, because the drawer
  is loose and a task is a compiled, fully authored bundle. Write the task with
  `deskops add task --from-drawer <selector> ...`, which records the drawer file in the task's
  `from_drawer` field.
  Treat anything still in inbox/drawer as not-yet-authorized to implement.

## Pills vs. atoms

- A **pill** is transient, task- or phase-bound context: not-yet-incorporated knowledge needed to
  execute a specific bugfix/feature/migration correctly, or a pointer to already-settled
  atoms/code/docs/specs. A pill can be reused across several tasks as long as it stays atomic and
  applicable, and is attached explicitly with `deskops bind pill`.
- An **atom** is the stable documentation core: one durable answer to exactly one 5W1H question
  (what/why/how/how_not/when/where/for_whom), tagged with namespaced semantic tags
  (`system:x`, `topic:y`). Every durable doc, spec rationale, README section, or diagram
  explanation should either be an atom or a human-facing *materialization* of selected atoms.
- The lifecycle rule: once a pill's knowledge stabilizes and should outlive its task, it must be
  distilled into an atom (`deskops add atom`) so future specs/code/docs can comply with the
  durable ruling instead of depending on an old, task-scoped pill. A pill that never stabilizes
  and never gets used again should be deleted, not left indefinitely.

## Specs, diagrams, catalogs

- A **diagram spec** is a semantic YAML file (sequence, state, component, activity, deployment,
  matrix, or ast) validated against Pydantic models, then compiled to a renderer-agnostic IR
  before rendering. It is the source of truth.
- A **rendered diagram** (`.mmd`, `.puml`, `.svg`, Vega JSON, D2, `antonia-html`) is a projection
  of that spec through one renderer. If a rendered diagram is wrong, the fix is the spec (if the
  structure is wrong) or the renderer (if the spec is right but the output is malformed) — never
  a hand-patch of the rendered file, since the next render would silently discard the patch.
- A **catalog** aggregates many diagram specs (via a legacy `vistas.yml` registry or a
  hierarchical `diagram-store` config that can nest other stores) into one filterable HTML bundle,
  optionally cross-linked to atoms via `--atoms-dir`.
- Diagrams double as a **design surface**: their sections and labeled edges reveal candidate
  atoms, document references, routines, hooks, tests, and CLI nouns — read them for that signal
  rather than only for final output.

## Closeout discipline

A code change is not done when it merely works. Closeout means: validation command passed, bound
pills/guardrails satisfied, stale task/context docs updated or removed, the task removed from
`Board.md` once complete, and one coherent commit made (`deskops closeout commit` when a run-dir
exists, otherwise a descriptive plain commit). Skipping straight from "tests pass" to "next task"
without this reconciliation is how boards and atoms drift from reality.
