"""A store-backed repo for the closeout tests that write their task by hand (CC33b).

The closeout gate is the task type's ``rule-closeout-<type>`` (a ``RuleDoc`` of the desk's
store) evaluated on the evidence receipts ``deskops closeout verify`` writes, so a task can only
close in a repo whose store carries the lifecycle graph and tracks the task. ``store_repo``
turns the ``lifecycle_desk`` fixture (what ``deskops init`` leaves) into the repo those tests
used to build by hand: ``seed.txt`` and ``.gitignore`` committed with the desk. ``track_task``
tracks a hand-written task under the model of its ``task_type`` (``TaskDoc`` without one).
"""

from __future__ import annotations

from pathlib import Path
import subprocess

from deskops import doc_access
from deskops.models import TaskDoc
from deskops.models.task_types import TASK_TYPE_MODELS


def _git(root: Path, *argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def store_repo(root: Path) -> Path:
    """``lifecycle_desk`` with a committed ``seed.txt``, ``.gitignore`` and desk."""
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    # The store's cache and runtime stay out of git, as in a real desk.
    (root / ".gitignore").write_text(".deskops.log\n.sldb_cache/\n.sldb/runtime/\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")
    return root


def track_task(root: Path, task_id: str) -> None:
    """Track ``desk/tasks/<task_id>.md`` under the model its ``task_type`` names."""
    path = root / "desk" / "tasks" / f"{task_id}.md"
    task_type = str(doc_access.read_doc(path, TaskDoc).get("task_type") or "")
    doc_access.track_created_document(root, TASK_TYPE_MODELS.get(task_type, TaskDoc), path, task_id)
