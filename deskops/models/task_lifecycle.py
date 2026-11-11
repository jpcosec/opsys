"""The lifecycle coherence of a task: the table the ``TaskDoc`` validator checks against.

A task's ``status``, ``current_node`` and ``history`` are effects of the lifecycle graph
(``deskops advance``) and of closeout (``deskops closeout``). A write that does not go through
them (``sldb fields update``, ``sldb docs update``, ``sldb serve`` ``/save``) still builds the
document's model, so the model refuses a payload no transition could have produced (CC37).

The table comes from the package, not from a desk's store: the ``RelationDoc`` seeds of
``deskops/data/lifecycle/`` (each edge's ``relation_type``, its target ritual and the
``attributes.sets.status`` it writes; a ``terminal`` edge leads to ``complete``) and the
``entry_node`` of ``deskops/spec/workflows/task_lifecycle.yaml``. A desk's managed copy of
the edges that differs is restored by ``deskops desk update --apply``, so the package is the
source.

A task is coherent in one of three states:

* entry: ``history`` is empty, ``current_node`` is the entry node (or empty, which ``deskops
  advance`` reads as the entry node) and ``status`` is in ``ENTRY_STATUSES``; a task with no
  ``current_node`` is outside the lifecycle and may also hold a drawer status
  (``DRAWER_STATUSES``) or a pre-lifecycle resolved one (``LEGACY_RESOLVED_STATUSES``);
* after a transition: the last ``history`` item is the ``relation_type`` of an edge, and
  ``current_node`` and ``status`` are that edge's target and ``sets.status``;
* closed by closeout: ``(status, last history item)`` is a pair of ``CLOSEOUT_STATES``.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_PACKAGE_DIR = Path(__file__).resolve().parent.parent
LIFECYCLE_SEEDS_DIR = _PACKAGE_DIR / "data" / "lifecycle"
LIFECYCLE_SPEC_PATH = _PACKAGE_DIR / "spec" / "workflows" / "task_lifecycle.yaml"
COMPLETE = "complete"

#: The status a task may hold before its first transition: ``draft``, the ``status_default`` of
#: ``TaskDoc`` that ``compile_task_spec`` writes (``deskops add task`` and the drawer promotion
#: take no status). Every task of the six desks in the entry state holds ``draft`` (CC37 b2/c1);
#: a legacy value found in a desk would be added here, one line each.
ENTRY_STATUSES: frozenset[str] = frozenset({"draft"})

#: The statuses a drawer task outside the lifecycle may also hold (no ``current_node``, empty
#: history): ``deferred``, what ``deskops promote inbox-to-drawer-task`` writes
#: (``services/drawer.py``), and ``candidate``, the status of the 67 drawer candidates of the
#: workspace-documental plan in the deskops desk (``desk/drawer/tasks/workspace-documental/``).
#: Adding ``candidate`` is a revisable decision of the plan coordinator (CC37 c4).
DRAWER_STATUSES: frozenset[str] = frozenset({"deferred", "candidate"})

#: The statuses of a task resolved before the lifecycle existed (no ``current_node``, empty
#: history): what ``deskops closeout retire`` removes (``services/closure.py``, ``close_retired``).
#: ``cancelled`` is the legacy status of the pre-CC31 desks (Governance); adding it is a revisable
#: decision of the plan coordinator (task.debug of legacy states, d1).
LEGACY_RESOLVED_STATUSES: frozenset[str] = frozenset({"resolved", "closed", "done", "complete", "cancelled"})

#: Every status a task outside the lifecycle (``current_node`` and ``history`` empty) may hold.
OUTSIDE_LIFECYCLE_STATUSES: frozenset[str] = ENTRY_STATUSES | DRAWER_STATUSES | LEGACY_RESOLVED_STATUSES

#: ``status`` -> (last ``history`` item, required ``current_node`` or None for any node): the
#: states closeout writes. ``closed`` is the terminal edge ``task_completes`` (it leads to
#: ``complete``; ``deskops advance`` does not persist it and ``closeout commit`` removes the
#: task, so it appears only in a direct write); ``superseded`` and ``resolved`` are recorded by
#: ``deskops closeout supersede`` and ``closeout resolved-by`` from whatever node the task was in.
CLOSEOUT_STATES: dict[str, tuple[str, str | None]] = {
    "closed": ("task_completes", COMPLETE),
    "superseded": ("superseded", None),
    "resolved": ("resolved-by", None),
}

#: The statuses that end a task or keep it outside the lifecycle: what closeout writes
#: (``CLOSEOUT_STATES``, ``superseded`` among them), a pre-lifecycle resolved status and a drawer
#: status. Any other status that is not an entry status is non-terminal (``active``,
#: ``ready_for_testing``, ``blocked``...): with an empty history nothing backs it.
TERMINAL_STATUSES: frozenset[str] = (
    frozenset({"superseded"}) | frozenset(CLOSEOUT_STATES) | LEGACY_RESOLVED_STATUSES | DRAWER_STATUSES
)

#: The status a non-terminal task with an empty history is migrated to (decision of the
#: overlord, 2026-11-11, revisable): no transition and no receipt back its advanced status.
MIGRATED_STATUS = "draft"


@dataclass(frozen=True, slots=True)
class LifecycleEdge:
    relation_type: str
    target: str
    status: str


@dataclass(frozen=True, slots=True)
class LifecycleTable:
    entry_node: str
    edges: dict[str, LifecycleEdge]


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


@lru_cache(maxsize=1)
def lifecycle_table() -> LifecycleTable:
    """The entry node and the edges of the packaged lifecycle graph, by relation type."""
    spec = yaml.safe_load(LIFECYCLE_SPEC_PATH.read_text(encoding="utf-8")) or {}
    entry_node = str(spec.get("entry_node") or "")
    edges: dict[str, LifecycleEdge] = {}
    for path in sorted(LIFECYCLE_SEEDS_DIR.glob("*.md")):
        data = _frontmatter(path.read_text(encoding="utf-8"))
        relation_type = str(data.get("relation_type") or "")
        if not relation_type or "target_id" not in data:
            continue  # a RelationTypeDoc, not an edge
        attributes = data.get("attributes") or {}
        target = COMPLETE if attributes.get("terminal") else str(data["target_id"]).rsplit(":", 1)[-1]
        status = str((attributes.get("sets") or {}).get("status") or "")
        edges[relation_type] = LifecycleEdge(relation_type, target, status)
    return LifecycleTable(entry_node, edges)


def lifecycle_errors(status: str, current_node: str, history: list[str]) -> list[str]:
    """Why ``(status, current_node, history)`` is not a state the lifecycle can produce; ``[]``
    when it is. Each line names the field and the value expected."""
    table = lifecycle_table()
    if not history:
        errors = []
        if current_node not in ("", table.entry_node):
            errors.append(
                f"current_node: '{current_node}' needs a history; with an empty history a task is at "
                f"the entry node '{table.entry_node}'"
            )
        allowed = OUTSIDE_LIFECYCLE_STATUSES if current_node == "" else ENTRY_STATUSES
        where = "and no current_node" if current_node == "" else f"at '{table.entry_node}'"
        if status not in allowed:
            expected = ", ".join(f"'{s}'" for s in sorted(allowed))
            errors.append(
                f"status: '{status}' is not an entry status; a task with an empty history "
                f"{where} has status {expected} (status changes only through deskops "
                "advance and deskops closeout)"
            )
        return errors
    last = str(history[-1])
    closeout = CLOSEOUT_STATES.get(status)
    if closeout is not None and closeout[0] == last and closeout[1] in (None, current_node):
        return []
    edge = table.edges.get(last)
    if edge is None:
        pairs = ", ".join(f"'{h}' for status '{s}'" for s, (h, _) in sorted(CLOSEOUT_STATES.items()))
        return [
            f"history: last item '{last}' is neither a lifecycle transition "
            f"({', '.join(sorted(table.edges))}) nor a closeout record ({pairs})"
        ]
    errors = []
    if current_node != edge.target:
        errors.append(f"current_node: '{current_node}' does not follow history '{last}'; expected '{edge.target}'")
    if status != edge.status:
        errors.append(f"status: '{status}' does not follow history '{last}'; expected '{edge.status}'")
    return errors


#: What the owner of a task the migration table does not cover is told to do (b1).
UNMIGRATABLE_SUGGESTION = (
    "decide its state: deskops closeout supersede --task <id> --reason ... --ref ... if it was "
    "replaced, deskops closeout resolved-by --task <id> --reason ... --ref <commit> --test <file> "
    "if its work is done, or recreate it with deskops add task"
)


def legacy_state_migration(status: str, current_node: str, history: list[str]) -> dict[str, tuple[Any, Any]] | None:
    """The fields that bring a pre-CC31 task to a coherent state, as ``{field: (before, after)}``.

    ``{}`` when the state is already coherent; ``None`` when it is incoherent and the table does
    not decide it (the task's owner does). The table applies to an empty history only:

    * ``superseded``: ``history [superseded]``, the closeout record; ``current_node`` stays;
    * a pre-lifecycle resolved status (``LEGACY_RESOLVED_STATUSES``) or a drawer status
      (``DRAWER_STATUSES``) at a node: ``current_node ''``, outside the lifecycle;
    * a non-terminal status that is not an entry status (not in ``TERMINAL_STATUSES`` nor
      ``ENTRY_STATUSES``): ``status draft`` and, when ``current_node`` is set and is not the entry
      node, ``current_node`` the entry node (an empty one stays empty). ``deskops desk update``
      also prepends ``migration_note`` to the task's summary.

    The result is checked against ``lifecycle_errors``, so it never proposes an incoherent state.
    """
    if not lifecycle_errors(status, current_node, history):
        return {}
    if history:
        return None
    changes: dict[str, tuple[Any, Any]] = {}
    if status == "superseded":
        changes["history"] = ([], ["superseded"])
    elif status in LEGACY_RESOLVED_STATUSES | DRAWER_STATUSES and current_node:
        changes["current_node"] = (current_node, "")
    elif status not in TERMINAL_STATUSES and status not in ENTRY_STATUSES:
        changes["status"] = (status, MIGRATED_STATUS)
        entry_node = lifecycle_table().entry_node
        if current_node and current_node != entry_node:
            changes["current_node"] = (current_node, entry_node)
    else:
        return None
    after_status = changes.get("status", (status, status))[1]
    after_node = changes.get("current_node", (current_node, current_node))[1]
    after_history = changes.get("history", (history, history))[1]
    return None if lifecycle_errors(after_status, after_node, after_history) else changes


def migration_note(status: str, today: date | None = None) -> str:
    """The line the migration of a non-terminal status prepends to the task's summary."""
    day = (today or datetime.now(timezone.utc).date()).isoformat()
    return f"Migrada a draft por deskops desk update: estado heredado '{status}' sin history ({day})."


def summary_with_migration_note(summary: str, status: str, today: date | None = None) -> str:
    """``'<note> <previous summary>'`` on one line; the note alone when the summary was empty."""
    previous = " ".join(str(summary or "").split())
    note = migration_note(status, today)
    return f"{note} {previous}" if previous else note
