"""Task lifecycle service: create, advance, and next.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Shared document storage helpers
(read/write/track, selector resolution, lifecycle facts) stay on
``DeskopsOperations``; the service delegates to the operations instance it is
bound to instead of duplicating them.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_io
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import TaskDoc
from deskops.operations import TaskBundle
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import load_task_lifecycle_spec
from deskops.workflow.next_actions import match_workflow_state

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Shared document helpers stay in the operations layer.
    def ensure_workspace(self) -> None:
        self._ops.ensure_workspace()

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return self._ops._read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_doc(path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_new_doc(path, model, payload)

    def _track_created_document(self, model: type[Any], path: Path, doc_id: str) -> None:
        self._ops._track_created_document(model, path, doc_id)

    def _coerce_list(self, value: Any) -> list[str]:
        return self._ops._coerce_list(value)

    def _hydrate_task(self, payload: dict[str, Any]) -> Task:
        return self._ops._hydrate_task(payload)

    def _add_closeout_facts(self, payload: dict[str, Any]) -> None:
        self._ops._add_closeout_facts(payload)

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return self._ops._resolve_glob(directory, doc_id)

    def _normalize_task_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._ops._normalize_task_payload(payload)

    def _resolve_task_payload(self, task_id: str) -> dict[str, Any]:
        return self._ops._resolve_task_payload(task_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return self._ops._resolve_artifact_selector(artifact_id, directory, selector)

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        self.ensure_workspace()
        payload = self._normalize_task_payload(raw_payload)
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec(self._ops.spec_registry, payload, entry_node=spec.entry_node)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_io.DocTransaction(self.root):
            self._write_new_doc(task_path, TaskDoc, compiled.task_payload)
            self._track_created_document(TaskDoc, task_path, task_id)
            self._ops._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        task_path = self._next_task_path(task_selector, board_path)
        payload = self._resolve_task_payload(task_path.stem)
        spec = load_task_lifecycle_spec(self._ops.spec_root)
        state = match_workflow_state(spec, str(payload.get("current_node") or ""))
        pills = list(dict.fromkeys([*self._board_pills(board_path), *list(payload.get("effective_pills") or payload.get("pills") or [])]))
        return {
            "task": {
                "id": payload["id"],
                "title": payload["title"],
                "status": payload["status"],
                "current_node": payload.get("current_node", ""),
                "task_type": payload.get("task_type", ""),
                "inherits_from": list(payload.get("inherits_from") or []),
            },
            "phase": state["phase"],
            "ritual": state.get("ritual", ""),
            "pills": pills,
            "next_actions": list(state.get("next_actions") or []),
            "advance_when": list(state.get("advance_when") or []),
            "sources": {
                "task": str(task_path.relative_to(self.root)),
                "board": str(board_path.relative_to(self.root)),
                "workflow": "deskops/spec/workflows/task_lifecycle.yaml",
            },
        }

    def advance_task(self, task_id: str, target_node: str | None = None) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = self._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = self._read_doc(task_path, TaskDoc)

        if target_node:
            if target_node in ["draft", "open", "in_progress", "blocked", "closed"]:
                payload["status"] = target_node
            else:
                payload["current_node"] = target_node
                # Reaching the terminal node closes the task. The gated path
                # pairs current_node == "complete" with status == "closed"
                # (see the auto-commit check below); a forced transition that
                # moved only current_node left the two disagreeing, so the
                # task looked terminal but never read as closed.
                if target_node == lifecycle.COMPLETE:
                    payload["status"] = "closed"
            self._write_doc(task_path, TaskDoc, payload)
            advanced_task = self._hydrate_task(payload)
            self.logger.info(f"Advanced task {task_id} manually to {target_node}")
            return advanced_task, TransitionResult(target_node, payload.get("status", ""), True, False, f"Forced transition to {target_node}.")

        self._add_closeout_facts(payload)
        result = lifecycle.advance(self.root, payload)
        for key in ("closeout_evidence_verified", "pill_graduation_verified"):
            payload.pop(key, None)
        advanced_task = self._hydrate_task(payload)
        if payload.get("status") == "closed" and payload.get("current_node") == lifecycle.COMPLETE:
            self.logger.info(f"Task {task_id} is complete. Performing auto-commit and cleanup.")
            self._auto_commit_task_closure(payload, task_path)
            return advanced_task, result
        if result.progressed:
            self._write_doc(task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    def _auto_commit_task_closure(self, payload: dict[str, Any], task_path: Path) -> None:
        task_id = payload.get("id", "unknown-task")
        files = self._coerce_list(payload.get("files") or [])
        task_rel = str(task_path.relative_to(self.root)) if task_path.is_absolute() else str(task_path)
        board_rel = "desk/tasks/Board.md"
        sldb_rel = ".sldb"

        with doc_io.DocTransaction(self.root) as transaction:
            self.logger.debug(f"Removing task {task_id} from Board.md")
            board_path = self.desk_root / "tasks" / "Board.md"
            board_before = board_path.read_text(encoding="utf-8") if board_path.exists() else None
            if board_before is not None:
                board_payload = self._read_doc(board_path, BoardDoc)
                task_ref = f"desk/tasks/{task_id}.md"
                tasks = [str(item) for item in board_payload.get("tasks") or [] if str(item) != task_ref]
                board_payload["tasks"] = tasks
                self._write_doc(board_path, BoardDoc, board_payload)

            task_before = task_path.read_bytes() if task_path.exists() else None

            # Untrack before anything is staged: the .sldb delta this causes must be
            # part of the closeout commit, and a failure must abort the closeout.
            if task_before is not None:
                transaction.untrack(task_path)

            commit_paths: list[str] = []
            seen_paths: set[str] = set()

            def add_commit_path(path: str) -> None:
                if path not in seen_paths:
                    seen_paths.add(path)
                    commit_paths.append(path)

            # Only stage (and later commit) listed files that actually changed;
            # whatever the operator staged for other work must stay untouched.
            for file in files:
                status = subprocess.run(
                    ["git", "status", "--porcelain", "--", file],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                )
                if status.returncode != 0 or not status.stdout.strip():
                    continue
                self.logger.debug(f"Staging file: {file}")
                subprocess.run(["git", "add", "-A", "--", file], cwd=self.root, check=False)
                add_commit_path(file)

            if board_before is not None:
                subprocess.run(["git", "add", "--", board_rel], cwd=self.root, check=False)
                add_commit_path(board_rel)

            sldb_status = subprocess.run(
                ["git", "status", "--porcelain", "--", sldb_rel],
                cwd=self.root,
                capture_output=True,
                text=True,
            )
            if sldb_status.returncode == 0 and sldb_status.stdout.strip():
                subprocess.run(["git", "add", "-A", "--", sldb_rel], cwd=self.root, check=False)
                add_commit_path(sldb_rel)

            def restore_index() -> None:
                for path in commit_paths:
                    subprocess.run(["git", "restore", "--staged", "--", path], cwd=self.root, check=False)
                subprocess.run(["git", "restore", "--staged", "--", task_rel], cwd=self.root, check=False)
                if task_before is not None:
                    task_path.write_bytes(task_before)
                if board_before is not None:
                    board_path.write_text(board_before, encoding="utf-8")

            paths_to_remove = []
            if task_before is not None:
                paths_to_remove.append(task_path)
                tracked = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", "--", task_rel],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                ).returncode == 0
                if tracked:
                    # A pathspec commit records the working tree, so the gone task
                    # file must already be removed from both disk and the index.
                    # The bundle carries uncommitted lifecycle edits at closeout,
                    # so force the removal; its bytes are restored on failure.
                    removed = subprocess.run(
                        ["git", "rm", "-f", "--", task_rel], cwd=self.root, capture_output=True, text=True
                    )
                    if removed.returncode != 0:
                        restore_index()
                        raise RuntimeError(
                            f"Failed to remove task file {task_rel} for {task_id}. The bundle was not "
                            f"deleted and the desk was left unchanged. Git output: "
                            f"{removed.stderr or removed.stdout}"
                        )
                    add_commit_path(task_rel)

            commit_msg = f"closeout: {task_id}\n\nTask-Id: {task_id}\n"

            # Check if HEAD is already the closeout commit for this task. The
            # subject alone is not proof of ownership: `closeout: task-foo` also
            # prefixes `closeout: task-foo-bar`, so decide from the Task-Id
            # trailer that every closeout commit carries.
            head_task_id = ""
            result_log = subprocess.run(
                ["git", "log", "-1", "--format=%(trailers:key=Task-Id,valueonly)"],
                cwd=self.root,
                capture_output=True,
                text=True,
            )
            if result_log.returncode == 0:
                head_task_id = result_log.stdout.strip()

            if head_task_id == task_id:
                self.logger.info(f"Amending closeout commit for {task_id}")
                result = subprocess.run(
                    ["git", "commit", "--amend", "--no-edit", "--", *commit_paths],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                )
            else:
                self.logger.info(f"Committing closure for {task_id}: {commit_msg.strip()}")
                result = subprocess.run(
                    ["git", "commit", "-m", commit_msg, "--", *commit_paths],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                )

            if result.returncode != 0:
                # Nothing was committed, so put the desk back exactly as it was and
                # leave the bundle in place.
                restore_index()
                raise RuntimeError(
                    f"Failed to commit task closure for {task_id}. The bundle was not deleted "
                    f"and the desk was left unchanged. Git output: {result.stderr or result.stdout}"
                )

            for p in paths_to_remove:
                if p.exists():
                    self.logger.debug(f"Removing file {p.name}")
                    p.unlink()

    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = self._read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = self._read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]
