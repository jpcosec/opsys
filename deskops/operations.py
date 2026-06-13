from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import ChecklistDoc
from deskops.models import ConditionDoc
from deskops.models import EdgeDoc
from deskops.models import FAQDoc
from deskops.models import HookDoc
from deskops.models import InboxNoteDoc
from deskops.models import OperatorDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import RitualDoc
from deskops.models import RoutineDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.runtime import Checklist
from deskops.runtime import Condition
from deskops.runtime import Edge
from deskops.runtime import Hook
from deskops.runtime import Operator
from deskops.runtime import Routine
from deskops.runtime import Task
from deskops.runtime import TransitionResult
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
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
    "artifact.atom": "atoms",
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
            Path("routines"),
            Path("atoms"),
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
        ensure_default_namespaces(default_registry_path(self.root))

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        self.ensure_workspace()
        payload = self._normalize_task_payload(raw_payload)
        compiled = compile_task_bundle_spec(self.spec_registry, payload)
        task_id = compiled.task_payload["id"]

        written_paths: list[Path] = []

        def write_and_track(path: Path, model: type[Any], doc_payload: dict[str, Any]) -> None:
            self._write_doc(path, model, doc_payload)
            written_paths.append(path)

        try:
            write_and_track(self._task_path(task_id), TaskDoc, compiled.task_payload)
            write_and_track(self._routine_path(compiled.routine_payload["id"]), RoutineDoc, compiled.routine_payload)
            for item in compiled.condition_payloads:
                write_and_track(self._primitive_path("conditions", item["id"]), ConditionDoc, item)
            for item in compiled.checklist_payloads:
                write_and_track(self._primitive_path("checklists", item["id"]), ChecklistDoc, item)
            for item in compiled.operator_payloads:
                write_and_track(self._primitive_path("operators", item["id"]), OperatorDoc, item)
            for item in compiled.edge_payloads:
                write_and_track(self._primitive_path("edges", item["id"]), EdgeDoc, item)

            self._append_task_to_board(task_id)
            return TaskBundle(task_id=task_id, task_path=self._task_path(task_id), routine_path=self._routine_path(compiled.routine_payload["id"]))
        except Exception:
            for path in written_paths:
                if path.exists():
                    path.unlink()
            raise

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
        if artifact_id == "artifact.atom":
            validate_atom_tag_namespaces(
                list(compiled.artifact_payload.get("tags") or []),
                default_registry_path(self.root),
            )
        self._write_doc(path, model, compiled.artifact_payload)
        self._track_created_artifact(artifact_id, model, path, compiled.artifact_payload["id"])
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
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            try:
                tasks.append(self._load_task(path.stem))
            except Exception:
                pass
        return tasks

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        model = ARTIFACT_MODELS[artifact_id]
        directory = self.desk_root / ARTIFACT_PATHS[artifact_id]
        if not directory.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        pattern = self._artifact_glob_pattern(artifact_id)
        results = []
        for path in sorted(directory.rglob(pattern)):
            try:
                results.append(self._read_doc(path, model))
            except Exception:
                pass
        return results

    def list_routines(self) -> list[Routine]:
        routine_dir = self.desk_root / "routines"
        if not routine_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        results = []
        for path in sorted(routine_dir.glob("routine-*.md")):
            try:
                results.append(self._load_routine(path.stem))
            except Exception:
                pass
        return results

    def list_primitives(self, kind: str) -> list[dict[str, Any]]:
        directory, model = PRIMITIVE_KINDS[kind]
        primitive_dir = self.desk_root / "primitives" / directory
        if not primitive_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        prefix = f"{kind}-"
        results = []
        for path in sorted(primitive_dir.glob(f"{prefix}*.md")):
            try:
                results.append(self._read_doc(path, model))
            except Exception:
                pass
        return results

    def show_task(self, task_id: str) -> tuple[Task | None, dict[str, bool]]:
        try:
            task = self._load_task(task_id)
        except FileNotFoundError:
            return None, {}
        statuses = self._checklist_statuses(task)
        return task, statuses

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        if not doc_id:
            raise ValueError(f"No {artifact_id} ID provided")
        model = ARTIFACT_MODELS[artifact_id]
        directory = self.desk_root / ARTIFACT_PATHS[artifact_id]
        exact_match = directory / f"{doc_id}.md"
        if exact_match.exists():
            return self._read_doc(exact_match, model)
        exact_matches = sorted(directory.rglob(f"{doc_id}.md"))
        if exact_matches:
            return self._read_doc(exact_matches[0], model)
        matches = sorted(directory.rglob(f"{doc_id}*.md"))
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
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {})
        elif getattr(args, "payload", None):
            payload.update(json.loads(args.payload))

        if getattr(args, "title", None): payload["title"] = args.title
        if getattr(args, "goal", None): payload["goal"] = args.goal
        if getattr(args, "scope", None): payload["scope"] = args.scope
        if getattr(args, "implementation_path", None): payload["implementation_path"] = args.implementation_path
        if getattr(args, "done_when", None): payload["done_when"] = args.done_when
        if getattr(args, "validation", None): payload["validation"] = args.validation

        return payload

    def parse_artifact_input(self, artifact_id: str, args: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {})
        artifact = self.spec_registry.artifacts[artifact_id]
        for field_id in artifact["data"].get("fields", []):
            field_spec = self.spec_registry.fields[field_id]
            key = str(field_spec["data"]["key"])
            attr = key
            value = getattr(args, attr, None)
            if isinstance(value, list) and value:
                payload[key] = list(value)
            elif value is not None and not isinstance(value, list):
                payload[key] = value
        return payload

    def parse_primitive_input(self, kind: str, args: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {})

        if getattr(args, "title", None): payload["title"] = args.title
        if getattr(args, "summary", None): payload["summary"] = args.summary
        if getattr(args, "status", None): payload["status"] = args.status
        if getattr(args, "tags", None): payload["tags"] = args.tags

        if "title" not in payload: payload["title"] = getattr(args, "title", None)
        if "status" not in payload: payload["status"] = getattr(args, "status", "active") or "active"
        if "tags" not in payload: payload["tags"] = getattr(args, "tags", []) or [f"primitive:{kind}"]

        if kind == "condition":
            if getattr(args, "subject_path", None): payload["subject"] = args.subject_path
            if getattr(args, "predicate", None): payload["predicate"] = args.predicate
            if getattr(args, "expected", None): payload["expected"] = args.expected
            if "subject" not in payload: payload["subject"] = getattr(args, "subject_path", None)
            if "predicate" not in payload: payload["predicate"] = getattr(args, "predicate", None)
        elif kind == "operator":
            if getattr(args, "action", None): payload["action"] = args.action
            if getattr(args, "target", None): payload["target"] = args.target
            if getattr(args, "value", None): payload["value"] = args.value
            if "action" not in payload: payload["action"] = getattr(args, "action", None)
            if "target" not in payload: payload["target"] = getattr(args, "target", None)
        elif kind == "checklist":
            if getattr(args, "item", None): payload["items"] = list(args.item)
            if getattr(args, "condition_ref", None): payload["condition_refs"] = list(args.condition_ref)
            if getattr(args, "mode", None): payload["mode"] = args.mode
            if "items" not in payload: payload["items"] = list(getattr(args, "item", []) or [])
            if "condition_refs" not in payload: payload["condition_refs"] = list(getattr(args, "condition_ref", []) or [])
            if "mode" not in payload: payload["mode"] = getattr(args, "mode", "all") or "all"
        elif kind == "hook":
            if getattr(args, "event", None): payload["event"] = args.event
            if getattr(args, "target_ref", None): payload["target"] = args.target_ref
            if getattr(args, "condition_ref", None): payload["condition_ref"] = args.condition_ref
            if "event" not in payload: payload["event"] = getattr(args, "event", None)
            if "target" not in payload: payload["target"] = getattr(args, "target_ref", None)
        elif kind == "edge":
            if getattr(args, "source", None): payload["source"] = args.source
            if getattr(args, "target_node", None): payload["target"] = args.target_node
            if getattr(args, "condition_ref", None): payload["condition_ref"] = args.condition_ref
            if "source" not in payload: payload["source"] = getattr(args, "source", None)
            if "target" not in payload: payload["target"] = getattr(args, "target_node", None)

        return payload

    def parse_routine_input(self, args: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(yaml.safe_load(Path(args.from_yaml).read_text(encoding="utf-8")) or {})

        if getattr(args, "title", None): payload["title"] = args.title
        if getattr(args, "summary", None): payload["summary"] = args.summary
        if getattr(args, "entrypoint", None): payload["entrypoint"] = args.entrypoint
        if getattr(args, "decomposition", None): payload["decomposition"] = list(args.decomposition)
        if getattr(args, "edge", None): payload["edges"] = list(args.edge)
        if getattr(args, "terminal_node", None): payload["terminal_nodes"] = list(args.terminal_node)
        if getattr(args, "tags", None): payload["tags"] = args.tags

        if "title" not in payload: payload["title"] = getattr(args, "title", None)
        if "summary" not in payload: payload["summary"] = getattr(args, "summary", "") or ""
        if "entrypoint" not in payload: payload["entrypoint"] = getattr(args, "entrypoint", None)
        if "decomposition" not in payload: payload["decomposition"] = list(getattr(args, "decomposition", []) or [])
        if "edges" not in payload: payload["edges"] = list(getattr(args, "edge", []) or [])
        if "terminal_nodes" not in payload: payload["terminal_nodes"] = list(getattr(args, "terminal_node", ["complete"]) or ["complete"])
        if "tags" not in payload: payload["tags"] = getattr(args, "tags", []) or ["primitive:routine"]
        return payload

    def _normalize_task_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if payload.get("title") is None:
            raise KeyError("Task payload must include 'title'")
        title = str(payload["title"]).strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        task_id = str(payload.get("id") or f"task-{slugify(title)}")
        return {
            "title": title,
            "id": task_id,
            "status": str(payload.get("status") or "draft"),
            "goal": str(payload.get("goal") or ""),
            "scope": str(payload.get("scope") or ""),
            "references": self._coerce_list(payload.get("references") or []),
            "depends_on": self._coerce_list(payload.get("depends_on") or []),
            "pills": self._coerce_list(payload.get("pills") or []),
            "files": self._coerce_list(payload.get("files") or []),
            "routine": str(payload.get("routine") or ""),
            "checklists": self._coerce_list(payload.get("checklists") or []),
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
        if payload.get("title") is None:
            raise KeyError("Routine payload must include 'title'")
        title = str(payload["title"]).strip()
        if not title:
            raise ValueError("Routine title cannot be empty")
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
            checklists=list(payload.get("checklists") or []),
            implementation_path=payload.get("implementation_path", ""),
            validation=list(payload.get("validation") or []),
            done_when=payload.get("done_when", ""),
        )

    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _artifact_path(self, artifact_id: str, doc_id: str) -> Path:
        return self.desk_root / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"

    def _artifact_glob_pattern(self, artifact_id: str) -> str:
        if artifact_id in {"artifact.inbox_note", "artifact.board", "artifact.ritual"}:
            return "*.md"
        spec = self.spec_registry.artifacts[artifact_id]
        id_pattern = str(spec["data"]["doc"]["id_pattern"])
        return id_pattern.replace("{slug}", "*") + ".md"

    def _routine_path(self, routine_id: str) -> Path:
        return self.desk_root / "routines" / f"{routine_id}.md"

    def _primitive_path(self, kind: str, primitive_id: str) -> Path:
        return self.desk_root / "primitives" / kind / f"{primitive_id}.md"

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        exact_match = directory / f"{doc_id}.md"
        if exact_match.exists():
            return exact_match
        matches = sorted(directory.glob(f"{doc_id}*.md"))
        if not matches:
            raise FileNotFoundError(f"No file found for id '{doc_id}' in {directory}")
        return matches[0]

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_model_markdown(model, payload) + "\n", encoding="utf-8")

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        if artifact_id != "artifact.atom":
            return
        store_path = self.root / ".sldb"
        try:
            from sldb.cli.utils import resolve_model_ref
            from sldb.store.io import load_documents_index
            from sldb.store.io import load_models_index
            from sldb.store.io import load_store_index
            from sldb.store.layout import store_exists
            from sldb.store.ops import track_document
        except ImportError:
            return
        if not store_exists(store_path):
            return

        store_index = load_store_index(store_path)
        model_entry = next((entry for entry in store_index.models if entry.name == model.__name__), None)
        if model_entry is None:
            return

        models_index = load_models_index(self.root / model_entry.models_index)
        documents_index = load_documents_index(self.root / models_index.documents_index)
        if any(entry.name == doc_id for entry in documents_index.documents):
            return

        track_document(
            store_path,
            self.root,
            store_index,
            model,
            model_entry,
            path,
            doc_id,
            resolve_model_ref,
            str(Path(__file__).resolve().parents[1]),
        )

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        payload = extract_model_data(model, path.read_text(encoding="utf-8"))
        if "id" not in payload:
            payload["id"] = path.stem
        return payload
