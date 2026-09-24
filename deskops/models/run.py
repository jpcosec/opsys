from pydantic import Field

from sldb import StructuredNLDoc


class RunDoc(StructuredNLDoc):
    """One supervised agent execution.

    Additive by design: this document type is defined and registered so it
    can be tracked, drift-checked, and traversed like any other desk
    artifact, but nothing writes it yet. `deskops/cli/commands/closeout.py`
    still writes `run.yaml` and `runs/subagents/index.jsonl` unchanged. The
    next step — having one manifest drive both `run.yaml` and a tracked
    `RunDoc` instead of two independently-maintained records — is tracked in
    `desk/drawer/features/feature-herdr-supervised-execution-runtime.md`.
    """

    __references__ = ["task_id", "role_id"]
    __semantics__ = {"type": ["workflow", "run"], "workspace": ["desk", "runs"]}
    __template__ = """---
# run-xxx
id: ⸢rev•id⸥
# Task identifier this run executed against
task_id: ⸢rev•task_id⸥
# Role identifier dispatched for this run
role_id: ⸢rev•role_id⸥
# Runtime binary identifier, matching RuntimeProfileDoc.kind
kind: ⸢rev•kind⸥
# Run evidence directory, relative to the project root
run_dir: ⸢rev•run_dir⸥
# Herdr pane identifier, empty if not recorded
herdr_pane_id: ⸢rev•herdr_pane_id⸥
# Session/transcript file path, relative to the project root
session_path: ⸢rev•session_path⸥
# SHA-256 digest of the session file
session_sha256: ⸢rev•session_sha256⸥
# ISO 8601 start timestamp
started_at: ⸢rev•started_at⸥
# ISO 8601 end timestamp, empty while in progress
ended_at: ⸢rev•ended_at⸥
# in_progress | success | failure | aborted
outcome: ⸢rev•outcome⸥
# Closeout commit hash, empty until closeout completes
commit_sha: ⸢rev•commit_sha⸥
# e.g. system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this run attempted and its result._

⸢rev•summary⸥
""".strip()

    id: str = Field(description="Stable run identifier, conventionally 'run-<slug>'.")
    title: str = Field(description="Short human-readable label for the run.")
    summary: str = Field(description="Short summary of what this run attempted and its result.")
    task_id: str = Field(description="TaskDoc identifier this run executed against.")
    role_id: str = Field(description="RoleDoc identifier that was dispatched for this run.")
    kind: str = Field(description="Runtime binary identifier used for this run, matching RuntimeProfileDoc.kind.")
    run_dir: str = Field(description="Path to the run evidence directory under runs/subagents/, relative to the project root.")
    herdr_pane_id: str = Field(
        default="", description="Herdr pane identifier the agent ran in; empty if not recorded or the pane no longer exists."
    )
    session_path: str = Field(
        default="", description="Path to the session/transcript file produced by the runtime, relative to the project root."
    )
    session_sha256: str = Field(
        default="",
        description="SHA-256 digest of the session file at the time it was last recorded, matching the closeout commit trailer.",
    )
    started_at: str = Field(description="ISO 8601 timestamp when the run started.")
    ended_at: str = Field(default="", description="ISO 8601 timestamp when the run ended; empty while the run is in progress.")
    outcome: str = Field(default="in_progress", description="Run outcome: in_progress, success, failure, or aborted.")
    commit_sha: str = Field(
        default="", description="Git commit hash of the closeout commit linked to this run; empty until closeout completes."
    )
    tags: list[str] = Field(
        default_factory=list, description="Semantic tags placed at the end, using namespaced forms such as 'system:deskops'."
    )
