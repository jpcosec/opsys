"""Zero-cost-while-waiting supervision loop over a Herdr agent.

Herdr is a remote control, not a recorder: verified against a live server
that read-only calls and agent lifecycle transitions leave no history, and
`agent wait` returns instantly whenever the agent is already sitting in the
requested state rather than blocking for the *next* transition into it. A
naive `while True: wait(); handle()` loop would busy-spin the socket at
effectively zero delay for as long as an agent stays `blocked` or `done`.

This module guards against that with `state_change_seq`: Herdr increments it
on every real lifecycle transition, so a `wait()` result whose seq matches
the last one we already handled is a duplicate settle, not a new event, and
gets a short backoff instead of immediate re-handling.

Never answers a blocked agent's prompt and never advances desk state — both
are explicit anti-patterns carried over from `desk/roles/deskops-supervisor.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Callable

from deskops.runtime.herdr import HerdrProvider

# States that end the loop rather than being retried: a timeout means the
# caller's own timeout_ms expired, and "unknown" means Herdr could not
# classify the agent confidently — neither is something to spin-retry.
TERMINAL_STATUSES = frozenset({"timeout", "unknown"})


@dataclass(frozen=True, slots=True)
class SuperviseOutcome:
    agent_id: str
    status: str
    state_change_seq: int | None
    excerpt: str
    is_new_event: bool


def supervise_once(
    provider: HerdrProvider,
    agent_id: str,
    *,
    until: tuple[str, ...] = (),
    timeout_ms: int | None = None,
    read_lines: int = 200,
    last_seq: int | None = None,
) -> SuperviseOutcome:
    """Block once until `agent_id` settles, then classify the result.

    Purely observational: no notification, no file writes, no desk mutation.
    Side effects belong to the caller (`run_supervise_loop` below or a CLI
    wrapper) so this stays trivially testable with a fake Herdr runner.
    """
    result = provider.wait(agent_id, until=until, timeout_ms=timeout_ms)
    agent = result.get("agent", {})
    status = agent.get("agent_status", "unknown")
    seq = agent.get("state_change_seq")
    is_new_event = seq is None or seq != last_seq

    excerpt = ""
    if is_new_event and status in ("blocked", "done"):
        excerpt = provider.read(agent_id, lines=read_lines)

    return SuperviseOutcome(agent_id=agent_id, status=status, state_change_seq=seq, excerpt=excerpt, is_new_event=is_new_event)


def run_supervise_loop(
    provider: HerdrProvider,
    agent_id: str,
    *,
    max_iterations: int | None = None,
    poll_backoff_seconds: float = 2.0,
    read_lines: int = 200,
    timeout_ms: int | None = None,
    on_blocked: Callable[[SuperviseOutcome], None] | None = None,
    on_done: Callable[[SuperviseOutcome], None] | None = None,
    sleep: Callable[[float], Any] = time.sleep,
) -> list[SuperviseOutcome]:
    """Repeatedly settle on `agent_id`, dispatching only genuinely new events.

    `max_iterations=None` runs forever (the real CLI use). Tests pass a
    small integer to bound it, and inject `sleep` to avoid real delays.
    """
    outcomes: list[SuperviseOutcome] = []
    last_seq: int | None = None
    iterations = 0

    while max_iterations is None or iterations < max_iterations:
        outcome = supervise_once(provider, agent_id, read_lines=read_lines, last_seq=last_seq, timeout_ms=timeout_ms)
        iterations += 1

        if not outcome.is_new_event:
            sleep(poll_backoff_seconds)
            continue

        last_seq = outcome.state_change_seq
        outcomes.append(outcome)

        if outcome.status == "blocked" and on_blocked is not None:
            on_blocked(outcome)
        elif outcome.status == "done" and on_done is not None:
            on_done(outcome)

        if outcome.status in TERMINAL_STATUSES:
            break

    return outcomes
