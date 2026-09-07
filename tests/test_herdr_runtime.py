from __future__ import annotations

import json
from pathlib import Path
import subprocess

from deskops.runtime.herdr import AgentSpec
from deskops.runtime.herdr import ExecutionPlan
from deskops.runtime.herdr import HerdrClient
from deskops.runtime.herdr import HerdrProvider
from deskops.runtime.herdr import LayoutPaneSpec
from deskops.runtime.herdr import ProcessSpec


def test_provider_builds_one_workspace_and_captures_herdr_ids(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def fake_runner(command, **kwargs):
        calls.append(command)
        payloads = {
            "workspace": {"workspace_id": "w-1"},
            "tab": {"tab_id": "t-1"},
            "root_pane": {"pane_id": "w-1:p-1"},
        }
        if command[1:3] == ["workspace", "create"]:
            payload = {"result": payloads}
        elif command[1:3] == ["pane", "split"]:
            payload = {"result": {"pane": {"pane_id": "w-1:p-2"}}}
        elif command[1:3] == ["agent", "start"]:
            payload = {"result": {"agent": {"name": "executor"}}}
        else:
            payload = {"result": {}}
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    plan = ExecutionPlan(
        desk_id="desk-auth",
        cwd=tmp_path,
        label="desk-auth",
        panes=(
            LayoutPaneSpec("root", process=ProcessSpec("editor", ("nvim", "."))),
            LayoutPaneSpec("executor", agent=AgentSpec("executor"), parent="root"),
        ),
    )
    handle = HerdrProvider(HerdrClient(runner=fake_runner)).create_workspace(plan)

    assert handle.workspace_id == "w-1"
    assert handle.tab_id == "t-1"
    assert handle.panes == {"root": "w-1:p-1", "executor": "w-1:p-2"}
    assert handle.agents == {"executor": "w-1:p-2"}
    assert calls[0][0:3] == ["herdr", "workspace", "create"]
    assert calls[1][0:3] == ["herdr", "pane", "run"]
    assert calls[2][0:3] == ["herdr", "pane", "split"]
    assert calls[3][0:3] == ["herdr", "agent", "start"]


def test_runtime_document_marks_ids_as_ephemeral() -> None:
    from deskops.runtime.herdr import WorkspaceHandle

    document = WorkspaceHandle("desk", "w", "t", "p").runtime_document()
    assert document["desk_id"] == "desk"
    assert "runtime references" in document["identity_note"]
