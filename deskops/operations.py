from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from desk.models import BoardDoc
from desk.models import ChecklistDoc
from desk.models import ConditionDoc
from desk.models import EdgeDoc
from desk.models import FAQDoc
from desk.models import HookDoc
from desk.models import InboxNoteDoc
from desk.models import OperatorDoc
from desk.models import PillDoc
from desk.models import RepositoryDoc
from desk.models import RoutineDoc
from desk.models import RitualDoc
from desk.models import StepDoc
from desk.models import TaskDoc
from desk.models import AtomDoc
from desk.models import FieldInstanceDoc
from deskops.runtime import Checklist
from deskops.runtime import Condition
from deskops.runtime import Edge
from deskops.runtime import Hook
from deskops.runtime import Operator
from deskops.runtime import Routine
from deskops.runtime import Task
from deskops.runtime import TransitionResult
from deskops.specs import compile_artifact_spec
from deskops.specs import SpecRegistry
from deskops.specs import compile_task_bundle_spec
from deskops.workspace import scaffold_desk


PRIMITIVE_DIRS = {
    "conditions": ConditionDoc,
    "operators": OperatorDoc,
    "checklists": ChecklistDoc,
    "hooks": HookDoc,
    "edges": EdgeDoc,
}

PRIMITIVE_KINDS = {
    "condition": ("conditions", ConditionDoc),
    "operator": ("operators", OperatorDoc),
    "checklist": ("checklists", ChecklistDoc),
    "hook": ("hooks", HookDoc),
    "edge": ("edges", EdgeDoc),
}

ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": FAQDoc,
    "artifact.step": StepDoc,
}

ARTIFACT_PATHS = {
    "artifact.task": "tasks",
    "artifact.pill": "contexts",
    "artifact.ritual": "rituals",
    "artifact.board": "tasks",
    "artifact.atom": "drawer/atoms",
    "artifact.repository": "registry",
    "artifact.inbox_note": "inbox",
    "artifact.faq": "faq",
    "artifact.step": "steps",
}

