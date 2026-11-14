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
import re
from typing import Any

import yaml

REGISTER = "deskops desk update --apply"

#: The finding sldb writes for a tracked document its model rejects (inbox 3895e9f7, H1).
INVALID_DOCUMENT_CODE = "store/doc-invalid"

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
    # A missing document is read from its note, where it can be paired into a move. A
    # store/doc-invalid document is named by invalid_document_findings, with its path.
    docs.store_errors = [
        _entry_text(e)
        for e in payload.get("errors") or []
        if not str(_code(e)).endswith(("missing", "doc_invalid"))
    ]
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
    elif note == "doc_invalid":
        pass  # named from sldb's `store/doc-invalid` finding, once, by invalid_document_findings
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


#: The fields of a lifecycle ``RelationDoc`` that govern a transition: a difference there breaks
#: ``deskops advance`` (an error); any other difference of a managed seed is an alert (b1).
TRANSITION_FIELDS = frozenset({"source_id", "target_id", "relation_type", "condition", "attributes"})

#: The write provenance sldb adds to a document it edits (``sldb: {by, at, authority, via}``):
#: not a field of the seed, so it is named only when nothing else differs.
PROVENANCE_KEY = "sldb"


@dataclass(frozen=True)
class SeedDrift:
    """A managed seed of the desk that differs from the deskops package."""

    path: str
    fields: tuple[str, ...]
    governs_transition: bool

    @property
    def line(self) -> str:
        what = ", ".join(self.fields)
        return (
            f"lifecycle seed out of date: {self.path} differs from the deskops package ({what}). "
            f"Fix: {REGISTER}"
        )


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _body(text: str) -> str:
    parts = text.split("---", 2) if text.startswith("---") else ["", "", text]
    return parts[2] if len(parts) == 3 else text


def seed_drift(rel: str, package_text: str, desk_text: str) -> SeedDrift:
    """How the desk's copy of a managed seed differs from the package's: the top-level
    frontmatter keys whose values differ, sorted, without sldb's write provenance; ``body``
    when only the text below the frontmatter differs."""
    package, desk = _frontmatter(package_text), _frontmatter(desk_text)
    differ = sorted(k for k in set(package) | set(desk) if package.get(k) != desk.get(k))
    fields = tuple(k for k in differ if k != PROVENANCE_KEY)
    if not fields:
        fields = ("body",) if _body(package_text) != _body(desk_text) else tuple(differ)
    is_edge = "relation_type" in package and "target_id" in package
    return SeedDrift(rel, fields, is_edge and bool(TRANSITION_FIELDS & set(fields)))


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


def invalid_document_findings(payload: dict[str, Any]) -> list[tuple[str, str]]:
    """``(relative path, what sldb says)`` for each document it names ``store/doc-invalid``.

    Ordered by path. The finding carries the model's rejection (the validator's first errors);
    the path is the one the store tracks for ``<model>:<document>``, so a caller can leave out
    the documents its own frontmatter listing already reported (g3).
    """
    paths = {
        (str(model.get("name") or ""), str(doc.get("name") or "")): str(doc["path"])
        for model in payload.get("models") or []
        for doc in model.get("documents") or []
        if doc.get("path") and doc.get("name")
    }
    found: dict[str, str] = {}
    for entry in payload.get("errors") or []:
        if not isinstance(entry, dict) or entry.get("code") != INVALID_DOCUMENT_CODE:
            continue
        subject = str(entry.get("subject") or "")
        model, _sep, name = subject.partition(":")
        rel = paths.get((model, name or str(entry.get("document") or "")))
        if rel is None:
            match = re.search(r" rejects (.+?): \d+ validation error", str(entry.get("what") or ""))
            rel = match.group(1) if match else ""
        if rel:
            found[rel] = str(entry.get("what") or "its model rejects it")
    return sorted(found.items())


def invalid_task_paths(root: Path) -> set[str]:
    """The task files the frontmatter listing reports, so a store finding does not repeat them."""
    from deskops.workspace import legacy_task_states

    migratable, unmigratable = legacy_task_states(root)
    return {state.rel for state in [*migratable, *unmigratable]}


def invalid_task_findings(root: Path) -> list[str]:
    """One error per task the model rejects, read from its frontmatter so none hides the rest.

    `sldb stores check` names each rejected document as `store/doc-invalid` and goes on; doctor
    reads every task itself, with the file, the validator's text, and what fixes it,
    `deskops desk update --apply` when the migration table decides its state, or the owner's
    decision otherwise (b1).
    """
    from deskops.workspace import legacy_task_states

    migratable, unmigratable = legacy_task_states(root)
    lines = [
        (state.rel, f"Invalid task document: {state.rel}: {'; '.join(state.errors)}. Migrate it with {REGISTER}.")
        for state in migratable
    ]
    lines += [(state.rel, f"Invalid task document: {state.finding()}") for state in unmigratable]
    return [line for _rel, line in sorted(lines)]
