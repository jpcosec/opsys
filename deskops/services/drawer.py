"""Drawer lookup and inbox-to-drawer promotion.

The drawer holds disorganized material (features, issues, questions, loose task
candidates). This service resolves a drawer file by selector, records a task's
drawer origin, and promotes an inbox note into a loose drawer task candidate.
It never promotes drawer material into an active task.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
import re
from typing import Any

import yaml
from sldb.runtime.validation import extract_model_data

from deskops import doc_io
from deskops.models import TaskDoc
from deskops.operations import parse_task_sections


@dataclass
class DrawerPromotion:
    """Outcome of one inbox-to-drawer promotion, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


@dataclass
class DrawerRemoval:
    """Outcome of removing one drawer entry, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


class DrawerService:
    DRAWER_INDEX_FILES = {"README.md", "Board.md"}

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    def resolve_drawer_source(self, selector: str) -> Path:
        """The desk/drawer/ file a task is being authored from.

        Accepts a path (relative to the repo root, or absolute) or a stem /
        unique slug fragment searched across every drawer subfolder, since the
        drawer holds features, issues and questions, not only task candidates.
        The file must live under desk/drawer/.
        """
        drawer_root = (self.desk_root / "drawer").resolve()
        candidate = Path(selector)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            resolved = candidate.resolve()
            if drawer_root not in resolved.parents:
                raise ValueError(f"--from-drawer must point inside desk/drawer/: {selector}")
            return resolved
        if not drawer_root.exists():
            raise FileNotFoundError(f"No drawer found at {drawer_root}")
        files = sorted(
            path for path in drawer_root.rglob("*.md")
            if path.is_file() and path.name not in self.DRAWER_INDEX_FILES
        )
        exact = [path for path in files if selector in {path.name, path.stem}]
        matches = exact or [path for path in files if selector.lower() in path.stem.lower()]
        if not matches:
            raise FileNotFoundError(f"No drawer file matches '{selector}'")
        if len(matches) > 1:
            listing = ", ".join(str(path.relative_to(drawer_root)) for path in matches)
            raise ValueError(f"Ambiguous drawer selector '{selector}': {listing}")
        return matches[0].resolve()

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        """Record where an authored task came from, without copying or deleting it.

        Stored in the task's own from_drawer field, not in references:
        `deskops edit task <id> references ...` replaces that whole list (the
        closeout step does exactly that), which would silently drop the origin.
        One field, one fact -- no parallel tag that could drift from it.
        Cleanup of the drawer file is left to a human."""
        relative = drawer_file.resolve().relative_to(self.root.resolve()).as_posix()
        return {**payload, "from_drawer": relative}

    def promote_inbox_to_drawer_task(
        self,
        selector: str,
        title_override: str | None = None,
    ) -> DrawerPromotion:
        """Promote one inbox note into a loose drawer task candidate."""
        source = self._resolve_unique(self.desk_root / "inbox", selector)
        if source is None:
            return DrawerPromotion(1, [f"No inbox note found for {selector}"])
        if isinstance(source, list):
            listing = ", ".join(path.stem for path in source)
            return DrawerPromotion(1, [f"Ambiguous inbox note selector {selector}: {listing}"])

        note = self._read_markdown(source)
        title = (title_override or note["title"] or source.stem).strip()
        task_id = f"task-{self._slug(title)}"
        target = self.desk_root / "drawer" / "tasks" / f"{task_id}.md"
        if target.exists():
            return DrawerPromotion(1, [f"Drawer task already exists: {target}"])

        parsed = parse_task_sections(note["body"])
        messages = [f"Created drawer task candidate {task_id}"]
        with doc_io.DocTransaction(self.root) as transaction:
            transaction.record(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                self._render_drawer_task(
                    title=title,
                    task_id=task_id,
                    source_path=source.relative_to(self.root),
                    body=note["body"],
                    parsed_sections=parsed,
                ),
                encoding="utf-8",
            )
            # Untrack before deleting: the note is a tracked InboxNoteDoc, so
            # unlinking the file alone leaves an orphan entry in the store and
            # `deskops status` reports it as an invalid missing document.
            # Untrack first so a store failure cannot destroy the source file.
            untrack_message = self._untrack_note(transaction, source)
            source.unlink(missing_ok=True)
        if untrack_message:
            messages.append(untrack_message)
        messages.append(f"Deleted source file {source}")
        messages.append(f"Path: {target}")
        return DrawerPromotion(0, messages)

    def remove_entry(self, selector: str, *, force: bool = False) -> DrawerRemoval:
        """Remove one drawer file, its tracking, and its bullets on the drawer board.

        A task in desk/tasks/ that records the entry in from_drawer blocks the
        removal unless force is set, so deleting the source cannot silently
        leave active work pointing at a file someone still expects to exist.
        """
        try:
            source = self.resolve_drawer_source(selector)
        except (FileNotFoundError, ValueError) as exc:
            return DrawerRemoval(1, [f"Error: {exc}"])

        relative = source.relative_to(self.root).as_posix()
        if not force:
            owners = self._tasks_recording(relative)
            if owners:
                listing = ", ".join(owners)
                return DrawerRemoval(
                    1,
                    [
                        f"Error: refusing to remove {relative}: "
                        f"task records it in from_drawer ({listing}). Use --force to remove it anyway."
                    ],
                )

        board = self.desk_root / "drawer" / "tasks" / "Board.md"
        board_changed = False
        with doc_io.DocTransaction(self.root) as transaction:
            if board.exists():
                original = board.read_text(encoding="utf-8")
                updated = self._without_entry_bullets(original, source.stem)
                if updated != original:
                    transaction.record(board)
                    board.write_text(updated, encoding="utf-8")
                    board_changed = True
            transaction.delete(source)

        messages = [f"Removed drawer entry {relative}"]
        if board_changed:
            messages.append(f"Removed its bullets from {board.relative_to(self.root).as_posix()}")
        return DrawerRemoval(0, messages)

    def _tasks_recording(self, relative: str) -> list[str]:
        """Active task ids in desk/tasks/ whose from_drawer points at relative."""
        tasks_dir = self.desk_root / "tasks"
        if not tasks_dir.exists():
            return []
        owners: list[str] = []
        for path in sorted(tasks_dir.glob("task-*.md")):
            try:
                payload = extract_model_data(TaskDoc, path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 - one unreadable task must not block the check
                continue
            if payload.get("from_drawer") == relative:
                owners.append(str(payload.get("id") or path.stem))
        return owners

    def _without_entry_bullets(self, text: str, stem: str) -> str:
        """Drop every line that starts with ``- `<stem>` ``."""
        prefix = f"- `{stem}` "
        return "".join(
            line for line in text.splitlines(keepends=True) if not line.startswith(prefix)
        )

    def _untrack_note(self, transaction: doc_io.DocTransaction, source: Path) -> str | None:
        """Drop the promoted note from the sldb store, best effort.

        Returns a human-readable line describing what happened, or None when
        there is nothing to say. Never raises: a promotion must not be left
        half-done because the store was unavailable."""
        store_path = self.root / ".sldb"
        if not store_path.exists():
            return None
        try:
            transaction.untrack(source.stem)
            return None
        except Exception as exc:  # noqa: BLE001 - store problems must not abort the promotion
            return f"Warning: could not untrack '{source.stem}' from the store: {exc}"

    def _resolve_unique(self, directory: Path, selector: str) -> Path | list[Path] | None:
        if not directory.exists():
            return None
        candidates = sorted(directory.glob("*.md"))
        exact = [path for path in candidates if selector in {path.name, path.stem}]
        if exact:
            return exact[0] if len(exact) == 1 else exact
        lowered = selector.lower()
        matches = [path for path in candidates if lowered in path.stem.lower()]
        if not matches:
            return None
        return matches[0] if len(matches) == 1 else matches

    def _read_markdown(self, path: Path) -> dict[str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, Any] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else str(frontmatter.get("title") or path.stem)
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return {"title": title, "body": content}

    def _render_drawer_task(
        self,
        *,
        title: str,
        task_id: str,
        source_path: Path,
        body: str,
        parsed_sections: dict[str, Any],
    ) -> str:
        fields = parsed_sections["fields"]
        scope = fields.get("scope") or body.strip() or "No additional detail provided."
        lines = [
            f"# {title}",
            "",
            f"ID: {task_id}",
            "Status: deferred",
            "Priority: medium",
            "",
        ]

        if fields.get("why"):
            lines.extend(["## Rationale", "", fields["why"], ""])
        lines.extend([
            "## Goal",
            "",
            fields.get("goal") or f"Triage and resolve the inbox message promoted from `{source_path}`.",
            "",
            "## Scope",
            "",
            scope,
            "",
        ])
        if fields.get("implementation_path"):
            lines.extend(["## Implementation Path", "", fields["implementation_path"], ""])
        if fields.get("validation"):
            lines.extend(["## Validation", "", fields["validation"], ""])
        lines.extend([
            "## Source",
            "",
            f"- `{source_path}`",
            "",
            "## Done When",
            "",
            fields.get("done_when") or "- The message is resolved, answered, or promoted into active work.",
            "",
        ])
        return "\n".join(lines)

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "task"
