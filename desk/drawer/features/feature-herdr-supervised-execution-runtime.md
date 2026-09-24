# Herdr supervised-execution runtime

## Kind

feature

## Status

Implemented and merged into working tree, uncommitted. `question-herdr-runtime-open-decisions.md` is resolved; all four decisions were carried through:

- `RoleDoc` has typed frontmatter (`kind`, `model`, `fallback_models`, `tools`, `system_prompt_mode`, `inherit_project_context`, `inherit_skills`, `default_context`); `ROLE_AGENT_SPECS` is deleted; the three tracked role docs are migrated and the supervisor's model is the deployed `anthropic/claude-opus-4-8` (decision 1).
- `RuntimeProfileDoc` is registered and tracked (`desk/runtimes/runtime-pi.md`, `desk/runtimes/runtime-claude.md`); `deskops/materializers/runtime_profiles.py::build_agent_spec_args` is the pure role+profile -> CLI-args translation; `deskops/runtime/initializer.py::build_role_agent_panes` derives every agent pane from tracked RoleDocs, no role name or kind hardcoded anywhere.
- `deskops drift check` now also runs `drift_check_runtime_bindings`: missing-profile and silent-capability-loss findings.
- `deskops runtime supervise <agent>` exists (`deskops/runtime/supervise.py` + `deskops/cli/commands/runtime.py`), verified end-to-end against a live Herdr agent. It never answers a blocked prompt and never advances desk state on done — both are print+notify only.
- `.gitignore` excludes `runs/subagents/*/session.jsonl` (decision 2); `RunDoc` is defined and registered but nothing writes it yet (decision 4, additive phasing) — `closeout.py` is untouched.
- Decision 3 (retarget the tmux launcher task onto Herdr) is **not** done here — it is a separate, larger effort on `task-adhoc-subagent-launcher-tmux-multi-cli`, left for its own pass.

Session-scoped launches (`--session` pinned to `runs/subagents/<run-dir>/session.jsonl`, which is what would finally populate `run_id`/`session_sha256` in `index.jsonl`) are NOT wired: `build_agent_spec_args` accepts `session_path`/`system_prompt_path` and is tested for both, but nothing in `initialize_desk`/`runtime init --agents` calls it with a real run dir, since those are long-lived dev panes, not one-shot supervised runs. That wiring belongs to whatever implements decision 3.

Verification run this session: `sldb stores check` PASS, `deskops drift check` clean, full suite 252 passed (0 failed), `grep -rn "ROLE_AGENT_SPECS" deskops/` empty, and `deskops runtime supervise` exercised live against a real Herdr pi agent (correctly caught a real transition, read its output, reported, and did not touch any task).

One incidental finding worth carrying forward: registering a document model with zero tracked documents (`sldb models add` on `RunDoc`, which decision 4 requires stay empty) leaves `hash_b: ''` in `.sldb/core/models/<Name>.yaml` instead of the hash of an empty documents index, and `sldb stores check` then FAILs until `sldb models update <Name>` is run once. Worth reporting upstream to sldb; not something to route around here.

## Problem

Deskops already models supervision. `desk/roles/deskops-supervisor.md` defines duties, hard boundaries (allowlist `read, grep, find, ls, bash`, no `edit`/`write`), dispatch rules and a closeout checklist. But it supervises **forensically**: it dispatches a lane, the lane writes files under `runs/subagents/<run-dir>/`, and the supervisor reads them afterwards. It never observes anything live, and it cannot learn that a lane is sitting on an approval prompt.

Herdr supplies exactly that missing half — `agent wait --until blocked|done`, `agent read`, `agent prompt` — but **keeps no trace**. Verified on this machine: the server log contains zero `agent.*` events; read-only calls are not logged at all (only `changes_ui=true` ones); pane scrollback is 10MB held in memory; and TUI agents run on the alternate screen, whose rows never enter that scrollback. Herdr is a remote control, not a recorder.

The durable trace already exists and is half-wired:

- `deskops/cli/commands/closeout.py` requires four evidence files, writes `run.yaml`, appends to `runs/subagents/index.jsonl`, and stamps `Task-Id`/`Run-Dir`/`Run-Id`/`Session-Sha256` commit trailers.
- pi writes complete JSONL session transcripts and accepts `--session <path>` to pin their location.
- Herdr's integrations for `pi`, `claude`, `codex` and `opencode` report `agent_session_path`/`agent_session_id` back to the server via `pane.report_agent_session`; the API schema exposes `agent_session`.

**But nothing passes `--session` or `--run-id`.** Every real entry in `index.jsonl` carries `run_id: null` and `session_sha256: null`, so the closeout gate is a no-op for both fields.

Separately, `deskops/materializers/roles.py:23-59` holds a hardcoded `ROLE_AGENT_SPECS` table that has already drifted from the documents it materializes (see question doc, decision 1).

## Desired Outcome

Herdr owns live control; deskops owns the durable trace. Nothing hardcoded — not the role, not the runtime, not the flag mapping.

