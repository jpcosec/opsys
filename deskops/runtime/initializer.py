from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import time

from deskops.config import DeskConfig
from deskops.materializers.roles import iter_role_doc_paths, load_role_doc
from deskops.materializers.runtime_profiles import build_agent_spec_args, load_runtime_profiles
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
        panes.extend(build_role_agent_panes(root))
    handle = HerdrProvider(client).create_workspace(
        ExecutionPlan(desk_id=desk_config.project_identity, cwd=root, label=desk_config.project_identity, panes=tuple(panes))
    )
    return DeskRuntimeInfo(desk_config.project_identity, len(tasks)), handle


def build_role_agent_panes(root: Path) -> list[LayoutPaneSpec]:
    """One agent pane per tracked RoleDoc, launched with role-derived flags.

    Nothing here is hardcoded to a fixed set of roles or to a single runtime
    kind: every RoleDoc under desk/roles/ gets a pane, and each pane's
    AgentSpec (kind + CLI args) comes from that role plus its matching
    RuntimeProfileDoc. A role whose kind has no tracked profile is skipped
    rather than guessed at; `deskops drift check` reports that gap.
    """
    profiles = load_runtime_profiles(root)
    panes: list[LayoutPaneSpec] = []
    directions = ("right", "down")
    for index, role_path in enumerate(iter_role_doc_paths(root)):
        role_doc = load_role_doc(role_path)
        role_name = role_doc.get("name")
        kind = role_doc.get("kind")
        profile = profiles.get(kind)
        if not role_name or profile is None:
            continue
        args = build_agent_spec_args(role_doc, profile)
        panes.append(
            LayoutPaneSpec(
                role_name,
                parent="root",
                direction=directions[index % len(directions)],
                agent=AgentSpec(role_name, kind=kind, args=args),
            )
        )
    return panes


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
