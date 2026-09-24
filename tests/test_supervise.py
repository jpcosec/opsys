from __future__ import annotations

import json
import subprocess

from deskops.runtime.herdr import HerdrClient, HerdrProvider
from deskops.runtime.supervise import run_supervise_loop, supervise_once


def _agent_info_runner(states: list[tuple[str, int]]):
    """Fake Herdr runner returning one canned agent_status/state_change_seq
    pair per call to `agent wait`, in order; `agent read` returns a fixed
    excerpt string so tests can assert it was (or wasn't) fetched."""
    calls: list[list[str]] = []
    remaining = iter(states)

    def runner(command, **kwargs):
        calls.append(command)
        if command[1:3] == ["agent", "wait"]:
            status, seq = next(remaining)
            payload = {"result": {"agent": {"agent_status": status, "state_change_seq": seq}, "type": "agent_info"}}
            return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")
        if command[1:3] == ["agent", "read"]:
            return subprocess.CompletedProcess(command, 0, "excerpt text\n", "")
        raise AssertionError(f"unexpected command: {command}")

    return runner, calls


def test_supervise_once_treats_unchanged_seq_as_not_new() -> None:
    """Regression: verified against live Herdr that `agent wait --until idle`
    on an already-idle agent returns instantly with the SAME state; a caller
    must not treat that as a fresh event or it busy-loops."""
    runner, calls = _agent_info_runner([("idle", 42)])
    provider = HerdrProvider(HerdrClient(runner=runner))

    outcome = supervise_once(provider, "executor", last_seq=42)

    assert outcome.is_new_event is False
    assert outcome.status == "idle"
    # A duplicate settle must not trigger a read() of the pane.
    assert all(c[1:3] != ["agent", "read"] for c in calls)


def test_supervise_once_treats_new_seq_as_new_and_reads_on_blocked() -> None:
    runner, calls = _agent_info_runner([("blocked", 43)])
    provider = HerdrProvider(HerdrClient(runner=runner))

    outcome = supervise_once(provider, "executor", last_seq=42)

    assert outcome.is_new_event is True
    assert outcome.status == "blocked"
    assert outcome.excerpt == "excerpt text\n"
    assert any(c[1:3] == ["agent", "read"] for c in calls)


def test_supervise_once_does_not_read_on_idle() -> None:
    """idle is a genuine new event but not one the supervisor escalates on;
    no need to pay for a read() of the pane."""
    runner, calls = _agent_info_runner([("idle", 43)])
    provider = HerdrProvider(HerdrClient(runner=runner))

    outcome = supervise_once(provider, "executor", last_seq=42)

    assert outcome.is_new_event is True
    assert outcome.excerpt == ""
    assert all(c[1:3] != ["agent", "read"] for c in calls)


def test_run_supervise_loop_skips_duplicate_settles_without_calling_handlers() -> None:
    """The core busy-loop regression test: three consecutive wait() calls
    all reporting the SAME state_change_seq must dispatch on_blocked at most
    once, and must back off (sleep) on the duplicates instead of spinning."""
    runner, _ = _agent_info_runner([("blocked", 7), ("blocked", 7), ("blocked", 7)])
    provider = HerdrProvider(HerdrClient(runner=runner))
    blocked_calls: list[object] = []
    sleeps: list[float] = []

    run_supervise_loop(
        provider,
        "executor",
        max_iterations=3,
        on_blocked=blocked_calls.append,
        sleep=sleeps.append,
    )

    assert len(blocked_calls) == 1
    assert len(sleeps) == 2  # the two duplicate iterations backed off


def test_run_supervise_loop_dispatches_each_new_transition() -> None:
    runner, _ = _agent_info_runner([("blocked", 1), ("blocked", 1), ("done", 2)])
    provider = HerdrProvider(HerdrClient(runner=runner))
    blocked_calls: list[object] = []
    done_calls: list[object] = []

    outcomes = run_supervise_loop(
        provider,
        "executor",
        max_iterations=3,
        on_blocked=blocked_calls.append,
        on_done=done_calls.append,
        sleep=lambda _seconds: None,
    )

    assert len(blocked_calls) == 1
    assert len(done_calls) == 1
    assert [o.status for o in outcomes] == ["blocked", "done"]


def test_run_supervise_loop_stops_on_timeout_without_reaching_max_iterations() -> None:
    def timing_out_runner(command, **kwargs):
        if command[1:3] == ["agent", "wait"]:
            raise subprocess.TimeoutExpired(cmd=command, timeout=0)
        raise AssertionError(f"unexpected command: {command}")

    provider = HerdrProvider(HerdrClient(runner=timing_out_runner))

    outcomes = run_supervise_loop(provider, "executor", max_iterations=100, sleep=lambda _s: None)

    assert len(outcomes) == 1
    assert outcomes[0].status == "timeout"


def test_run_supervise_loop_never_advances_desk_state() -> None:
    """A structural guardrail: on_done/on_blocked are the ONLY side-effect
    seams the loop exposes. It has no reference to DeskopsOperations, no
    advance_task call, nothing that could mutate a task's current_node."""
    import deskops.runtime.supervise as supervise_module

    source = open(supervise_module.__file__).read()

    assert "advance_task" not in source
    assert "DeskopsOperations" not in source
