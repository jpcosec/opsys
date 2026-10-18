"""One closure path for task bundles.

Every way of closing a task ends here: ``deskops closeout commit`` (run-linked
and manual routes), ``deskops closeout supersede``, and the legacy
``_auto_commit_task_closure`` hook. The
service owns the whole closure: closeout gates for a board-routed task, Board
update, store untracking, bundle removal, exactly one closing commit carrying
the route's trailers, and the append-only index entry.

``advance`` no longer closes: it refuses at the closeout node and points here.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
from typing import TYPE_CHECKING

import yaml

from deskops import doc_io
from deskops.models import BoardDoc
from deskops.models import TaskDoc

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class ClosureCommitError(RuntimeError):
    """The closing commit could not be made; the desk was restored."""


@dataclass
class ClosureOutcome:
    """What one closure did, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


class ClosureService:
    """Build the closing commit and its run-index entry as one clean unit.

    ``runs/subagents/index.jsonl`` records ``task_id``, ``run_dir`` and the
    route fields, but not the closing commit hash: the index line is written
    after the commit exists and folded into that same commit with one
    ``git commit --amend --no-edit``, which changes the hash. ``commit`` is
    therefore always null in new entries. Readers resolve the closing commit
    with ``git log -1 --grep 'Task-Id: <task_id>'``, using the trailer every
    closing commit already carries. The amend is limited to the index path so
    the working tree is clean when the command returns.
    """

    REQUIRED_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]

    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root

    # ---------------------------------------------------------------- routes
    def close_manual(
        self,
        task_id: str,
        *,
        reason: str,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["--no-run needs a non-empty --reason saying why the task closes without a subagent run."],
            )
        subject = message or f"closeout: {task_id}"
        trailers = [f"Task-Id: {task_id}", "Closeout-Mode: manual", f"Closeout-Reason: {reason}"]
        return self._close(
            task_id,
            route="manual",
            subject=subject,
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=paths is not None,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "manual",
            },
            success_line=f"Closing commit {{commit}} made manually (no run): {reason}",
        )

    def close_superseded(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Close a task whose subject no longer exists, from any lifecycle node.

        No evidence gates run: tests, atoms and a run would all describe work
        that was never done. The reason and at least one resolvable ref (an
        ancestor commit or an existing path) are the evidence instead, and the
        closing commit says ``Closeout-Mode: superseded``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Supersede needs a non-empty --reason saying why the task's subject no longer exists."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Supersede needs at least one --ref naming an ancestor commit or an existing path."],
            )
        unresolved = [ref for ref in cleaned_refs if not self._ref_resolves(ref)]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need an ancestor commit or an existing path)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        original = task_path.read_bytes()
        payload = self._ops._read_doc(task_path, TaskDoc)
        payload["status"] = "superseded"
        payload["history"] = [*(payload.get("history") or []), "superseded"]
        try:
            self._ops._write_doc(task_path, TaskDoc, payload)
        except Exception as exc:  # noqa: BLE001 - a task that cannot record superseded is not closed
            task_path.write_bytes(original)
            return ClosureOutcome(1, [f"Could not record superseded status on {task_id}: {exc}"])

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: superseded",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        try:
            outcome = self._close(
                task_id,
                route="superseded",
                subject=message or f"closeout: {task_id}",
                trailers=trailers,
                paths=list(paths or []),
                explicit_paths=True,
                run_gates=False,
                index_entry={
                    "task_id": task_id,
                    "run_id": None,
                    "run_dir": None,
                    "session_sha256": None,
                    "mode": "superseded",
                },
                success_line=f"Closing commit {{commit}} made in superseded mode: {reason}",
            )
        except Exception:
            task_path.write_bytes(original)
            raise
        if outcome.exit_code != 0:
            task_path.write_bytes(original)
        return outcome

    def _ref_resolves(self, reference: str) -> bool:
        if self._ops.closeout_gates.reference_points_to_commit(reference):
            return True
        path = Path(reference)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def close_with_run(
        self,
        task_id: str,
        *,
        run_dir: str | Path,
        paths: list[str] | None = None,
        run_id: str | None = None,
        session: str | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        root = self.root
        resolved_run_dir = Path(run_dir)
        if not resolved_run_dir.is_absolute():
            resolved_run_dir = (root / resolved_run_dir).resolve()

        if not self._is_under(resolved_run_dir, root / "runs" / "subagents"):
            return ClosureOutcome(1, [f"Run dir must live under runs/subagents/: {resolved_run_dir}"])
        if not resolved_run_dir.is_dir():
            return ClosureOutcome(1, [f"Run dir not found: {resolved_run_dir}"])

        missing = [name for name in self.REQUIRED_EVIDENCE if not (resolved_run_dir / name).exists()]
        if missing:
            return ClosureOutcome(
                1,
                [f"Missing required evidence in {resolved_run_dir}: {', '.join(missing)}"],
            )

        manifest_path = resolved_run_dir / "run.yaml"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

        run_id = run_id or manifest.get("run_id")
        session = session or manifest.get("session")
        session_sha256 = manifest.get("session_sha256")
        session_path = Path(str(session)) if session else None
        if session_path and session_path.is_file():
            session_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()

        rel_run_dir = resolved_run_dir.relative_to(root).as_posix()
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

        staged_paths = list(paths) if paths is not None else list(manifest.get("touched") or [])
        trailers = [f"Task-Id: {task_id}", f"Run-Dir: {rel_run_dir}"]
        if run_id:
            trailers.append(f"Run-Id: {run_id}")
        if session_sha256:
            trailers.append(f"Session-Sha256: {session_sha256}")

        return self._close(
            task_id,
            route="run",
            subject=message or f"closeout: {task_id}",
            trailers=trailers,
            paths=staged_paths,
            explicit_paths=True,
            extra_stage_paths=[rel_run_dir],
            index_entry={
                "task_id": task_id,
                "run_id": run_id,
                "run_dir": rel_run_dir,
                "session_sha256": session_sha256,
            },
            success_line=f"Closing commit {{commit}} linked to run {rel_run_dir}",
        )

    def close_auto(self, payload: dict[str, Any], task_path: Path) -> None:
        """Legacy hook used by ``DeskopsOperations._auto_commit_task_closure``."""
        task_id = payload.get("id", "unknown-task")
        files = [str(item) for item in payload.get("files") or []]
        try:
            self._close(
                task_id,
                route="legacy",
                subject=f"closeout: {task_id}",
                trailers=[f"Task-Id: {task_id}"],
                paths=files,
                explicit_paths=True,
                task_path=task_path,
                run_gates=False,
                index_entry={},
                success_line="",
            )
        except ClosureCommitError as exc:
            raise RuntimeError(
                f"Failed to commit task closure for {task_id}. The bundle was not deleted "
                f"and the desk was left unchanged. Git output: {exc}"
            ) from exc

    # ---------------------------------------------------------------- internals
    def _close(
        self,
        task_id: str,
        *,
        route: str,
        subject: str,
        trailers: list[str],
        paths: list[str],
        explicit_paths: bool,
        index_entry: dict[str, Any],
        success_line: str,
        task_path: Path | None = None,
        extra_stage_paths: list[str] | None = None,
        run_gates: bool = True,
    ) -> ClosureOutcome:
        task_path = task_path or self._task_path(task_id)
        task_rel = self._relative(task_path)
        board_path = self.desk_root / "tasks" / "Board.md"
        board_before = board_path.read_text(encoding="utf-8") if board_path.exists() else None
        routed = self._board_routes(board_path, task_id, task_path) if board_before is not None else False

        if run_gates and task_path.exists() and routed:
            gate_outcome = self._gate_outcome(task_id)
            if gate_outcome is not None:
                return gate_outcome

        staged_before = self._git("diff", "--cached", "--name-only", check=False)
        if explicit_paths:
            for path in paths:
                self._git("add", "-A", "--", path, check=False)
            for path in extra_stage_paths or []:
                self._git("add", "-A", "--", path, check=False)
        elif not staged_before:
            if route == "manual":
                return ClosureOutcome(1, ["Nothing staged and no paths given. Pass --paths."])
            return ClosureOutcome(
                1,
                ["Nothing staged and no paths given. Pass --paths or record 'touched' in run.yaml."],
            )

        commit_paths: list[str] = []
        if explicit_paths:
            commit_paths.extend(paths)
            commit_paths.extend(extra_stage_paths or [])

        def add_commit_path(path: str) -> None:
            if path not in commit_paths:
                commit_paths.append(path)

        task_bytes = task_path.read_bytes() if task_path.exists() else None
        paths_to_remove: list[Path] = []

        try:
            with doc_io.DocTransaction(self.root) as transaction:
                if routed and board_before is not None:
                    board_payload = self._ops._read_doc(board_path, BoardDoc)
                    references = [
                        str(item)
                        for item in board_payload.get("tasks") or []
                        if not self._board_reference_matches(str(item), task_id, task_rel)
                    ]
                    board_payload["tasks"] = references
                    self._ops._write_doc(board_path, BoardDoc, board_payload)
                    self._git("add", "--", "desk/tasks/Board.md", check=False)
                    add_commit_path("desk/tasks/Board.md")

                if task_bytes is not None:
                    transaction.untrack(task_path)

                sldb_status = self._git("status", "--porcelain", "--", ".sldb", check=False)
                if sldb_status:
                    self._git("add", "-A", "--", ".sldb", check=False)
                    add_commit_path(".sldb")

                if task_bytes is not None:
                    # Committed means present in HEAD, not merely staged: a directory in
                    # --paths can stage a task created in this cycle, and HEAD never had it.
                    in_head = subprocess.run(
                        ["git", "cat-file", "-e", f"HEAD:{task_rel}"],
                        cwd=self.root,
                        capture_output=True,
                    ).returncode == 0
                    if not in_head:
                        self._git("rm", "--cached", "-q", "--ignore-unmatch", "--", task_rel, check=False)
                    if in_head:
                        removed = subprocess.run(
                            ["git", "rm", "-f", "--", task_rel],
                            cwd=self.root,
                            capture_output=True,
                            text=True,
                        )
                        if removed.returncode != 0:
                            raise ClosureCommitError(
                                removed.stderr.strip() or removed.stdout.strip() or f"git rm failed for {task_rel}"
                            )
                        add_commit_path(task_rel)
                    else:
                        paths_to_remove.append(task_path)

                message = subject + "\n\n" + "\n".join(trailers) + "\n"

                head_task_id = self._git(
                    "log", "-1", "--format=%(trailers:key=Task-Id,valueonly)", check=False
                )
                pathspec = list(dict.fromkeys(commit_paths)) if explicit_paths else None
                if pathspec:
                    # A path git knows neither in the index nor in HEAD (a directory whose
                    # only file was the never-committed task) would fail the whole commit.
                    pathspec = [path for path in pathspec if self._git_knows(path)]
                    if not pathspec:
                        raise ClosureCommitError("None of the --paths match a file git knows; nothing to commit.")
                if head_task_id == task_id:
                    argv = ["commit", "--amend", "--no-edit"]
                else:
                    argv = ["commit", "-m", message]
                if pathspec:
                    argv.extend(["--", *pathspec])

                result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
                if result.returncode != 0:
                    raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

            # The commit exists; only now remove an untracked bundle from disk.
            for path in paths_to_remove:
                if path.exists():
                    path.unlink()
        except Exception:
            self._restore_index(commit_paths, task_rel)
            if task_bytes is not None:
                task_path.parent.mkdir(parents=True, exist_ok=True)
                task_path.write_bytes(task_bytes)
            if board_before is not None:
                board_path.write_text(board_before, encoding="utf-8")
            raise

        commit = self._git("rev-parse", "HEAD")
        messages: list[str] = []
        if index_entry:
            index_path = self.root / "runs" / "subagents" / "index.jsonl"
            index_rel = index_path.relative_to(self.root).as_posix()
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_before = index_path.read_bytes() if index_path.exists() else None
            entry = {**index_entry, "commit": None}
            with index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            try:
                self._git("add", "--", index_rel)
                self._git("commit", "--amend", "--no-edit", "--", index_rel)
            except Exception:
                if index_before is None:
                    index_path.unlink(missing_ok=True)
                else:
                    index_path.write_bytes(index_before)
                self._git("restore", "--staged", "--", index_rel, check=False)
                raise
            commit = self._git("rev-parse", "HEAD")
            messages.append(f"Index: {index_path}")
        if success_line:
            messages.insert(0, success_line.format(commit=commit[:12]))
        return ClosureOutcome(0, messages)

    def _gate_outcome(self, task_id: str) -> ClosureOutcome | None:
        try:
            report = self._ops.verify_task_closeout(task_id)
        except Exception as exc:  # noqa: BLE001 - a gate that cannot run blocks closure
            return ClosureOutcome(1, [f"Closeout verify failed for {task_id}; the closing commit was not made.", f"- {exc}"])
        if report.get("ok"):
            return None
        messages = [f"Closeout verify failed for {task_id}; the closing commit was not made."]
        for finding in report.get("findings") or []:
            code = finding.get("code", "finding")
            detail = finding.get("message") or finding.get("path") or ""
            messages.append(f"- {code}: {detail}")
        messages.append(f"Run 'deskops closeout verify --task {task_id}' for the full report.")
        return ClosureOutcome(1, messages)

    def _task_path(self, task_id: str) -> Path:
        try:
            return self._ops._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return self.desk_root / "tasks" / f"{task_id}.md"

    def _board_routes(self, board_path: Path, task_id: str, task_path: Path) -> bool:
        try:
            payload = self._ops._read_doc(board_path, BoardDoc)
        except Exception:
            return False
        task_rel = self._relative(task_path)
        return any(
            self._board_reference_matches(str(item), task_id, task_rel)
            for item in payload.get("tasks") or []
        )

    @staticmethod
    def _board_reference_matches(reference: str, task_id: str, task_rel: str) -> bool:
        return reference in {
            task_rel,
            f"desk/tasks/{task_id}",
            f"desk/tasks/{task_id}.md",
        }

    def _restore_index(self, commit_paths: list[str], task_rel: str) -> None:
        for path in dict.fromkeys([*commit_paths, task_rel]):
            self._git("restore", "--staged", "--", path, check=False)

    def _relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    @staticmethod
    def _is_under(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _git_knows(self, path: str) -> bool:
        """Whether `path` matches anything in the index or in HEAD."""
        for argv in (["ls-files", "--", path], ["ls-tree", "-r", "--name-only", "HEAD", "--", path]):
            listed = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
            if listed.returncode == 0 and listed.stdout.strip():
                return True
        return False

    def _git(self, *argv: str, check: bool = True) -> str:
        result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise ClosureCommitError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result.stdout.strip()
