"""The `agents` view of `deskops view`: what is not a document (CC34 b5, DA1).

The live Herdr workers and the run index (`runs/subagents/index.jsonl`) are not documents of
the desk's store, so no ViewDoc reads them: the CLI composes them here, with the keys and order
of the contract (`docs/deskops-ui.md`, view `agents`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from deskops import doc_access
from deskops.models import BoardDoc
from deskops.models import TaskDoc

CONTRACT_VERSION = 1
RUN_INDEX = Path("runs") / "subagents" / "index.jsonl"
DEFAULT_RUNS_LIMIT = 20


def _error(errors: list[dict[str, str]], reference: str, cause: str) -> None:
    item = {"reference": reference, "cause": cause}
    if item not in errors:
        errors.append(item)


def _list_workers(herdr: str, provider: Callable[[], list[dict[str, Any]]] | None) -> list[dict[str, Any]]:
    if provider is not None:
        agents = provider()
    else:
        from deskops.runtime.herdr import HerdrClient, HerdrProvider

        agents = HerdrProvider(HerdrClient(herdr)).list_agents()
    from deskops.cli.commands.runtime import RuntimeCLI

    return [RuntimeCLI._project_agent(agent) for agent in agents]


def _board_task_ids(root: Path) -> set[str]:
    """Ids of the tasks the Board lists (the `on_board` of each run)."""
    tasks_dir = (root / "desk" / "tasks").resolve()
    ids: set[str] = set()
    for ref in doc_access.read_doc(root / "desk" / "tasks" / "Board.md", BoardDoc).get("tasks") or []:
        path = (root / str(ref)).resolve()
        if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md" or not path.is_file():
            continue
        try:
            ids.add(str(doc_access.read_doc(path, TaskDoc).get("id") or path.stem))
        except Exception:
            continue
    return ids


def agents_view(
    root: Path,
    *,
    runs_limit: int = DEFAULT_RUNS_LIMIT,
    herdr: str = "herdr",
    workers_provider: Callable[[], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    errors: list[dict[str, str]] = []
    workers: list[dict[str, Any]] | None
    workers_error = None
    try:
        workers = _list_workers(herdr, workers_provider)
    except Exception as exc:
        workers = None
        workers_error = f"{type(exc).__name__}: {exc}"
        _error(errors, "runtime workers", f"Herdr runtime unavailable: {workers_error}")
    board_ids = _board_task_ids(root)
    runs: list[dict[str, Any]] = []
    index = root / RUN_INDEX
    total = 0
    if index.is_file():
        parsed = []
        for number, line in enumerate(index.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if not isinstance(entry, dict):
                    raise ValueError("entry is not an object")
            except ValueError as exc:
                _error(errors, f"{RUN_INDEX.as_posix()}:{number}", f"Run index line does not parse: {exc}")
                continue
            parsed.append(entry)
        total = len(parsed)
        for entry in reversed(parsed[-runs_limit:] if runs_limit > 0 else []):
            task_id = str(entry.get("task_id") or "")
            runs.append(
                {
                    "task_id": task_id,
                    "run_id": entry.get("run_id"),
                    "run_dir": entry.get("run_dir"),
                    "commit": entry.get("commit"),
                    "mode": entry.get("mode"),
                    "on_board": task_id in board_ids,
                }
            )
    return {
        "view": "agents",
        "contract": CONTRACT_VERSION,
        "root": str(root),
        "workers": workers,
        "workers_error": workers_error,
        "live_workers": None if workers is None else len(workers),
        "runs": runs,
        "runs_total": total,
        "runs_limit": runs_limit,
        "errors": errors,
    }
