"""RunDoc: rellenable por el EJECUTOR, no por deskops. deskops lo lee y valida."""

from pydantic import Field

from sldb import StructuredNLDoc


class RunDoc(StructuredNLDoc):
    __semantics__ = {"type": ["execution", "run"], "workspace": ["desk", "runs"]}
    __containment__ = {}
    __references__ = ["move_id"]
    __template__ = """---
# run-xxx
id: ⸢rev•id⸥
kind: ⸢rev•kind⸥
run_dir: ⸢rev•run_dir⸥
herdr_pane_id: ⸢rev•herdr_pane_id⸥
session_path: ⸢rev•session_path⸥
session_sha256: ⸢rev•session_sha256⸥
started_at: ⸢rev•started_at⸥
ended_at: ⸢rev•ended_at⸥
# in_progress | success | failure | aborted
outcome: ⸢rev•outcome⸥
commit_sha: ⸢rev•commit_sha⸥
# MoveDoc del ledger de pron
move_id: ⸢rev•move_id⸥
model: ⸢rev•model⸥
tokens_in: ⸢rev•tokens_in⸥
tokens_out: ⸢rev•tokens_out⸥
cost_usd: ⸢rev•cost_usd⸥
# e.g., type:run
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Result Summary

⸢rev•result_summary⸥

## Validation Log

⸢rev•validation_log⸥
""".strip()

    id: str = Field(description="Stable run identifier.")
    title: str = Field(description="Short run title.")
    kind: str = Field(description="Run kind.")
    run_dir: str = Field(description="Directory where the run artifacts live.")
    herdr_pane_id: str = Field(description="Herdr pane id for this run.")
    session_path: str = Field(description="Path to the session artifact.")
    session_sha256: str = Field(description="SHA-256 of the session artifact.")
    started_at: str = Field(description="Start timestamp (ISO 8601).")
    ended_at: str = Field(description="End timestamp (ISO 8601).")
    outcome: str = Field(description="Run outcome: in_progress, success, failure, or aborted.")
    commit_sha: str = Field(description="Commit sha the run produced.")
    move_id: str = Field(description="MoveDoc id from pron's ledger.")
    model: str = Field(description="Model used for the run.")
    tokens_in: int = Field(description="Input tokens consumed.")
    tokens_out: int = Field(description="Output tokens produced.")
    cost_usd: float = Field(description="Cost of the run in USD.")
    result_summary: str = Field(description="What today is result-summary.md.")
    validation_log: str = Field(description="What today is validation.log.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )