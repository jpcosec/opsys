"""Herdr runtime adapter.

This module is deliberately small and semantic-boundary oriented. DeskOps owns
the execution plan; Herdr owns the live workspace, panes and processes. The
adapter never derives Herdr IDs from DeskOps IDs: Herdr is the authority for
runtime handles and returns them in its JSON responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import shlex
import subprocess
from typing import Any, Callable


class HerdrError(RuntimeError):
    """A Herdr command failed or returned an unusable response."""


@dataclass(frozen=True, slots=True)
class ProcessSpec:
    id: str
    command: tuple[str, ...]
    cwd: Path | None = None


@dataclass(frozen=True, slots=True)
class AgentSpec:
    id: str
    kind: str = "pi"
    args: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LayoutPaneSpec:
    id: str
    process: ProcessSpec | None = None
    agent: AgentSpec | None = None
    parent: str = "root"
    direction: str = "right"


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    """The Herdr-facing subset of an Opsys execution plan."""

    desk_id: str
    cwd: Path
    label: str
    panes: tuple[LayoutPaneSpec, ...] = ()


@dataclass(slots=True)
class WorkspaceHandle:
    """Ephemeral Herdr references for one DeskOps desk."""

    desk_id: str
    workspace_id: str
    tab_id: str
    root_pane_id: str
    panes: dict[str, str] = field(default_factory=dict)
    agents: dict[str, str] = field(default_factory=dict)

    def runtime_document(self) -> dict[str, Any]:
        """Return a durable-safe projection without making IDs semantic."""
        return {
            "desk_id": self.desk_id,
            "workspace_id": self.workspace_id,
            "tab_id": self.tab_id,
            "root_pane_id": self.root_pane_id,
            "panes": dict(self.panes),
            "agents": dict(self.agents),
            "identity_note": "Herdr IDs are runtime references; rebuild from the desk plan if absent.",
        }


Runner = Callable[..., subprocess.CompletedProcess[str]]


class HerdrClient:
    """Thin JSON CLI client. Keeping this separate makes the adapter testable."""

    def __init__(self, executable: str = "herdr", *, runner: Runner = subprocess.run, timeout: float = 30.0) -> None:
        self.executable = executable
        self.runner = runner
        self.timeout = timeout

    def call(self, *args: str, timeout: float | None = None) -> dict[str, Any]:
        command = [self.executable, *args]
        try:
            result = self.runner(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout or self.timeout,
            )
        except FileNotFoundError as exc:
            raise HerdrError(f"Herdr executable not found: {self.executable}") from exc
        except subprocess.TimeoutExpired as exc:
            raise HerdrError(f"Herdr command timed out: {shlex.join(command)}") from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise HerdrError(f"{shlex.join(command)}: {detail}")
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise HerdrError(f"Herdr returned non-JSON output for {shlex.join(command)}") from exc
        if not isinstance(payload, dict):
            raise HerdrError(f"Herdr returned an invalid response for {shlex.join(command)}")
        return payload

    def call_text(self, *args: str, timeout: float | None = None) -> str:
        """Run a Herdr command whose successful response is terminal text."""
        command = [self.executable, *args]
        try:
            result = self.runner(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout or self.timeout,
            )
        except FileNotFoundError as exc:
            raise HerdrError(f"Herdr executable not found: {self.executable}") from exc
        except subprocess.TimeoutExpired as exc:
            raise HerdrError(f"Herdr command timed out: {shlex.join(command)}") from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise HerdrError(f"{shlex.join(command)}: {detail}")
        return result.stdout


class HerdrProvider:
    """Translate one DeskOps execution plan into one Herdr workspace."""

    def __init__(self, client: HerdrClient | None = None) -> None:
        self.client = client or HerdrClient()

    def create_workspace(self, plan: ExecutionPlan) -> WorkspaceHandle:
        response = self.client.call(
            "workspace",
            "create",
            "--cwd",
            str(plan.cwd),
            "--label",
            plan.label,
            "--no-focus",
        )
        result = self._result(response)
        workspace_id = self._id(result, "workspace", "workspace_id")
        tab_id = self._id(result, "tab", "tab_id")
        root_pane_id = self._id(result, "root_pane", "pane_id")
        handle = WorkspaceHandle(plan.desk_id, workspace_id, tab_id, root_pane_id)
        handle.panes["root"] = root_pane_id

        for pane in plan.panes:
            pane_id = self._pane(handle, pane.parent)
            if pane.id != "root":
                split = self.client.call(
                    "pane", "split", pane_id,
                    "--direction", pane.direction,
                    "--cwd", str(pane.process.cwd if pane.process and pane.process.cwd else plan.cwd),
                    "--no-focus",
                )
                pane_id = self._id(self._result(split), "pane", "pane_id")
            handle.panes[pane.id] = pane_id
            previous_pane = pane_id
            if pane.process:
                self.start_process(handle, pane.id, pane.process)
            if pane.agent:
                self.start_agent(handle, pane.id, pane.agent)
        return handle

    def start_process(self, workspace: WorkspaceHandle, pane_key: str, spec: ProcessSpec) -> dict[str, Any]:
        pane_id = self._pane(workspace, pane_key)
        command = shlex.join(list(spec.command))
        output = self.client.call_text("pane", "run", pane_id, command)
        return {"output": output}

    def start_agent(self, workspace: WorkspaceHandle, pane_key: str, spec: AgentSpec) -> dict[str, Any]:
        pane_id = self._pane(workspace, pane_key)
        args: list[str] = ["agent", "start", spec.id, "--kind", spec.kind, "--pane", pane_id]
        if spec.args:
            args.extend(["--", *spec.args])
        response = self.client.call(*args, timeout=35.0)
        workspace.agents[spec.id] = pane_id
        return response

    def send(self, workspace: WorkspaceHandle, agent_id: str, message: str, *, wait: bool = False) -> dict[str, Any]:
        args = ["agent", "prompt", agent_id, message]
        if wait:
            args.extend(["--wait", "--timeout", "120000"])
        return self.client.call(*args, timeout=130.0 if wait else None)

    def status(self, workspace: WorkspaceHandle) -> dict[str, Any]:
        return self.client.call("workspace", "get", workspace.workspace_id)

    def attach(self, workspace: WorkspaceHandle) -> dict[str, Any]:
        return self.client.call("workspace", "focus", workspace.workspace_id)

    def stop(self, workspace: WorkspaceHandle) -> dict[str, Any]:
        return self.client.call("workspace", "close", workspace.workspace_id)

    @staticmethod
    def _result(response: dict[str, Any]) -> dict[str, Any]:
        result = response.get("result")
        if not isinstance(result, dict):
            raise HerdrError("Herdr response is missing result object")
        return result

    @staticmethod
    def _id(result: dict[str, Any], key: str, field: str) -> str:
        item = result.get(key)
        if not isinstance(item, dict) or not isinstance(item.get(field), str):
            raise HerdrError(f"Herdr response is missing result.{key}.{field}")
        return item[field]

    @staticmethod
    def _pane(workspace: WorkspaceHandle, pane_key: str) -> str:
        try:
            return workspace.panes[pane_key]
        except KeyError as exc:
            raise HerdrError(f"Unknown pane in desk workspace: {pane_key}") from exc
