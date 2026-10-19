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
from deskops.models import BoardDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

_DEDICATED_VERBS = (
    ("desk/tasks/", "deskops closeout commit|supersede|retire"),
    ("desk/drawer/", "deskops drawer remove"),
    ("desk/atoms/", "deskops atoms delete"),
    ("desk/registry/", "deskops repo remove"),
)
_REFERENCE_SURFACES = ("desk", "docs")
_REFERENCE_FILES = ("README.md", "AGENTS.md")
#: Paths `deskops doctor` and `deskops desk update` require as the desk's structure.
_REQUIRED_STRUCTURE = frozenset(
    {
        "desk/config.json",
        "desk/drawer",
        "desk/rituals/phase.md",
        "desk/tasks/Board.md",
    }
)


@dataclass(frozen=True)
class RetireResult:
    path: str
    reason: str
    refs: tuple[str, ...]
    boards: tuple[str, ...] = ()


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
    if not relative.startswith("desk/"):
        raise DomainError(f"{relative} is not a file under desk/")
    closed_issue = _is_retirable_drawer_issue(path, relative)
    for prefix, verb in _DEDICATED_VERBS:
        if relative.startswith(prefix) and not closed_issue:
            if relative.startswith("desk/drawer/issues/"):
                verb = "deskops issue close (open issues), then deskops retire"
            raise DomainError(f"{relative} has its own retirement verb: use `{verb}`.")
    if relative in _REQUIRED_STRUCTURE:
        raise DomainError(
            f"{relative} is required desk structure: `deskops doctor` repairs it, so it cannot be retired."
        )
    if not path.is_file():
        raise DomainError(f"{relative} is not a file under desk/")

    reason = " ".join(reason.split())
    if not reason:
        raise DomainError("--reason must not be empty.")
    clean_refs = tuple(ref.strip() for ref in refs if ref.strip())
    if not clean_refs:
        raise DomainError("Give at least one --ref: the commit or file that replaces or resolves this document.")
    unresolved = [ref for ref in clean_refs if not _ref_resolves(root, ref, ref_resolves)]
    if unresolved:
        raise DomainError(f"Unresolvable --ref: {', '.join(unresolved)} (use an ancestor commit or an existing path).")

    updates = _board_pill_updates(root, path, relative)
    drawer_board = root / "desk" / "drawer" / "tasks" / "Board.md"
    unrouted_drawer = closed_issue and drawer_board.is_file() and _drawer_bullets_removed(drawer_board, path.stem) is not None
    if not force:
        skip = _handled_boards(root, updates, path, relative)
        if unrouted_drawer:
            skip.add(drawer_board.resolve())
        inbound = _inbound_references(root, path, relative, skip=skip)
        if inbound:
            raise DomainError(
                f"Refusing to retire {relative}: still referenced by {', '.join(inbound)}. "
                "Update those first, or pass --force."
            )

    with doc_io.DocTransaction(root) as transaction:
        for board_path, payload in updates:
            _write_board(root, board_path, payload)
        if unrouted_drawer:
            transaction.record(drawer_board)
            drawer_board.write_text(_drawer_bullets_removed(drawer_board, path.stem), encoding="utf-8")
        transaction.delete(path)
    boards = [board_path.relative_to(root).as_posix() for board_path, _ in updates]
    if unrouted_drawer:
        boards.append(drawer_board.relative_to(root).as_posix())
    return RetireResult(path=relative, reason=reason, refs=clean_refs, boards=tuple(boards))


def _is_retirable_drawer_issue(path: Path, relative: str) -> bool:
    """A drawer issue that is already closed or resolved, or an archived record."""
    if not relative.startswith("desk/drawer/issues/") or path.suffix != ".md" or not path.is_file():
        return False
    from deskops.services.issues import issue_status

    text = path.read_text(encoding="utf-8")
    if issue_status(text) in {"closed", "resolved"}:
        return True
    return _frontmatter_record(text)


def _frontmatter_record(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    import yaml

    try:
        block = text.split("---\n", 2)[1]
        loaded = yaml.safe_load(block)
    except (IndexError, yaml.YAMLError):
        return False
    return isinstance(loaded, dict) and loaded.get("record") is True


def _drawer_bullets_removed(board: Path, stem: str) -> str | None:
    """The drawer Board without its ``- `<stem>` `` bullets, or None when it has none."""
    text = board.read_text(encoding="utf-8")
    prefix = f"- `{stem}`"
    kept = "".join(line for line in text.splitlines(keepends=True) if not line.startswith(prefix))
    return kept if kept != text else None


def _pill_reference_matches(reference: str, relative: str, stem: str) -> bool:
    return reference in {
        relative,
        f"desk/contexts/{stem}",
        f"desk/contexts/{stem}.md",
        stem,
    }


def _board_pill_updates(root: Path, path: Path, relative: str) -> list[tuple[Path, dict]]:
    """Boards whose ``pills`` list routes ``relative``, with that entry removed."""
    if not relative.startswith("desk/contexts/"):
        return []
    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    updates: list[tuple[Path, dict]] = []
    for board_path in sorted(tasks_dir.glob("*.md")):
        if board_path.name != "Board.md" and not board_path.stem.startswith("board-"):
            continue
        try:
            payload = extract_model_data(BoardDoc, board_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        payload.setdefault("id", board_path.stem)
        pills = [str(item) for item in payload.get("pills") or []]
        kept = [item for item in pills if not _pill_reference_matches(item, relative, path.stem)]
        if kept == pills:
            continue
        payload["pills"] = kept
        updates.append((board_path, payload))
    return updates


def _handled_boards(root: Path, updates: list[tuple[Path, dict]], path: Path, relative: str) -> set[Path]:
    """Boards whose rewrite removes every textual reference to the retired pill."""
    needles = {relative, path.stem}
    handled: set[Path] = set()
    for board_path, payload in updates:
        try:
            rewritten = render_model_markdown(BoardDoc, payload) + "\n"
        except ValueError:
            continue
        if not any(needle in rewritten for needle in needles):
            handled.add(board_path.resolve())
    return handled


def _write_board(root: Path, board_path: Path, payload: dict) -> None:
    from deskops.operations import DeskopsOperations

    DeskopsOperations(root)._write_doc(board_path, BoardDoc, payload)


def _ref_resolves(root: Path, ref: str, ref_resolves) -> bool:
    if ref_resolves is not None:
        return ref_resolves(ref)
    if (root / ref).exists():
        return True
    from deskops.services.closeout_gates import CloseoutGatesService

    return CloseoutGatesService(root).reference_points_to_commit(ref)


def _inbound_references(root: Path, path: Path, relative: str, *, skip: set[Path] | None = None) -> list[str]:
    skip = skip or set()
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
        if candidate.resolve() == path or candidate.resolve() in skip:
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(needle in text for needle in needles):
            found.append(candidate.relative_to(root).as_posix())
    return found
