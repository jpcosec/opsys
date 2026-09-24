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


def test_wait_repeats_until_flag_per_state(tmp_path: Path) -> None:
    """Regression: --until must be repeated per state, never joined with '|'.

    Herdr's CLI rejects a single '--until a|b' argument outright ("invalid
    agent status"); it only accepts repeated '--until a --until b' flags.
    """
    calls: list[list[str]] = []

    def fake_runner(command, **kwargs):
        calls.append(command)
        payload = {"result": {"agent": {"agent_status": "blocked"}, "type": "agent_info"}}
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    provider = HerdrProvider(HerdrClient(runner=fake_runner))
    result = provider.wait("executor", until=("idle", "blocked"), timeout_ms=5000)

    assert calls[0] == ["herdr", "agent", "wait", "executor", "--until", "idle", "--until", "blocked", "--timeout", "5000"]
    assert result["agent"]["agent_status"] == "blocked"


def test_wait_with_no_timeout_ms_waits_indefinitely_on_the_client_side() -> None:
    """Regression: wait() must not silently cap an unbounded wait at 30s.

    HerdrClient defaults to a 30s subprocess timeout. wait() explicitly opts
    out of that by passing timeout=None, which must reach subprocess.run as
    a real None (block forever), not collapse back to the 30s default.
    """
    captured: dict[str, object] = {}

    def fake_runner(command, **kwargs):
        captured["timeout"] = kwargs.get("timeout")
        payload = {"result": {"agent": {"agent_status": "idle"}, "type": "agent_info"}}
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    provider = HerdrProvider(HerdrClient(runner=fake_runner, timeout=30.0))
    provider.wait("executor")

    assert captured["timeout"] is None


def test_wait_reports_timeout_as_status_instead_of_raising() -> None:
    def timing_out_runner(command, **kwargs):
        raise subprocess.TimeoutExpired(cmd=command, timeout=kwargs.get("timeout") or 0)

    provider = HerdrProvider(HerdrClient(runner=timing_out_runner))
    result = provider.wait("executor", until=("blocked",), timeout_ms=5000)

    assert result["agent"]["agent_status"] == "timeout"


def test_read_uses_call_text_because_herdr_agent_read_returns_plain_text() -> None:
    """Regression: `herdr agent read` prints raw terminal output, not JSON.

    Routing it through HerdrClient.call (which json.loads()s stdout) raises
    'Herdr returned non-JSON output' on every real invocation.
    """
    calls: list[list[str]] = []

    def fake_runner(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "$ some prompt\nnot json at all\n", "")

    provider = HerdrProvider(HerdrClient(runner=fake_runner))
    output = provider.read("executor", source="detection", lines=40)

    assert output == "$ some prompt\nnot json at all\n"
    assert calls[0] == ["herdr", "agent", "read", "executor", "--source", "detection", "--lines", "40"]


def test_call_distinguishes_omitted_timeout_from_explicit_none() -> None:
    """Regression: timeout=None must mean 'no limit', not 'use the default'.

    The original bug used `timeout or self.timeout`, so passing timeout=None
    silently fell back to the 30s default; a caller had no way to actually
    request an unbounded wait. A prior fix changed the `or` to an `if ... is
    not None`, which still could not distinguish "omitted" from "explicit
    None" because both are indistinguishable once the parameter default
    itself is None. HerdrClient must use a sentinel default instead.
    """
    captured: list[object] = []

    def fake_runner(command, **kwargs):
        captured.append(kwargs.get("timeout"))
        return subprocess.CompletedProcess(command, 0, "{}", "")

    client = HerdrClient(runner=fake_runner, timeout=30.0)

    client.call("agent", "list")
    assert captured[-1] == 30.0, "omitting timeout should use the client default"

    client.call("agent", "wait", "x", timeout=None)
    assert captured[-1] is None, "explicit timeout=None must mean unlimited, not the default"

    client.call("agent", "start", "x", timeout=35.0)
    assert captured[-1] == 35.0, "an explicit numeric timeout must be respected"


def test_notify_sends_notification_show_with_body_and_sound() -> None:
    calls: list[list[str]] = []

    def fake_runner(command, **kwargs):
        calls.append(command)
        payload = {"result": {"reason": "shown", "shown": True, "type": "notification_show"}}
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    provider = HerdrProvider(HerdrClient(runner=fake_runner))
    result = provider.notify("executor blocked", body="waiting on input")

    assert calls[0] == ["herdr", "notification", "show", "executor blocked", "--body", "waiting on input", "--sound", "request"]
    assert result["result"]["shown"] is True
