# Plan: deskops-pron — deskops rebuilt on pron

Status: **planning → implementation coordination**. This is the master plan for the
total refactor of deskops onto the pron library API, executed in the `deskops-pron`
worktree/branch. Fireproof test for pron; total refactoring for deskops.

## 0. Goal and non-negotiables

- **Only door**: every contact deskops has with sldb/kgdb goes through
  `pron.World` / `pron.World.store` / `pron.World.graph`. No `import sldb` or
  `import kgdb` outside the single seam module (`deskops/world.py`).
- **Carried over 1:1**: `deskops/models/*.py` (document models) — plus
  conservative improvements (§4).
- **Preserved**: the CLI verb surface (`about, doctor, status, faq, bootstrap,
  init, inbox, promote, add, edit, bind, next, list, show, advance, repo, desk,
  atoms, graph, materialize, drift, closeout, runtime`) — same verbs, same
  flags, same printed artifacts. `desk/` content, skills, and docs keep working.
- **Acceptance gate**: the 273 existing tests are the behavioral contract. All
  must pass against the pron-backed implementation. CLI checks:
  `python -m deskops --help`, `deskops faq`, `deskops graph build`,
  `deskops graph missing`, plus `World` semantic checks after each write lane.
- **Gap log**: every pron limitation found during the rewrite goes to
  `desk/pron-gap-log.md` (worktree) with a repro. This log is the deliverable
  that later feeds pron's inbox. Do NOT patch around gaps in deskops code.

## 1. Current state (measured)

- Worktree: `../deskops-pron` (branch `deskops-pron`, from main `529e990`).
- Uncommitted main-repo changes are derived store state only (`hash_b`,
  document indexes) — nothing carried; the store re-registers models via pron.
- deskops Python: 11,227 lines. Hot spots: `operations.py` (2,765),
  `cli/parser.py` (1,000), `graph/extract_coverage.py` (907), `workspace.py`
  (569).