- Roles declare how they launch, as typed fields on their own document.
- Each runtime kind declares how abstract role settings become its CLI flags, as its own document. Adding a runtime means writing a `.md`, not editing Python.
- Every supervised run pins its transcript where closeout already expects it, so `run_id` and `session_sha256` stop being null.
- A supervisor process blocks on agent lifecycle state at zero cost and escalates to a human on `blocked` — it never answers an approval dialog itself.

## Scope boundary

This document covers the deskops side only: models, materializers, adapter, CLI and store migration. The workstation side — the `desk/runtime.yaml` layout contract that nothing reads, `herdr/init_opsys.py` duplicating `deskops/runtime/initializer.py`, and Herdr's own lack of trace and log rotation — is tracked in the setup repo at `desk/drawer/herdr-runtime-contract-gaps.md`.

## Relationship to the tmux launcher feature

`feature-adhoc-subagent-launcher-tmux-multi-cli.md` and its ready-to-promote drawer task cover substantially this same ground, over tmux + `codex`/`agy`/`pi`. Its already-resolved operator principles (context compiled via sldb from tracked RoleDocs, minimal bundle per profile, one launch = one task = one run dir, everything persisted to disk) apply unchanged here and should be inherited, not restated.

The difference is transport. Herdr provides agent detection and lifecycle states that tmux cannot, is already installed and running, and already reports session identity. Recommendation is to retarget the existing task rather than build a second launcher; that is decision 3 in the question doc.

## Proposed CLI surface

```
deskops runtime supervise [--root .] [--herdr herdr]
```

Registered alongside the existing `runtime init|status|attach|stop`. Loop:

1. `wait(executor)` with no `--until` — settles on the first `idle`/`done`/`blocked`.
2. On `blocked`: capture `read(...)`, raise `herdr notification show ... --sound request`, record a note. **Do not answer the dialog.** Herdr's own skill requires inspecting and asking the human; an auto-approving supervisor is the mechanism by which an unattended agent does something destructive.
3. On `done`: capture evidence into the run dir, digest the session, write the run record, evaluate the role's closeout checklist, and **report**. Does not run `deskops advance` — the desk does not change state unobserved.

## Design notes (grounding in what already exists)

### Blocker to clear first

`deskops/runtime/herdr.py:100`, and the same line in `call_text`:

```python
timeout=timeout or self.timeout,
```

With `self.timeout = 30.0`, a caller **cannot** disable the limit: `timeout=None` falls through the `or` back to 30s. `HerdrProvider.send(wait=False)` already suffers this. An `agent wait --until blocked` can legitimately block for hours and would die at 30 seconds with a misleading `HerdrError: ... timed out`. Needs a sentinel distinguishing "omitted" from "no limit". Nothing else works until this is fixed.

### Adapter additions

`wait(agent_id, *, until=(), timeout_ms=None)` returns the settled `agent_status`. `agent wait` returns JSON shaped exactly like `agent get` — `{"result": {"agent": {...}, "type": "agent_info"}}` (verified) — so `_result()` is reused as-is.

`read(agent_id, *, source="recent-unwrapped", lines=200)` **must** go through `call_text`, not `call`: `herdr agent read` returns plain terminal text, not JSON (verified). Using `call` raises `Herdr returned non-JSON output`. This is the easiest mistake to make here.

While in the file: `send`/`status`/`attach`/`stop` on `HerdrProvider` are currently dead code — `cli/commands/runtime.py` bypasses the provider and talks to the client directly. Wire them up.

### RoleDoc becomes the single source of truth

Replace the catch-all `⸢rev,dict•frontmatter⸥` with explicit per-field frontmatter markers, following `deskops/models/pill.py:8-13`. Three concrete reasons:

1. The catch-all *requires* the hardcoded `body_fields` set in `render_payload()` — the pattern is itself more hardcoding than explicit fields.
2. Fields living inside the dict bypass the `Field(description=...)` enforcement in `StructuredNLDoc.__pydantic_init_subclass__` — exactly the undocumented, driftable surface being removed.
3. `_check_render_validity` treats the whole dict as one `rev` field, so confusing `model` with `tools` is not caught field-by-field. Wrong risk profile for agent-launch parameters.

New fields: `kind`, `model`, `fallback_models`, `tools`, `system_prompt_mode`, `inherit_project_context`, `inherit_skills`, `default_context`. Then delete `RoleAgentSpec`, `ROLE_AGENT_SPECS` and `role_agent_spec`; `render_pi_agent_markdown`, `materialize_role_docs` and `drift_check_role_docs` derive from the document and filter on `kind == "pi"`.

Verified sldb details: lists and bools round-trip fine with a plain `⸢rev•field⸥` in frontmatter — the `,list` trait is only for body bullets (`ChecklistDoc.items`); precedent is `RoutineDoc.decomposition`. No new field may default to `None`: when a value is `None` and the marker is not `optrev`/`render`, the renderer leaves the literal marker unresolved in the output. Defaults must be `""`, `[]`, `True`/`False`.

