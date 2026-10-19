#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/tmp/rw/wt/apply}"

D() {
  PYTHONPATH=/tmp/rw/wt/apply python -m deskops "$@" --root "$ROOT"
}

# ---------------------------------------------------------------------------
# atoms-a: UPDATE
# ---------------------------------------------------------------------------
D edit atom atom-atom-lifecycle-includes-validate-and-delete-with-inbound-reference-guard answer 'deskops atoms validate checks atom integrity, including domain-tree crossroad parents, and deskops atoms delete removes an atom only when no inbound atom references exist (override with --force). Split, merge, and create-from-source are implemented alongside validate and delete.'

closing_answer=$(cat <<'EOF'
A task closing commit must never depend on agent discretion. It is created by deskops closeout commit, which takes exactly one of two routes. With a subagent run, use --task <id> --run-dir <runs/subagents/dir>: it refuses to run without board.txt, task.txt, git-status.txt and result-summary.md, updates run.yaml with task_id, run_dir, run_id, session and session_sha256, embeds Task-Id/Run-Dir/Run-Id/Session-Sha256 git trailers, and appends an index entry to runs/subagents/index.jsonl. Without a run, use --task <id> --no-run --reason "<why>": it embeds Task-Id, Closeout-Mode: manual and Closeout-Reason trailers and appends an index entry with run_dir null and mode manual. Passing both routes or neither is refused, and --no-run without a non-empty reason is refused. The index commit field is always null because the entry is amended into the closing commit; resolve the commit with git log -1 --grep "Task-Id: <task-id>". Do not handcraft closing commits with plain git commit, do not fabricate a run dir for work no subagent did, and do not treat a green test run as closeout without the tool-made commit.
EOF
)
D edit atom atom-closing-commits-are-tool-made-and-run-linked answer "$closing_answer"

D edit atom atom-cross-desk-inbox-delivery-is-verifiable-and-acknowledgeable answer 'Cross-desk messaging resolves the target through the canonical identity resolver, writes a structured delivery result (sender, target, path, tracked_name, verified), and supports acknowledgement: deskops message send/list/read plus deskops message ack <selector> closes the note and records target_project, acknowledged_by and acknowledged_at. deskops inbox remains a deprecated alias.'

health_delegates_answer=$(cat <<'EOF'
Desk health keeps desk workspace repair and SLDB store health separate. deskops doctor delegates document validity and store integrity to sldb stores check; it detects missing deskops model registrations from the store index, and owns workspace checks (desk structure, legacy classification, unmodeled and untracked documents). Desk repair does not initialize or repair the SLDB store itself.

## Boundary Rationale

- **Desk** owns workflow artifacts: tasks, boards, pills, rituals, atoms, and lifecycle documents
- **SLDB** owns document infrastructure: models, templates, fields, store indexes, validation

Mixing these concerns into one health command creates ambiguity about ownership and repair responsibility.

## Delegation Pattern

```
deskops doctor
  ├── desk structure checks  → deskops (own repair)
  ├── untracked docs         → deskops (report only)
  ├── invalid docs           → sldb stores check (report via delegation)
  └── store integrity        → sldb stores check (delegate)
```

## Evidence

`deskops/cli/commands/doctor.py` calls `sldb stores check` for document validity and propagates findings to the operator.

## Tags

- system:deskops
- topic:workspace-health
- topic:boundary
- topic:sldb
EOF
)
D edit atom atom-desk-health-delegates-store-diagnostics-to-sldb answer "$health_delegates_answer"

