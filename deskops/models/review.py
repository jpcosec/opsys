"""A review receipt anchored to the contract of the document it reviewed (``ReviewDoc``).

A review is a document, not a fact computed in Python (plan gates-por-tipo, D2): the
``ReviewDoc`` records what was reviewed (``subject``), who ran it and with which engine, the
run evidence under ``runs/``, the input/output hashes, and the verdict written by whoever
operates the desk. ``deskops review`` (GC03) writes the receipt with ``verdict: pending``;
``deskops review dispose`` writes the verdict; ``deskops edit review`` refuses to touch it
because a new review is a new document (DC3).

The subject is a document anchor: ``doc:<Model>:<id>``, pinned by sldb (GO07) with
``@sha256:<contract hash>`` when the receipt is saved through ``save_document_payload``. The
field is declared in ``__doc_anchors__``, not ``__references__``: sldb reads every
``__doc_anchors__`` field as a reference too (the ``^subject`` edge the activation rules walk)
and computes its ``anchor_state`` (``intact``, ``changed``, ``lost``) when it composes the
index. Nothing here fabricates that edge or that state.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import Field, model_validator

from sldb import StructuredNLDoc


REVIEW_ID_PATTERN = r"^review-.+-(preflight|bundle|reproduction|goldens|owner|node)-[0-9]+$"
SUBJECT_PATTERN = r"^(doc:[A-Z][A-Za-z0-9_]*:[^\s:@]+(@sha256:[0-9a-f]{64})?)?$"
SUBJECT_REF_PATTERN = r"^([^\s#]+#node:[A-Za-z0-9_-]+)?$"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

ReviewKind = Literal["preflight", "bundle", "reproduction", "goldens", "owner", "node"]
ReviewVerdict = Literal["pending", "accepted", "rejected", "incomplete"]


class ReviewDoc(StructuredNLDoc):
    """Receipt of one cold review (or another external check) bound to a document contract."""

    #: sldb treats every ``__doc_anchors__`` field as a reference too (GO07) and pins it on
    #: save; no Python here fakes the anchor edge or its state.
    __doc_anchors__ = ["subject"]
    __references__ = []
    __semantics__ = {"type": ["workflow", "review"], "workspace": ["desk", "runs"]}
    __template__ = """---
# review-<task>-<kind>-<n>
id: ⸢rev•id⸥
# preflight | bundle | reproduction | goldens | owner | node
kind: ⸢rev•kind⸥
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: ⸢rev•subject⸥
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ⸢rev•subject_ref⸥
# RuntimeProfileDoc name or "human"
engine: ⸢rev•engine⸥
actor: ⸢rev•actor⸥
# Run evidence directory under runs/, relative to the project root
run_dir: ⸢rev•run_dir⸥
input_sha256: ⸢rev•input_sha256⸥
output_sha256: ⸢rev•output_sha256⸥
# pending | accepted | rejected | incomplete
verdict: ⸢rev•verdict⸥
reason: ⸢rev•reason⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# ISO 8601 timestamp, empty while pending
disposed_at: ⸢rev•disposed_at⸥
disposed_by: ⸢rev•disposed_by⸥
# e.g. workspace:desk
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what was reviewed and the evidence this receipt records._

⸢rev•summary⸥

## Disposition

_Record the verdict rationale and who disposed of the review._

⸢rev•disposition⸥
""".strip()

    id: str = Field(
        description="Stable review identifier: 'review-<task-id>-<kind>-<n>'.",
        pattern=REVIEW_ID_PATTERN,
    )
    title: str = Field(description="Short human-readable label for the review.")
    kind: ReviewKind = Field(description="Review kind: preflight, bundle, reproduction, goldens, or owner.")
    subject: str = Field(
        default="",
        description="Document anchor 'doc:<Model>:<id>' (optionally pinned with @sha256:<hash>); "
        "empty for reviews of plan nodes.",
        pattern=SUBJECT_PATTERN,
    )
    subject_ref: str = Field(
        default="",
        description="Plan-node reference '<plan>/dag.yaml#node:<ID>'; empty when subject names a document.",
        pattern=SUBJECT_REF_PATTERN,
    )
    engine: str = Field(default="", description="RuntimeProfileDoc name that produced the review, or 'human'.")
    actor: str = Field(default="", description="Identity that ran or disposed of the review (deskops/identity.py).")
    run_dir: str = Field(
        default="", description="Run evidence directory under runs/, relative to the project root."
    )
    input_sha256: str = Field(default="", description="SHA-256 of the review input, 64 lowercase hex digits or empty.")
    output_sha256: str = Field(default="", description="SHA-256 of the review output, 64 lowercase hex digits or empty.")
    verdict: ReviewVerdict = Field(
        default="pending", description="Review verdict: pending, accepted, rejected, or incomplete."
    )
    reason: str = Field(default="", description="Why the verdict was reached; required when accepted or rejected.")
    created_at: str = Field(description="ISO 8601 timestamp when the review receipt was created.")
    disposed_at: str = Field(default="", description="ISO 8601 timestamp of the disposition; empty while pending.")
    disposed_by: str = Field(default="", description="Identity that disposed of the review; empty while pending.")
    summary: str = Field(default="", description="What was reviewed and what evidence the receipt records.")
    disposition: str = Field(default="", description="Verdict rationale and who disposed of the review.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'workspace:desk'.",
    )

    @model_validator(mode="after")
    def _validate_review(self) -> "ReviewDoc":
        subject = self.subject.strip()
        subject_ref = self.subject_ref.strip()
        if bool(subject) == bool(subject_ref):
            raise ValueError("exactly one of subject or subject_ref must be non-empty")
        if self.verdict in {"accepted", "rejected"}:
            if not self.reason.strip():
                raise ValueError(f"verdict {self.verdict!r} requires a non-empty reason")
            if not self.disposed_by.strip():
                raise ValueError(f"verdict {self.verdict!r} requires disposed_by")
        if self.verdict == "pending" and (self.disposed_at.strip() or self.disposed_by.strip()):
            raise ValueError("disposed_at and disposed_by must be empty while verdict is pending")
        for field_name in ("input_sha256", "output_sha256"):
            value = getattr(self, field_name).strip()
            if value and not SHA256_PATTERN.fullmatch(value):
                raise ValueError(f"{field_name} must be 64 lowercase hex digits or empty")
        if self.run_dir and self.run_dir != "runs" and not self.run_dir.startswith("runs/"):
            raise ValueError("run_dir must be relative to the project root and under runs/")
        return self
