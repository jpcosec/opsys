# Primitivas de deskops frente a lo que sldb hace hoy (2026-10-16)

Relevamiento de solo lectura hecho con pi/deepseek-v4-pro. Lo verificado a mano: sldb no tiene motor de workflow (no hay checklists, rutinas ni transiciones en ../sldb/src); el evaluador `--where` es `compile_where` en ../sldb/src/sldb/store/query_engine/where_parse.py:24 (interno, lee solo `doc.payload`; `has(x)` es verdadero para una lista vacía); `HookDoc` no tiene llamador en `advance`; docs/opsys/ en sldb es diseño de mayo, no código.

# DeskOps primitives vs sldb — redundancy audit

## 1. DeskOps primitive machinery (file:line)

### Models (all extend `sldb.StructuredNLDoc`)

| Piece | Stores | Read by | Behavior depends on |
|---|---|---|---|
| `ConditionDoc` `deskops/models/condition.py:8-29` | `subject`, `predicate`, `expected` | `runtime/primitives.py:22-40 Condition.evaluate`, `_load_conditions` `operations.py:2468-2484` | gate evaluation during `advance` |
| `ChecklistDoc` `deskops/models/checklist.py:8-44` | `items`, `condition_refs`, `mode` (all/any); `__containment__` → `ConditionDoc` | `runtime/primitives.py:62-76 Checklist.is_complete`, `_load_checklists` `operations.py:2507-2524` | completion gate |
| `OperatorDoc` `deskops/models/operator.py:8-29` | `action`, `target`, `value` | `runtime/primitives.py:43-60 Operator.apply`, `_load_operators` `operations.py:2486-2505` | state mutation (`set_field`, `append_list`) |
| `EdgeDoc` `deskops/models/edge.py:8-29` | `source`, `target`, `condition_ref`; `__references__` | `runtime/primitives.py:78-86 Edge.is_available`, `_load_edge` `operations.py:2453-2466` | transition choice |
| `HookDoc` `deskops/models/hook.py:8-31` | `event`, `target`, `condition_ref`; `__references__` | `runtime/primitives.py:88-100 Hook.matches` | (no active caller found — dead path in `advance`) |
| `RoutineDoc` `deskops/models/routine.py:8-43` | `entrypoint`, `decomposition`, `edges`, `terminal_nodes`; `__containment__`, `__references__` | `runtime/primitives.py:124-225 Routine.advance`, `_load_routine` `operations.py:2432-2451` | state-machine graph |
| `StepDoc` `deskops/models/step.py:6-37` | `action`, `outcome` | rituals/steps artifact CRUD only | plain structured doc |
| `CrossroadDoc` `deskops/models/crossroad.py:22-51` | `path`, `title`, `content` | `deskops.domain_tree` parent-checking | domain tree validity |
| `PrimitiveDoc`/`OperationalArtifactDoc` `deskops/models/base.py:6-39` | `id/status/summary/tags`, plus `routine/current_node/history` | all runtime dataclasses | shared base |

`TaskDoc` references primitives: `routine`, `current_node`, `checklists` fields `task.py:49-58`; `__containment__` maps `routine→RoutineDoc`, `current_node→[ChecklistDoc,StepDoc]`, `checklists→[ChecklistDoc]` `task.py:8-24`.

### Spec registry/compiler

- `SpecRegistry.load` loads `spec/artifacts`, `spec/primitives`, `spec/workflows` (`deskops/specs/loader.py`).
- `compile_task_bundle_spec` `deskops/specs/compiler.py:28-87`: expands `artifact.task` operational section → 5 conditions + 3 checklists + 3 operators + 6 edges + 1 routine; sets `task.routine`, `task.checklists`, `task.current_node` (`compiler.py:74-81`).
- Spec source: `spec/artifacts/task.yaml:24-58` lists 5 conditions, 3 checklists, 3 operators, `primitive.task.edges`; `spec/primitives/task_edges.yaml:10-52` = 6 edges. Total = **17 primitives + 1 routine** (verified).

### Runtime state machine

- `deskops/runtime/primitives.py`: `Condition.evaluate` `:22-40` (equals/not_equals/truthy/falsy/not_empty/contains), `Operator.apply` `:43-60`, `Checklist.is_complete` `:62-76`, `Edge.is_available` `:78-86`, `Routine.advance` loop `:124-225` (checklists→operators→edges→terminal).
- `advance_task` `operations.py:1024-1070` hydrates task, loads routine/conditions/operators/checklists, calls `routine.advance`, writes back, auto-commits at `current_node==complete && status==closed`.
- `next_action_report`/`render_next_action_diagram` `operations.py:505-545` + `deskops/workflow/next_actions.py:9-42`: `match_workflow_state` matches `current_node` against `spec/workflows/task_lifecycle.yaml`; `--diagram` renders Mermaid.

