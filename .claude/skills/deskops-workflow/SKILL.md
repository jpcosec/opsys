---
name: deskops-workflow
description: This skill should be used when a repository has a top-level desk/ directory, or when the user asks to "add a task", "check the board", "advance a task", "create a pill", "create an atom", "promote from the drawer", "create or update a diagram spec", "render a diagram", "validate a spec", "build the architecture catalog", "agregar tarea", "revisar el board", "avanzar tarea", "crear un pill", "crear un atom", "promover del drawer", "renderizar diagrama", "validar spec", or otherwise mentions deskops, spec2viz, sldb, desk/, atoms, pills, routines, the desk board, or a diagram/spec YAML source. It forces use of the `deskops` and `spec2viz` CLIs instead of hand-editing desk/ files or generated diagram outputs, and enforces following the spec -> atoms|diagrams -> tasks|pills -> code|documental-projection pipeline instead of ad hoc workflow habits.
---

# deskops + spec2viz Workflow

> Where this skill lives: the deskops repo (`jpcosec/opsys`), `.claude/skills/deskops-workflow/`.
> `~/.claude/skills/deskops-workflow` is a symlink to that folder. Edit it in the repo and commit it there;
> see the deskops README, «Pi/project agent guidance».

`deskops` and `spec2viz` are CLI-driven layers for structured project workflow and structured
diagrams. `deskops` sits on top of `sldb` (structured-Markdown document infrastructure) and owns
tasks, routines, pills, atoms, drawer, and board. `spec2viz` owns diagrams the same way: a YAML
spec is the source of truth, and every rendered Mermaid/PlantUML/Vega/D2/HTML file is a generated
projection of it. Both CLIs are on PATH as `deskops` and `spec2viz` — always run `--help` on an
unfamiliar subcommand instead of guessing flags.

## The pipeline this skill enforces

Work in a deskops-managed repo flows through one pipeline. Do not skip stages or substitute a
hand-written file for a stage's generated artifact:

1. **Spec** — a structured YAML source (a deskops artifact spec or a spec2viz diagram spec).
   This is where intent and structure get declared first.
2. **Atoms | Diagrams** — durable knowledge units (`deskops atoms ...`) and rendered diagrams
   (`spec2viz diagram render` / `spec2viz catalog build`) derive from specs and decisions. Atoms
   answer exactly one 5W1H question each; diagrams are visual projections, never hand-authored
   Mermaid/PlantUML files maintained in parallel with a spec.
3. **Tasks | Pills** — routed, gated work (`deskops add task`, `deskops advance task`, the
   `desk/tasks/Board.md`) consumes atoms and diagrams as context. Pills (`deskops add pill`,
   `deskops bind pill`) carry transient, task/phase-bound knowledge needed to execute correctly.
4. **Code | Documental projection** — implementation closes with tests and a commit
   (`deskops closeout commit` when a run-dir exists). Generated docs/diagrams/materializations are
   projections of atoms and specs — if one is wrong, fix the atom/spec/renderer, never patch the
   generated file directly.

A pill that stabilizes into durable knowledge must graduate into an atom
(`deskops add atom`) instead of being left as a permanent pill. Work that is not yet ready to
execute belongs in the drawer or inbox. Inbox notes move into the drawer with
`deskops promote inbox-to-drawer-task`; a drawer item never becomes a task directly — the drawer is
loose by design and a task is a fully authored, compiled bundle. Author the task in full with
`deskops add task ... --from-drawer <selector>`, which records the drawer file in the task's own
`from_drawer` field and keeps it for manual cleanup. Never jump straight to code.

## Hard rules

- **Orient before acting.** At the start of any non-trivial work in a repo with `desk/`, run
  `deskops status --root .` and `deskops list tasks --root .` (or read `desk/tasks/Board.md`)
  before inventing a plan. Routed work already tracked there takes priority over ad hoc scope.
- **Never hand-write or hand-edit modeled `desk/` artifacts** (tasks, pills, atoms, routines,
  boards, inbox notes, repositories, faq-docs, steps, conditions, operators, checklists, hooks,
  edges, rituals). Create them with `deskops add <kind> ...` and change one field at a time with
  `deskops edit <kind> <selector> <field> <value> --root .`. If the CLI cannot express something
  needed, log it with `deskops inbox "<gap>" --kind unclear --root .` instead of bypassing the
  model with a raw file edit.
