from __future__ import annotations

from deskops.runtime.grouping import group_agents_by_workspace


def _agent(
    pane_id: str,
    workspace_id: str,
    *,
    name: str | None = None,
    status: str = "idle",
) -> dict:
    return {
        "pane_id": pane_id,
        "agent": "pi",
        "name": name,
        "agent_status": status,
        "cwd": f"/tmp/{pane_id}",
        "workspace_id": workspace_id,
    }


def _workspace(workspace_id: str, label: str, number: int) -> dict:
    return {
        "workspace_id": workspace_id,
        "label": label,
        "number": number,
        "agent_status": "active",
        "pane_count": 2,
        "focused": False,
    }


def test_group_orders_spaces_by_number_ascending_not_alphabetically() -> None:
    agents = [
        _agent("w-1:p-1", "w-1", name="zed"),
        _agent("w-2:p-1", "w-2", name="alpha"),
        _agent("w-3:p-1", "w-3", name="mid"),
    ]
    # Labels are deliberately in REVERSE alphabetical order relative to their
    # numbers: sorting by label would yield [1]->"zeta" last, so an
    # implementation that sorts alphabetically produces a different order and
    # fails. A fixture whose labels happen to be alphabetical by number cannot
    # tell the two implementations apart.
    workspaces = [
        _workspace("w-1", "alpha", number=3),
        _workspace("w-2", "zeta", number=1),
        _workspace("w-3", "middle", number=2),
    ]

    groups = group_agents_by_workspace(agents, workspaces)

    assert [group["workspace"] for group in groups] == ["w-2", "w-3", "w-1"]
    assert [group["label"] for group in groups] == ["zeta", "middle", "alpha"]
    assert [group["number"] for group in groups] == [1, 2, 3]


def test_group_orders_workers_by_pane_within_each_space() -> None:
    agents = [
        _agent("w-1:p-2", "w-1", name="second"),
        _agent("w-1:p-1", "w-1", name="first"),
        _agent("w-1:p-4", "w-1", name="fourth"),
        _agent("w-1:p-3", "w-1", name="third"),
    ]
    workspaces = [_workspace("w-1", "sldb", number=1)]

    groups = group_agents_by_workspace(agents, workspaces)

    assert [worker["pane_id"] for worker in groups[0]["workers"]] == [
        "w-1:p-1",
        "w-1:p-2",
        "w-1:p-3",
        "w-1:p-4",
    ]


def test_group_keeps_orphan_agents_in_trailing_group_with_null_label() -> None:
    agents = [
        _agent("w-2:p-1", "w-2", name="known"),
        _agent("w-99:p-5", "w-99", name="stray"),
    ]
    workspaces = [_workspace("w-2", "setup", number=1)]

    groups = group_agents_by_workspace(agents, workspaces)

    assert len(groups) == 2
    assert groups[0]["workspace"] == "w-2"
    assert groups[1] == {
        "workspace": None,
        "label": None,
        "number": None,
        "status": None,
        "workers": [agents[1]],
    }


def test_group_skips_workspaces_without_agents() -> None:
    agents = [_agent("w-1:p-1", "w-1", name="only")]

    def make_workspace(workspace_id: str, number: int) -> dict:
        return _workspace(workspace_id, f"label-{workspace_id}", number)

    workspaces = [
        make_workspace("w-1", 2),
        make_workspace("w-2", 1),
        make_workspace("w-3", 3),
    ]

    groups = group_agents_by_workspace(agents, workspaces)

    assert [(group["workspace"], group["label"]) for group in groups] == [("w-1", "label-w-1")]
    assert len(groups) == 1


def test_group_carries_workspace_label_number_and_status_per_space() -> None:
    agents = [_agent("w-1:p-1", "w-1")]
    workspaces = [
        {
            "workspace_id": "w-1",
            "label": "sldb",
            "number": 2,
            "agent_status": "busy",
            "pane_count": 5,
            "focused": True,
        }
    ]

    groups = group_agents_by_workspace(agents, workspaces)

    assert groups[0]["label"] == "sldb"
    assert groups[0]["number"] == 2
    assert groups[0]["status"] == "busy"
    assert len(groups[0]["workers"]) == 1


def test_group_returns_empty_list_for_empty_agents() -> None:
    groups = group_agents_by_workspace([], [_workspace("w-1", "sldb", number=1)])

    assert groups == []