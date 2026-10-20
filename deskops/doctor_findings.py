"""What `deskops doctor` finds, split into errors and alerts.

An **error** is something broken: the desk cannot be worked as it is (missing structure, a
store that cannot be read, a document its own model cannot read, an unregistered model, a
tracked document that is gone). It makes `doctor` fail.

An **alert** is the store having moved under an expected change: a document edited, moved or
added by hand, a model contract that changed. Nothing is broken; the store just has not
registered the change yet. An alert does not make `doctor` fail, and it is always printed,
with the command that registers it (`deskops desk update --apply`).

The rule is sldb's (docs/architecture/code-anchoring.md in sldb, section 10); deskops applies
it to the desk so that a file moved or edited is no longer reported as a broken desk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REGISTER = "deskops desk update --apply"

# Per-document notes of `sldb stores check`: the document is fine, or it moved under an
# expected change. Any other note (`missing`, or one this deskops does not know) is an error.
CLEAN_NOTES = frozenset({"ok", "benign_mutation"})
ALERT_NOTES = {
    "data_mutation": "edited since the store indexed it",
    "contract_mutation": "its model's contract changed since it was indexed",
}


@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)
    manual: list[str] = field(default_factory=list)


@dataclass
class StoreDocs:
    """What `sldb stores check --format json` says about the desk's tracked documents."""

    tracked: set[Path] = field(default_factory=set)
    by_model: list[tuple[str | None, Path]] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    missing: list[Path] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    store_alerts: list[str] = field(default_factory=list)
    store_errors: list[str] = field(default_factory=list)


def read_store_check(root: Path, payload: dict[str, Any]) -> StoreDocs:
    """Sort each tracked desk document of a `stores check` payload into clean, changed or broken."""
    docs = StoreDocs()
    for model in payload.get("models", []):
        for doc in model.get("documents", []):
            _read_doc(root, model.get("name"), doc, docs)
    docs.store_alerts = _store_level_alerts(payload)
    # A missing document is read from its note, where it can be paired into a move.
    docs.store_errors = [_entry_text(e) for e in payload.get("errors") or [] if not str(_code(e)).endswith("missing")]
    return docs


def _read_doc(root: Path, model_name: str | None, doc: dict[str, Any], docs: StoreDocs) -> None:
    if not (rel := doc.get("path")):
        return
    path = (root / rel).resolve()
    docs.tracked.add(path)
    if not rel.startswith("desk/"):
        return
    docs.by_model.append((model_name, path))
    note = doc.get("note")
    if note in ALERT_NOTES:
        docs.changed.append(f"{rel} ({ALERT_NOTES[note]})")
    elif note == "missing":
        docs.missing.append(path)
    elif note not in CLEAN_NOTES:
        docs.unknown.append(f"{rel} ({note})")


def _store_level_alerts(payload: dict[str, Any]) -> list[str]:
    """Store-wide moves: the `alerts` sldb reports, or what older sldb versions only implied."""
    if "alerts" in payload:
        return [_entry_text(a) for a in payload.get("alerts") or [] if not _is_document_alert(a)]
    moved = [f"model contract changed: {name}" for name in payload.get("moved_contracts") or []]
    roster = [f"document list of {name} not reindexed" for name in payload.get("roster_only") or []]
    return moved + roster


def _is_document_alert(alert: Any) -> bool:
    """A per-document alert is already reported from that document's note."""
    return str(_code(alert)).endswith(("data_mutation", "contract_mutation"))


def _code(entry: Any) -> str:
    """The entry's code with `-` read as `_`: sldb writes `store/data-mutation`."""
    return str(entry.get("code", "")).replace("-", "_") if isinstance(entry, dict) else ""


def _entry_text(entry: Any) -> str:
    if not isinstance(entry, dict):
        return str(entry)
    subject, what = entry.get("subject") or "", entry.get("what") or entry.get("code") or ""
    return f"{subject}: {what}" if subject else str(what)


def moved_documents(root: Path, missing: list[Path], untracked: list[Path]) -> tuple[list[str], list[Path], list[Path]]:
    """Pair a tracked document that is gone with an untracked one of the same file name.

    That pair is a file moved by hand, an expected change; returns the moves, then what is
    left of each list.
    """
    by_name = {p.name: p for p in untracked}
    moves, gone = [], []
    for old in missing:
        if (new := by_name.pop(old.name, None)) is not None:
            moves.append(f"{old.relative_to(root)} -> {new.relative_to(root)}")
        else:
            gone.append(old)
    return moves, gone, list(by_name.values())


def print_findings(findings: Findings, *, repair: bool) -> None:
    """Errors first, then alerts with the command that registers them, then what was repaired."""
    _section("Errors (the desk is broken):", findings.errors + findings.manual)
    if findings.alerts:
        _section("Alerts (the store moved under an expected change; nothing is broken):", findings.alerts)
        print(f"  register edits, moves and new documents with: {REGISTER}")
    if findings.fixed:
        _section("Repairs applied:", findings.fixed)
    if findings.errors and not repair:
        print("\nRun with --repair to attempt automatic fixes.")


def _section(title: str, lines: list[str]) -> None:
    if lines:
        print(title)
        for line in lines:
            print(f"- {line}")
