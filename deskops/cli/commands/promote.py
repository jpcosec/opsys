from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml

from deskops.operations import parse_task_sections


class PromoteCLI:
    """Promote inbox notes into loose drawer candidates.

    There is deliberately no drawer -> active task promotion. The drawer holds
    disorganized, loosely shaped material; an active task is a compiled bundle
    (TaskDoc, routine, conditions, checklists, operators, edges, board route).
    Converting one into the other mechanically meant filling every required
    field with generic placeholders, producing a task that looked structured
    but was not. A drawer item becomes active work only when someone authors
    the task explicitly with `deskops add task`.
    """

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            return self._inbox_to_drawer_task(root, args.selector, args.title)
        return 1

    def _inbox_to_drawer_task(self, root: Path, selector: str, title_override: str | None) -> int:
        source = self._resolve_unique(root / "desk" / "inbox", selector)
        if source is None:
            print(f"No inbox note found for {selector}")
            return 1
        if isinstance(source, list):
            print(f"Ambiguous inbox note selector {selector}: {', '.join(path.stem for path in source)}")
            return 1

        note = self._read_markdown(source)
        title = (title_override or note["title"] or source.stem).strip()
        task_id = f"task-{self._slug(title)}"
        target = root / "desk" / "drawer" / "tasks" / f"{task_id}.md"
        if target.exists():
            print(f"Drawer task already exists: {target}")
            return 1

        parsed = parse_task_sections(note["body"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            self._render_drawer_task(
                title=title,
                task_id=task_id,
                source_path=source.relative_to(root),
                body=note["body"],
                parsed_sections=parsed,
            ),
            encoding="utf-8",
        )
        # Untrack before deleting: the note is a tracked InboxNoteDoc, so
        # unlinking the file alone leaves an orphan entry in the store and
        # `deskops status` reports it as an invalid missing document. Untrack
        # first so a store failure cannot destroy the source file.
        untrack_message = self._untrack_note(root, source)
        source.unlink(missing_ok=True)
        print(f"Created drawer task candidate {task_id}")
        if untrack_message:
            print(untrack_message)
        print(f"Deleted source file {source}")
        print(f"Path: {target}")
        return 0

    def _untrack_note(self, root: Path, source: Path) -> str | None:
        """Drop the promoted note from the sldb store, best effort.

        Returns a human-readable line describing what happened, or None when
        there is nothing to say. Never raises: a promotion must not be left
        half-done because the store was unavailable."""
        store_path = root / ".sldb"
        if not store_path.exists():
            return None
        try:
            from types import SimpleNamespace

            from sldb.cli.commands.doc import DocCLI

            DocCLI().untrack(SimpleNamespace(store=str(store_path), pythonpath=None, doc=source.stem))
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
