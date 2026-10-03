"""Pure grouping of live Herdr agents by workspace.

No Herdr subprocess or client dependency: this module only reshapes two
already-fetched inventories (``herdr agent list`` and ``herdr workspace
list``) into the order deskops displays them in. Sorting, orphan handling,
and empty-space suppression are all tested here without touching Herdr.
"""

from __future__ import annotations

from typing import Any


def group_agents_by_workspace(
    agents: list[dict[str, Any]],
    workspaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Group agents into spaces, following Herdr's workspace-number order.

    Returns one entry per space that has at least one agent, sorted by the
    workspace ``number`` ascending (Herdr's order), with workers inside each
    space sorted by ``pane_id``. Spaces without agents are omitted.

    Agents whose ``workspace_id`` does not appear in ``workspaces`` are never
    dropped: they land in a trailing group with ``workspace``, ``label``,
    ``number`` and ``status`` all ``None``.
    """
    by_id = {
        item.get("workspace_id"): item
        for item in workspaces
        if isinstance(item, dict) and item.get("workspace_id") is not None
    }
    groups: list[dict[str, Any]] = []
    orphan_workers: list[dict[str, Any]] = []
    for agent in agents:
        workspace = by_id.get(agent.get("workspace_id"))
        if workspace is None:
            orphan_workers.append(agent)
            continue
        group = next(
            (candidate for candidate in groups if candidate["workspace"] == workspace["workspace_id"]),
            None,
        )
        if group is None:
            group = {
                "workspace": workspace["workspace_id"],
                "label": workspace.get("label"),
                "number": workspace.get("number"),
                "status": workspace.get("agent_status"),
                "workers": [],
            }
            groups.append(group)
        group["workers"].append(agent)

    groups.sort(key=lambda group: group["number"] if group["number"] is not None else float("inf"))
    for group in groups:
        group["workers"].sort(key=lambda agent: agent.get("pane_id") or "")

    if orphan_workers:
        orphan_workers.sort(key=lambda agent: agent.get("pane_id") or "")
        groups.append(
            {
                "workspace": None,
                "label": None,
                "number": None,
                "status": None,
                "workers": orphan_workers,
            }
        )
    return groups