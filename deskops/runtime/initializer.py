from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import time

from deskops.config import DeskConfig
from deskops.operations import DeskopsOperations
from deskops.runtime.herdr import AgentSpec, ExecutionPlan, HerdrClient, HerdrError
from deskops.runtime.herdr import HerdrProvider, LayoutPaneSpec, ProcessSpec, WorkspaceHandle


@dataclass(frozen=True, slots=True)
class DeskRuntimeInfo:
    identity: str
    task_count: int


def initialize_desk(root: Path, *, agents: bool = False, executable: str = "herdr") -> tuple[DeskRuntimeInfo, WorkspaceHandle | None]:
    root = root.resolve()
    desk_config = DeskConfig.load(root / "desk")
    if desk_config.project_identity == "unknown-project":
        raise ValueError("DeskOps project_identity is not established in desk/config.json")
    tasks = DeskopsOperations(root).list_tasks()
    client = HerdrClient(executable)
    existing = client.call("workspace", "list").get("result", {}).get("workspaces", [])
    for workspace in existing:
        if isinstance(workspace, dict) and workspace.get("label") == desk_config.project_identity:
            return DeskRuntimeInfo(desk_config.project_identity, len(tasks)), None

    panes = [
        LayoutPaneSpec("root", process=ProcessSpec("editor", ("nvim", "."))),
        LayoutPaneSpec("navigator", parent="root", direction="right", process=ProcessSpec("navigator", ("yazi", "."))),
        LayoutPaneSpec("tests", parent="root", direction="down", process=ProcessSpec("tests", ("pytest",))),
    ]
    if agents:
        panes.extend([
            LayoutPaneSpec("executor", parent="root", direction="right", agent=AgentSpec("executor", kind="pi")),
            LayoutPaneSpec("tester", parent="root", direction="down", agent=AgentSpec("tester", kind="pi")),
        ])
    handle = HerdrProvider(client).create_workspace(
        ExecutionPlan(desk_id=desk_config.project_identity, cwd=root, label=desk_config.project_identity, panes=tuple(panes))
    )
    return DeskRuntimeInfo(desk_config.project_identity, len(tasks)), handle


def ensure_herdr_server(executable: str = "herdr") -> None:
    if shutil.which(executable) is None:
        raise HerdrError(f"Herdr executable not found: {executable}")
    client = HerdrClient(executable)
    try:
        if client.call("status", "server", "--json").get("running") is True:
            return
    except HerdrError:
        pass
    subprocess.Popen([executable, "server"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(30):
        try:
            if client.call("status", "server", "--json").get("running") is True:
                return
        except HerdrError:
            pass
        time.sleep(0.2)
    raise HerdrError("Herdr server did not become ready")