- sldb/kgdb contact points today:
  - subprocess `python -m sldb`: `bootstrap.py`, `doctor.py`.
  - direct imports: `sldb.store.io`, `sldb.store.layout`, `sldb.store.ops`,
    `sldb.cli.*` (doc_helpers, model_utils, store_context),
    `sldb.runtime.validation`, `sldb.core.exceptions`
    (operations.py, identity.py, domain_tree.py, repo.py, promote.py,
    materializers/*).
  - kgdb: `kgdb.contracts.io.GraphSnapshot` (graph/snapshot.py),
    `kgdb.graph.load_graph/save_graph` (cli/main.py networkx projection).
- pron API available (`World(root, pythonpath)`): `store` = StructuralQuery +
  DocumentTracker + PayloadEditor + ModelEditor + ModelRegistry + LinkedStores
  (`find`, `list`, `get`, `glob`, `matches`, `doc(s)`, `payload`, `create`,
  `track`, `untrack`, `update_field`, `append`, `remove_field`, `replace`,
  `register_model`, `schema`, `model_catalog`, `update_index`); `graph` =
  persisted-graph reads without networkx; `refresh()`, `refresh_if_stale()`,
  `ensure_ready()`; `pron.client` (stdlib daemon client, optional).

## 2. Target architecture

```
deskops/
  world.py            NEW  ~40 lines. The ONLY seam. get_world(root) ->
                      pron.World(root, pythonpath="deskops.models").
                      Modules import World/Store/Graph from here, never from
                      sldb/kgdb.
  models/             CARRIED 1:1 (+ improvements §4). Registered through
                      World.store.register_model.
  repo_ops/           NEW  split of operations.py, one module per concern,
                      each small (see §3 lanes). All persistence via Store.
  cli/                KEPT  argparse surface 1:1 (parser.py verbs/flags
                      unchanged). Handlers delegate to repo_ops; thin main.
  workspace.py        REWRITTEN on Store (find/matches).
  identity.py         REWRITTEN on World (replaces sldb.cli.store_context).
  domain_tree.py      REWRITTEN on Store (model_catalog/model_names/schema).
  bootstrap.py        REWRITTEN on World.ensure_ready/refresh (no subprocess).
  materializers/      KEPT logic; payloads via Store; rendering via seam §5.
  graph/              KEPT  deskops-specific extractors + snapshot artifact
                      (own domain logic, minimal store contact). kgdb
                      contract validation of the deskops snapshot stays.
  runtime/, specs/,   KEPT; touched only where they hit sldb.
  workflow/
```

Explicit exceptions inside `deskops/world.py` only (gap-logged, one-line swap
when pron re-exports):
1. `sldb.runtime.validation.extract_model_data` / `render_model_markdown`
   — pron's own `docs_sync` imports these directly today; deskops mirrors that
   until pron re-exports them.
2. `kgdb.contracts.io.GraphSnapshot` — validates deskops' own snapshot
   artifact (KGDB contract layer, not document access).

## 3. Lanes (herdr dispatch units)

Shared-file reality: most lanes touch `operations.py`/`cli/`. **Sequential
dispatch, one worker at a time; verify pytest between lanes.** No two workers
in the same worktree concurrently.

| # | Lane | Scope | Files touched | Gate |
|---|------|-------|---------------|------|
| P0 | Baseline (coordinator) | worktree ready: pron importable, pytest green at HEAD, models re-register via `World` | none (env only) | `pytest -q` green; `python -c "from deskops.world import get_world; ..."` |
| P1 | Seam + models | `deskops/world.py`; carry models; conservative improvements; register via `register_model`; refresh; gap-log file | models/*, world.py, desk/pron-gap-log.md | models registered; `pytest tests/test_model_templates.py tests/test_registry_robustness.py` |
| P2 | Read paths | workspace.py, identity.py, domain_tree.py; read commands: list/show/next/desk/status/faq/about | workspace.py identity.py domain_tree.py cli/commands/{desk,faq}.py | read-command tests + `pytest -q` (subset) |
| P3 | Write paths | create/edit/track flows: create_task_bundle, write_and_track, create_artifact/primitive/routine, edit_artifact_field, bind, promote, inbox | repo_ops/{tasks,board,inbox}.py | lifecycle end-to-end + promotion tests |
| P4 | Atoms + closeout | atoms split/merge/delete/create-from-source, closeout gates, drift, materialize | repo_ops/{atoms,closeout}.py cli/commands/{atoms,closeout,drift,materialize}.py | atom + closeout + materialization tests |
| P5 | Graph + runtime + doctor | graph CLI wiring (kgdb contract stays), doctor without subprocess, bootstrap on World, specs, runtime | cli/main.py graph/snapshot.py doctor.py bootstrap.py | graph CLI tests + doctor tests; full `pytest -q` green |
| P6 | Closeout (coordinator) | gap-log summary → pron inbox note; docs/skills updated; phase-closing commit | desk/*, docs | full pytest + CLI checks + one coherent commit history |

Commit discipline: one atomic commit per lane (task closure commit), commit
drawer→active promotion before implementation starts.

## 4. Model improvements (conservative, non-breaking)

The models lane may apply ONLY these classes of changes; anything else becomes
a drawer item:
- Make `__semantics__`, `__containment__`, `__references__` metadata complete
  and consistent across all model classes.
- Fill missing field descriptions; align `model_config` (`extra`) policy.
- Fix typos/dead fields discovered while registering through pron.
- Any behavioral field change → stop, gap-log it, leave as drawer follow-up.

## 5. Gap log format (fireproof test deliverable)

`desk/pron-gap-log.md` rows: `date | lane | what deskops needed | pron API
consulted | gap | repro (cmd/pytest) | proposed pron change`. Feed to pron
inbox at closeout (P6).

## 6. Worker protocol (herdr)

- Worker: `pi` (DeepSeek Flash via openrouter), spawned with cwd = worktree.
- One dispatch = one lane task with: lane scope, files touched, gate command,
  commit message template, pointer to this plan + routed task doc. Workers
  don't see this conversation — every dispatch is self-contained.
- Between lanes: coordinator runs the lane gate + `pytest -q`, then dispatches
  the next lane. Failure → follow-up dispatch to the same worker, never a new
  lane on red.
- No implementation before P0–P1 land: seam module first, always.

## 7. Risks

- `Store` API gaps vs `operations.py`'s 60+ helpers (e.g. `save_untrack_indexes`
  behavior, section indexes, board append ordering) — expected; each becomes a
  gap-log row, with a local workaround ONLY inside repo_ops, never in the seam.
- argparse surface drift — parser.py is carried, not rewritten, until P5.
- Store index staleness after bulk writes — every write lane ends with
  `World.refresh_if_stale()` (or explicit `refresh()`), mirroring pron's turn
  semantics.
