"""Task lifecycle service: create, advance, and next.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Shared document storage helpers
(read/write/track, selector resolution, lifecycle facts) stay on
``DeskopsOperations``; the service delegates to the operations instance it is
bound to instead of duplicating them.
"""

from __future__ import annotations

from pathlib import Path
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
            # Closing is the closeout command's job. A forced transition to the
            # terminal node must not leave a half-closed task behind.
            if target_node == lifecycle.COMPLETE:
                return self._hydrate_task(payload), self._closure_required(task_id, payload)
            if target_node in ["draft", "open", "in_progress", "blocked", "closed"]:
                payload["status"] = target_node
            else:
                payload["current_node"] = target_node
            self._write_doc(task_path, TaskDoc, payload)
            advanced_task = self._hydrate_task(payload)
            self.logger.info(f"Advanced task {task_id} manually to {target_node}")
            return advanced_task, TransitionResult(target_node, payload.get("status", ""), True, False, f"Forced transition to {target_node}.")

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        self._add_closeout_facts(payload)
        result = lifecycle.advance(self.root, payload)
        for key in ("closeout_evidence_verified", "pill_graduation_verified"):
            payload.pop(key, None)
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return self._hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = self._hydrate_task(payload)
        if result.progressed:
            self._write_doc(task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    @staticmethod
    def _closure_required(task_id: str, payload: dict[str, Any]) -> TransitionResult:
        node = str(payload.get("current_node") or "")
        status = str(payload.get("status") or "")
        message = (
            f"Task {task_id} closes with 'deskops closeout commit --task {task_id} "
            f"--run-dir <runs/subagents/dir>' or 'deskops closeout commit --task {task_id} "
            f"--no-run --reason <why>'."
        )
        return TransitionResult(node, status, False, True, message)

    def _auto_commit_task_closure(self, payload: dict[str, Any], task_path: Path) -> None:
        # Compatibility hook: closure logic lives in ClosureService.
        self._ops.closure.close_auto(payload, task_path)

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
