"""Contract tests for CLI subcommands that had no in-process main() coverage."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Callable

import pytest

import deskops.cli.commands.runtime as runtime_module
import deskops.runtime.initializer as initializer_module
from deskops.cli.main import main
from deskops.runtime.herdr import HerdrClient


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str, str]:
    code = main(list(argv))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _add_contract_atom(root: Path, capsys: pytest.CaptureFixture[str]) -> str:
    code, out, err = _run(
        capsys,
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        "Contract rule",
        "--five-wh-one-plus",
        "what",
        "--answer",
        "The CLI contract stays stable.",
    )
    assert code == 0, err
    assert "Created atom atom-contract-rule" in out
    return "atom-contract-rule"


def test_add_faq_doc(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, out, err = _run(
        capsys,
        "add",
        "faq-doc",
        "--root",
        str(lifecycle_desk),
        "--title",
        "CLI contract FAQ",
        "--body",
        "Question?\n\nAnswer.",
    )

    assert code == 0, err
    assert "Created faq faq-cli-contract-faq" in out
    assert (lifecycle_desk / "desk" / "faq" / "faq-cli-contract-faq.md").exists()


def test_atoms_list(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _add_contract_atom(lifecycle_desk, capsys)

    code, out, err = _run(capsys, "atoms", "list", "--root", str(lifecycle_desk))

    assert code == 0, err
    assert "atom-contract-rule | Contract rule" in out


def test_atoms_show(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _add_contract_atom(lifecycle_desk, capsys)

    code, out, err = _run(
        capsys, "atoms", "show", "atom-contract-rule", "--root", str(lifecycle_desk)
    )

    assert code == 0, err
    assert "Atom: atom-contract-rule" in out
    assert "five_wh_one_plus: what" in out


def _fake_herdr_runner(
    calls: list[list[str]],
    *,
    workspaces: list[dict[str, Any]] | None = None,
    agent_status: str = "done",
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """Minimal Herdr stand-in, in the style of tests/test_herdr_runtime.py."""

    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ["workspace", "list"]:
            payload: dict[str, Any] = {"result": {"workspaces": workspaces or []}}
        elif command[1:3] == ["workspace", "create"]:
            payload = {
                "result": {
                    "workspace": {"workspace_id": "w-1"},
                    "tab": {"tab_id": "t-1"},
                    "root_pane": {"pane_id": "w-1:p-1"},
                }
            }
        elif command[1:3] == ["pane", "split"]:
            payload = {"result": {"pane": {"pane_id": "w-1:p-2"}}}
        elif command[1:3] == ["agent", "wait"]:
            payload = {
                "result": {
                    "agent": {"agent_status": agent_status, "state_change_seq": 2},
                    "type": "agent_info",
                }
            }
        else:
            payload = {"result": {}}
        if command[1:3] == ["agent", "read"]:
            return subprocess.CompletedProcess(command, 0, "line one\nline two\n", "")
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    return runner


def _stub_herdr(
    monkeypatch: pytest.MonkeyPatch,
    runner: Callable[..., subprocess.CompletedProcess[str]],
    *,
    stub_initializer: bool = False,
) -> None:
    def factory(executable: str = "herdr") -> HerdrClient:
        return HerdrClient(executable, runner=runner)

    monkeypatch.setattr(runtime_module, "HerdrClient", factory)
    if stub_initializer:
        monkeypatch.setattr(initializer_module, "HerdrClient", factory)


def test_runtime_init(lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[list[str]] = []
    runner = _fake_herdr_runner(calls)
    _stub_herdr(monkeypatch, runner, stub_initializer=True)
    monkeypatch.setattr(runtime_module, "ensure_herdr_server", lambda executable="herdr": None)

    code, out, err = _run(capsys, "runtime", "init", "--root", str(lifecycle_desk))

    assert code == 0, err
    assert "DeskOps identity: repo; tasks discovered: 0" in out
    assert "Created Herdr Space: w-1 (repo)" in out
    assert calls[0] == ["herdr", "workspace", "list"]


@pytest.mark.parametrize(
    ("subcommand", "expected_line", "expected_call"),
    [
        ("status", "w-1 | repo | panes=3", None),
        ("attach", "Focused Herdr Space: w-1 (repo)", ["herdr", "workspace", "focus", "w-1"]),
        ("stop", "Closed Herdr Space: w-1 (repo)", ["herdr", "workspace", "close", "w-1"]),
    ],
    ids=("status", "attach", "stop"),
)
def test_runtime_status_attach_stop(
    lifecycle_desk: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    subcommand: str,
    expected_line: str,
    expected_call: list[str] | None,
) -> None:
    calls: list[list[str]] = []
    runner = _fake_herdr_runner(
        calls,
        workspaces=[{"workspace_id": "w-1", "label": "repo", "pane_count": 3}],
    )
    _stub_herdr(monkeypatch, runner)

    code, out, err = _run(capsys, "runtime", subcommand, "--root", str(lifecycle_desk))

    assert code == 0, err
    assert expected_line in out
    if expected_call is not None:
        assert expected_call in calls


def test_runtime_supervise(lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[list[str]] = []
    runner = _fake_herdr_runner(calls)
    _stub_herdr(monkeypatch, runner)

    code, out, err = _run(
        capsys,
        "runtime",
        "supervise",
        "executor",
        "--root",
        str(lifecycle_desk),
        "--max-iterations",
        "1",
    )

    assert code == 0, err
    assert "[done] executor settled. Recent output:" in out
    assert "[done] executor did not advance any task" in out
    assert ["herdr", "agent", "wait", "executor"] in calls
