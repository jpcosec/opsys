"""Issue lookup, status rewrite, and listing.

Issues live under ``desk/issues/`` or ``desk/drawer/issues/`` and are plain
Markdown, not modeled documents. Three status shapes are accepted, in this
order: a YAML frontmatter ``status:`` key, a ``## Status`` section whose body
is the status word, and a ``Status: <word>`` line near the top of the file.

Closing rewrites the status in place and appends a ``## Resolution`` section.
The file is never deleted: it is the trace of why the issue closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from typing import Iterable

import yaml

from deskops import doc_io
from deskops.desk_paths import resolve_selector
from deskops.errors import DomainError


_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
_STATUS_SECTION_RE = re.compile(r"(?m)^##[ \t]+Status[ \t]*\r?\n")
_STATUS_LINE_RE = re.compile(r"(?m)^Status:[ \t]*(.*)$", re.IGNORECASE)
_HEADING_RE = re.compile(r"(?m)^#{1,2}[ \t]+\S")

#: Words accepted as a status. Anything else is treated as an unreadable
#: status so a prose line in a ``## Status`` section is not mistaken for one.
KNOWN_STATUSES = frozenset(
    {
        "open",
        "closed",
        "resolved",
        "done",
        "fixed",
        "verified",
        "implemented",
        "wontfix",
        "blocked",
        "pending",
        "wip",
        "in-progress",
        "in_progress",
        "archived",
    }
)

#: Statuses that count as closed when filtering ``deskops issue list``.
CLOSED_STATUSES = frozenset(
    {
        "closed",
        "resolved",
        "done",
        "fixed",
        "verified",
        "implemented",
        "wontfix",
        "archived",
    }
)


@dataclass(frozen=True)
class Issue:
    """One issue discovered on disk."""

    path: Path
    issue_id: str
    status: str
    title: str


@dataclass(frozen=True)
class IssueCloseResult:
    """Outcome of one issue close, ready for the CLI to print."""

    path: Path
    issue_id: str
    status: str = "closed"


def _relative(path: Path, root: Path | None = None) -> str:
    if root is not None:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def find_issue(root: Path, selector: str) -> Path:
    """Resolve one issue selector across ``desk/issues`` and the drawer.

    Ambiguous and missing selectors keep the shared :mod:`deskops.desk_paths`
    behavior: ``ValueError`` and ``FileNotFoundError`` respectively.
    """
    desk_root = root.resolve() / "desk"
    return resolve_selector(
        desk_root,
        [desk_root / "issues", desk_root / "drawer" / "issues"],
        selector,
        "issue-*.md",
        "issue",
        recursive=True,
    )


def _frontmatter(text: str) -> dict[str, object]:
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        return {}
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _normalize_status(value: object) -> str | None:
    if value is None:
        return None
    token = str(value).strip().strip("\"'").split()
    if not token:
        return None
    word = token[0].strip().lower().rstrip(":")
    return word if word in KNOWN_STATUSES else None


def _frontmatter_status(text: str) -> str | None:
    payload = _frontmatter(text)
    for key, value in payload.items():
        if str(key).lower() == "status":
            return _normalize_status(value)
    return None


def _status_section_span(text: str) -> tuple[int, int] | None:
    match = _STATUS_SECTION_RE.search(text)
    if match is None:
        return None
    body_start = match.end()
    following = _HEADING_RE.search(text[body_start:])
    body_end = body_start + following.start() if following is not None else len(text)
    return body_start, body_end


def _section_status(text: str) -> str | None:
    span = _status_section_span(text)
    if span is None:
        return None
    body = text[span[0] : span[1]]
    for line in body.splitlines():
        if line.strip():
            return _normalize_status(line)
    return None


def _status_line_status(text: str) -> str | None:
    frontmatter = _FRONTMATTER_RE.match(text)
    offset = frontmatter.end() if frontmatter is not None else 0
    body = text[offset:]
    # "Near the top" means before the first level-2 heading. Issue files may
    # put the H1 title above the Status line, as sldb's issues do.
    boundary = re.search(r"(?m)^##[ \t]+\S", body)
    region = body[: boundary.start()] if boundary is not None else body
    for match in _STATUS_LINE_RE.finditer(region):
        status = _normalize_status(match.group(1))
        if status is not None:
            return status
    return None


def issue_status(text: str) -> str | None:
    """The normalized status word, or ``None`` when no format is recognizable."""
    return (
        _frontmatter_status(text)
        or _section_status(text)
        or _status_line_status(text)
    )


def _issue_id(text: str, path: Path) -> str:
    payload = _frontmatter(text)
    for key, value in payload.items():
        if str(key).lower() == "id" and str(value).strip():
            return str(value).strip()
    for line in text.splitlines():
        match = re.match(r"^ID:[ \t]*(\S+)", line)
        if match:
            return match.group(1).strip()
    return path.stem


def _issue_title(text: str) -> str:
    payload = _frontmatter(text)
    for key, value in payload.items():
        if str(key).lower() == "title" and str(value).strip():
            return str(value).strip()
    match = re.search(r"(?m)^#[ \t]+(.+?)[ \t]*$", text)
    return match.group(1).strip() if match is not None else ""


def read_issue(path: Path, *, root: Path | None = None) -> Issue:
    """Read one issue, raising a typed error when its status is unreadable."""
    text = path.read_text(encoding="utf-8")
    status = issue_status(text)
    if status is None:
        raise DomainError(
            f"No recognizable status in issue file {_relative(path, root)}; "
            "expected frontmatter 'status:', a '## Status' section, or a 'Status:' line."
        )
    return Issue(
        path=path,
        issue_id=_issue_id(text, path),
        status=status,
        title=_issue_title(text),
    )


def _set_frontmatter_status(text: str) -> str:
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        return text
    block, count = re.subn(
        r"(?mi)^(status:[ \t]*).*$", r"\g<1>closed", match.group(1), count=1
    )
    if not count:
        return text
    return text[: match.start(1)] + block + text[match.end(1) :]


def _set_section_status(text: str) -> str:
    span = _status_section_span(text)
    if span is None:
        return text
    start, end = span
    lines = text[start:end].splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.strip():
            ending = line[len(line.rstrip("\r\n")) :]
            lines[index] = "closed" + ending
            break
    return text[:start] + "".join(lines) + text[end:]


def _set_status_line(text: str) -> str:
    frontmatter = _FRONTMATTER_RE.match(text)
    offset = frontmatter.end() if frontmatter is not None else 0
    body = text[offset:]
    boundary = re.search(r"(?m)^##[ \t]+\S", body)
    limit = boundary.start() if boundary is not None else len(body)
    region, count = re.subn(
        r"(?mi)^(status:[ \t]*).*$", r"\g<1>closed", body[:limit], count=1
    )
    if not count:
        return text
    return text[:offset] + region + body[limit:]


def _set_status(text: str) -> str:
    """Set every status representation present in ``text`` to ``closed``."""
    changed = _set_frontmatter_status(text)
    changed = _set_section_status(changed)
    return _set_status_line(changed)


def _append_resolution(text: str, reason: str, refs: Iterable[str], today: str) -> str:
    block = [
        "## Resolution",
        "",
        f"Closed: {today}",
        f"Reason: {reason}",
        f"Refs: {', '.join(refs)}",
    ]
    if text and not text.endswith("\n"):
        text += "\n"
    if text and not text.endswith("\n\n"):
        text += "\n"
    return text + "\n".join(block) + "\n"


def _tracked_identity(root: Path, path: Path) -> tuple[str, str] | None:
    """The model and document name already tracking ``path``, if any."""
    from sldb.api import doc_status

    store = root / ".sldb"
    if not store.is_dir():
        return None
    try:
        status = doc_status(store, _relative(path, root))
    except Exception:  # noqa: BLE001 - an unreadable store must not block closing
        return None
    if status is None or not getattr(status, "exists", False):
        return None
    return str(status.model), str(status.name)


def close_issue(
    path: Path,
    reason: str,
    refs: Iterable[str],
    today: str,
    *,
    root: Path | None = None,
    force: bool = False,
) -> IssueCloseResult:
    """Close one issue in place and append its resolution.

    Already-closed issues are refused unless ``force`` is set. The tracked
    document, when present, is retracked after the write so the store hash and
    derived indexes match the file.
    """
    resolved_root = root.resolve() if root is not None else _infer_root(path)
    issue = read_issue(path, root=resolved_root)
    slug = _relative(path, resolved_root)
    if issue.status in CLOSED_STATUSES and not force:
        raise DomainError(
            f"Issue {issue.issue_id} is already closed ({issue.status}): {slug}. "
            "Use --force to close it again."
        )

    normalized_reason = " ".join((reason or "").split())
    if not normalized_reason:
        raise DomainError("Closing an issue needs a non-empty --reason.")

    ref_list = [str(ref).strip() for ref in refs if str(ref).strip()]
    text = path.read_text(encoding="utf-8")
    updated = _set_status(text)
    updated = _append_resolution(updated, normalized_reason, ref_list, today)

    identity = _tracked_identity(resolved_root, path)
    with doc_io.DocTransaction(resolved_root) as transaction:
        transaction.record(path)
        if identity is not None:
            doc_io.untrack(resolved_root, identity[1])
        path.write_text(updated, encoding="utf-8")
        if identity is not None:
            doc_io.track(resolved_root, path, identity[0], name=identity[1])
    return IssueCloseResult(path=path, issue_id=issue.issue_id)


def _infer_root(path: Path) -> Path:
    for parent in [path.parent, *path.parents]:
        if (parent / "desk").is_dir():
            return parent
    return path.parent


def list_issues(root: Path, status: str = "all") -> list[Issue]:
    """List issues from both issue locations, filtered by status group."""
    if status not in {"open", "closed", "all"}:
        raise DomainError(f"Unknown issue status filter: {status}")

    desk_root = root.resolve() / "desk"
    paths: list[Path] = []
    for directory in (desk_root / "issues", desk_root / "drawer" / "issues"):
        if directory.exists():
            paths.extend(directory.rglob("issue-*.md"))
    records = [read_issue(path, root=root) for path in sorted(set(paths))]

    if status == "all":
        return records
    closed = status == "closed"
    return [
        record
        for record in records
        if (record.status in CLOSED_STATUSES) == closed
    ]
