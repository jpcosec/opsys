from __future__ import annotations

from dataclasses import dataclass
import json
import logging
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable
from urllib.parse import urlparse

import yaml
from sldb.cli.utils import parse_data_value
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
from deskops.models import MaterializationContractDoc
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
from deskops.workflow.next_actions import load_task_lifecycle_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid


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
    "artifact.materialization": MaterializationContractDoc,
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
    "artifact.materialization": "materializations",
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
    "artifact.materialization": {"subject": "materialization", "list_subject": "materializations"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    return "-".join(parts) or "item"


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML payload in {path}: {exc}") from exc
    return _ensure_mapping_payload(payload, f"YAML payload in {path}")


def _load_json_mapping(raw: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc
    return _ensure_mapping_payload(payload, "JSON payload")


def _ensure_mapping_payload(payload: Any, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        kind = type(payload).__name__
        raise ValueError(f"{label} must be a mapping/object, got {kind}")
    return dict(payload)


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


@dataclass(slots=True)
class RepoTaskRoute:
    repo_id: str
    repo_root: Path
    task_id: str
    task_path: Path
    board_path: Path
    title: str
    status: str


@dataclass(slots=True)
class AtomValidationRecord:
    doc_id: str
    path: Path
    errors: list[str]


@dataclass(slots=True)
class CloseoutGateReport:
    ok: bool
    evidence: list[str]
    findings: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "evidence": list(self.evidence),
            "findings": [dict(item) for item in self.findings],
        }


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = Path(__file__).resolve().parents[1] / "spec"
        self._spec_registry: SpecRegistry | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

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
            Path("materializations"),
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

        rollback_actions: list[Callable[[], None]] = []

        def write_and_track(path: Path, model: type[Any], doc_payload: dict[str, Any]) -> None:
            self._write_new_doc(path, model, doc_payload)
            rollback_actions.append(lambda path=path: self._remove_created_file(path))

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

            board_path = self.desk_root / "tasks" / "Board.md"
            board_text = board_path.read_text(encoding="utf-8")
            rollback_actions.append(lambda: board_path.write_text(board_text, encoding="utf-8"))
            self._append_task_to_board(task_id)
            return TaskBundle(task_id=task_id, task_path=self._task_path(task_id), routine_path=self._routine_path(compiled.routine_payload["id"]))
        except Exception:
            self._rollback(rollback_actions)
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
        self._write_new_doc(path, model, compiled.artifact_payload)
        try:
            self._track_created_artifact(artifact_id, model, path, compiled.artifact_payload["id"])
        except Exception:
            self._remove_created_file(path)
            raise
        return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=compiled.artifact_payload["id"], path=path)

    def create_primitive(self, kind: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        directory, model = PRIMITIVE_KINDS[kind]
        payload = self._normalize_primitive_payload(kind, raw_payload)
        path = self._primitive_path(directory, payload["id"])
        self._write_new_doc(path, model, payload)
        return DocumentRecord(kind=kind, doc_id=payload["id"], path=path)

    def create_routine(self, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        payload = self._normalize_routine_payload(raw_payload)
        path = self._routine_path(payload["id"])
        self._write_new_doc(path, RoutineDoc, payload)
        return DocumentRecord(kind="routine", doc_id=payload["id"], path=path)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        self.ensure_workspace()
        model, path, kind = self._editable_artifact(subject, selector)
        field_name = field.replace("-", "_")
        if field_name not in model.model_fields:
            raise ValueError(f"Unknown field '{field_name}' for {subject}")
        if field_name == "id":
            raise ValueError("Cannot edit immutable field 'id'")
        payload = self._read_doc(path, model)
        payload[field_name] = parse_data_value(raw_value)
        self._write_doc(path, model, payload)
        return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        self.ensure_workspace()
        task_path = self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", task_selector)
        pill_path = self._resolve_artifact_selector("artifact.pill", self.desk_root / "contexts", pill_selector)
        task_payload = self._read_doc(task_path, TaskDoc)
        self._read_doc(pill_path, PillDoc)
        pill_ref = str(pill_path.relative_to(self.root))
        pills = list(task_payload.get("pills") or [])
        if pill_ref in pills:
            return DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path), pill_ref, False
        task_payload["pills"] = [*pills, pill_ref]
        self._write_doc(task_path, TaskDoc, task_payload)
        return DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path), pill_ref, True

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        task_path = self._next_task_path(task_selector, board_path)
        payload = self._resolve_task_payload(task_path.stem)
        spec = load_task_lifecycle_spec(self.spec_root)
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
                "workflow": "spec/workflows/task_lifecycle.yaml",
            },
        }

    def render_next_action_diagram(self) -> str:
        return render_workflow_mermaid(load_task_lifecycle_spec(self.spec_root))

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
            except Exception as e:
                print(f"Warning: Failed to load task {path}: {e}", file=sys.stderr)
        return tasks

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        routes: list[RepoTaskRoute] = []
        for repository in self._registered_repositories():
            repo_root = self._repository_root(repository)
            board_path = repo_root / "desk" / "tasks" / "Board.md"
            if not board_path.exists():
                continue
            try:
                board_payload = self._read_doc(board_path, BoardDoc)
            except Exception:
                continue
            for task_ref in board_payload.get("tasks") or []:
                task_path = self._resolve_repo_board_task_path(repo_root, str(task_ref))
                if task_path is None:
                    continue
                try:
                    summary = self._task_route_summary(task_path)
                except (OSError, UnicodeDecodeError, ValueError):
                    continue
                routes.append(
                    RepoTaskRoute(
                        repo_id=str(repository["id"]),
                        repo_root=repo_root,
                        task_id=summary["id"],
                        task_path=task_path,
                        board_path=board_path,
                        title=summary["title"],
                        status=summary["status"],
                    )
                )
        return routes

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
            except Exception as e:
                print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
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
            except Exception as e:
                print(f"Warning: Failed to load routine {path}: {e}", file=sys.stderr)
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
            except Exception as e:
                print(f"Warning: Failed to load primitive {path}: {e}", file=sys.stderr)
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
        return self._read_doc(self._resolve_artifact_selector(artifact_id, directory, doc_id), model)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        self.ensure_workspace()
        paths = [self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)] if selector else self._all_atom_paths()
        results: list[dict[str, Any]] = []
        for path in paths:
            record = self._validate_atom_path(path)
            results.append({
                "id": record.doc_id,
                "path": str(path),
                "errors": list(record.errors),
            })
        return results

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to delete {atom_id}; inbound references found: {refs}. Re-run with --force to delete without rewriting references."
            )
        untracked = self._untrack_atom_document(atom_id)
        if path.exists():
            path.unlink()
        return DocumentRecord(kind="atom-untracked" if untracked else "atom", doc_id=atom_id, path=path)

    def show_routine(self, routine_id: str) -> Routine | None:
        return self._load_routine(routine_id)

    def show_primitive(self, kind: str, primitive_id: str) -> dict[str, Any]:
        directory_name, model = PRIMITIVE_KINDS[kind]
        return self._read_doc(
            self._resolve_glob(self.desk_root / "primitives" / directory_name, primitive_id),
            model,
        )

    def advance_task(self, task_id: str, target_node: str | None = None) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = self._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = self._read_doc(task_path, TaskDoc)
        task = self._hydrate_task(payload)
        
        if target_node:
            from .runtime.primitives import TransitionResult
            if target_node in ["draft", "open", "in_progress", "blocked", "closed"]:
                payload["status"] = target_node
            else:
                payload["current_node"] = target_node
            self._write_doc(task_path, TaskDoc, payload)
            advanced_task = self._hydrate_task(payload)
            self.logger.info(f"Advanced task {task_id} manually to {target_node}")
            return advanced_task, TransitionResult(target_node, payload.get("status", ""), True, False, f"Forced transition to {target_node}.")

        routine = self._load_routine(task.routine)
        if routine is None:
            return task, None
        conditions = self._load_conditions(task)
        operators = self._load_operators(routine)
        checklists = self._load_checklists(task)
        payload["closeout_evidence_verified"] = self._has_verified_task_closeout_evidence(payload)
        payload["pill_graduation_verified"] = self._has_verified_task_pill_graduation(payload)
        result = routine.advance(
            payload,
            conditions=conditions,
            operators=operators,
            checklists=checklists,
        )
        advanced_task = self._hydrate_task(payload)
        if payload.get("status") == "closed" and payload.get("current_node") == "complete":
            self.logger.info(f"Task {task_id} is complete. Performing auto-commit and cleanup.")
            self._auto_commit_task_closure(payload, task_path)
            return advanced_task, result
        self._write_doc(task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    def parse_task_input(self, args: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(_load_yaml_mapping(Path(args.from_yaml)))
        elif getattr(args, "payload", None):
            payload.update(_load_json_mapping(args.payload))

        if getattr(args, "title", None): payload["title"] = args.title
        if getattr(args, "why", None): payload["why"] = args.why
        if getattr(args, "goal", None): payload["goal"] = args.goal
        if getattr(args, "scope", None): payload["scope"] = args.scope
        if getattr(args, "implementation_path", None): payload["implementation_path"] = args.implementation_path
        if getattr(args, "done_when", None): payload["done_when"] = args.done_when
        if getattr(args, "validation", None): payload["validation"] = args.validation
        if getattr(args, "depends_on", None): payload["depends_on"] = args.depends_on
        if getattr(args, "task_type", None): payload["task_type"] = args.task_type
        if getattr(args, "inherits_from", None): payload["inherits_from"] = args.inherits_from
        if getattr(args, "atom", None): payload["atoms"] = args.atom
        if getattr(args, "inherit_acceptance_context", False): payload["inherit_acceptance_context"] = True

        return payload

    def parse_artifact_input(self, artifact_id: str, args: Any) -> dict[str, Any]:
        """Parse a raw payload for artifact creation.

        YAML payload (--from-yaml) is loaded first, then CLI args override it.
        Field names come from the Pydantic model (the single source of truth),
        not from the YAML spec's fields list.
        """
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(_load_yaml_mapping(Path(args.from_yaml)))

        model = ARTIFACT_MODELS.get(artifact_id)
        if model is not None:
            # Iterate over model fields, not YAML spec fields
            for field_name in model.model_fields:
                if field_name == "id":
                    continue  # id is generated from slug
                value = getattr(args, field_name, None)
                if isinstance(value, list) and value:
                    payload[field_name] = list(value)
                elif value is not None and not isinstance(value, list):
                    payload[field_name] = value

        return payload

    def parse_primitive_input(self, kind: str, args: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if getattr(args, "from_yaml", None):
            payload.update(_load_yaml_mapping(Path(args.from_yaml)))

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
            payload.update(_load_yaml_mapping(Path(args.from_yaml)))

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
            "why": str(payload.get("why") or "Not provided."),
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
            "task_type": str(payload.get("task_type") or ""),
            "inherits_from": self._coerce_list(payload.get("inherits_from") or []),
            "inherit_acceptance_context": bool(payload.get("inherit_acceptance_context") or False),
            "atoms": self._coerce_list(payload.get("atoms") or []),
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
                "title": "Durable evidence is verified",
                "id": f"condition-{task_id}-has-closeout-evidence",
                "status": "active",
                "summary": "Task references must point to a real atom, test, or git commit before closeout.",
                "subject": "closeout_evidence_verified",
                "predicate": "truthy",
                "expected": "",
                "tags": ["primitive:condition"],
            },
            {
                "title": "Pill knowledge is graduated when required",
                "id": f"condition-{task_id}-pill-knowledge-graduated",
                "status": "active",
                "summary": "Tasks with bound pills should reference an atom when durable pill knowledge was discovered; tasks without bound pills pass trivially.",
                "subject": "pill_graduation_verified",
                "predicate": "truthy",
                "expected": "",
                "tags": ["primitive:condition"],
            },
            {
                "title": "Ready for closeout",
                "id": f"condition-{task_id}-ready-for-closeout",
                "status": "active",
                "summary": "Task must be in ready_for_testing and carry testing evidence before closeout.",
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
                "items": ["Task can enter active execution"],
                "condition_refs": [],
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
                "items": [
                    "Task is ready for closeout",
                    "Durable evidence is verified",
                    "Pill knowledge is graduated to atoms when required",
                ],
                "condition_refs": [
                    f"condition-{task_id}-ready-for-closeout",
                    f"condition-{task_id}-has-closeout-evidence",
                ],
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

    def _auto_commit_task_closure(self, payload: dict[str, Any], task_path: Path) -> None:
        task_id = payload.get("id", "unknown-task")
        routine_id = payload.get("routine", "")
        files = self._coerce_list(payload.get("files") or [])

        # 1. Stage project files modified by the task.
        for file in files:
            file_path = self.root / file
            if file_path.exists():
                self.logger.debug(f"Staging file: {file}")
                subprocess.run(["git", "add", str(file)], cwd=self.root, check=False)

        # 2. Stage board changes before removing the task.
        subprocess.run(["git", "add", "desk/tasks/Board.md"], cwd=self.root, check=False)

        # 3. Clean up and stage task removal.
        if task_path.exists():
            subprocess.run(["git", "rm", "--ignore-unmatch", str(task_path.relative_to(self.root))], cwd=self.root, check=False)

        if routine_id:
            routine_path = self._routine_path(routine_id)
            if routine_path.exists():
                subprocess.run(["git", "rm", "--ignore-unmatch", str(routine_path.relative_to(self.root))], cwd=self.root, check=False)

        self._remove_task_runtime_artifacts(task_id, routine_id)

        subprocess.run(["git", "add", "-u", "desk/tasks/"], cwd=self.root, check=False)
        subprocess.run(["git", "add", "-u", "desk/routines/"], cwd=self.root, check=False)
        subprocess.run(["git", "add", "-u", "desk/primitives/"], cwd=self.root, check=False)

        # 4. Commit using the standardized closeout subject used by the CLI closeout surface.
        commit_msg = f"closeout: {task_id}\n\nTask-Id: {task_id}\n"
        self.logger.info(f"Committing closure for {task_id}: {commit_msg.strip()}")
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.root, check=False)

    def _remove_task_runtime_artifacts(self, task_id: str, routine_id: str) -> None:
        self.logger.debug(f"Removing runtime artifacts for task {task_id}")
        board_path = self.desk_root / "tasks" / "Board.md"
        if board_path.exists():
            board_payload = self._read_doc(board_path, BoardDoc)
            task_ref = f"desk/tasks/{task_id}.md"
            tasks = [str(item) for item in board_payload.get("tasks") or [] if str(item) != task_ref]
            board_payload["tasks"] = tasks
            self._write_doc(board_path, BoardDoc, board_payload)
        task_path = self.desk_root / "tasks" / f"{task_id}.md"
        if task_path.exists():
            task_path.unlink()
        if routine_id:
            routine_path = self._routine_path(routine_id)
            if routine_path.exists():
                routine_path.unlink()
        
        # Clean up task-specific primitives
        for directory in ["conditions", "checklists", "operators", "edges", "hooks"]:
            prim_dir = self.desk_root / "primitives" / directory
            if prim_dir.exists():
                for prim_path in prim_dir.glob(f"*-{task_id}*.md"):
                    self.logger.debug(f"Removing primitive {prim_path.name}")
                    prim_path.unlink()

    def _has_verified_task_closeout_evidence(self, payload: dict[str, Any]) -> bool:
        evidence = self._closeout_reference_evidence(payload)
        return any(
            bool(evidence[key])
            for key in ("atom", "tests", "commit")
        )

    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        task_path = self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", task_selector)
        payload = self._resolve_task_payload(task_path.stem)
        reference_evidence = self._closeout_reference_evidence(payload)
        changed_files = self._coerce_list(payload.get("files") or [])
        link_gate = self._closeout_link_gate(payload, changed_files, reference_evidence)
        tests_gate = CloseoutGateReport(
            ok=bool(reference_evidence["tests"]),
            evidence=reference_evidence["tests"],
            findings=[] if reference_evidence["tests"] else [{"code": "missing_tests_evidence", "message": "No resolvable test evidence reference found."}],
        )
        commit_gate = CloseoutGateReport(
            ok=bool(reference_evidence["commit"]),
            evidence=reference_evidence["commit"],
            findings=[] if reference_evidence["commit"] else [{"code": "missing_commit_evidence", "message": "No resolvable commit reference found."}],
        )
        gate_dict = {
            "tests": tests_gate.to_dict(),
            "atom_or_materialization_link": link_gate.to_dict(),
            "commit": commit_gate.to_dict(),
        }
        findings = [
            *tests_gate.findings,
            *link_gate.findings,
            *commit_gate.findings,
        ]
        report = {
            "task_id": str(payload.get("id") or task_path.stem),
            "ok": tests_gate.ok and link_gate.ok and commit_gate.ok,
            "gates": gate_dict,
            "findings": findings,
        }
        if "pill_graduation_verified" in payload:
            report["pill_graduation_verified"] = payload.get("pill_graduation_verified")
        return report

    def _closeout_reference_evidence(self, payload: dict[str, Any]) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": []}
        for reference in self._coerce_list(payload.get("references") or []):
            ref = str(reference).strip()
            if not ref:
                continue
            if self._reference_points_to_test(ref):
                evidence["tests"].append(ref)
            if self._reference_points_to_atom(ref):
                evidence["atom"].append(ref)
            if self._reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if self._reference_points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
        return evidence

    def _closeout_link_gate(
        self,
        payload: dict[str, Any],
        changed_files: list[str],
        reference_evidence: dict[str, list[str]],
    ) -> CloseoutGateReport:
        evidence = list(reference_evidence["atom"])
        findings: list[dict[str, str]] = []
        graph_context = self._build_closeout_graph_context()

        for raw_path in changed_files:
            relative_path = self._normalize_repo_relative_path(raw_path)
            if relative_path is None:
                findings.append(
                    {
                        "code": "changed_file_missing",
                        "path": str(raw_path),
                        "message": "Changed file path does not resolve inside the repository.",
                    }
                )
                continue

            source_finding = self._generated_artifact_source_finding(relative_path)
            if source_finding is not None:
                findings.append(source_finding)

            file_evidence = self._changed_file_link_evidence(relative_path, graph_context)
            if file_evidence:
                evidence.extend(file_evidence)
                continue

            if reference_evidence["follow_up"]:
                for follow_up in reference_evidence["follow_up"]:
                    evidence.append(f"follow-up:{follow_up} -> {relative_path}")
                continue

            findings.append(
                {
                    "code": "missing_changed_file_link",
                    "path": relative_path,
                    "message": "Changed file has no atom/materialization link and no routed follow-up reference.",
                }
            )

        if not changed_files and not reference_evidence["atom"]:
            findings.append(
                {
                    "code": "missing_atom_or_materialization_link",
                    "message": "No atom reference or changed-file materialization coverage found.",
                }
            )

        return CloseoutGateReport(ok=not findings, evidence=self._dedupe_preserve_order(evidence), findings=findings)

    def _has_verified_task_pill_graduation(self, payload: dict[str, Any]) -> bool:
        pills = self._coerce_list(payload.get("pills") or [])
        if not pills:
            return True
        return any(
            self._reference_points_to_atom(str(reference).strip())
            for reference in self._coerce_list(payload.get("references") or [])
            if str(reference).strip()
        )

    def _reference_points_to_atom(self, reference: str) -> bool:
        candidate = reference.strip()
        if not candidate:
            return False
        path_text = candidate.split("::", 1)[0]
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        if path.suffix == ".md" and path.exists():
            try:
                path.relative_to(self.desk_root / "atoms")
                return True
            except ValueError:
                pass
        atom_id = candidate.removeprefix("atom:")
        if not atom_id.startswith("atom-"):
            return False
        return any(atom_path.stem == atom_id for atom_path in (self.desk_root / "atoms").rglob("*.md"))

    def _reference_points_to_routed_follow_up(self, reference: str) -> bool:
        candidate = reference.strip()
        if not candidate:
            return False
        if candidate.startswith(("task:", "issue:")):
            return self._reference_points_to_existing_route(candidate)
        if candidate.endswith(".md"):
            path = Path(candidate.split("::", 1)[0])
            if not path.is_absolute():
                path = self.root / path
            return path.exists() and any(
                self._is_under(path, self.root / relative)
                for relative in ("desk/tasks", "desk/drawer/issues", "desk/drawer/tasks")
            )
        return False

    def _reference_points_to_existing_route(self, reference: str) -> bool:
        kind, _, identifier = reference.partition(":")
        if not identifier:
            return False
        if kind == "task":
            return any(path.stem == identifier for path in (self.desk_root / "tasks").glob("task-*.md"))
        if kind == "issue":
            return any(path.stem == identifier for path in (self.desk_root / "drawer" / "issues").rglob("issue-*.md"))
        return False

    def _all_atom_paths(self) -> list[Path]:
        atoms_dir = self.desk_root / "atoms"
        if not atoms_dir.exists():
            return []
        return sorted(
            path for path in atoms_dir.rglob("*.md")
            if path.name != "tag-namespaces.yaml"
        )

    def _validate_atom_path(self, path: Path) -> AtomValidationRecord:
        errors: list[str] = []
        doc_id = path.stem
        payload: dict[str, Any] | None = None
        try:
            payload = self._read_doc(path, AtomDoc)
            doc_id = str(payload.get("id") or path.stem)
            AtomDoc(**payload)
        except Exception as exc:
            errors.append(f"model validation failed: {exc}")
            return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")
        if not self._is_valid_atom_slug(doc_id):
            errors.append("atom id must follow slug convention atom-<slug>")

        try:
            validate_atom_tag_namespaces(
                list(payload.get("tags") or []),
                default_registry_path(self.root),
            )
        except ValueError as exc:
            errors.append(str(exc))

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

    def _is_valid_atom_slug(self, atom_id: str) -> bool:
        if not atom_id.startswith("atom-"):
            return False
        slug = atom_id.removeprefix("atom-")
        return bool(slug) and slug == slugify(slug)

    def _provenance_is_resolvable(self, provenance: str) -> bool:
        parsed = urlparse(provenance)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return True
        path_text = provenance.split("::", 1)[0].split("#", 1)[0].strip()
        if not path_text:
            return False
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def _find_inbound_atom_references(self, atom_id: str, *, excluded_path: Path | None = None) -> list[str]:
        needle = f"atom:{atom_id}"
        matches: list[str] = []
        if not self.desk_root.exists():
            return matches
        for path in sorted(self.desk_root.rglob("*")):
            if excluded_path is not None and path == excluded_path:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line_number, line in enumerate(lines, start=1):
                for reference in re.findall(r"atom:[a-zA-Z0-9_.-]+", line):
                    if reference == needle and self._reference_points_to_atom(reference):
                        matches.append(f"{path.relative_to(self.root)}:{line_number}")
                        break
        return matches

    def _untrack_atom_document(self, atom_id: str) -> bool:
        store_path = self.root / ".sldb"
        try:
            from sldb.store.io import load_documents_index
            from sldb.store.io import load_models_index
            from sldb.store.io import load_store_index
            from sldb.store.layout import store_exists
            from sldb.cli.commands.doc_helpers import save_untrack_indexes
        except ImportError:
            return False
        if not store_exists(store_path):
            return False

        store_index = load_store_index(store_path)
        model_entry = next((entry for entry in store_index.models if entry.name == AtomDoc.__name__), None)
        if model_entry is None:
            return False

        models_index = load_models_index(self.root / model_entry.models_index)
        documents_index = load_documents_index(self.root / models_index.documents_index)
        tracked_doc = next((entry for entry in documents_index.documents if entry.name == atom_id or entry.path.endswith(f"/{atom_id}.md") or entry.path == f"desk/atoms/{atom_id}.md"), None)
        if tracked_doc is None:
            return False
        documents_index.documents = [entry for entry in documents_index.documents if entry.name != tracked_doc.name]
        save_untrack_indexes(store_path, self.root, store_index, model_entry, models_index, documents_index, str(Path(__file__).resolve().parents[1]))
        return True

    def _reference_points_to_test(self, reference: str) -> bool:
        candidates: list[str] = []
        stripped = reference.strip()
        if stripped.startswith("pytest "):
            for token in stripped.split()[1:]:
                token = token.strip("\"'")
                if token.startswith("-"):
                    continue
                if ".py" in token:
                    candidates.append(token)
        elif ".py" in stripped:
            candidates.append(stripped)
        for candidate in candidates:
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path.is_absolute():
                path = self.root / path
            if path.suffix == ".py" and path.exists():
                return True
        return False

    def _reference_points_to_commit(self, reference: str) -> bool:
        candidate = reference.strip()
        if not candidate or " " in candidate:
            return False
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return result.returncode == 0

    def _build_closeout_graph_context(self) -> dict[str, Any]:
        from deskops.graph.extract_docs import extract_doc_nodes
        from deskops.graph.extract_edges import extract_declared_edges
        from deskops.graph.extract_sources import extract_source_file_nodes

        doc_nodes = extract_doc_nodes(self.root)
        source_nodes = extract_source_file_nodes(self.root)
        by_path = {node.path: node.id for node in [*doc_nodes, *source_nodes]}
        extraction = extract_declared_edges(self.root)
        invalid_materializations = {
            missing.source_id
            for missing in extraction.missing_targets
            if missing.source_id.startswith("materialization:")
        }
        return {
            "node_ids_by_path": by_path,
            "edges": extraction.edges,
            "invalid_materializations": invalid_materializations,
        }

    def _changed_file_link_evidence(self, relative_path: str, graph_context: dict[str, Any]) -> list[str]:
        evidence: list[str] = []
        path = self.root / relative_path
        if path.suffix == ".md" and self._is_under(path, self.desk_root / "atoms"):
            evidence.append(f"atom-doc:{relative_path}")
        node_id = graph_context["node_ids_by_path"].get(relative_path)
        if node_id is None:
            return evidence
        for edge in graph_context["edges"]:
            if edge.source_id == node_id and edge.target_id.startswith("atom:"):
                evidence.append(f"graph:{node_id}->{edge.target_id}")
            if edge.target_id == node_id and edge.source_id.startswith("materialization:"):
                if edge.source_id in graph_context["invalid_materializations"]:
                    continue
                evidence.append(f"materialization:{edge.source_id}->{relative_path}")
        return self._dedupe_preserve_order(evidence)

    def _generated_artifact_source_finding(self, relative_path: str) -> dict[str, str] | None:
        path = self.root / relative_path
        sibling = self._find_generated_artifact_source_sibling(path)
        if sibling is None or not path.exists() or path.suffix not in {".md", ".json"}:
            return None
        if self._declares_materialization_sources(path):
            return None
        return {
            "code": "generated_artifact_missing_declared_sources",
            "path": relative_path,
            "message": f"Rendered artifact has sibling source {sibling.name} but does not declare source_atoms or provenance.",
        }

    def _find_generated_artifact_source_sibling(self, path: Path) -> Path | None:
        for suffix in (".mmd", ".yaml", ".yml"):
            sibling = path.with_suffix(suffix)
            if sibling != path and sibling.exists():
                return sibling
        return None

    def _declares_materialization_sources(self, path: Path) -> bool:
        if path.suffix not in {".md", ".yaml", ".yml", ".json"}:
            return False
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return False
        if path.suffix == ".json":
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                return False
            if not isinstance(loaded, dict):
                return False
            return bool(loaded.get("source_atoms") or loaded.get("provenance"))
        if not text.startswith("---\n"):
            return False
        try:
            _, rest = text.split("---\n", 1)
            block, _body = rest.split("\n---", 1)
        except ValueError:
            return False
        loaded = yaml.safe_load(block) or {}
        if not isinstance(loaded, dict):
            return False
        return bool(loaded.get("source_atoms") or loaded.get("provenance"))

    def _normalize_repo_relative_path(self, raw_path: str) -> str | None:
        candidate = Path(str(raw_path).split("::", 1)[0].strip())
        if not candidate:
            return None
        if not candidate.is_absolute():
            candidate = (self.root / candidate).resolve()
        else:
            candidate = candidate.resolve()
        try:
            return candidate.relative_to(self.root).as_posix()
        except ValueError:
            return None

    def _dedupe_preserve_order(self, values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    def _is_under(self, path: Path, parent: Path) -> bool:
        try:
            path.resolve().relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _merge_unique(self, *values: list[str]) -> list[str]:
        merged: list[str] = []
        seen: set[str] = set()
        for value_list in values:
            for value in value_list:
                item = str(value)
                if item in seen:
                    continue
                seen.add(item)
                merged.append(item)
        return merged

    def _resolve_task_payload(self, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
        if task_id in stack:
            chain = " -> ".join([*stack, task_id])
            raise ValueError(f"Task inheritance cycle detected: {chain}")
        path = self._resolve_glob(self.desk_root / "tasks", task_id)
        payload = self._normalize_task_payload(self._read_doc(path, TaskDoc))
        inherited_ids = self._coerce_list(payload.get("inherits_from") or [])
        inherited_payloads = [self._resolve_task_payload(parent_id, (*stack, task_id)) for parent_id in inherited_ids]

        payload["effective_references"] = self._merge_unique(
            *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
            payload.get("references", []),
        )
        payload["effective_pills"] = self._merge_unique(
            *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
            payload.get("pills", []),
        )
        payload["effective_tags"] = self._merge_unique(
            *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
            payload.get("tags", []),
        )
        payload["effective_atoms"] = self._merge_unique(
            *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
            payload.get("atoms", []),
        )

        if payload.get("inherit_acceptance_context"):
            payload["effective_validation"] = self._merge_unique(
                *[parent.get("effective_validation", parent.get("validation", [])) for parent in inherited_payloads],
                payload.get("validation", []),
            )
            parent_done_when = next(
                (
                    str(parent.get("effective_done_when") or parent.get("done_when") or "")
                    for parent in inherited_payloads
                    if str(parent.get("effective_done_when") or parent.get("done_when") or "")
                ),
                "",
            )
            payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
        else:
            payload["effective_validation"] = self._coerce_list(payload.get("validation") or [])
            payload["effective_done_when"] = str(payload.get("done_when") or "")
        return payload

    def _load_task(self, task_id: str) -> Task:
        return self._hydrate_task(self._resolve_task_payload(task_id))

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
            task_type=payload.get("task_type", ""),
            inherits_from=list(payload.get("inherits_from") or []),
            inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
            atoms=list(payload.get("atoms") or []),
            effective_references=list(payload.get("effective_references") or payload.get("references") or []),
            effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
            effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
            effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
            effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
            effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
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

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        pattern = self._artifact_glob_pattern(artifact_id)
        candidates = sorted(directory.rglob(pattern))
        exact = [path for path in candidates if selector in {path.name, path.stem}]
        if exact:
            return self._one_artifact_match(artifact_id, directory, selector, exact)

        prefix = [path for path in candidates if path.name.startswith(selector) or path.stem.startswith(selector)]
        if not prefix:
            raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}' in {directory}")
        return self._one_artifact_match(artifact_id, directory, selector, prefix)

    def _registered_repositories(self) -> list[dict[str, Any]]:
        registry_dir = self.desk_root / "registry"
        if not registry_dir.exists():
            return []
        repositories = []
        for path in sorted(registry_dir.glob("repo-*.md")):
            try:
                repositories.append(self._read_doc(path, RepositoryDoc))
            except Exception as e:
                print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
                continue
        return repositories

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

    def _repository_root(self, repository: dict[str, Any]) -> Path:
        repo_path = Path(str(repository["path"]))
        if repo_path.is_absolute():
            return repo_path.resolve()
        return (self.root / repo_path).resolve()

    def _resolve_repo_board_task_path(self, repo_root: Path, task_ref: str) -> Path | None:
        tasks_root = (repo_root / "desk" / "tasks").resolve()
        task_path = Path(task_ref)
        if not task_path.is_absolute():
            task_path = repo_root / task_path
        task_path = task_path.resolve()
        try:
            task_path.relative_to(tasks_root)
        except ValueError:
            return None
        if not task_path.name.startswith("task-") or task_path.suffix != ".md":
            return None
        if not task_path.is_file():
            return None
        return task_path

    def _task_route_summary(self, task_path: Path) -> dict[str, str]:
        text = task_path.read_text(encoding="utf-8")
        payload: dict[str, Any] = {}
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    frontmatter = None
                if isinstance(frontmatter, dict):
                    payload = frontmatter
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), task_path.stem)
        legacy_status = next((line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Status:")), "unknown")
        task_id = str(payload.get("id") or task_path.stem)
        if not task_id.startswith("task-"):
            raise ValueError(f"Routed task id must start with 'task-': {task_id}")
        return {
            "id": task_id,
            "status": str(payload.get("status") or legacy_status),
            "title": title,
        }

    def _one_artifact_match(self, artifact_id: str, directory: Path, selector: str, matches: list[Path]) -> Path:
        if len(matches) == 1:
            return matches[0]
        relative = ", ".join(str(path.relative_to(directory)) for path in matches)
        raise ValueError(f"Ambiguous {artifact_id} selector '{selector}' in {directory}: {relative}")

    def _editable_artifact(self, subject: str, selector: str) -> tuple[type[Any], Path, str]:
        if subject == "task":
            return TaskDoc, self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", selector), "task"
        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if subject not in artifact_subjects:
            raise ValueError(f"Unsupported edit subject: {subject}")
        artifact_id = artifact_subjects[subject]
        model = ARTIFACT_MODELS[artifact_id]
        directory = self.desk_root / ARTIFACT_PATHS[artifact_id]
        path = self._resolve_artifact_selector(artifact_id, directory, selector)
        return model, path, subject

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_model_markdown(model, payload) + "\n", encoding="utf-8")

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing document: {path}")
        try:
            self._write_doc(path, model, payload)
        except Exception:
            self._remove_created_file(path)
            raise

    def _remove_created_file(self, path: Path) -> None:
        if path.exists():
            path.unlink()

    def _rollback(self, rollback_actions: list[Callable[[], None]]) -> None:
        for action in reversed(rollback_actions):
            action()

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        if artifact_id != "artifact.atom":
            return
        store_path = self.root / ".sldb"
        try:
            from sldb.cli.model_utils import resolve_model_ref
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