### Bundle creation & closeout deletion

- `create_task_bundle` `operations.py:409-432`: writes task + routine + 17 primitives, tracks each in `.sldb`, appends to `desk/tasks/Board.md`, rollback on failure.
- `_auto_commit_task_closure` `operations.py:1499-1579`: removes task from Board, `git rm --cached` task + routine + glob `desk/primitives/{conditions,checklists,operators,edges,hooks}/*-{task_id}*.md`, commits, then `sldb.api.documents.untrack_document` + unlink (`operations.py:1566-1579`).

## 2. sldb replacements (file:line)

| Capability | Exact API/CLI | Evidence |
|---|---|---|
| Predicate vocabulary | `sldb predicates add/list/show/validate/remove/sync/export` | `sldb/src/sldb/cli/commands/predicates.py:12-75`, `predicates_file.py:24-37` |
| Field predicates | `sldb find --where 'has(f)'`, `'f = "v"'`, `'f != "v"'`, `'"x" in f'`, `'f ~ "re"'`, `'f >= n'`, `'model <= Base'` | `README.md:100-116`, `store/query_engine/where_parse.py:26-80` |
| Relation types | `sldb docs create --model RelationTypeDoc` | `models/relation_type_doc.py:13-54` |
| Edges | `sldb edges init|rebuild|show|check` | `cli/commands/edges.py:11-38` |
| Builtin structural edges | `references`, `contains`, `composes` from `__references__`/`__containment__`/`__compositions__` | `models/structured_doc.py:9-16`, `models/builtin_relation_types.py:24-41` |
| Graph query | `sldb graph get|list|query|neighborhood|snapshot`; `StructuredQuery`/`FieldCondition` (`eq,ne,contains,gt,lt,starts_with,is_null,is_not_null`) | `cli/commands/graph.py:20-78`, `store/graph/language/field_condition.py:11-20`, `structured_query.py:8-16` |
| Links/transclusion | `sldb links recover`, `sldb links compose` | `cli/commands/links.py:14-70` |
| Docs existence | `sldb docs exists REF` (exit 0/1/2/5) | `cli/commands/docs_exists.py:16-27` |
| Linked stores (`alias:ref`) | `sldb stores add --name <alias>`; refs `alias:name`, `alias:Model/name`, `local:` | `api/stores/link_store.py:29-48`, `api/stores/doc_ref.py:16-26` |
| Field queries/mutation | `sldb fields show`, `fields query <field> --global`, `fields update/append/remove` | `cli/commands/fields_show.py:9-46`, `api/records/fields.py:11-32`, `fields_mutate.py` |
| Journal | `sldb journal show|verify` | `cli/commands/journal.py:15-25` |
| Store integrity | `sldb stores check` | README `:74-78` |

## 3. Mapping table

| DeskOps piece | What it does | sldb replacement | Gap | Verdict |
|---|---|---|---|---|
| `ConditionDoc` model + `Condition.evaluate` | stored evaluable rule `(subject,predicate,expected)` | `--where` field predicates (`where_parse.py:26-80`); graph `FieldCondition` (`field_condition.py:11-20`); `predicates add` for vocabulary | sldb predicates store only name/axis/description, not `subject/predicate/expected`; evaluation is query-time, not a stored doc | **REPLACE** (predicate vocabulary + `--where`; keep thin doc model if stored rules are required) |
| `ChecklistDoc` model + `is_complete` | items + condition refs + all/any | none (no checklist, no all/any) | total | **KEEP** |
| `OperatorDoc` model + `Operator.apply` | `set_field`/`append_list` mutation | `sldb fields update/append/remove` | imperative CLI only; no stored operator doc, no state-machine execution | **REPLACE** for the mutation primitive; KEEP doc if auto-execution is required |
| `EdgeDoc` model | `source/target/condition_ref` transition | `RelationDoc` (`relation_doc.py:17-52`) + `sldb edges` | `RelationDoc.condition` is a `--where` predicate string, not a ref to a guard doc; deskops edges drive `Routine.advance` | **REPLACE** for graph edges; KEEP guard-edge doc for state machine |
| `HookDoc` model | event→target guard | none | total | **KEEP** |
| `RoutineDoc` model | entrypoint/decomposition/edges/terminals | none (no state machine) | total | **KEEP** |
| `StepDoc` model | structured action/outcome | any sldb model via `models create`/`docs create` | no shipped StepDoc; rituals reference it | **KEEP** (deskops model over sldb base) |
| `CrossroadDoc` model | domain-path parent description | none | total | **KEEP** |
| Spec registry/compiler (`specs/`) | YAML → expand `{task_id}` into 18 payloads | none (no template-expansion compiler) | total | **KEEP** |
| Runtime state machine (`runtime/primitives.py`) | advance/evaluate/apply loop | none | total | **KEEP** |
| `create_task_bundle` | orchestrate writes + Board append + tracking | `docs create`/`models list` (write+track individual docs) | no bundle compilation, no Board append, no rollback | **KEEP** (orchestration glue over sldb) |
| `advance_task` / `next` | walk routine, match lifecycle state | none | total | **KEEP** |
| `next --diagram` | Mermaid from `task_lifecycle.yaml` | `graph snapshot`/`spec2viz` projection tools | no workflow-lifecycle Mermaid | **KEEP** |
| Closeout deletion | git rm + untrack + unlink primitives | `sldb.api.documents.untrack_document` (`operations.py:1566-1579`); `git` is external | orchestration (git add/rm/commit, Board removal) is deskops | **REPLACE** (thin glue over sldb untrack) |
| `deskops/graph/extract_edges.py` | re-derives declared edges from `__containment__`/`__references__` | `sldb edges rebuild` / `edges show` (same schema-driven edges, `builtin_relation_types.py:32-40`) | deskops adds atom/diagram/provenance declarations not covered by sldb's index | **REPLACE** (prefer sldb index; keep only deskops-specific declaration extraction) |