health_measured_answer=$(cat <<'EOF'
Desk health is measured through deskops doctor, which classifies the workspace as absent, empty, legacy or current and reports missing desk structure (desk/, tasks/Board.md, drawer/, rituals/phase.md), untracked modeled documents, documents the model cannot read, invalid documents, an unreadable store index, and unregistered deskops models. --repair scaffolds missing structure and registers missing models; document tracking and content repairs are reported for manual follow-up.

## Diagnostic Surface

`deskops doctor` reports:
1. **Missing desk structure** — `desk/`, `desk/tasks/Board.md`, `desk/drawer/`, `desk/rituals/phase.md`
2. **Untracked desk documents** — Markdown files in `desk/` not registered in `.sldb`
3. **Unreadable desk documents** — Modeled documents whose current text does not extract their fields
4. **Invalid desk documents** — Documents with malformed YAML, missing required fields, or validation errors
5. **Unreadable store index** — Local store index records doctor cannot load
6. **Unregistered deskops models** — Deskops models missing from the local store

## Repairability

| Finding | Auto-repair | Manual required |
|---------|-------------|-----------------|
| Missing structure | Scaffold with `deskops doctor --repair` | — |
| Unregistered models | Register with `deskops doctor --repair` | — |
| Untracked docs | Report only | Use `sldb docs track` |
| Unreadable or invalid docs | Report only | Fix the text or run `sldb stores update` |

## Evidence

`deskops/cli/commands/doctor.py` — `DoctorCLI.run()` method implements these checks.

## Tags

- system:deskops
- topic:workspace-health
- topic:diagnosis
- topic:cli
EOF
)
D edit atom atom-desk-health-is-measured-by-cli-diagnostics answer "$health_measured_answer"

health_integrity_answer=$(cat <<'EOF'
Desk health is the integrity state of the desk/ workspace: whether it has the expected structure, tracked modeled documents, readable document content, and registered deskops models, and whether it classifies as absent, empty, legacy or current. deskops doctor measures it; store-level document validity is delegated to sldb stores check.

## Evidence

`deskops/cli/commands/doctor.py` checks:
- Missing or malformed `desk/` directory structure
- Untracked modeled documents in `desk/`
- Documents the model cannot read
- Invalid task/pill/atom/ritual documents (malformed YAML frontmatter)
- An unreadable local store index
- Unregistered deskops models

## Related Atoms

- `atom-stale-state-causes-agent-hallucination` — explains why health matters for agents
- `atom-desk-health-delegates-store-diagnostics-to-sldb` — defines the boundary

## Tags

- system:deskops
- topic:workspace-health
- topic:diagnosis
EOF
)
D edit atom atom-desk-health-is-workspace-integrity-state answer "$health_integrity_answer"

D edit atom atom-deskops-imports-sldb-cli-helpers-from-their-current-modules answer 'Deskops depends on sldb CLI helper API (get_store_context in sldb.cli.store_context; registered_model/resolve_model_ref in sldb.cli.model_utils); when sldb relocates helpers, deskops must repoint imports rather than pin stale paths. TaskDoc declares its frontmatter fields explicitly and has no frontmatter dict or render_payload override; the sldb renderer invokes render_payload internally.'

desk_repair_answer=$(cat <<'EOF'
Desk repair covers the operations that fix or scaffold desk-owned workflow surfaces. deskops doctor --repair creates missing desk/ structure and registers missing deskops models; it reports untracked or unreadable documents and legacy desks for manual migration. Deskops does not own SLDB store initialization, model schema changes, or document-content repair.

## Owned Operations

`deskops` owns repair for:
- Missing or incomplete `desk/` directory structure
- Registration of missing deskops models
- Detection and reporting of untracked desk documents
- Detection and reporting of malformed desk artifacts

## Not Owned

`deskops` does not own:
- SLDB store initialization or repair
- Model registration or field schema changes
- Document content repair (only detection, not correction)

## Evidence

`deskops/cli/commands/doctor.py` — implements the desk-owned repair surface.

## Tags

- system:deskops
- topic:workspace-health
- topic:ownership
- topic:boundary
EOF
)
D edit atom atom-desk-repair-is-owned-by-deskops answer "$desk_repair_answer"

D edit atom atom-promotion-flattens-structured-source-sections-into-task-fields answer 'Inbox-to-drawer promotion parses task-shaped headings (Rationale, Goal, Scope, Implementation Path, Validation, Done When) out of the free-form note and flattens them into the drawer candidate task fields. Drawer-to-active is explicit authoring with deskops add task --from-drawer <selector>, which records the origin in TaskDoc.from_drawer and keeps the drawer file rather than copying its sections.'

D edit atom atom-task-bundles-are-tracked-in-the-store-at-creation-time answer 'deskops add task writes the TaskDoc and tracks it through doc_io.track_document_file (sldb.api) inside a DocTransaction at creation time; if a store exists but TaskDoc is not registered, tracking fails and the task is rolled back instead of leaving an untracked document.'

