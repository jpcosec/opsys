from __future__ import annotations

from dataclasses import dataclass
import json
import logging
from pathlib import Path
import re
import sys
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import yaml
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import FAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.runtime import Task
from deskops import doc_io
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import axis_values
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.desk_paths import resolve_selector
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.paths import data_path
from deskops.specs import compile_artifact_spec
from deskops.specs import SpecRegistry
from deskops.workspace import scaffold_desk
from deskops.workflow.next_actions import load_task_lifecycle_spec
from deskops.workflow.next_actions import render_workflow_mermaid

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closeout import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService


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
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    Free text such as `Fuente: a.md:3, b` is a YAML mapping error (or a dict), not
    what the user meant for a `str` field, so those fall back to the raw string.
    """
    annotation = model.model_fields[field_name].annotation
    try:
        value = parse_data_value(raw_value)
    except Exception:
        if annotation is str:
            return raw_value
        raise
    if annotation is str and not isinstance(value, str):
        return raw_value
    return value


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path


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
class AtomSplitResult:
    original_id: str
    original_path: Path
    created: list[DocumentRecord]
    redirect_kept: bool
    inbound_references: list[str]


@dataclass(slots=True)
class AtomMergeResult:
    source_id: str
    source_path: Path
    target_id: str
    target_path: Path
    redirect_kept: bool
    rewritten_references: list[str]
    ambiguities: list[str]


@dataclass(slots=True)
class AtomCreateResult:
    doc_id: str
    path: Path
    source_kind: str
    source_selector: str
    provenance: str


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
        self.spec_root = data_path("spec")
        self._spec_registry: SpecRegistry | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
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
            Path("atoms"),
            Path("materializations"),
            Path("steps"),
            Path("registry"),
            Path("faq"),
        ]:
            (self.desk_root / relative).mkdir(parents=True, exist_ok=True)
        ensure_default_namespaces(default_registry_path(self.root))

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        self.ensure_workspace()
        model = ARTIFACT_MODELS[artifact_id]
        compiled = compile_artifact_spec(
            self.spec_registry,
            artifact_id,
            raw_payload,
            model_fields=model.model_fields.keys(),
        )
        if artifact_id == "artifact.atom":
            validate_atom_tag_namespaces(
                list(compiled.artifact_payload.get("tags") or []),
                default_registry_path(self.root),
            )
            from deskops.domain_tree import require_domain_parents

            require_domain_parents(self.desk_root / "atoms", list(compiled.artifact_payload.get("tags") or []))
            path = self._atom_doc_path(
                compiled.artifact_payload["id"],
                list(compiled.artifact_payload.get("tags") or []),
            )
        else:
            path = self._artifact_path(artifact_id, compiled.artifact_payload["id"])
        with doc_io.DocTransaction(self.root):
            self._write_new_doc(path, model, compiled.artifact_payload)
            self._track_created_artifact(artifact_id, model, path, compiled.artifact_payload["id"])
        return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=compiled.artifact_payload["id"], path=path)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        self.ensure_workspace()
        model, path, kind = self._editable_artifact(subject, selector)
        field_name = field.replace("-", "_")
        if field_name not in model.model_fields:
            raise ValueError(f"Unknown field '{field_name}' for {subject}")
        if field_name == "id":
            raise ValueError("Cannot edit immutable field 'id'")
        payload = self._read_doc(path, model)
        payload[field_name] = _parse_field_value(model, field_name, raw_value)
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

    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService
            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService
            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService
            self._tasks = TasksService(self.root, self)
        return self._tasks

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def advance_task(self, task_id: str, target_node: str | None = None) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id, target_node=target_node)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def _auto_commit_task_closure(self, payload: dict[str, Any], task_path: Path) -> None:
        # Kept as a delegating hook: the closure commit itself lives in the
        # tasks service, but tests and callers exercise it through operations.
        self.tasks._auto_commit_task_closure(payload, task_path)

    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

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

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        """The task and the lifecycle transitions leaving its current node, each with
        whether its condition holds now (empty when the graph is missing or the task is
        complete)."""
        try:
            task = self._load_task(task_id)
        except FileNotFoundError:
            return None, []
        return task, self._lifecycle_gates(task)

    def _lifecycle_gates(self, task: Task) -> list[dict[str, Any]]:
        if not task.current_node or task.current_node == lifecycle.COMPLETE:
            return []
        try:
            transitions = lifecycle.transitions_from(self.root, task.current_node)
        except Exception:
            return []
        payload = self._read_doc(self._resolve_glob(self.desk_root / "tasks", task.id), TaskDoc)
        self._add_closeout_facts(payload)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": lifecycle.condition_holds(t.condition, payload),
            }
            for t in transitions
        ]

    def _add_closeout_facts(self, payload: dict[str, Any]) -> None:
        """Facts the lifecycle conditions test with has(): present only when they hold."""
        for key, holds in (
            ("closeout_evidence_verified", self._has_verified_task_closeout_evidence(payload)),
            ("pill_graduation_verified", self._has_verified_task_pill_graduation(payload)),
        ):
            if holds:
                payload[key] = "verified"
            else:
                payload.pop(key, None)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        if not doc_id:
            raise ValueError(f"No {artifact_id} ID provided")
        model = ARTIFACT_MODELS[artifact_id]
        directories = [self.desk_root / ARTIFACT_PATHS[artifact_id]]
        if artifact_id == "artifact.pill":
            directories.append(self.desk_root / "drawer" / "pills")
        return self._read_doc(self._resolve_artifact_selector_multi(artifact_id, directories, doc_id), model)

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService
            self._atoms = AtomsService(self.root, self)
        return self._atoms

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = self._read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            self._write_doc(board_path, BoardDoc, board_payload)

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
            "from_drawer": str(payload.get("from_drawer") or ""),
        }

    def _coerce_list(self, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if value in (None, ""):
            return []
        return [str(value)]

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
        return self.closeout_gates.closeout_reference_evidence(
            payload,
            points_to_atom=self._reference_points_to_atom,
            points_to_routed_follow_up=self._reference_points_to_routed_follow_up,
        )

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

    def _find_inbound_atom_references(self, atom_id: str, *, excluded_path: Path | None = None) -> list[str]:
        return self.atoms._find_inbound_atom_references(atom_id, excluded_path=excluded_path)

    def _rewrite_inbound_atom_references(
        self,
        source_id: str,
        target_id: str,
        *,
        excluded_paths: set[Path] | None = None,
        transaction: doc_io.DocTransaction | None = None,
    ) -> list[str]:
        return self.atoms._rewrite_inbound_atom_references(
            source_id,
            target_id,
            excluded_paths=excluded_paths,
            transaction=transaction,
        )

    def _reference_points_to_test(self, reference: str) -> bool:
        return self.closeout_gates.reference_points_to_test(reference)

    def _reference_points_to_commit(self, reference: str) -> bool:
        return self.closeout_gates.reference_points_to_commit(reference)

    def _build_closeout_graph_context(self) -> dict[str, Any]:
        return self.closeout_gates.build_closeout_graph_context()

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

    def _hydrate_task(self, payload: dict[str, Any]) -> Task:
        return Task(
            id=payload["id"],
            title=payload["title"],
            status=payload["status"],
            summary=payload["goal"],
            tags=list(payload.get("tags") or []),
            current_node=payload.get("current_node", ""),
            history=list(payload.get("history") or []),
            goal=payload.get("goal", ""),
            scope=payload.get("scope", ""),
            references=list(payload.get("references") or []),
            depends_on=list(payload.get("depends_on") or []),
            pills=list(payload.get("pills") or []),
            files=list(payload.get("files") or []),
            implementation_path=payload.get("implementation_path", ""),
            validation=list(payload.get("validation") or []),
            done_when=payload.get("done_when", ""),
            task_type=payload.get("task_type", ""),
            inherits_from=list(payload.get("inherits_from") or []),
            inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
            atoms=list(payload.get("atoms") or []),
            from_drawer=payload.get("from_drawer") or "",
            effective_references=list(payload.get("effective_references") or payload.get("references") or []),
            effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
            effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
            effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
            effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
            effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
        )

    def _artifact_path(self, artifact_id: str, doc_id: str) -> Path:
        return self.desk_root / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        return self.atoms.atom_folder_axis()

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return self.atoms._atom_doc_path(atom_id, tags)

    def _artifact_glob_pattern(self, artifact_id: str) -> str:
        if artifact_id in {"artifact.inbox_note", "artifact.board", "artifact.ritual"}:
            return "*.md"
        spec = self.spec_registry.artifacts[artifact_id]
        id_pattern = str(spec["data"]["doc"]["id_pattern"])
        return id_pattern.replace("{slug}", "*") + ".md"

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return resolve_selector(self.desk_root, [directory], doc_id, f"{doc_id}*.md", "task", recursive=False)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return resolve_selector(
            self.desk_root,
            directories,
            selector,
            self._artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        try:
            return resolve_selector(
                self.desk_root,
                [directory],
                selector,
                self._artifact_glob_pattern(artifact_id),
                artifact_id,
                recursive=True,
            )
        except FileNotFoundError:
            tracked = self._tracked_task_paths() if artifact_id == "artifact.task" else set()
            if not tracked:
                raise
        # Tasks written before the `task-*` naming are still tracked TaskDocs.
        return resolve_selector(
            self.desk_root,
            [directory],
            selector,
            "*.md",
            artifact_id,
            recursive=True,
            keep=lambda path: path.resolve() in tracked,
        )

    def _tracked_task_paths(self) -> set[Path]:
        records = self.root / ".sldb" / "core" / "documents" / "TaskDoc"
        if not records.is_dir():
            return set()
        tracked = set()
        for record in records.glob("*.yaml"):
            try:
                path = (yaml.safe_load(record.read_text(encoding="utf-8")) or {}).get("path")
            except (OSError, yaml.YAMLError):
                continue
            if path:
                tracked.add((self.root / path).resolve())
        return tracked

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

    def _editable_artifact(self, subject: str, selector: str) -> tuple[type[Any], Path, str]:
        if subject == "task":
            return TaskDoc, self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", selector), "task"
        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if subject not in artifact_subjects:
            raise ValueError(f"Unsupported edit subject: {subject}")
        artifact_id = artifact_subjects[subject]
        model = ARTIFACT_MODELS[artifact_id]
        directories = [self.desk_root / ARTIFACT_PATHS[artifact_id]]
        if artifact_id == "artifact.pill":
            directories.append(self.desk_root / "drawer" / "pills")
        path = self._resolve_artifact_selector_multi(artifact_id, directories, selector)
        return model, path, subject

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        rendered = render_model_markdown(model, payload) + "\n"
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            # A short new value is not proof the model cannot read the file: only
            # refuse when the current text really extracts empty for that field.
            unreadable = set(is_unreadable_by_model(model, existing))
            lost = [field for field in unread_section_fields(model, existing, rendered) if field in unreadable]
            if lost:
                raise ValueError(
                    f"Refusing to rewrite {path.name}: its model cannot read "
                    f"{', '.join(lost)} from the current file, so writing this payload "
                    "would erase that content. The document was not produced by the "
                    "model's own renderer; rewrite it through sldb (or fix the model's "
                    "template) before editing it here."
                )
            # Headings and frontmatter keys the template never declares are dropped by
            # extraction; refuse when the rewrite would erase one. A heading counts only
            # if re-rendering the file's own payload loses it, so replacing a field that
            # carries a heading (atoms split/merge) is not refused.
            kept = set((render_model_markdown(model, extract_model_data(model, existing)) + "\n").splitlines())
            erased = [line for line in find_structural_noise(model, existing, path.name).undeclared if line not in kept]
            erased += [f"frontmatter key '{key}'" for key in undeclared_frontmatter_keys(model, existing)]
            if erased:
                raise ValueError(
                    f"Refusing to rewrite {path.name}: it has content its model "
                    f"({model.__name__}) does not declare, and rewriting would erase it: "
                    f"{'; '.join(erased)}. Move that content into a declared field "
                    "(or remove it) before editing the document here."
                )
        with doc_io.DocTransaction(self.root) as transaction:
            transaction.write(path, model, payload)

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

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        if artifact_id != "artifact.atom":
            return
        self._track_created_document(model, path, doc_id)

    def _track_created_document(self, model: type[Any], path: Path, doc_id: str) -> None:
        doc_io.track(self.root, path, model, name=doc_id)

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        raw_text = path.read_text(encoding="utf-8")
        payload = extract_model_data(model, raw_text)
        if "id" not in payload:
            payload["id"] = path.stem
        return payload
