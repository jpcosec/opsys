from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import yaml

from deskops.operations import DeskopsOperations


class CloseoutCLI:
    """Tool-made closing commits linked to run evidence.

    The closing commit is created here, not by agent discretion. The commit
    message carries immutable trailers linking it to the run evidence
    directory, and an append-only index records the commit hash back to the
    run.
    """

    REQUIRED_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]

    def run(self, args: Any) -> int:
        command = getattr(args, "closeout_command", None)
        if command == "commit":
            return self._commit(args)
        if command == "verify":
            return self._verify(args)
        print("Usage: deskops closeout {commit|verify} ...")
        return 1

    def _verify(self, args: Any) -> int:
        root = Path(args.root).resolve()
        report = DeskopsOperations(root).verify_task_closeout(args.task)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1

    def _commit(self, args: Any) -> int:
        root = Path(args.root).resolve()
        run_dir = Path(args.run_dir)
        if not run_dir.is_absolute():
            run_dir = (root / run_dir).resolve()
        task_id = args.task

        if not self._is_under(run_dir, root / "runs" / "subagents"):
            print(f"Run dir must live under runs/subagents/: {run_dir}")
            return 1
        if not run_dir.is_dir():
            print(f"Run dir not found: {run_dir}")
            return 1

        missing = [name for name in self.REQUIRED_EVIDENCE if not (run_dir / name).exists()]
        if missing:
            print(f"Missing required evidence in {run_dir}: {', '.join(missing)}")
            return 1

        manifest_path = run_dir / "run.yaml"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

        run_id = getattr(args, "run_id", None) or manifest.get("run_id")
        session = getattr(args, "session", None) or manifest.get("session")
        session_sha256 = manifest.get("session_sha256")
        session_path = Path(session) if session else None
        if session_path and session_path.is_file():
            session_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()

        rel_run_dir = run_dir.relative_to(root).as_posix()
        manifest.update(
            {
                "task_id": task_id,
                "run_dir": rel_run_dir,
                "run_id": run_id,
                "session": session,
                "session_sha256": session_sha256,
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")

        staged = self._git(root, "diff", "--cached", "--name-only").split()
        paths = getattr(args, "paths", None) or manifest.get("touched")
        if paths:
            self._git(root, "add", "--", *paths)
        elif not staged:
            print("Nothing staged and no paths given. Pass --paths or record 'touched' in run.yaml.")
            return 1
        self._git(root, "add", "--", rel_run_dir)

        subject = getattr(args, "message", None) or f"closeout: {task_id}"
        trailers = [f"Task-Id: {task_id}", f"Run-Dir: {rel_run_dir}"]
        if run_id:
            trailers.append(f"Run-Id: {run_id}")
        if session_sha256:
            trailers.append(f"Session-Sha256: {session_sha256}")
        message = subject + "\n\n" + "\n".join(trailers) + "\n"

        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip() or result.stdout.strip())
            return 1

        commit = self._git(root, "rev-parse", "HEAD")
        index_path = root / "runs" / "subagents" / "index.jsonl"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        with index_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "task_id": task_id,
                        "run_id": run_id,
                        "run_dir": rel_run_dir,
                        "commit": commit,
                        "session_sha256": session_sha256,
                    }
                )
                + "\n"
            )

        print(f"Closing commit {commit[:12]} linked to run {rel_run_dir}")
        print(f"Index: {index_path}")
        return 0

    @staticmethod
    def _is_under(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    @staticmethod
    def _git(root: Path, *argv: str) -> str:
        result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result.stdout.strip()
