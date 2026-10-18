from __future__ import annotations

from pathlib import Path

from deskops.graph.self_reflection import drift_check_knowledge_surfaces
from deskops.task_policy import TaskPolicyLeak
from deskops.task_policy import scan_task_policy_leaks


def test_leaked_sentence_produces_one_finding(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-leaky.md",
        """---
id: task-leaky
---
# Task

The supervisor commits after review.
""",
    )

    assert scan_task_policy_leaks(tmp_path) == [
        TaskPolicyLeak(path="desk/tasks/task-leaky.md", line=6, phrase="supervisor commits")
    ]


def test_task_local_validation_line_is_not_found(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-local.md",
        """---
id: task-local
---
# Task

Run a task-specific pytest command for the touched module.
""",
    )

    assert scan_task_policy_leaks(tmp_path) == []


def test_frontmatter_is_ignored(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-frontmatter.md",
        """---
id: task-frontmatter
summary: Closing always requires green tests.
---
# Task

Only local facts here.
""",
    )

    assert scan_task_policy_leaks(tmp_path) == []


def test_drawer_tasks_are_scanned(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/drawer/tasks/task-drawer.md",
        """---
id: task-drawer
---
# Task

Every closed task repeats its validation.
""",
    )

    assert [leak.line for leak in scan_task_policy_leaks(tmp_path)] == [6]


def test_regex_and_quoted_examples_are_not_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-example.md",
        """---
id: task-example
---
# Task

Patterns: `\\b(supervisor|executor)\\b.*\\b(commit|promote|close)\\b`.

The quote "The supervisor commits" is only an example.

```text
do not skip the phase gate
```
""",
    )

    assert scan_task_policy_leaks(tmp_path) == []


def test_scanner_does_not_modify_task_bytes(tmp_path: Path) -> None:
    path = tmp_path / "desk/tasks/task-leaky.md"
    write(
        path,
        """---
id: task-leaky
---
# Task

The supervisor commits after review.
""",
    )
    before = path.read_bytes()

    scan_task_policy_leaks(tmp_path)

    assert path.read_bytes() == before


def test_drift_check_reports_task_policy_leak(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-leaky.md",
        """---
id: task-leaky
---
# Task

The supervisor commits after review.
""",
    )

    findings = drift_check_knowledge_surfaces(tmp_path)

    assert (
        "task-policy-leak: desk/tasks/task-leaky.md:6 repeats global policy phrase "
        "'supervisor commits'; reference desk/rituals/closeout.md or a pill instead"
    ) in findings


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
