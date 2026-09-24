# Resolve open decisions for the Herdr supervised-execution runtime

ID: question-herdr-runtime-open-decisions
Status: resolved

## Question

Four decisions block implementation of `desk/drawer/features/feature-herdr-supervised-execution-runtime.md`. Each one changes what gets built or what gets committed, and none should be resolved implicitly by whoever writes the code first.

### 1. Which model is canonical for the supervisor role?

**Decision:** Keep the deployed value (`anthropic/claude-opus-4-8`). Reconcile the prose in `desk/roles/deskops-supervisor.md` separately so it points at the frontmatter.

### 2. Do pinned agent session transcripts get committed?

**Decision:** Do not commit the transcripts. We will gitignore `runs/subagents/*/session.jsonl` and commit only the digest and `result-summary.md` to avoid permanently bloating the repository with hundreds of megabytes of JSONL traces.

### 3. Does Herdr supersede tmux in the ad-hoc launcher, or are they separate?

**Decision:** Yes, retarget the existing task onto Herdr. Herdr already provides agent detection and lifecycle states (`idle`/`working`/`blocked`/`done`), and already reports session identity back to the server.

### 4. Does the run record become an sldb document now, or stay `run.yaml`?

**Decision:** Additive phasing is acceptable. Define and register `RunDoc`, write nothing yet. Keep `run.yaml` as the only record for now, and have the manifest drive both later to prevent drift.

## Why It Matters

Decisions 1 and 3 are both instances of the same failure this feature exists to remove: two representations of one fact, with no check that they agree. Resolving them silently during implementation would reintroduce the drift while ostensibly fixing it.

Decision 2 is irreversible in practice — once transcripts are in git history, removing them means rewriting history.

Decision 4 determines whether the durable run record is queryable through the store and the graph, or stays an untracked YAML file outside every validation surface.

## Needs Answer Before

- migrating `RoleDoc` to typed fields
- registering `RunDoc` in the store
- promoting `task-adhoc-subagent-launcher-tmux-multi-cli`
- any `deskops runtime supervise` implementation

## Blocked Surface

`deskops inbox` cannot record these notes today. The command aborts with `Duplicate repository root` because `desk/registry/` holds nine repo documents pointing at this same root — `described-repo`, `repo-deskops-alt`, `deskops-dir`, `deskops`, `my-repo`, `myrepo`, `pythonpath-repo`, `store-test`, `tagged-repo`. All but `deskops` look like stress-test leftovers. Passing `--sender` does not bypass it. Until the registry is deduplicated, coordination intake is unavailable and notes like this one have to live in the drawer.
