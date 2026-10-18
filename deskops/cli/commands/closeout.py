from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService


class CloseoutCLI:
    """Tool-made closing commits, linked to run evidence or marked manual.

    The closing commit is created by ``ClosureService``, not by agent
    discretion. With --run-dir the commit message carries immutable trailers
    linking it to the run evidence directory; with --no-run it carries
    Closeout-Mode: manual and the stated reason instead. ``supersede`` closes a
    task whose subject no longer exists, with a reason and a resolvable ref
    instead of run evidence; ``retire`` removes a task that was already resolved
    before the ritual lifecycle, keeping its status. Either way an append-only
    index records the task
    and run, committed together with the closing commit; the commit hash is
    resolved from its Task-Id trailer.
    """

    def run(self, args: Any) -> int:
        command = getattr(args, "closeout_command", None)
        if command == "commit":
            return self._commit(args)
        if command == "supersede":
            return self._supersede(args)
        if command == "retire":
            return self._retire(args)
        if command == "verify":
            return self._verify(args)
        print("Usage: deskops closeout {commit|supersede|retire|verify} ...")
        return 1

    def _retire(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_retired(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _supersede(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_superseded(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _verify(self, args: Any) -> int:
        root = Path(args.root).resolve()
        report = DeskopsOperations(root).verify_task_closeout(args.task)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1

    def _commit(self, args: Any) -> int:
        run_dir_arg = getattr(args, "run_dir", None)
        no_run = bool(getattr(args, "no_run", False))
        reason = getattr(args, "reason", None)
        if run_dir_arg and no_run:
            print("Pass either --run-dir or --no-run, not both.")
            return 1
        if not run_dir_arg and not no_run:
            print(
                "Closing a task needs one of two routes: --run-dir <runs/subagents/dir> to link the "
                "commit to a subagent run, or --no-run --reason \"<why>\" to close it manually."
            )
            return 1
        if no_run:
            return self._commit_manual(args, reason)
        if reason is not None:
            print("--reason applies only to --no-run; a --run-dir closeout takes its evidence from the run.")
            return 1
        return self._commit_with_run(args)

    def _commit_manual(self, args: Any, reason: str | None) -> int:
        root = Path(args.root).resolve()
        run_only = [flag for flag, attr in (("--run-id", "run_id"), ("--session", "session")) if getattr(args, attr, None)]
        if run_only:
            print(f"{', '.join(run_only)} applies only to --run-dir; a --no-run closeout has no run to record.")
            return 1
        if not " ".join((reason or "").split()):
            print("--no-run needs a non-empty --reason saying why the task closes without a subagent run.")
            return 1

        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_manual(
            args.task,
            reason=reason or "",
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _commit_with_run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_with_run(
            args.task,
            run_dir=args.run_dir,
            paths=getattr(args, "paths", None),
            run_id=getattr(args, "run_id", None),
            session=getattr(args, "session", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code
