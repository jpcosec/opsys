# Ad-hoc subagent launcher (tmux + codex/agy/pi)

## Kind

feature

## Status

drawer / deferred — needs promotion to an active task (or a small task phase) before implementation.

## Problem

Deskops can *describe* task-scoped subagent work (it generates `runs/subagents/<id>/` evidence: `brief.md`, `board.txt`, `task.txt`, `next.txt`, `graph.txt`) and it can *close out* a run (`deskops closeout commit --run-dir ...`). But it cannot **launch** an agent. Today launching is done by hand from an outside harness (the parent assistant's `subagent` tool), so:

- There is no deskops-native way to start a bounded agent against a task.
- Runs are not monitorable from deskops (no live status, no attach).
- The context bundle deskops already knows how to assemble is not actually fed to the launched agent — the operator re-passes it manually.
- Output is captured ad-hoc; there is no uniform "inspect this run later" surface beyond what closeout expects.

## Desired Outcome

A deskops command that launches an ad-hoc, bounded subagent for a task using an external agent CLI (`codex`, `agy`, or `pi`), inside a `tmux` session, with:

1. **Context injection** — reuse the existing bundle builder so the agent starts with `brief.md` + task doc + board + bound pills + linked atoms + linked files + `next` state, instead of a cold prompt.
2. **Monitoring** — list running launches, show live status, and attach to the tmux pane.
3. **Persisted output** — stream the agent's stdout/stderr to `runs/subagents/<id>/console.log` (append-only) so a finished or crashed run is inspectable after the fact, alongside the existing evidence files.
4. **Clean handoff to closeout** — the run dir it produces is directly consumable by `deskops closeout commit`.

## Proposed CLI surface

```
deskops launch <task-selector> --agent {codex|agy|pi} [--model ...] [--role executor] [--root .]
deskops launch list                 # running + recent launches with status
deskops launch status <run-id>      # tmux alive?, last N console lines, evidence files present
deskops launch attach <run-id>      # tmux attach-session to watch live
deskops launch stop <run-id>        # kill tmux session, mark run stopped
```

## Design notes (grounding in what already exists)

- **Run dir contract already exists**: `runs/subagents/<timestamp>-<task-id>/` with `brief.md`, `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `result-summary.md`, `validation.log`, `session.txt`, `run.yaml`. `deskops closeout commit` already validates `board.txt/task.txt/git-status.txt/result-summary.md`. Reuse this exactly; add only `console.log` and a `launch.yaml` (agent, model, tmux session name, pid, started_at, status).
- **Bundle builder**: the logic that currently writes `brief.md`/`board.txt`/`task.txt`/`next.txt` lives near `deskops/cli/commands/closeout.py` + `parser.py`. Extract it into a reusable `deskops/launch/context.py` so both launch and closeout share one bundle contract (avoid a second divergent copy).
- **Headless invocation per CLI** (verified available on this machine):
  - `codex exec "<prompt>"` (non-interactive; alias `codex e`)
  - `agy -p "<prompt>"` / `agy --print` (single prompt, non-interactive; `--print-timeout`, `--output-format stream-json`)
  - `pi -p "<prompt>"` / `pi --print` (non-interactive; `--append-system-prompt <file>`, `--system-prompt`)
- **tmux pattern**: `tmux new-session -d -s deskops-<run-id> '<agent-cmd> 2>&1 | tee runs/subagents/<run-id>/console.log'`. Status = `tmux has-session -t deskops-<run-id>`. Attach = `tmux attach -t ...`. Stop = `tmux kill-session -t ...`.
- **Context feed mechanism differs per CLI**: pi takes `--append-system-prompt <brief-file>`; codex/agy take the prompt as an argument or stdin. The launcher must adapt the bundle into the right injection channel per agent, but assemble the bundle once.

## Scope boundaries (to keep one coherent task)

- IN: single-task launch, run dir + console.log, list/status/attach/stop, context injection from the existing bundle, one adapter per CLI.
- OUT (defer to follow-up drawer tasks): parallel fan-out / phase-level launch, auto-closeout after run, cross-repo launches, retry/resume, resource quotas, non-tmux backends.

## Open questions / ambiguities (resolve before implementation)

1. **Permissions posture**: codex/agy/pi each have their own auto-approve flags (`agy --dangerously-skip-permissions`). Does launch default to sandboxed/interactive-approval, or auto-approve? This is a safety decision.
2. **tmux dependency**: hard-require tmux, or fall back to a detached background process + logfile when tmux is absent?
3. **Prompt/system-prompt shape per agent**: exact injection channel (arg vs stdin vs `--append-system-prompt` file) must be pinned per CLI.
4. **Run id / session naming**: reuse the `<timestamp>-<task-id>` scheme; confirm tmux session-name length/charset limits (task ids are long — may need a short hash).
5. **Role prompts**: should launch pull the RoleDoc materializations (executor/tester/supervisor) that now exist under `desk/roles/` and prepend them to the brief?
6. **Completion signal**: how does launch know a run finished vs stalled? (tmux session exit vs presence of `result-summary.md` vs a sentinel line.)
7. **Concurrency/registry**: where is the list of active launches tracked — scan tmux sessions prefixed `deskops-`, or a `runs/subagents/launches.jsonl` index (mirroring `index.jsonl`)?

## Related surfaces

- `deskops/cli/commands/closeout.py` — run-dir contract + evidence trailers.
- `runs/subagents/index.jsonl` — existing run index; launch index could mirror it.
- `desk/roles/` (RoleDoc materializations) — executor/tester/supervisor role prompts.
- Pills: subagent-execution, task-scoped subagent lanes, real-cli-surfaces-prove-operator-contracts.

## Related atoms (candidates to capture at implementation)

- Launching is a deskops workflow surface; the bundle contract is the single source of context for both launch and closeout.
- Ad-hoc agent runs must persist inspectable output (console.log) independent of the agent's own session storage.
