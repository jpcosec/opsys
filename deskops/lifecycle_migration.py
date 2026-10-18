"""Move a desk from per-task primitives to the lifecycle graph (deskops/lifecycle.py).

Desks written before the lifecycle graph carry, for every task, a routine under
desk/routines/ and 17 primitives under desk/primitives/, all tracked in the store, and
TaskDocs whose frontmatter holds `routine`, `checklists` and a `current_node` naming one of
those primitives. `deskops desk update --apply` calls `migrate_legacy_lifecycle` to:

- unregister the six retired models together with their tracked documents
  (`sldb.api.remove_model(..., untrack_documents=True)`, structuredLanguageDB >= 0.1.8), then
  delete every routine and primitive file;
- rewrite each task: drop `routine`, `checklists` and the gate facts older versions leaked
  into the frontmatter, and map `current_node` onto the ritual it stood for;
- write the lifecycle graph and refresh the store's indexes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

import yaml

from deskops import doc_io
from deskops import lifecycle

LEGACY_MODELS = ("RoutineDoc", "ConditionDoc", "ChecklistDoc", "OperatorDoc", "EdgeDoc", "HookDoc")
LEGACY_DIRS = (Path("desk") / "routines", Path("desk") / "primitives")
LEGACY_TASK_KEYS = ("routine", "checklists", "closeout_evidence_verified", "pill_graduation_verified")
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# checklist-<task id>-<gate>-ready -> the ritual that gate belonged to
_LEGACY_NODE = re.compile(r"^checklist-.+-(execution|testing|closeout)-ready$")


class LegacyMigrationBlocked(RuntimeError):
    """The store refused a step; nothing irreversible was done for that step."""


@dataclass
class LegacyLifecycleReport:
    primitive_docs: list[Path] = field(default_factory=list)
    tasks_to_rewrite: list[Path] = field(default_factory=list)
    graph_missing: bool = False
    registered_legacy_models: list[str] = field(default_factory=list)

    @property
    def needs_migration(self) -> bool:
        return bool(self.primitive_docs or self.tasks_to_rewrite or self.graph_missing)


def legacy_node_to_ritual(node: str) -> str:
    """The lifecycle node a legacy `current_node` stood for (unchanged if not legacy)."""
    match = _LEGACY_NODE.match(node or "")
    if match:
        return f"ritual-{match.group(1)}"
    return node


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _task_needs_rewrite(path: Path) -> bool:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return False
    data, _ = parsed
    if any(key in data for key in LEGACY_TASK_KEYS):
        return True
    return legacy_node_to_ritual(str(data.get("current_node") or "")) != str(data.get("current_node") or "")


def legacy_registered_models(root: Path) -> list[str]:
    store = root / ".sldb"
    if not store.exists():
        return []
    try:
        from sldb.store.io import load_store_index

        names = {entry.name for entry in load_store_index(store).models}
    except Exception:
        return []
    return [name for name in LEGACY_MODELS if name in names]


def inspect_legacy_lifecycle(root: Path) -> LegacyLifecycleReport:
    root = root.resolve()
    report = LegacyLifecycleReport()
    for directory in LEGACY_DIRS:
        base = root / directory
        if base.exists():
            report.primitive_docs.extend(sorted(base.rglob("*.md")))
    tasks_dir = root / "desk" / "tasks"
    if tasks_dir.exists():
        report.tasks_to_rewrite = [p for p in sorted(tasks_dir.glob("task-*.md")) if _task_needs_rewrite(p)]
    report.graph_missing = (root / ".sldb").exists() and not lifecycle.lifecycle_graph_present(root)
    report.registered_legacy_models = legacy_registered_models(root)
    return report


def _rewrite_task(path: Path) -> bool:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return False
    data, text = parsed
    changed = False
    for key in LEGACY_TASK_KEYS:
        if key in data:
            data.pop(key)
            changed = True
    node = str(data.get("current_node") or "")
    mapped = legacy_node_to_ritual(node)
    if mapped != node:
        data["current_node"] = mapped
        changed = True
    if not changed:
        return False
    body = text[_FRONTMATTER.match(text).end():]
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body, encoding="utf-8")
    return True


def migrate_legacy_lifecycle(root: Path) -> list[str]:
    """Apply the migration; return one line per change. Safe to run twice."""
    root = root.resolve()
    store = root / ".sldb"
    report = inspect_legacy_lifecycle(root)
    changes: list[str] = []

    # The store lets go first: each retired model is unregistered together with its tracked
    # documents (sldb never imports the deleted class). Files are deleted only after that
    # succeeded, so a refusal leaves every file in place and a rerun picks up from there.
    pythonpath = str(Path(__file__).resolve().parents[1])
    if store.exists():
        for name in legacy_registered_models(root):
            try:
                doc_io.remove_model_from(root, name, pythonpath=pythonpath, untrack_documents=True)
            except Exception as exc:
                raise LegacyMigrationBlocked(
                    f"sldb could not unregister {name} with its documents: {exc}. No file was deleted. "
                    "This needs structuredLanguageDB >= 0.1.8."
                ) from exc
            changes.append(f"unregistered model {name} and untracked its documents")
    for path in report.primitive_docs:
        path.unlink()
        changes.append(f"deleted {path.relative_to(root).as_posix()}")
    for directory in LEGACY_DIRS:
        base = root / directory
        if base.exists():
            for sub in sorted((p for p in base.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                if not any(sub.iterdir()):
                    sub.rmdir()
            if not any(base.iterdir()):
                base.rmdir()
                changes.append(f"removed {directory.as_posix()}/")

    for path in report.tasks_to_rewrite:
        if _rewrite_task(path):
            changes.append(f"rewrote {path.relative_to(root).as_posix()} (lifecycle fields)")

    if store.exists():
        for change in lifecycle.ensure_lifecycle_graph(root):
            changes.append(f"lifecycle graph: {change}")
        doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
        changes.append("updated store indexes")
    return changes
