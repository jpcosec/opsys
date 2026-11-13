# deskops CLI reference

Captured from `deskops --help` and per-subcommand `--help`. Run `deskops <command> --help` (or
`deskops <command> <subcommand> --help`) to confirm current flags before relying on this file —
the CLI evolves.

Top-level: `deskops {about,doctor,status,faq,bootstrap,init,inbox,promote,add,edit,bind,next,list,show,advance,repo,desk,atoms,graph,drift,materialize,closeout}`

Most subcommands take `--root <path>` to target a repository other than the current directory.
Selectors (task ids, pill ids, atom ids, etc.) accept an exact id, filename, stem, or unique slug
fragment.

## Setup

- `deskops bootstrap` — install/repair the sibling `sldb` checkout, create `~/.sldb`, register
  deskops models in the global store. Run once per machine.
- `deskops init .` — ensure bootstrap prerequisites, create a local `.sldb/` store, scaffold
  `desk/` if missing. Run once per repo.
- `deskops desk install .` — scaffold a minimal `desk/` without touching the local store.
- `deskops repo register` — canonically register a repository in the ecosystem registry and track
  it in SLDB.
- `deskops repo context` — manage repository contexts.

## Orientation

- `deskops about` — short overview and first-use commands.
- `deskops status --root .` — current workspace/workflow status.
- `deskops faq` — browse the first-use FAQ by question.
- `deskops doctor --root . [--repair]` — detect (and optionally non-destructively repair) broken
  desk states.
- `deskops drift check --root .` — detect drift between atoms and their materializations.
- `deskops graph missing --root . [--graph <path>]` — report missing graph targets / dangling
  declared references.
- `deskops graph neighbors` — incoming/outgoing neighbors for one graph node.
- `deskops graph trace` — trace a graph node to its root sources.
- `deskops graph reflect --root . [--graph <path>]` — write review-only self-reflection findings
  for a graph snapshot.
- `deskops graph build` — build the KGDB graph snapshot runtime artifact.

## Inbox and drawer promotion

- `deskops inbox "<message>" --kind {unclear,suggestion} --title "<title>" --root .` — log a note.
- `deskops inbox --list --root .` / `deskops inbox --show <selector> --root .` — list/show notes.
- `deskops promote inbox-to-drawer-task <selector> --root . [--title ...]` — promote an inbox note
  into a deferred drawer task candidate.
- There is no drawer-to-task promotion. A drawer item becomes a task only by authoring it with
  `deskops add task --from-drawer <selector> ...` (see below); the drawer file is kept and cleaned
  up by hand.

## Creating artifacts (`deskops add <kind> ...`)

Kinds: `task, condition, operator, checklist, hook, edge, routine, pill, ritual, board, atom,
repository, inbox-note, faq-doc, step`. Any kind accepts `--from-yaml <file>` or an inline JSON
payload instead of individual flags.

- `deskops add task --root . --title "..." --goal "..." --scope "..." \
  --implementation-path "..." --done-when "..." --validation "pytest" [more --validation ...] \
  [--why "..."] [--depends-on task-a task-b] [--task-type design|implementation|test|reflection|closeout] \
  [--inherits-from task-x] [--atom atom-id ...] [--inherit-acceptance-context] \
  [--from-drawer <drawer-path|stem|fragment>]`
  Creates the task, its routine, and primitive checklists/conditions/operators/edges, and adds a
  board entry. `--from-drawer` records the source drawer file in the task's `from_drawer` field
  (not in `references`, which `edit task` replaces wholesale); it does not copy content or delete
  the drawer file.
- `deskops add pill --root . --what "..." --why "..." --when "..." --where "..." --how "..." \
  --how-not "..." [--title "..."] [--summary "..."] [--tags namespace:value ...]`
  All six of `--what/--why/--when/--where/--how/--how-not` are required.
- `deskops add atom --root . --five-wh-one-plus {what,why,how,how_not,when,where,for_whom} \
  --answer "..." [--title "..."] [--tags namespace:value ...] [--provenance <url-or-path>]`
  One atom answers exactly one 5W1H question.
- Other kinds (`routine`, `ritual`, `board`, `repository`, `inbox-note`, `faq-doc`, `step`,
  `condition`, `operator`, `checklist`, `hook`, `edge`) follow the same `--root`/`--from-yaml`
  pattern; run `deskops add <kind> --help` for kind-specific flags before use.

## Editing one field (`deskops edit <kind> <selector> <field> <value> --root .`)

Kinds: `task, pill, ritual, board, atom, repository, inbox-note, faq-doc, step`. Values are parsed
through SLDB's field-value parser and the document is re-rendered from its model — this is the
correct way to change a single field without hand-editing Markdown.

Example: `deskops edit pill pill-keep-layers-clean how-not "Do not bypass the guardrail." --root .`

## Binding context

- `deskops bind pill <task-selector> <pill-selector> --root .` — updates the task's modeled
  `pills` list through the artifact layer.

## Listing and showing

- `deskops list {tasks,routines,conditions,operators,checklists,hooks,edges,pills,rituals,boards,
  atoms,repositories,inbox-notes,faq-docs,steps} --root .`
- `deskops show {task,routine,condition,operator,checklist,hook,edge,pill,ritual,board,atom,
  repository,inbox-note,faq-doc,step} <selector> --root .`
- `deskops atoms list --root . [--format text|json]`
- `deskops atoms show <selector> --root .`
- `deskops atoms new --root .` — interactive/guided atom creation.
- `deskops atoms validate <selector> --root .` — validate an atom's materializations.
- `deskops atoms add-namespace` — add an extensible atom tag namespace to
  `desk/atoms/tag-namespaces.yaml`.

## Advancing work

- `deskops advance task <selector> --root .` — walk a task through execution, testing, and
  closeout gates when its checklist conditions pass. This is the only supported way to move a
  task's runtime status.
- `deskops next [<selector>] --root . [--diagram]` — show the next valid workflow action for a
  task without mutating it; `--diagram` renders the workflow state machine as Mermaid from its
  source spec (useful for understanding the gate structure itself).

## Closeout

- `deskops materialize --root .` — materialize workflow artifacts (regenerate human-facing docs
  from atoms/models).
- `deskops closeout commit --root . --task <task-id> --run-dir runs/subagents/<dir> \
  [-m "<subject>"] [--paths path1 path2 ...] [--run-id <id>] [--session <session.jsonl>]`
  Creates the tool-made closing commit linked to run evidence; stamps Task-Id/Run-Dir/Run-Id/
  Session-Sha256 trailers and records the commit hash back into `runs/subagents/index.jsonl`.
  Prefer this over a bare `git commit` whenever a run-dir exists for the task.
- `deskops closeout {commit,supersede,retire,resolved-by,verify}` — pick the verb by why the task closes
  (run `deskops closeout <verb> --help`; never conclude a task "can't be closed" without checking all five):
  - `supersede --task <id> --reason "..." --ref <commit|path>` — the task was replaced or its subject no
    longer exists (work never done). Skips the evidence gates; makes one closing commit with
    Closeout-Mode: superseded and removes the task from the Board.
  - `resolved-by --task <id> ...` — the work already entered history; names an ancestor commit and a test.
  - `retire` — a task resolved before the ritual lifecycle.
  - `verify --task <id>` — check declared evidence without committing.
  `deskops retire <path>` (top-level) is for other desk documents (inbox notes, pills, steps…), not tasks.