D edit atom atom-workflow-role-model-routing answer 'Each deskops workflow role is bound to an explicit model in its installed agent frontmatter (~/.pi/agent/agents/), not left to inherit the pi default. Supervisor: anthropic/claude-opus-4-8 with fallback openai-codex/gpt-5.4 (routing and review). Executor: openai-codex/gpt-5.4 with fallback google-gemini-cli/gemini-3.1-pro-preview (implementation; supervisor may override per dispatch with model=). Tester: openrouter/nvidia/nemotron-3-super-120b-a12b:free with fallback openrouter/openai/gpt-oss-20b:free (mechanical validation).'

D edit atom atom-atom-references-carry-roles answer 'An atom reference carries the role the atom plays. deskops accepts these roles for explicit atom references: references, documents, specifies, constrains and validates (deskops/atom_references.py ALLOWED_ROLES). Graph edges also carry field-derived roles such as supports, uses, materializes, implements, tests, violates, invokes, defines, routes and configures.'

D edit atom atom-knowledge-graph-connects-desk-and-source-files tags '["system:deskops","system:sldb","topic:knowledge-graph","topic:source-code"]'

D edit atom atom-networkx-is-first-graph-runtime answer 'The sldb graph runtime (sldb.api.graph) uses NetworkX for traversal, neighborhood queries, path analysis and snapshot export; deskops builds its graph snapshot from that API before introducing heavier ontology or OWL reasoning.'

D edit atom atom-sldb-semantics-are-graph-inputs answer 'SLDB semantic tags, semantic DAG nodes, equivalences, tracked documents, sections and model semantics are inputs to the ecosystem graph through sldb.api.graph rather than being reimplemented by a separate graph project.'
D edit atom atom-sldb-semantics-are-graph-inputs tags '["system:deskops","system:sldb","topic:knowledge-graph"]'

# ---------------------------------------------------------------------------
# atoms-b: UPDATE
# ---------------------------------------------------------------------------
D edit atom atom-automatic-routines-vs-llm-tasks title 'Deterministic checks are not LLM tasks'
D edit atom atom-automatic-routines-vs-llm-tasks answer 'Actions that require semantic judgment belong to LLM/subagent tasks. Deterministic checks over known inputs, such as running touched-surface tests, closeout validation, or phase end-to-end checks, belong to tests, CI, or CLI gates. The routine and hook models were retired with the primitive layer.'
D edit atom atom-automatic-routines-vs-llm-tasks tags '["system:deskops", "topic:automation", "topic:workflow"]'

D edit atom atom-clean-agents-start-from-minimum-workflow-set answer 'A clean agent needs the README orientation, active board, bound pills, the phase, execution, testing, and closeout rituals, and relevant atoms before making a safe repository change.'

D edit atom atom-cli-is-thin-over-primitives-and-sldb tags '["system:deskops", "system:sldb", "topic:cli", "topic:lifecycle"]'

D edit atom atom-drawer-is-not-active-work answer 'Drawer items are deferred candidates and do not execute until someone authors a routed task from them with `deskops add task --from-drawer` and the task is routed through the workflow.'

D edit atom atom-drawers-feed-tasks-through-promotion title 'Drawers feed tasks through explicit authoring'
D edit atom atom-drawers-feed-tasks-through-promotion answer 'Future, uncertain, or loosely shaped work enters `desk/drawer/` as features, issues, questions, or other lax artifacts, then becomes active execution only when a person or agent authors a routed task from it with `deskops add task --from-drawer`. There is no drawer-to-active promotion command; the drawer file is kept for manual cleanup.'
D edit atom atom-drawers-feed-tasks-through-promotion tags '["system:deskops", "topic:drawer", "topic:tasks", "topic:authoring"]'

D edit atom atom-field-oriented-document-composition answer 'Field specs define reusable semantic dimensions for artifacts. Artifact specs list those field IDs, but the Pydantic model for each artifact owns its concrete fields and values; there are no separate field-instance documents.'

D edit atom atom-inbox-is-coordination-intake answer 'Inbox notes are messages addressed to the current project: questions, bugs, blockers, suggestions, requirements, cross-project coordination messages, or explicit self-messages. They are not an agent scratchpad for deferred work; that belongs in drawers until a routed task is authored from it.'