## 4. External contract that removal breaks

- **21 registered models** in `deskops/.sldb/core/store_index.yaml:2-128`: `AtomDoc, RepositoryDoc, TaskDoc, RoutineDoc, ConditionDoc, ChecklistDoc, OperatorDoc, EdgeDoc, RoleDoc, RuntimeProfileDoc, RunDoc, ProtoAtomDoc, CrossroadDoc, PillDoc, FAQDoc, StepDoc, RitualDoc, InboxNoteDoc, BoardDoc, HookDoc, MaterializationContractDoc` (count verified = 21).
- **TaskDoc primitive references**: `routine`, `current_node`, `checklists` fields `task.py:49-58`; `__containment__` `task.py:8-24`. Model contract hash covers `__references__/__containment__/__compositions__` (`desk/drawer/tasks/task-rw-f1-model-contract-snapshot.md:38`); changing them puts every tracking store in FAIL until `sldb models update` + `deskops desk update --apply` (`desk/drawer/tasks/task-rw-f6-migrate-tracking-stores.md:29,50`).
- **CLI commands**: `add condition|operator|checklist|hook|edge|routine` (`cli/parser.py:713-783`), `list routines|conditions|operators|checklists|hooks|edges` (`parser.py:916-959`), `show routine|condition|operator|checklist|hook|edge` (`parser.py:962-1029`), `next` + `--diagram` (`parser.py:888-913`), `advance task` (`parser.py:1032-1066`).
- **Tests**: `tests/test_specs.py:14-76` (registry + `compile_task_bundle_spec`), `tests/test_lifecycle_end_to_end.py:96-172` (bundle, advance, deletion), `tests/test_inbox_promote_cli_gaps.py:163-215` (`advance --to`), `tests/test_promotion_nesting.py:58-97`, `tests/test_model_templates.py:53-217`, `tests/test_composition.py:82-127`, `tests/test_graph_declared_edges.py:1-121`, `tests/test_operational.py`.

## 5. Unverifiable / corrected claims

- **"24 stores track TaskDoc"** — not verifiable in this checkout. Source is only `runs/planning/deskops-rewrite-inventory.md:14,174` and drawer tasks (`task-rw-f6-migrate-tracking-stores.md:29`). The repo's own `.sldb` tracks exactly 1 TaskDoc (`deskops/.sldb/core/models/TaskDoc.yaml:10 documents_count: 1`); `task.py:145` says "123 tasks across 13 stores" (older figure). Count is machine-specific.
- **HookDoc has no active consumer** in `Routine.advance` — `Hook.matches` (`runtime/primitives.py:88-100`) is defined but I found no call site in `advance_task`/`runtime`. Dead model.
- **sldb "graph queries" are not a workflow engine**: `StructuredQuery`/`FieldCondition` operate over graph-node facets; they do not mutate payloads, advance state, or trigger closeout.
- **`deskops.graph.extract_edges`** is a parallel, non-trivial reimplementation of sldb's schema-driven edge index with deskops-specific extensions (atom/diagram/provenance) — a redundancy the audit target did not list explicitly.
