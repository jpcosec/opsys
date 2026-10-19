"""Retire one obsolete desk document, leaving the reason for the commit that removes it.

Kinds with their own lifecycle keep their own verb: tasks close through closeout,
drawer entries through ``drawer remove``, atoms through ``atoms delete`` and registry
entries through ``repo remove``. Everything else under desk/ (pills, inbox notes,
steps, roles, runtimes, faq, logbook, materializations, leftover files) retires here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops import doc_io
from deskops.errors import DomainError

_DEDICATED_VERBS = (
    ("desk/tasks/", "deskops closeout commit|supersede|retire"),
    ("desk/drawer/", "deskops drawer remove"),
    ("desk/atoms/", "deskops atoms delete"),
    ("desk/registry/", "deskops repo remove"),
)
_REFERENCE_SURFACES = ("desk", "docs")
_REFERENCE_FILES = ("README.md", "AGENTS.md")


@dataclass(frozen=True)
class RetireResult:
    path: str
    reason: str
    refs: tuple[str, ...]


def retire_document(
    root: Path,
    target: str,
    reason: str,
    refs: list[str],
    *,
    force: bool = False,
    ref_resolves=None,
) -> RetireResult:
    """Delete one file under desk/ (and its store record) after checking the reason, refs and inbound links."""
    root = root.resolve()
    path = Path(target)
    path = (path if path.is_absolute() else root / path).resolve()
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError as exc:
        raise DomainError(f"{target} is not inside {root}") from exc
    if not relative.startswith("desk/") or not path.is_file():
        raise DomainError(f"{relative} is not a file under desk/")
    for prefix, verb in _DEDICATED_VERBS:
        if relative.startswith(prefix):
            raise DomainError(f"{relative} has its own retirement verb: use `{verb}`.")

    reason = " ".join(reason.split())
    if not reason:
        raise DomainError("--reason must not be empty.")
    clean_refs = tuple(ref.strip() for ref in refs if ref.strip())
    if not clean_refs:
        raise DomainError("Give at least one --ref: the commit or file that replaces or resolves this document.")
    unresolved = [ref for ref in clean_refs if not _ref_resolves(root, ref, ref_resolves)]
    if unresolved:
        raise DomainError(f"Unresolvable --ref: {', '.join(unresolved)} (use an ancestor commit or an existing path).")

    if not force:
        inbound = _inbound_references(root, path, relative)
        if inbound:
            raise DomainError(
                f"Refusing to retire {relative}: still referenced by {', '.join(inbound)}. "
                "Update those first, or pass --force."
            )

    with doc_io.DocTransaction(root) as transaction:
        transaction.delete(path)
    return RetireResult(path=relative, reason=reason, refs=clean_refs)


def _ref_resolves(root: Path, ref: str, ref_resolves) -> bool:
    if ref_resolves is not None:
        return ref_resolves(ref)
    if (root / ref).exists():
        return True
    from deskops.services.closeout_gates import CloseoutGatesService

    return CloseoutGatesService(root).reference_points_to_commit(ref)


def _inbound_references(root: Path, path: Path, relative: str) -> list[str]:
    needles = {relative}
    if path.suffix == ".md":
        needles.add(path.stem)
    found: list[str] = []
    candidates: list[Path] = []
    for surface in _REFERENCE_SURFACES:
        base = root / surface
        if base.is_dir():
            candidates.extend(sorted(base.rglob("*.md")))
    candidates.extend(root / name for name in _REFERENCE_FILES if (root / name).is_file())
    for candidate in candidates:
        if candidate.resolve() == path:
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(needle in text for needle in needles):
            found.append(candidate.relative_to(root).as_posix())
    return found