### RuntimeProfileDoc — one document per kind

Lives in `desk/runtimes/`, extends `PrimitiveDoc`. Declares `kind`, `binary`, and a deliberately closed vocabulary: `model_flag`, `fallback_models_flag` + `fallback_models_join`, `tools_flag` + `tools_join`, `system_prompt_flag` + `system_prompt_delivery`, `session_flag`, `extra_args`, `unsupported_role_fields`. Join modes are `comma`/`space`/`repeat`; delivery is `inline`/`file`. No conditionals, no expression language.

`unsupported_role_fields` exists so a capability the runtime cannot express becomes visible rather than silently dropped.

Do **not** reach for the `table[col,col]` marker trait. It exists in sldb but has zero uses anywhere in the codebase and two different extraction paths depending on marker placement. The flat scalar fields above are the proven pattern.

A pure `build_agent_spec_args(role_doc, profile, *, session_path, system_prompt_path)` in a new `deskops/materializers/runtime_profiles.py` does the translation — dict in, tuple out, no filesystem, no subprocess, trivially testable. `AgentSpec.args` already forwards after `--` to `herdr agent start` (`herdr.py:184-189`), so no structural change is needed.

### RunDoc

Extends `StructuredNLDoc` directly, not `PrimitiveDoc`: the latter's `status` means document lifecycle (`draft|active|archived`) and would collide with a run's `outcome`. Fields: `id`, `task_id`, `role_id`, `kind`, `run_dir`, `herdr_pane_id`, `session_path`, `session_sha256`, `started_at`, `ended_at`, `outcome`, `commit_sha`, `tags`, plus `title`/`summary` in the body. `__references__ = ["task_id", "role_id"]`; `kind` stays out of it, being a short join key rather than a document id.

Phasing is decision 4 in the question doc.

### Launching from documents

`deskops/runtime/initializer.py:38-42` currently hardcodes `AgentSpec("executor", kind="pi")` and `AgentSpec("tester", kind="pi")`. These become specs built from each RoleDoc plus its profile. The supervisor, which has a RoleDoc but is never started today, comes up like the others. The session path is injected here.

### Drift check gains real teeth

`deskops drift check` only calls `drift_check_role_docs`. Once that renders from the document, it detects the supervisor discrepancy for the first time. Add two checks: every `RoleDoc.kind` must resolve to a tracked `RuntimeProfileDoc.kind`; and a role setting `tools`/`fallback_models` against a profile with an empty corresponding flag, not listed in `unsupported_role_fields`, is silent capability loss and should be reported.

### Graph

`deskops/graph/extract_docs.py` needs globs for `desk/runtimes` (kind `runtime_profile`) and `desk/runs` (kind `run`), both added to the `_identity_for` set that uses the `id` field as identity.

### Store migration order

`resolve_model_ref` imports live on every invocation, so editing `role.py` takes effect immediately — there is no schema recompile step, and only the two new models need `sldb models add`.

Migrate the three tracked role documents with `sldb docs update` **before** touching the store, then run `sldb models update RoleDoc` for hash housekeeping, then `sldb models add` the new models, then `sldb docs create` the runtime profiles, then `sldb stores check`.

Order matters: `sldb models update` does **not** validate round-trip, and on an extraction exception it silently sets `hash_d = ""` and persists that as the new baseline. Running it against an un-migrated role file would "succeed" while rebaselining a broken hash. `sldb docs update` does validate (`validate_model_input_roundtrip`, raising `SLDBValidationError`) and is the safe path for content migration.

## Verification

- Unit, with no live Herdr: extend the `fake_runner` seam in `tests/test_herdr_runtime.py` for `agent wait` (JSON) and `agent read` (plain text), plus a case proving `timeout=None` no longer collapses to 30s.
- `build_agent_spec_args`: `comma` vs `repeat` joins, `inline` vs `file` delivery, absent flag omitted, `extra_args` appended last.
- `sldb models validate` on all three models, then `sldb stores check` must pass.
- `grep -rn "ROLE_AGENT_SPECS\|kind=\"pi\"" deskops/` returns nothing.
- `deskops drift check` before and after: silent before, reporting after, until re-materialized.
- `tests/test_role_materialization.py` fixtures need the new fields and a `kind="claude"` exclusion case; `tests/test_model_templates.py` gains the two new models; `tests/test_specs.py` needs no change.
- Note `tests/test_cli.py:42` already fails on HEAD, unrelated to this work: commit `529e990` added the `runtime` subcommand without updating the expected list. Fix it in passing or the suite never goes green.
- End to end: `deskops runtime init --agents`, `deskops runtime supervise` in a pane, force an approval prompt — notification arrives, note recorded, task does **not** advance. Then let it finish and confirm `index.jsonl` finally carries non-null `run_id` and `session_sha256`.

## Suggested sequencing

The adapter work (timeout sentinel, `wait`, `read`) touches no models and can be exercised by hand against a throwaway agent before committing to the model migration, which touches the store and needs the documents migrated in the right order.