ARTIFACT_SUBJECTS = {
    "artifact.pill": {"subject": "pill", "list_subject": "pills"},
    "artifact.ritual": {"subject": "ritual", "list_subject": "rituals"},
    "artifact.board": {"subject": "board", "list_subject": "boards"},
    "artifact.atom": {"subject": "atom", "list_subject": "atoms"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    return "-".join(parts) or "item"


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path
    routine_path: Path


@dataclass(slots=True)
class DocumentRecord:
    kind: str
    doc_id: str
    path: Path


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = Path(__file__).resolve().parents[1] / "spec"
        self._spec_registry: SpecRegistry | None = None

    @property
    def spec_registry(self) -> SpecRegistry:
        if self._spec_registry is None:
            self._spec_registry = SpecRegistry.load(self.spec_root)
        return self._spec_registry

    def ensure_workspace(self) -> None:
        scaffold_desk(self.root)
        for relative in [
            Path("fields"),
            Path("routines"),
            Path("steps"),
            Path("registry"),
            Path("faq"),
            Path("primitives/conditions"),
            Path("primitives/operators"),
            Path("primitives/checklists"),
            Path("primitives/hooks"),
            Path("primitives/edges"),
        ]:
            (self.desk_root / relative).mkdir(parents=True, exist_ok=True)

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        self.ensure_workspace()
        payload = self._normalize_task_payload(raw_payload)
        compiled = compile_task_bundle_spec(self.spec_registry, payload)
        task_id = compiled.task_payload["id"]

        self._write_doc(self._task_path(task_id), TaskDoc, compiled.task_payload)
        self._write_doc(self._routine_path(compiled.routine_payload["id"]), RoutineDoc, compiled.routine_payload)
        for item in compiled.field_payloads:
            self._write_doc(self._field_path(item["id"]), FieldInstanceDoc, item)
        for item in compiled.condition_payloads:
            self._write_doc(self._primitive_path("conditions", item["id"]), ConditionDoc, item)
        for item in compiled.checklist_payloads:
            self._write_doc(self._primitive_path("checklists", item["id"]), ChecklistDoc, item)
        for item in compiled.operator_payloads:
            self._write_doc(self._primitive_path("operators", item["id"]), OperatorDoc, item)
        for item in compiled.edge_payloads:
            self._write_doc(self._primitive_path("edges", item["id"]), EdgeDoc, item)

        self._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=self._task_path(task_id), routine_path=self._routine_path(compiled.routine_payload["id"]))

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        model = ARTIFACT_MODELS[artifact_id]
        compiled = compile_artifact_spec(
            self.spec_registry,
            artifact_id,
            raw_payload,
            model_fields=model.model_fields.keys(),
        )
        path = self._artifact_path(artifact_id, compiled.artifact_payload["id"])
        self._write_doc(path, model, compiled.artifact_payload)
        for item in compiled.field_payloads:
            self._write_doc(self._field_path(item["id"]), FieldInstanceDoc, item)
        return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=compiled.artifact_payload["id"], path=path)

    def create_primitive(self, kind: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        directory, model = PRIMITIVE_KINDS[kind]
        payload = self._normalize_primitive_payload(kind, raw_payload)
        path = self._primitive_path(directory, payload["id"])
        self._write_doc(path, model, payload)
        return DocumentRecord(kind=kind, doc_id=payload["id"], path=path)

    def create_routine(self, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        payload = self._normalize_routine_payload(raw_payload)
        path = self._routine_path(payload["id"])
        self._write_doc(path, RoutineDoc, payload)
        return DocumentRecord(kind="routine", doc_id=payload["id"], path=path)

    def list_tasks(self) -> list[Task]:
        task_dir = self.desk_root / "tasks"
        if not task_dir.exists():
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            tasks.append(self._load_task(path.stem))
        return tasks

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        model = ARTIFACT_MODELS[artifact_id]
        directory = self.desk_root / ARTIFACT_PATHS[artifact_id]
        if not directory.exists():
            return []
        pattern = self._artifact_glob_pattern(artifact_id)
        return [self._read_doc(path, model) for path in sorted(directory.glob(pattern))]

    def list_routines(self) -> list[Routine]:
        routine_dir = self.desk_root / "routines"
        if not routine_dir.exists():
            return []
        return [self._load_routine(path.stem) for path in sorted(routine_dir.glob("routine-*.md"))]

    def list_primitives(self, kind: str) -> list[dict[str, Any]]:
        directory, model = PRIMITIVE_KINDS[kind]
        primitive_dir = self.desk_root / "primitives" / directory
        if not primitive_dir.exists():
            return []
        prefix = f"{kind}-"
        return [
            self._read_doc(path, model)
            for path in sorted(primitive_dir.glob(f"{prefix}*.md"))
        ]

    def show_task(self, task_id: str) -> tuple[Task | None, dict[str, bool]]:
        try:
            task = self._load_task(task_id)
        except FileNotFoundError:
            return None, {}
        statuses = self._checklist_statuses(task)
        return task, statuses

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        model = ARTIFACT_MODELS[artifact_id]
        directory = self.desk_root / ARTIFACT_PATHS[artifact_id]
        matches = sorted(directory.glob(f"{doc_id}*.md"))
        if not matches:
            raise FileNotFoundError(f"No {artifact_id} file found for id '{doc_id}' in {directory}")
        return self._read_doc(matches[0], model)

    def show_routine(self, routine_id: str) -> Routine | None:
        return self._load_routine(routine_id)

    def show_primitive(self, kind: str, primitive_id: str) -> dict[str, Any]:
        directory_name, model = PRIMITIVE_KINDS[kind]
        return self._read_doc(
            self._resolve_glob(self.desk_root / "primitives" / directory_name, primitive_id),
            model,
        )

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = self._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = self._read_doc(task_path, TaskDoc)
        task = self._hydrate_task(payload)
        routine = self._load_routine(task.routine)
        if routine is None:
            print(f"Task {task_id} has no routine — cannot advance")
            return task, None
        conditions = self._load_conditions(task)
        operators = self._load_operators(routine)
        checklists = self._load_checklists(task)
        result = routine.advance(
            payload,
            conditions=conditions,
            operators=operators,
            checklists=checklists,
        )
        self._write_doc(task_path, TaskDoc, payload)
        return self._hydrate_task(payload), result

    def parse_task_input(self, args: Any) -> dict[str, Any]:
        if getattr(args, "from_yaml", None):
            return yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {}
        if getattr(args, "payload", None):
            return json.loads(args.payload)
        return {
            "title": args.title,
            "goal": args.goal,
            "scope": args.scope,
            "implementation_path": args.implementation_path,
            "done_when": args.done_when,
            "validation": args.validation or [],
            "references": [],
            "depends_on": [],
            "pills": [],
            "files": [],
            "history": [],
            "tags": ["workspace:desk", "artifact:task"],
        }

    def parse_artifact_input(self, artifact_id: str, args: Any) -> dict[str, Any]:
        if getattr(args, "from_yaml", None):
            return yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {}
        artifact = self.spec_registry.artifacts[artifact_id]
        payload: dict[str, Any] = {}
        for field_id in artifact["data"].get("fields", []):
            field_spec = self.spec_registry.fields[field_id]
            key = str(field_spec["data"]["key"])
            attr = key
            value = getattr(args, attr, None)
            if isinstance(value, list):
                payload[key] = list(value)
            elif value is not None:
                payload[key] = value
        return payload

    def parse_primitive_input(self, kind: str, args: Any) -> dict[str, Any]:
        if getattr(args, "from_yaml", None):
            return yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {}
        payload: dict[str, Any] = {
            "title": args.title,
            "summary": getattr(args, "summary", "") or "",
            "status": getattr(args, "status", "active") or "active",
            "tags": getattr(args, "tags", []) or [f"primitive:{kind}"],
        }
        if kind == "condition":
            payload.update(
                {
                    "subject": args.subject_path,
                    "predicate": args.predicate,
                    "expected": args.expected or "",
                }
            )
        elif kind == "operator":
            payload.update(
                {
                    "action": args.action,
                    "target": args.target,
                    "value": args.value or "",
                }
            )
        elif kind == "checklist":
            payload.update(
                {
                    "items": list(args.item or []),
                    "condition_refs": list(args.condition_ref or []),
                    "mode": args.mode or "all",
                }
            )
        elif kind == "hook":
            payload.update(
                {
                    "event": args.event,
                    "target": args.target_ref,
                    "condition_ref": args.condition_ref or "",
                }
            )
        elif kind == "edge":
            payload.update(
                {
                    "source": args.source,
                    "target": args.target_node,
                    "condition_ref": args.condition_ref or "",
                }
            )
        return payload

    def parse_routine_input(self, args: Any) -> dict[str, Any]:
        if getattr(args, "from_yaml", None):
            return yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {}
        return {
            "title": args.title,
            "summary": args.summary or "",
            "entrypoint": args.entrypoint,
            "decomposition": list(args.decomposition or []),
            "edges": list(args.edge or []),
            "terminal_nodes": list(args.terminal_node or ["complete"]),
            "tags": getattr(args, "tags", []) or ["primitive:routine"],
        }

    def _normalize_task_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        title = str(payload["title"]).strip()
        task_id = str(payload.get("id") or f"task-{slugify(title)}")
        return {
            "title": title,
            "id": task_id,
            "status": str(payload.get("status") or "draft"),
            "goal": str(payload.get("goal") or ""),
            "scope": str(payload.get("scope") or ""),
            "references": list(payload.get("references") or []),
            "depends_on": list(payload.get("depends_on") or []),
            "pills": list(payload.get("pills") or []),
            "files": list(payload.get("files") or []),
            "routine": str(payload.get("routine") or ""),
            "checklists": list(payload.get("checklists") or []),
            "current_node": str(payload.get("current_node") or ""),
            "implementation_path": str(payload.get("implementation_path") or ""),
            "validation": self._coerce_list(payload.get("validation") or []),
            "done_when": str(payload.get("done_when") or ""),
            "history": self._coerce_list(payload.get("history") or []),
            "tags": self._coerce_list(payload.get("tags") or ["workspace:desk", "artifact:task"]),
        }

    def _normalize_primitive_payload(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        title = str(payload["title"]).strip()
        primitive_id = str(payload.get("id") or f"{kind}-{slugify(title)}")
        base = {
            "title": title,
            "id": primitive_id,
            "status": str(payload.get("status") or "active"),
            "summary": str(payload.get("summary") or ""),
            "tags": self._coerce_list(payload.get("tags") or [f"primitive:{kind}"]),
        }
        if kind == "condition":
            base.update(
                {
                    "subject": str(payload.get("subject") or ""),
                    "predicate": str(payload.get("predicate") or "truthy"),
                    "expected": str(payload.get("expected") or ""),
                }
            )
        elif kind == "operator":
            base.update(
                {
                    "action": str(payload.get("action") or "set_field"),
                    "target": str(payload.get("target") or ""),
                    "value": str(payload.get("value") or ""),
                }
            )
        elif kind == "checklist":
            base.update(
                {
                    "items": self._coerce_list(payload.get("items") or []),
                    "condition_refs": self._coerce_list(payload.get("condition_refs") or []),
                    "mode": str(payload.get("mode") or "all"),
                }
            )
        elif kind == "hook":
            base.update(
                {
                    "event": str(payload.get("event") or ""),
                    "target": str(payload.get("target") or ""),
                    "condition_ref": str(payload.get("condition_ref") or ""),
                }
            )
        elif kind == "edge":
            base.update(
                {
                    "source": str(payload.get("source") or ""),
                    "target": str(payload.get("target") or ""),
                    "condition_ref": str(payload.get("condition_ref") or ""),
                }
            )
        return base

    def _normalize_routine_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        title = str(payload["title"]).strip()
        routine_id = str(payload.get("id") or f"routine-{slugify(title)}")
        return {
            "title": title,
            "id": routine_id,
            "status": str(payload.get("status") or "active"),
            "summary": str(payload.get("summary") or ""),
            "entrypoint": str(payload.get("entrypoint") or ""),
            "decomposition": self._coerce_list(payload.get("decomposition") or []),
            "edges": self._coerce_list(payload.get("edges") or []),
            "terminal_nodes": self._coerce_list(payload.get("terminal_nodes") or ["complete"]),
            "tags": self._coerce_list(payload.get("tags") or ["primitive:routine"]),
        }

    def _coerce_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if value in (None, ""):
            return []
        return [str(value)]

    def _default_condition_payloads(self, task_id: str) -> list[dict[str, Any]]:
        return [
            {
                "title": "Implementation path exists",
                "id": f"condition-{task_id}-has-implementation-path",
                "status": "active",
                "summary": "Task implementation path must exist before execution.",
                "subject": "implementation_path",
                "predicate": "truthy",
                "expected": "",
                "tags": ["primitive:condition"],
            },
            {
                "title": "Validation exists",
                "id": f"condition-{task_id}-has-validation",
                "status": "active",
                "summary": "Task validation must exist before testing handoff.",
                "subject": "validation",
                "predicate": "not_empty",
                "expected": "",
                "tags": ["primitive:condition"],
            },
            {
                "title": "Ready for closeout",
                "id": f"condition-{task_id}-ready-for-closeout",
                "status": "active",
                "summary": "Task must be in ready_for_testing before closeout.",
                "subject": "status",
                "predicate": "equals",
                "expected": "ready_for_testing",
                "tags": ["primitive:condition"],
            },
        ]

    def _default_checklist_payloads(self, task_id: str) -> list[dict[str, Any]]:
        return [
            {
                "title": "Execution ready",
                "id": f"checklist-{task_id}-execution-ready",
                "status": "active",
                "summary": "Confirms the task is ready to enter active execution.",
                "items": ["Implementation path exists"],
                "condition_refs": [f"condition-{task_id}-has-implementation-path"],
                "mode": "all",
                "tags": ["primitive:checklist"],
            },
            {
                "title": "Testing ready",
                "id": f"checklist-{task_id}-testing-ready",
                "status": "active",
                "summary": "Confirms the task is ready for testing handoff.",
                "items": ["Validation exists"],
                "condition_refs": [f"condition-{task_id}-has-validation"],
                "mode": "all",
                "tags": ["primitive:checklist"],
            },
            {
                "title": "Closeout ready",
                "id": f"checklist-{task_id}-closeout-ready",
                "status": "active",
                "summary": "Confirms the task is ready for closeout.",
                "items": ["Task is ready for closeout"],
                "condition_refs": [f"condition-{task_id}-ready-for-closeout"],
                "mode": "all",
                "tags": ["primitive:checklist"],
            },
        ]

    def _default_operator_payloads(self, task_id: str) -> list[dict[str, Any]]:
        return [
            {
                "title": "Activate task",
                "id": f"operator-{task_id}-activate",
                "status": "active",
                "summary": "Moves the task into active execution.",
                "action": "set_field",
                "target": "status",
                "value": "active",
                "tags": ["primitive:operator"],
            },
            {
                "title": "Mark ready for testing",
                "id": f"operator-{task_id}-ready-for-testing",
                "status": "active",
                "summary": "Moves the task into the testing gate.",
                "action": "set_field",
                "target": "status",
                "value": "ready_for_testing",
                "tags": ["primitive:operator"],
            },
            {
                "title": "Close task",
                "id": f"operator-{task_id}-close",
                "status": "active",
                "summary": "Closes the task in the operational runtime.",
                "action": "set_field",
                "target": "status",
                "value": "closed",
                "tags": ["primitive:operator"],
            },
        ]

    def _default_edge_payloads(self, task_id: str) -> list[dict[str, Any]]:
        return [
            {
                "title": "Execution gate to activation",
                "id": f"edge-{task_id}-execution-to-activate",
                "status": "active",
                "summary": "Execution gate passed.",
                "source": f"checklist-{task_id}-execution-ready",
                "target": f"operator-{task_id}-activate",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
            {
                "title": "Activation to testing gate",
                "id": f"edge-{task_id}-activate-to-testing",
                "status": "active",
                "summary": "Activation complete.",
                "source": f"operator-{task_id}-activate",
                "target": f"checklist-{task_id}-testing-ready",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
            {
                "title": "Testing gate to testing-ready operator",
                "id": f"edge-{task_id}-testing-to-ready",
                "status": "active",
                "summary": "Testing gate passed.",
                "source": f"checklist-{task_id}-testing-ready",
                "target": f"operator-{task_id}-ready-for-testing",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
            {
                "title": "Testing-ready operator to closeout gate",
                "id": f"edge-{task_id}-ready-to-closeout",
                "status": "active",
                "summary": "Ready-for-testing state entered.",
                "source": f"operator-{task_id}-ready-for-testing",
                "target": f"checklist-{task_id}-closeout-ready",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
            {
                "title": "Closeout gate to close operator",
                "id": f"edge-{task_id}-closeout-to-close",
                "status": "active",
                "summary": "Closeout gate passed.",
                "source": f"checklist-{task_id}-closeout-ready",
                "target": f"operator-{task_id}-close",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
            {
                "title": "Close operator to complete",
                "id": f"edge-{task_id}-close-to-complete",
                "status": "active",
                "summary": "Task closed.",
                "source": f"operator-{task_id}-close",
                "target": "complete",
                "condition_ref": "",
                "tags": ["primitive:edge"],
            },
        ]

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = self._read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            self._write_doc(board_path, BoardDoc, board_payload)

    def _load_task(self, task_id: str) -> Task:
        path = self._resolve_glob(self.desk_root / "tasks", task_id)
        return self._hydrate_task(self._read_doc(path, TaskDoc))

    def _load_routine(self, routine_id: str) -> Routine | None:
        if not routine_id:
            return None
        try:
            payload = self._read_doc(self._resolve_glob(self.desk_root / "routines", routine_id), RoutineDoc)
        except FileNotFoundError:
            return None
        edges = [e for e in (self._load_edge(edge_id) for edge_id in payload.get("edges", [])) if e is not None]
        return Routine(
            id=payload["id"],
            title=payload["title"],
            status=payload["status"],
            summary=payload["summary"],
            tags=list(payload.get("tags") or []),
            entrypoint=payload["entrypoint"],
            decomposition=list(payload.get("decomposition") or []),
            edges=edges,
            terminal_nodes=list(payload.get("terminal_nodes") or []),
        )

    def _load_edge(self, edge_id: str) -> Edge | None:
        try:
            payload = self._read_doc(self._resolve_glob(self.desk_root / "primitives" / "edges", edge_id), EdgeDoc)
        except FileNotFoundError:
            return None
        return Edge(
            id=payload["id"],
            title=payload["title"],
            status=payload["status"],
            summary=payload["summary"],
            tags=list(payload.get("tags") or []),
            source=payload["source"],
            target=payload["target"],
            condition_ref=payload.get("condition_ref", ""),
        )

    def _load_conditions(self, task: Task) -> dict[str, Condition]:
        conditions: dict[str, Condition] = {}
        for path in (self.desk_root / "primitives" / "conditions").glob("condition-*.md"):
            if task.id not in path.stem:
                continue
            payload = self._read_doc(path, ConditionDoc)
            conditions[payload["id"]] = Condition(
                id=payload["id"],
                title=payload["title"],
                status=payload["status"],
                summary=payload["summary"],
                tags=list(payload.get("tags") or []),
                subject=payload["subject"],
                predicate=payload["predicate"],
                expected=payload.get("expected", ""),
            )
        return conditions

    def _load_operators(self, routine: Routine) -> dict[str, Operator]:
        operators: dict[str, Operator] = {}
        for node_id in routine.decomposition:
            if not node_id.startswith("operator-"):
                continue
            try:
                payload = self._read_doc(self._resolve_glob(self.desk_root / "primitives" / "operators", node_id), OperatorDoc)
            except FileNotFoundError:
                continue
            operators[node_id] = Operator(
                id=payload["id"],
                title=payload["title"],
                status=payload["status"],
                summary=payload["summary"],
                tags=list(payload.get("tags") or []),
                action=payload["action"],
                target=payload["target"],
                value=payload.get("value", ""),
            )
        return operators

    def _load_checklists(self, task: Task) -> dict[str, Checklist]:
        checklists: dict[str, Checklist] = {}
        for checklist_id in task.checklists:
            try:
                payload = self._read_doc(self._resolve_glob(self.desk_root / "primitives" / "checklists", checklist_id), ChecklistDoc)
            except FileNotFoundError:
                continue
            checklists[checklist_id] = Checklist(
                id=payload["id"],
                title=payload["title"],
                status=payload["status"],
                summary=payload["summary"],
                tags=list(payload.get("tags") or []),
                items=list(payload.get("items") or []),
                condition_refs=list(payload.get("condition_refs") or []),
                mode=payload.get("mode", "all"),
            )
        return checklists

    def _checklist_statuses(self, task: Task) -> dict[str, bool]:
        payload = self._read_doc(self._resolve_glob(self.desk_root / "tasks", task.id), TaskDoc)
        conditions = self._load_conditions(task)
        checklists = self._load_checklists(task)
        return {
            checklist_id: checklist.is_complete(payload, conditions)
            for checklist_id, checklist in checklists.items()
        }

    def _hydrate_task(self, payload: dict[str, Any]) -> Task:
        return Task(
            id=payload["id"],
            title=payload["title"],
            status=payload["status"],
            summary=payload["goal"],
            tags=list(payload.get("tags") or []),
            routine=payload.get("routine", ""),
            current_node=payload.get("current_node", ""),
            history=list(payload.get("history") or []),
            goal=payload.get("goal", ""),
            scope=payload.get("scope", ""),
            references=list(payload.get("references") or []),
            depends_on=list(payload.get("depends_on") or []),
            pills=list(payload.get("pills") or []),
            files=list(payload.get("files") or []),
            field_refs=list(payload.get("field_refs") or []),
            checklists=list(payload.get("checklists") or []),
            implementation_path=payload.get("implementation_path", ""),
            validation=list(payload.get("validation") or []),
            done_when=payload.get("done_when", ""),
        )

    def _field_path(self, field_id: str) -> Path:
        return self.desk_root / "fields" / f"{field_id}.md"

    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _artifact_path(self, artifact_id: str, doc_id: str) -> Path:
        return self.desk_root / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"

    def _artifact_glob_pattern(self, artifact_id: str) -> str:
        spec = self.spec_registry.artifacts[artifact_id]
        id_pattern = str(spec["data"]["doc"]["id_pattern"])
        return id_pattern.replace("{slug}", "*") + ".md"

    def _routine_path(self, routine_id: str) -> Path:
        return self.desk_root / "routines" / f"{routine_id}.md"

    def _primitive_path(self, kind: str, primitive_id: str) -> Path:
        return self.desk_root / "primitives" / kind / f"{primitive_id}.md"

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        matches = sorted(directory.glob(f"{doc_id}*.md"))
        if not matches:
            raise FileNotFoundError(f"No file found for id '{doc_id}' in {directory}")
        return matches[0]

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_model_markdown(model, payload) + "\n", encoding="utf-8")

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        payload = extract_model_data(model, path.read_text(encoding="utf-8"))
        if "id" not in payload:
            payload["id"] = path.stem
        return payload
