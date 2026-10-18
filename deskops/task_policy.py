"""Detect global workflow policy restated inside task files.

Task files carry task-local facts: goal, scope, implementation path, validation,
and done-when evidence. Global workflow rules already live in rituals, pills,
``AGENTS.md``, and ``docs/workflow-policy-reference.md``; a task that repeats
them should reference the ritual or pill instead.

This module is review-only. It never edits task files, and ``deskops drift
check`` reports its findings without changing any gate.

Only the Markdown body after the YAML frontmatter is scanned. Fenced code
blocks, inline code spans, and double-quoted examples are skipped because they
demonstrate a phrase instead of asserting it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


TASK_DIRECTORIES = ("desk/tasks", "desk/drawer/tasks")
TASK_GLOB = "task-*.md"

#: Sentence-level phrases that restate global workflow policy.
POLICY_PATTERNS: tuple[str, ...] = (
    r"\b(supervisor|executor)\b.*\b(commit|promote|close)",
    r"\bclosing always requires\b",
    r"\bevery closed task\b",
    r"\bphase\b.*\bgate\b",
    r"\bdo not skip\b",
)

_COMPILED_PATTERNS = tuple(re.compile(pattern, re.IGNORECASE) for pattern in POLICY_PATTERNS)
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_INLINE_CODE = re.compile(r"`[^`]*`")
_DOUBLE_QUOTED = re.compile(r'"[^"\n]*"')


@dataclass(frozen=True)
class TaskPolicyLeak:
    """One task body sentence that repeats a global policy phrase."""

    path: str
    line: int
    phrase: str

    def to_dict(self) -> dict[str, object]:
        return {"path": self.path, "line": self.line, "phrase": self.phrase}


def scan_task_policy_leaks(root: Path) -> list[TaskPolicyLeak]:
    """Report global-policy phrases restated in task bodies under ``root``.

    ``Board.md`` files are routing surfaces, not task files, so they are never
    scanned even though they can mention policy.
    """
    project_root = Path(root)
    leaks: list[TaskPolicyLeak] = []
    for directory in TASK_DIRECTORIES:
        base = project_root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.glob(TASK_GLOB)):
            if path.name == "Board.md":
                continue
            leaks.extend(_scan_file(project_root, path))
    return leaks


def _scan_file(project_root: Path, path: Path) -> list[TaskPolicyLeak]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    body_lines, first_line = _body_after_frontmatter(text)
    relative_path = path.relative_to(project_root).as_posix()
    leaks: list[TaskPolicyLeak] = []
    in_fence = False

    for offset, raw_line in enumerate(body_lines):
        line_number = first_line + offset
        if raw_line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        line = _DOUBLE_QUOTED.sub(" ", _INLINE_CODE.sub(" ", raw_line))
        for sentence in _SENTENCE_SPLIT.split(line):
            phrase = _first_policy_phrase(sentence)
            if phrase is not None:
                leaks.append(TaskPolicyLeak(path=relative_path, line=line_number, phrase=phrase))

    return leaks


def _first_policy_phrase(sentence: str) -> str | None:
    for pattern in _COMPILED_PATTERNS:
        match = pattern.search(sentence)
        if match is not None:
            end = match.end()
            while end < len(sentence) and sentence[end].isalnum():
                end += 1
            return " ".join(sentence[match.start() : end].split())
    return None


def _body_after_frontmatter(text: str) -> tuple[list[str], int]:
    """Return body lines and the 1-based file line of the first body line."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return lines, 1
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[index + 1 :], index + 2
    return lines, 1