D edit atom atom-kgdb-owns-relations-between-knowledge-surfaces title 'SLDB graph owns relations between knowledge surfaces'
D edit atom atom-kgdb-owns-relations-between-knowledge-surfaces answer 'Relations between artifacts belong in the SLDB graph (`sldb.api.graph`): the graph should represent how code, docs, specs, tests, diagrams, tasks, pills, libraries, languages, patterns, linters, and consumers connect to each other and to atoms. KGDB was retired and merged into SLDB.'
D edit atom atom-kgdb-owns-relations-between-knowledge-surfaces tags '["system:deskops", "system:sldb", "topic:knowledge-graph", "topic:relations"]'

D edit atom atom-operational-primitives-model tags '["system:deskops", "topic:lifecycle", "layer:workflow"]'

D edit atom atom-orphan-artifacts-are-knowledge-system-failures answer 'A repository should not keep orphan documents or files that lack SLDB graph relations to relevant atoms and are not represented as materializations through SLDB-managed knowledge surfaces.'

D edit atom atom-primitives-encode-operational-rules tags '["system:deskops", "topic:lifecycle", "topic:workflow"]'

D edit atom atom-repo-artifacts-need-atom-traceability answer 'Every codebase artifact should be traceable to one or more atoms, either directly as a materialization or through SLDB graph relations that connect artifact function, language, library, pattern, consumers, tests, linting, composition, or usage to durable knowledge.'

D edit atom atom-rituals-precede-routines title 'Rituals are lifecycle graph states'
D edit atom atom-rituals-precede-routines answer 'Rituals are the human-readable states of the lifecycle graph. Each transition between them is a typed sldb RelationDoc with a `--where` gate, so ritual prose and executable graph state stay aligned.'
D edit atom atom-rituals-precede-routines tags '["system:deskops", "topic:rituals", "topic:lifecycle"]'

D edit atom atom-routine-based-task-execution tags '["system:deskops", "topic:tasks", "topic:lifecycle"]'

D edit atom atom-self-generating-spec-derived-cli title 'Self-generating model-derived CLI'
D edit atom atom-self-generating-spec-derived-cli answer 'The deskops CLI derives artifact add/list/show/edit surfaces from the Pydantic artifact models registered in `ARTIFACT_SUBJECTS`, so intentionally exposed workflow artifacts share parser and dispatch behavior instead of duplicating argparse code for every model.'
D edit atom atom-self-generating-spec-derived-cli tags '["system:deskops", "layer:cli", "topic:models"]'

D edit atom atom-spec-driven-artifact-architecture answer 'Deskops artifact YAML specs supply artifact-level config such as id patterns, status defaults, tag defaults, and field lists for structure diagrams. The Pydantic model owns the fields of each artifact, and the task lifecycle is declared in its own workflow spec, `deskops/spec/workflows/task_lifecycle.yaml`, not in artifact specs.'

D edit atom atom-spec-fields-compile-into-model-fields title 'Spec fields describe model fields'
D edit atom atom-spec-fields-compile-into-model-fields answer 'Spec field YAML defines reusable field vocabulary used by artifact specs and structure diagrams. The Pydantic model for each artifact owns its fields, and concrete values belong inside the artifact payload rather than in separate desk field documents.'

D edit atom atom-spec-to-visualization-pipeline answer 'Deskops renders the lifecycle state machine as Mermaid from its workflow spec (`deskops next --diagram`). Artifact structure diagrams can be rendered from artifact specs through `deskops.specs.mermaid`, but the CLI does not currently expose that projection.'

D edit atom atom-upstream-routing-needs-convenient-command title 'Upstream routing has a convenient command'
D edit atom atom-upstream-routing-needs-convenient-command answer 'Deskops provides `deskops message send --to <registered-repo>` to capture gaps in sibling tool inboxes, because relying on agents to hand-write upstream notes makes the intended routing rule easy to skip.'

D edit atom atom-used-source-artifacts-are-deleted answer 'When inbox, drawer, or other source artifacts are consumed into active tasks, atoms, docs, specs, code, tests, or commits, the original source file should be deleted rather than marked with terminal statuses such as promoted or stable. `promote inbox-to-drawer-task` deletes the inbox note automatically; a drawer file recorded by `add task --from-drawer` is kept for manual cleanup and should be removed by hand.'

# ---------------------------------------------------------------------------
# contexts.md: UPDATE
# ---------------------------------------------------------------------------
D edit pill pill-009 tags '["system:deskops","pill-type:model","topic:source-code","topic:traceability"]'

D edit pill pill-010 tags '["system:deskops","system:sldb","pill-type:guardrail","topic:runtime","topic:drift-control"]'
D edit pill pill-010 when 'Apply this pill whenever a task writes deskops graph snapshot JSON, generated indexes, query results, or self-reflection reports.'

