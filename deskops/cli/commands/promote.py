from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from deskops.services.drawer import DrawerService


_TASK_SECTION_FIELDS: tuple[tuple[str, str], ...] = (
    ("why", "Rationale"),
    ("goal", "Goal"),
    ("scope", "Scope"),
    ("implementation_path", "Implementation Path"),
    ("validation", "Validation"),
    ("done_when", "Done When"),
)

_TASK_HEADING_TO_FIELD = {heading.lower(): field for field, heading in _TASK_SECTION_FIELDS}

_TASK_SECTION_PLACEHOLDERS = {
    "Rationale": "_Explain why this task exists or the business driver behind it._",
    "Goal": "_Describe the concrete result this task must produce._",
    "Scope": "_State what is in scope and what is out of scope._",
    "Implementation Path": "_Outline the expected implementation route or affected surface._",
    "Validation": "_List the checks required before this task can close._",
    "Done When": "_Name the observable condition that makes the task complete._",
}


def _strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    try:
        _, rest = text.split("---\n", 1)
        _frontmatter, body = rest.split("\n---\n", 1)
    except ValueError:
        return text
    return body


def _parse_task_sections(text: str) -> dict[str, Any]:
    """Read task-shaped headings from a free-form inbox note.

    Inbox notes are not TaskDocs: they have no frontmatter contract and no
    model that can extract them. This private helper only recovers sections
    that happen to look like a task so the drawer candidate preserves them.
    TaskDoc reads never use it; they go through sldb's extractor.
    """
    body = _strip_markdown_frontmatter(text)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    preamble: list[str] = []
    sections: dict[str, str] = {}
    active_heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, active_heading
        if active_heading is None:
            return
        heading = active_heading
        active_heading = None
        field = _TASK_HEADING_TO_FIELD[heading.lower()]
        if field in sections:
            buffer = []
            return
        content = "\n".join(buffer).strip()
        placeholder = _TASK_SECTION_PLACEHOLDERS.get(heading)
        if placeholder:
            content_lines = content.splitlines()
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            if content_lines and content_lines[0].strip() == placeholder:
                content_lines.pop(0)
                while content_lines and not content_lines[0].strip():
                    content_lines.pop(0)
            content = "\n".join(content_lines).strip()
        sections[field] = content
        buffer = []

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            heading = match.group(1).strip()
            if heading.lower() in _TASK_HEADING_TO_FIELD:
                flush()
                active_heading = heading
                continue
        if active_heading is None:
            preamble.append(line)
        else:
            buffer.append(line)
    flush()

    cleaned_preamble = "\n".join(preamble).strip()
    return {
        "fields": sections,
        "preamble": cleaned_preamble,
        "has_task_sections": bool(sections),
    }


class PromoteCLI:
    """Promote inbox notes into loose drawer candidates.

    There is deliberately no drawer -> active task promotion. The drawer holds
    disorganized, loosely shaped material; an active task is a fully authored
    TaskDoc routed on the board and walked through the desk's lifecycle graph.
    Converting one into the other mechanically meant filling every required
    field with generic placeholders, producing a task that looked structured
    but was not. A drawer item becomes active work only when someone authors
    the task explicitly with `deskops add task`.
    """

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            result = DrawerService(root).promote_inbox_to_drawer_task(
                args.selector,
                args.title,
                parse_sections=_parse_task_sections,
            )
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1