- **Never hand-edit a generated diagram.** `.mmd`, `.puml`, `.svg`, and generated `.html` catalog
  files are projections. Fix the YAML diagram spec (or the renderer, if the gap is systemic) and
  re-run `spec2viz diagram render` / `spec2viz catalog build`. Validate before rendering:
  `spec2viz diagram validate <spec.yml>`.
- **Advance tasks through the CLI, not by editing status fields.** Use
  `deskops advance task <selector> --root .` and check what is next with
  `deskops next <selector> --root .` rather than manually flipping a task's phase/status text.
- **Bind context explicitly.** Attach a pill to a task with `deskops bind pill <task> <pill> --root .`
  instead of referencing it only in prose. Bind atoms to a task via `--atom` on `deskops add task`
  or a follow-up edit, so the task's context is queryable, not implicit.
- **Promote deliberately, author tasks explicitly.** Move an inbox note into the drawer with
  `deskops promote inbox-to-drawer-task`. There is no drawer-to-task promotion: write the task
  yourself with `deskops add task --from-drawer <selector> --title ... --goal ... --scope ...
  --validation ...`, then remove the drawer item by hand once the task supersedes it. Do not
  silently start implementing something that only exists as an inbox note, a drawer item, or a
  chat request.
- **Close code changes with tests and a commit.** Run the task's validation command, then commit.
  If a `runs/subagents/<run-dir>` exists for the task, prefer
  `deskops closeout commit --root . --task <task> --run-dir <dir> ...` over a plain `git commit`,
  since it stamps the commit with task/run trailers deskops can trace later.
- **Check consistency instead of assuming it.** Use `deskops doctor --root .`,
  `deskops drift check --root .`, and `deskops graph missing --root .` when something looks
  inconsistent, before manually reconciling files by hand.
- **Desk-only changes go straight on the main checkout, never in a worktree** (JP, 2026-11-04).
  Creating a task, sending inbox notes, editing a field or committing a closeout is done with
  `deskops` in the repo's main checkout on its integration branch (e.g. `dev`): sync with the
  remote branch first, `git add` only the `desk/` files deskops touched (never `git add -A`: other
  sessions may have uncommitted work there), commit with `[skip ci]` and push. Worktrees are for code
  changes that go through a PR; a worktree just to document a task is ceremony.
- **Bootstrap once per machine, init once per repo.** If `deskops`/`sldb` or a local `.sldb/`
  store are missing, run `deskops bootstrap` then `deskops init .` — do not scaffold `desk/`
  by copying files from another repo.

## Quick command map

| Intent | Command |
|---|---|
| Orient in a repo | `deskops status --root .`, `deskops about` |
| See routed work | `deskops list tasks --root .`, `deskops show task <id> --root .` |
| Create a task | `deskops add task --root . --title ... --goal ... --scope ... --validation ...` |
| Advance a task | `deskops advance task <id> --root .` / `deskops next <id> --root .` |
| Create/bind a pill | `deskops add pill --root . --what ... --why ... --when ... --where ... --how ... --how-not ...` then `deskops bind pill <task> <pill> --root .` |
| Create an atom | `deskops add atom --root . --five-wh-one-plus <what\|why\|how\|how_not\|when\|where\|for_whom> --answer ...` |
| Promote / author work | `deskops promote inbox-to-drawer-task <selector> --root .`, then `deskops add task --root . --from-drawer <selector> --title ... --goal ... --scope ... --validation ...` (no drawer-to-task promotion) |
| Validate a diagram spec | `spec2viz diagram validate <spec.yml>` |
| Render a diagram | `spec2viz diagram render <spec.yml> --out <dir> [--renderer mermaid\|plantuml\|vega\|d2\|antonia-html\|json]` |
| Build a diagram catalog | `spec2viz catalog build --config <catalog.yml> --out <out.html>` |
| Close a task's code | run the task's validation, then `deskops closeout commit --root . --task <id> --run-dir <dir> ...` (or plain commit if no run-dir) |
| Check consistency | `deskops doctor --root .`, `deskops drift check --root .`, `deskops graph missing --root .` |

## Additional resources

- `references/deskops-cli.md` — full `deskops` subcommand reference (all `add`/`edit`/`list`/`show`
  kinds, `atoms`, `graph`, `promote`, `closeout`, `repo`, `desk`).
- `references/spec2viz-cli.md` — full `spec2viz` subcommand reference (`diagram`, `catalog`,
  renderers, schema export, legacy aliases).
- `references/vocabulary.md` — precise definitions of task/routine/phase/board, drawer/promotion,
  pill-vs-atom lifecycle, and the spec2viz mirror-of-sldb relationship, for when the mental model
  itself (not just a command) needs grounding.