D edit pill pill-011 where 'Applies to desk/tasks/*self-reflection*.md, deskops graph reflect, and any generated inbox or drawer output.'

D edit pill pill-cross-desk-inbox-needs-delivery-verification-and-follow-up where 'Applies to deskops/cli/commands/message.py, the deprecated deskops inbox alias, repo registry resolution, deskops desk update, and cross-desk acknowledgement or reply flows.'

D edit pill pill-zero-context-preflight-precedes-executor how_not 'Do not dispatch an Executor when the fresh-context subagent could not restate the TaskDoc without guessing, and do not let coordinator chat memory fill gaps the TaskDoc does not contain.'

# closeout ritual: replace the hand untrack/delete steps and drop the stale precondition.
steps_value=$(ROOT="$ROOT" python - <<'PY'
import json, os, re
from sldb.runtime.validation import extract_model_data
from deskops.models import RitualDoc
root = os.environ["ROOT"]
payload = extract_model_data(RitualDoc, open(os.path.join(root, "desk/rituals/closeout.md"), encoding="utf-8").read())
steps = list(payload["steps"])

def body(step):
    return re.sub(r"^\d+\.\s*", "", step).strip()

replacement = "1. Leave removal and untracking to deskops closeout commit: it removes the task from the Board, untracks it, and deletes the bundle in the closing commit. Do not delete or untrack by hand first."
kept = [s for s in steps if not body(s).startswith("Untrack the task document") and not body(s).startswith("Delete the resolved task file") and not body(s).startswith("Leave removal and untracking")]
index = next((i for i, s in enumerate(kept) if body(s).startswith("If the task's subject no longer exists")), len(kept))
kept.insert(index, replacement)
print(json.dumps(kept))
PY
)
D edit ritual ritual-closeout steps "$steps_value"

preconditions_value=$(ROOT="$ROOT" python - <<'PY'
import json, os
from sldb.runtime.validation import extract_model_data
from deskops.models import RitualDoc
root = os.environ["ROOT"]
payload = extract_model_data(RitualDoc, open(os.path.join(root, "desk/rituals/closeout.md"), encoding="utf-8").read())
print(json.dumps([p for p in payload["preconditions"] if p != "Board updates are prepared."]))
PY
)
D edit ritual ritual-closeout preconditions "$preconditions_value"

D edit repository repo-graph_ui description 'Visual editor for pron and sldb stores; active mindmap frontend under frontends/mindmap.'
D edit repository repo-spec2viz description 'Turns semantic YAML specs into diagrams and charts (PlantUML, Mermaid, Vega).'

D edit board Board purpose 'Route the active execution set for deskops.'
D edit board Board notes 'No active tasks routed.'

# ---------------------------------------------------------------------------
# drawer.md: UPDATE (the one modeled drawer task)
# ---------------------------------------------------------------------------
D edit task task-adhoc-subagent-launcher-tmux-multi-cli goal 'Add `deskops launch` for one task using the existing Herdr runtime (`RuntimeProfileDoc` plus RoleDoc) with sldb-compiled context, persisted output, and deskops-mediated signals.'

why_value=$(ROOT="$ROOT" python - <<'PY'
import os
from sldb.runtime.validation import extract_model_data
from deskops.models import TaskDoc
root = os.environ["ROOT"]
payload = extract_model_data(TaskDoc, open(os.path.join(root, "desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md"), encoding="utf-8").read())
print(payload["why"].replace("desk/drawer/features/feature-adhoc-subagent-launcher-tmux-multi-cli.md", "desk/drawer/features/feature-runtime-and-launcher.md"))
PY
)
D edit task task-adhoc-subagent-launcher-tmux-multi-cli why "$why_value"

scope_value=$(ROOT="$ROOT" python - <<'PY'
import os
from sldb.runtime.validation import extract_model_data
from deskops.models import TaskDoc
root = os.environ["ROOT"]
payload = extract_model_data(TaskDoc, open(os.path.join(root, "desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md"), encoding="utf-8").read())
text = payload["scope"]
for old, new in (("tool_allowlist", "tools"), ("model_primary", "model"), ("model_fallback", "fallback_models")):
    text = text.replace(old, new)
print(text)
PY
)
D edit task task-adhoc-subagent-launcher-tmux-multi-cli scope "$scope_value"

