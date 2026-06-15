from __future__ import annotations

from pathlib import Path
import json
import re
from typing import Any

import yaml

from deskops.operations import DeskopsOperations


class PromoteCLI:
    """Promote inbox and drawer items into the next workflow surface."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            return self._inbox_to_drawer_task(root, args.selector, args.title)
        if args.promote_command == "drawer-task-to-active-task":
            return self._drawer_task_to_active_task(
                root,
                args.selector,
                args.title,
                getattr(args, "payload", None),
                getattr(args, "from_yaml", None),
            )
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

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            self._render_drawer_task(
                title=title,
                task_id=task_id,
                source_path=source.relative_to(root),
                body=note["body"],
            ),
            encoding="utf-8",
        )
        source.unlink(missing_ok=True)
        print(f"Created drawer task candidate {task_id}")
        print(f"Deleted source file {source}")
        print(f"Path: {target}")
        return 0

    def _drawer_task_to_active_task(
        self,
        root: Path,
        selector: str,
        title_override: str | None,
        payload_override: str | None = None,
        from_yaml: str | None = None,
    ) -> int:
        source = self._resolve_unique(root / "desk" / "drawer" / "tasks", selector)
        if source is None:
            print(f"No drawer task found for {selector}")
            return 1
        if isinstance(source, list):
            print(f"Ambiguous drawer task selector {selector}: {', '.join(path.stem for path in source)}")
            return 1

        candidate = self._read_markdown(source)
        title = (title_override or candidate["title"] or source.stem).strip()
        task_id = f"task-{self._slug(title)}"
        target = root / "desk" / "tasks" / f"{task_id}.md"
        if target.exists():
            print(f"Active task already exists: {target}")
            return 1

        operations = DeskopsOperations(root)
        
        override_data = {}
        if from_yaml:
            override_data = yaml.safe_load(Path(from_yaml).read_text(encoding="utf-8")) or {}
        elif payload_override:
            override_data = json.loads(payload_override)

        task_payload = {
            "id": override_data.get("id", task_id),
            "title": override_data.get("title", title),
            "status": override_data.get("status", "active"),
            "goal": override_data.get("goal") or self._section(candidate["body"], "Goal") or f"Promote deferred work from {source.name}.",
            "scope": override_data.get("scope") or self._section(candidate["body"], "Scope") or candidate["body"],
            "implementation_path": override_data.get("implementation_path") or f"Promoted from {source.relative_to(root)}.",
            "validation": override_data.get("validation", ["pytest"]),
            "done_when": override_data.get("done_when") or "Promoted work is completed, validated, and closed with a commit.",
            "references": override_data.get("references", [str(source.relative_to(root))]),
            "tags": override_data.get("tags", ["workspace:desk", "artifact:task", "source:drawer"]),
        }

        bundle = operations.create_task_bundle(task_payload)
        source.unlink(missing_ok=True)
        print(f"Created active task bundle {bundle.task_id}")
        print(f"Deleted source file {source}")
        print(f"Task: {bundle.task_path}")
        return 0

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

    def _render_drawer_task(self, *, title: str, task_id: str, source_path: Path, body: str) -> str:
        return "\n".join(
            [
                f"# {title}",
                "",
                f"ID: {task_id}",
                "Status: deferred",
                "Priority: medium",
                "",
                "## Goal",
                "",
                f"Triage and resolve the inbox message promoted from `{source_path}`.",
                "",
                "## Scope",
                "",
                body.strip() or "No additional detail provided.",
                "",
                "## Source",
                "",
                f"- `{source_path}`",
                "",
                "## Done When",
                "",
                "- The message is resolved, answered, or promoted into active work.",
                "",
            ]
        )

    def _section(self, body: str, heading: str) -> str:
        pattern = rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
        match = re.search(pattern, body, flags=re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "task"
