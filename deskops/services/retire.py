"""Retire one obsolete desk document, leaving the reason for the commit that removes it.

Kinds with their own lifecycle keep their own verb: tasks close through closeout,
drawer entries through ``drawer remove``, atoms through ``atoms delete`` and registry
entries through ``repo remove``. Everything else under desk/ (pills, inbox notes,
steps, roles, runtimes, faq, logbook, materializations, leftover files) retires here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops import doc_access
from deskops.errors import DomainError
from deskops.services.references import referrers_of
from deskops.services.references import rewrite_referrers

_DEDICATED_VERBS = (
    ("desk/tasks/", "deskops closeout commit|supersede|retire"),
    ("desk/drawer/", "deskops drawer remove"),
    ("desk/atoms/", "deskops atoms delete"),
    ("desk/registry/", "deskops repo remove"),
)
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
    #: The files the retired document was removed from: the Boards and tasks whose fields named it, and the drawer Board.
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
    """Delete one file under desk/ (and its store record) after checking the reason, refs and inbound links.

    The declared fields that name it (`sldb.api.referrers`: a Board's or a task's `pills`) lose that
    entry in the same transaction that deletes it, so a failure leaves every file as it was. A
    mention in prose is never rewritten: it refuses the retirement unless `force` is given.
    """
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

    drawer_board = root / "desk" / "drawer" / "tasks" / "Board.md"
    unrouted_drawer = closed_issue and drawer_board.is_file() and _drawer_bullets_removed(drawer_board, path.stem) is not None
    if not force:
        # Declared fields (a Board's or a task's `pills`) are removed below; a mention in prose is never rewritten.
        excluded = (drawer_board,) if unrouted_drawer else ()
        kept = [item.path for item in referrers_of(root, path, excluded=excluded) if item.referrer.origin != "schema"]
        if kept:
            raise DomainError(
                f"Refusing to retire {relative}: still referenced by {', '.join(dict.fromkeys(kept))}. "
                "Update those first, or pass --force."
            )

    with doc_access.desk_transaction(root) as transaction:
        unrouted = rewrite_referrers(root, path, None, transaction=transaction)
        if unrouted_drawer:
            if transaction is not None:
                transaction.record(drawer_board)
            drawer_board.write_text(_drawer_bullets_removed(drawer_board, path.stem), encoding="utf-8")
        doc_access.delete_doc(root, path)
    boards = list(dict.fromkeys(location.rsplit(" (", 1)[0] for location in unrouted))
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


def _ref_resolves(root: Path, ref: str, ref_resolves) -> bool:
    if ref_resolves is not None:
        return ref_resolves(ref)
    if (root / ref).exists():
        return True
    from deskops.services.closeout_gates import CloseoutGatesService

    return CloseoutGatesService(root).reference_points_to_commit(ref)