implementation_value=$(ROOT="$ROOT" python - <<'PY'
import os
from sldb.runtime.validation import extract_model_data
from deskops.models import TaskDoc
root = os.environ["ROOT"]
payload = extract_model_data(TaskDoc, open(os.path.join(root, "desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md"), encoding="utf-8").read())
text = payload["implementation_path"]
for old, new in (("tool_allowlist", "tools"), ("model_primary", "model"), ("model_fallback", "fallback_models")):
    text = text.replace(old, new)
print(text)
PY
)
D edit task task-adhoc-subagent-launcher-tmux-multi-cli implementation_path "$implementation_value"

# ---------------------------------------------------------------------------
# RETIRE: drawer entries
# ---------------------------------------------------------------------------
D drawer remove workflow-execution-engine
D drawer remove feature-materialization-pipeline
D drawer remove st-06-spec-pipeline
D drawer remove st-10-materialization
D drawer remove uc-06-spec-to-artifact-pipeline
D retire desk/inbox/20260827-165024-unclear-pilldoc-sin-slot-status-y-edit-pill-no-alcanza-drawer-pills.md --reason 'Empty closed note: body is only the template placeholder and the issue is closed and acknowledged.' --ref d35726a --force

# ---------------------------------------------------------------------------
# RETIRE: atoms
# ---------------------------------------------------------------------------
D atoms delete atom-anti-pattern-monolithic-api-endpoints-in-sldb-viewer
D atoms delete atom-hook-automation-can-be-powerful-but-opaque
D atoms delete atom-kgdb-is-graph-substrate-not-reasoner
D atoms delete atom-kgdb-should-parallel-sldb-not-compete

# ---------------------------------------------------------------------------
# RETIRE: contexts, rituals, steps, faq, features, leftovers
# ---------------------------------------------------------------------------
D retire desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md --reason 'Resolved by docs/operator-manual.md and tests/test_operator_manual.py; the pill only remained as a stale drawer board entry.' --ref 978fd98 --force
D retire desk/rituals/ritual-deployment-ritual.md --reason 'Legacy placeholder fixture; it is not a lifecycle state declared by the task lifecycle spec and is replaced by the execution, testing, and closeout rituals.' --ref afdec7f
D retire desk/steps/step-build.md --reason 'Obsolete fixture from the retired StepDoc architecture; ritual steps are prose in deskops/models/ritual.py.' --ref e60cdb3
D retire desk/steps/step-document-the-cli.md --reason 'Obsolete fixture from the retired StepDoc architecture; ritual steps are prose in deskops/models/ritual.py.' --ref e60cdb3 --force
D retire desk/faq/faq-how-to-deploy.md --reason 'Legacy placeholder; deskops faq reads docs/faq.md and the packaged deskops/data/faq.md, never desk/faq/.' --ref docs/faq.md
D retire desk/faq/faq-how-to-test.md --reason 'Legacy placeholder; deskops faq reads docs/faq.md and the packaged deskops/data/faq.md, never desk/faq/.' --ref docs/faq.md
D retire desk/faq/faq-how-to-test-comprehensively.md --reason 'Legacy placeholder; deskops faq reads docs/faq.md and the packaged deskops/data/faq.md, never desk/faq/.' --ref docs/faq.md
D retire desk/features/feature-atom-model-kinds-and-question-facets.md --reason 'No FeatureDoc model exists; the feature backlog lives in desk/drawer/features/.' --ref desk/drawer/features
D retire desk/models/__init__.py --reason 'Leftover of the removed desk/ Python package; it imports retired model modules and is replaced by deskops/models/__init__.py.' --ref 13b1421

# Any tracked or untracked leftover file under the removed desk/ package dirs.
for leftover in \
  $(find "$ROOT/desk/__pycache__" "$ROOT/desk/drawer/__pycache__" "$ROOT/desk/models/__pycache__" "$ROOT/desk/cli" "$ROOT/desk/materializers" "$ROOT/desk/primitives" -type f 2>/dev/null | sort); do
  rel=${leftover#"$ROOT"/}
  case "$rel" in
    desk/drawer/*)
      D drawer remove "$rel"
      ;;
    *)
      D retire "$rel" --reason 'Leftover of the removed desk/ Python package.' --ref 13b1421
      ;;
  esac
done
