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
from deskops.models import FAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.runtime import Task
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
from deskops.specs import compile_artifact_spec
from deskops.specs import SpecRegistry
from deskops.specs import compile_task_spec
from deskops.workspace import scaffold_desk
from deskops.workflow.next_actions import load_task_lifecycle_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid


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


TASK_SECTION_FIELDS: tuple[tuple[str, str], ...] = (
    ("why", "Rationale"),
    ("goal", "Goal"),
    ("scope", "Scope"),
    ("implementation_path", "Implementation Path"),
    ("validation", "Validation"),
    ("done_when", "Done When"),
)

TASK_HEADING_TO_FIELD = {heading.lower(): field for field, heading in TASK_SECTION_FIELDS}
TASK_FIELD_TO_HEADING = {field: heading for field, heading in TASK_SECTION_FIELDS}
TASK_SECTION_PLACEHOLDERS = {
    "Rationale": "_Explain why this task exists or the business driver behind it._",
    "Goal": "_Describe the concrete result this task must produce._",
    "Scope": "_State what is in scope and what is out of scope._",
    "Implementation Path": "_Outline the expected implementation route or affected surface._",
    "Validation": "_List the checks required before this task can close._",
    "Done When": "_Name the observable condition that makes the task complete._",
}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


def strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    try:
        _, rest = text.split("---\n", 1)
        _frontmatter, body = rest.split("\n---\n", 1)
    except ValueError:
        return text
    return body


def parse_task_sections(text: str) -> dict[str, Any]:
    body = strip_markdown_frontmatter(text)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    preamble: list[str] = []
    sections: dict[str, str] = {}
    active_heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, active_heading
        if active_heading is None:
            return
        heading = active_heading
        active_heading = None
        field = TASK_HEADING_TO_FIELD[heading.lower()]
        if field in sections:
            buffer = []
            return
        content = "\n".join(buffer).strip()
        placeholder = TASK_SECTION_PLACEHOLDERS.get(heading)
        if placeholder:
            content_lines = content.splitlines()
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            if content_lines and content_lines[0].strip() == placeholder:
                content_lines.pop(0)
                while content_lines and not content_lines[0].strip():
                    content_lines.pop(0)
            content = "\n".join(content_lines).strip()
        sections[field] = content
        buffer = []

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            heading = match.group(1).strip()
            if heading.lower() in TASK_HEADING_TO_FIELD:
                flush()
                active_heading = heading
                continue
        if active_heading is None:
            preamble.append(line)
        else:
            buffer.append(line)
    flush()

    cleaned_preamble = "\n".join(preamble).strip()
    return {
        "fields": sections,
        "preamble": cleaned_preamble,
        "has_task_sections": bool(sections),
    }


def parse_validation_section(content: str) -> list[str]:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    bullets: list[str] = []
    saw_bullet = False
    for line in lines:
        if line.startswith("-"):
            saw_bullet = True
            item = line[1:].strip()
            if item:
                bullets.append(item)
    if saw_bullet:
        return bullets
    return [line for line in lines if line != "-"]


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
            Path("atoms"),
            Path("materializations"),
            Path("steps"),
            Path("registry"),
            Path("faq"),
        ]:
            (self.desk_root / relative).mkdir(parents=True, exist_ok=True)
        ensure_default_namespaces(default_registry_path(self.root))

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        self.ensure_workspace()
        payload = self._normalize_task_payload(raw_payload)
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec(self.spec_registry, payload, entry_node=spec.entry_node)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        rollback_actions: list[Callable[[], None]] = []
        try:
            self._write_new_doc(task_path, TaskDoc, compiled.task_payload)
            rollback_actions.append(lambda: self._remove_created_file(task_path))
            self._track_created_document(TaskDoc, task_path, task_id)

            board_path = self.desk_root / "tasks" / "Board.md"
            board_text = board_path.read_text(encoding="utf-8")
            rollback_actions.append(lambda: board_path.write_text(board_text, encoding="utf-8"))
            self._append_task_to_board(task_id)
            return TaskBundle(task_id=task_id, task_path=task_path)
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
        self._write_new_doc(path, model, compiled.artifact_payload)
        try:
            self._track_created_artifact(artifact_id, model, path, compiled.artifact_payload["id"])
        except Exception:
            self._remove_created_file(path)
            raise
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

    DRAWER_INDEX_FILES = {"README.md", "Board.md"}

    def resolve_drawer_source(self, selector: str) -> Path:
        """The desk/drawer/ file a task is being authored from.

        Accepts a path (relative to the repo root, or absolute) or a stem /
        unique slug fragment searched across every drawer subfolder, since the
        drawer holds features, issues and questions, not only task candidates.
        The file must live under desk/drawer/.
        """
        drawer_root = (self.desk_root / "drawer").resolve()
        candidate = Path(selector)
        if not candidate.is_absolute():
            candidate = self.desk_root.parent / candidate
        if candidate.is_file():
            resolved = candidate.resolve()
            if drawer_root not in resolved.parents:
                raise ValueError(f"--from-drawer must point inside desk/drawer/: {selector}")
            return resolved
        if not drawer_root.exists():
            raise FileNotFoundError(f"No drawer found at {drawer_root}")
        files = sorted(
            path for path in drawer_root.rglob("*.md")
            if path.is_file() and path.name not in self.DRAWER_INDEX_FILES
        )
        exact = [path for path in files if selector in {path.name, path.stem}]
        matches = exact or [path for path in files if selector.lower() in path.stem.lower()]
        if not matches:
            raise FileNotFoundError(f"No drawer file matches '{selector}'")
        if len(matches) > 1:
            listing = ", ".join(str(path.relative_to(drawer_root)) for path in matches)
            raise ValueError(f"Ambiguous drawer selector '{selector}': {listing}")
        return matches[0].resolve()

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        """Record where an authored task came from, without copying or deleting it.

        Stored in the task's own from_drawer field, not in references:
        `deskops edit task <id> references ...` replaces that whole list (the
        closeout step does exactly that), which would silently drop the origin.
        One field, one fact -- no parallel tag that could drift from it.
        Cleanup of the drawer file is left to a human."""
        relative = drawer_file.resolve().relative_to(self.desk_root.parent.resolve()).as_posix()
        return {**payload, "from_drawer": relative}

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

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        """List atoms annotated with their folder-axis value.

        Returns (axis, payloads). Each payload carries 'axis_values' with every
        value of the configured axis namespace found on the atom's tags.
        """
        axis = self.atom_folder_axis()
        if axis_value is not None and axis is None:
            raise ValueError(
                "--axis-value requires 'atom_folder_axis' to be configured in desk/config.json."
            )
        payloads = self.list_artifacts("artifact.atom")
        results: list[dict[str, Any]] = []
        for payload in payloads:
            values = axis_values(list(payload.get("tags") or []), axis) if axis else []
            payload["axis_values"] = values
            if axis_value is not None and axis_value not in values:
                continue
            results.append(payload)
        return axis, results

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        """Move atoms carrying a folder-axis tag into their axis subfolder.

        Idempotent: atoms already in the right place are skipped. Atoms without
        an axis tag are left untouched, preserving manual folder organization.
        Atoms with multiple axis values are reported as errors and skipped.
        """
        self.ensure_workspace()
        axis = self.atom_folder_axis()
        if axis is None:
            raise ValueError(
                "No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize."
            )
        moves: list[dict[str, str]] = []
        errors: list[str] = []
        retargets: dict[str, str] = {}
        for path in self._all_atom_paths():
            try:
                payload = self._read_doc(path, AtomDoc)
            except Exception as exc:
                errors.append(f"{path.relative_to(self.root)}: unreadable atom ({exc})")
                continue
            atom_id = str(payload.get("id") or path.stem)
            tags = list(payload.get("tags") or [])
            try:
                value = folder_axis_value(tags, axis)
            except ValueError as exc:
                errors.append(f"{path.relative_to(self.root)}: {exc}")
                continue
            if value is None:
                continue
            target = self.desk_root / "atoms" / axis_folder_relpath(value) / f"{atom_id}.md"
            if target == path:
                continue
            if target.exists():
                errors.append(
                    f"{path.relative_to(self.root)}: target already exists at {target.relative_to(self.root)}"
                )
                continue
            moves.append({
                "id": atom_id,
                "from": str(path.relative_to(self.root)),
                "to": str(target.relative_to(self.root)),
            })
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                path.rename(target)
                retargets[atom_id] = str(target.relative_to(self.root))
        if retargets:
            self._retarget_atom_documents(retargets)
        return {"axis": axis, "moves": moves, "errors": errors, "dry_run": dry_run}

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
        self.ensure_workspace()
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(self.desk_root / "atoms", list(tags or []))
        source_flags = [flag for flag in (from_pill, from_graph, from_diagram) if flag]
        if len(source_flags) != 1:
            raise ValueError("Atom create requires exactly one source: --from-pill, --from-graph, or --from-diagram.")

        atom_id = str(atom_id).strip()
        if not self._is_valid_atom_slug(atom_id):
            raise ValueError(f"Atom id must follow slug convention atom-<slug>: {atom_id}")

        normalized_question = str(five_wh_one_plus).strip()
        if normalized_question not in {"what", "why", "how", "how_not", "when", "where", "for_whom"}:
            raise ValueError(f"Unsupported atom question '{normalized_question}'.")

        if tags:
            validate_atom_tag_namespaces(list(tags), default_registry_path(self.root))

        if from_pill:
            payload, source_selector, provenance = self._build_atom_from_pill(
                atom_id,
                from_pill,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "pill"
        elif from_graph:
            payload, source_selector, provenance = self._build_atom_from_graph_finding(
                atom_id,
                from_graph,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
                graph_path=graph_path,
            )
            source_kind = "graph"
        else:
            payload, source_selector, provenance = self._build_atom_from_diagram(
                atom_id,
                from_diagram or "",
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "diagram"

        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        self._write_new_doc(path, AtomDoc, payload)
        try:
            self._track_created_artifact("artifact.atom", AtomDoc, path, atom_id)
        except Exception:
            self._remove_created_file(path)
            raise
        return AtomCreateResult(
            doc_id=atom_id,
            path=path,
            source_kind=source_kind,
            source_selector=source_selector,
            provenance=provenance,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        original_text = path.read_text(encoding="utf-8")
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to split {atom_id}; inbound references found: {refs}. "
                "Re-run with --force to keep the original as a redirect stub without rewriting referrers."
            )

        normalized_ids = [str(item).strip() for item in into_ids if str(item).strip()]
        if len(normalized_ids) < 2:
            raise ValueError("Atom split requires at least two target ids via --into.")
        if len(set(normalized_ids)) != len(normalized_ids):
            raise ValueError("Atom split target ids must be unique.")
        if atom_id in normalized_ids:
            raise ValueError(f"Atom split target ids must not include the source atom id {atom_id}.")
        for target_id in normalized_ids:
            if not self._is_valid_atom_slug(target_id):
                raise ValueError(f"Atom split target id must follow slug convention atom-<slug>: {target_id}")

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])

        rollback_actions: list[Callable[[], None]] = [
            lambda: path.write_text(original_text, encoding="utf-8"),
        ]
        created: list[DocumentRecord] = []

        try:
            for target_id in normalized_ids:
                heading, content = assignments[target_id]
                title = f"{payload['title']} — {heading}"
                new_payload = {
                    "id": target_id,
                    "title": title,
                    "five_wh_one_plus": payload["five_wh_one_plus"],
                    "answer": content,
                    "tags": list(payload.get("tags") or []),
                    "provenance": payload.get("provenance"),
                }
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                self._write_new_doc(new_path, AtomDoc, new_payload)
                rollback_actions.append(lambda new_path=new_path: self._remove_created_file(new_path))
                self._track_created_artifact("artifact.atom", AtomDoc, new_path, target_id)
                rollback_actions.append(lambda target_id=target_id: self._untrack_atom_document(target_id))
                created.append(DocumentRecord(kind="atom", doc_id=target_id, path=new_path))

            payload["answer"] = self._render_atom_split_redirect_answer(atom_id, normalized_ids)
            self._write_doc(path, AtomDoc, payload)
        except Exception:
            self._rollback(rollback_actions)
            raise

        return AtomSplitResult(
            original_id=atom_id,
            original_path=path,
            created=created,
            redirect_kept=True,
            inbound_references=inbound_references,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        self.ensure_workspace()
        source_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        target_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", into_selector)
        if source_path == target_path:
            raise ValueError("Atom merge source and target must resolve to different atoms.")

        source_payload = self._read_doc(source_path, AtomDoc)
        target_payload = self._read_doc(target_path, AtomDoc)
        source_id = str(source_payload.get("id") or source_path.stem)
        target_id = str(target_payload.get("id") or target_path.stem)

        if not self._is_valid_atom_slug(source_id):
            raise ValueError(f"Atom merge source id must follow slug convention atom-<slug>: {source_id}")
        if not self._is_valid_atom_slug(target_id):
            raise ValueError(f"Atom merge target id must follow slug convention atom-<slug>: {target_id}")

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        inbound_references = self._find_inbound_atom_references(source_id, excluded_path=source_path)

        rollback_actions: list[Callable[[], None]] = [
            lambda: source_path.write_text(source_text, encoding="utf-8"),
            lambda: target_path.write_text(target_text, encoding="utf-8"),
        ]

        try:
            rewritten_references = self._rewrite_inbound_atom_references(
                source_id,
                target_id,
                excluded_paths={source_path, target_path},
            )
            merged_answer = self._merge_atom_answers(target_payload, source_payload)
            target_payload["answer"] = merged_answer
            target_payload["tags"] = self._merge_atom_tags(
                list(target_payload.get("tags") or []),
                list(source_payload.get("tags") or []),
            )
            self._write_doc(target_path, AtomDoc, target_payload)

            source_payload["answer"] = self._render_atom_merge_redirect_answer(source_id, target_id)
            self._write_doc(source_path, AtomDoc, source_payload)
        except Exception:
            self._rollback(rollback_actions)
            raise

        return AtomMergeResult(
            source_id=source_id,
            source_path=source_path,
            target_id=target_id,
            target_path=target_path,
            redirect_kept=True,
            rewritten_references=rewritten_references,
            ambiguities=ambiguities,
        )

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
        files = self._coerce_list(payload.get("files") or [])
        task_rel = str(task_path.relative_to(self.root)) if task_path.is_absolute() else str(task_path)
        board_rel = "desk/tasks/Board.md"

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

        try:
            from sldb.api.documents.untrack_document import untrack_document
        except ImportError:
            untrack_document = None

        for p in paths_to_remove:
            if untrack_document:
                try:
                    untrack_document(None, str(p.relative_to(self.root)), pythonpath=".")
                except Exception as e:
                    self.logger.warning(f"Failed to untrack {p}: {e}")
            if p.exists():
                self.logger.debug(f"Removing file {p.name}")
                p.unlink()

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
            # Crossroads and protoatoms have their own models: see deskops.domain_tree.
            and not path.name.startswith(("crossroad-", "proto-"))
        )

    def _build_atom_from_pill(
        self,
        atom_id: str,
        pill_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        field_map = {
            "what": "what",
            "why": "why",
            "how": "how",
            "how_not": "how_not",
            "when": "when",
            "where": "where",
        }
        source_field = field_map.get(five_wh_one_plus)
        if source_field is None:
            raise ValueError(
                "Atom create from pill only supports questions that map directly to pill sections: what, why, how, how_not, when, where."
            )
        directories = [self.desk_root / "contexts", self.desk_root / "drawer" / "pills"]
        pill_path = self._resolve_artifact_selector_multi("artifact.pill", directories, pill_selector)
        pill_payload = self._read_doc(pill_path, PillDoc)
        answer = str(pill_payload.get(source_field) or "").strip()
        if not answer:
            raise ValueError(f"Pill section '{source_field}' is empty; cannot create atom from it.")
        relative_path = pill_path.relative_to(self.root).as_posix()
        source_selector = str(pill_payload.get("id") or pill_path.stem)
        provenance = f"{relative_path}::{source_field}"
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{pill_payload['title']} — {source_field.replace('_', ' ').title()}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, source_selector, provenance

    def _build_atom_from_graph_finding(
        self,
        atom_id: str,
        finding_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
        graph_path: str | None,
    ) -> tuple[dict[str, Any], str, str]:
        from deskops.graph.checks import find_missing_graph_references

        source_id, target_id = self._parse_graph_finding_selector(finding_selector)
        resolved_graph_path = None
        if graph_path:
            resolved_graph_path = Path(graph_path)
            if not resolved_graph_path.is_absolute():
                resolved_graph_path = (self.root / resolved_graph_path).resolve()
        findings = [
            finding for finding in find_missing_graph_references(self.root, resolved_graph_path)
            if finding.source_id == source_id and finding.target_id == target_id
        ]
        if not findings:
            raise FileNotFoundError(
                f"Graph finding not found for selector {finding_selector}. Run 'deskops graph missing --root {self.root}' to inspect available findings."
            )
        if len(findings) > 1:
            kinds = ", ".join(sorted({finding.kind for finding in findings}))
            raise ValueError(
                f"Graph finding selector {finding_selector} matched multiple findings ({kinds}). Narrow the graph input so one finding remains."
            )
        finding = findings[0]
        provenance = self._compose_exact_provenance(finding.provenance_path, finding.provenance_locator)
        if provenance is None:
            raise ValueError(
                f"Graph finding {finding_selector} does not expose a resolvable provenance path; exact-source atom creation is blocked."
            )
        answer_lines = [
            f"Graph finding `{finding.kind}` records a missing reference from `{finding.source_id}` to `{finding.target_id}`.",
            "",
            f"- Reason: {finding.reason}",
        ]
        if finding.role:
            answer_lines.append(f"- Role: `{finding.role}`")
        if finding.extractor:
            answer_lines.append(f"- Extractor: `{finding.extractor}`")
        answer_lines.append(f"- Provenance: `{provenance}`")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"Graph finding — {source_id} → {target_id}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": "\n".join(answer_lines).strip(),
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, f"{source_id}->{target_id}", provenance

    def _build_atom_from_diagram(
        self,
        atom_id: str,
        diagram_path_value: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        diagram_path = Path(diagram_path_value)
        if not diagram_path.is_absolute():
            diagram_path = (self.root / diagram_path).resolve()
        if not diagram_path.exists() or not diagram_path.is_file():
            raise FileNotFoundError(f"Diagram source not found: {diagram_path_value}")
        relative_path = diagram_path.relative_to(self.root).as_posix()
        text = diagram_path.read_text(encoding="utf-8")
        provenance = relative_path
        answer = text.strip()
        if diagram_path.suffix == ".mmd":
            answer = f"```mermaid\n{answer}\n```".strip()
        elif diagram_path.suffix == ".md":
            mermaid_match = re.search(r"```mermaid\s*\n(?P<body>.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
            if mermaid_match is not None:
                answer = f"```mermaid\n{mermaid_match.group('body').strip()}\n```".strip()
                provenance = f"{relative_path}::mermaid:1"
        if not answer:
            raise ValueError(f"Diagram source {diagram_path_value} is empty; cannot create atom from it.")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{diagram_path.stem.replace('-', ' ').replace('_', ' ').title()} — Diagram",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, relative_path, provenance

    def _parse_graph_finding_selector(self, selector: str) -> tuple[str, str]:
        source_id, separator, target_id = str(selector).partition("->")
        source_id = source_id.strip()
        target_id = target_id.strip()
        if not separator or not source_id or not target_id:
            raise ValueError(
                f"Invalid --from-graph value '{selector}'. Expected SOURCE_ID->TARGET_ID."
            )
        return source_id, target_id

    def _compose_exact_provenance(self, provenance_path: str | None, provenance_locator: str | None) -> str | None:
        path_text = str(provenance_path or "").strip()
        if not path_text:
            return None
        locator_text = str(provenance_locator or "").strip()
        return f"{path_text}::{locator_text}" if locator_text else path_text

    def _split_atom_answer_sections(self, answer: str) -> list[tuple[str, str]]:
        trimmed = answer.strip()
        if not trimmed:
            raise ValueError("Source atom answer is empty; nothing to split.")
        matches = list(re.finditer(r"^(#{2,6})\s+(.+?)\s*$", answer, flags=re.MULTILINE))
        if not matches:
            raise ValueError(
                "Source atom answer does not contain markdown subsections. Add heading-based sections under ## Answer or pass a differently structured atom."
            )
        leading = answer[:matches[0].start()].strip()
        if leading:
            raise ValueError(
                "Source atom answer contains content before the first subsection heading; split only supports heading-based sections that start immediately in the answer body."
            )
        sections: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(answer)
            content = answer[match.end():end].strip()
            if not content:
                raise ValueError(f"Source atom subsection '{heading}' is empty.")
            sections.append((heading, content))
        return sections

    def _resolve_atom_split_assignments(
        self,
        into_ids: list[str],
        sections: list[tuple[str, str]],
        section_flags: list[str],
    ) -> dict[str, tuple[str, str]]:
        by_heading = {heading: content for heading, content in sections}
        if len(by_heading) != len(sections):
            raise ValueError("Source atom answer subsection headings must be unique to support atom splitting.")

        if not section_flags:
            if len(sections) != len(into_ids):
                raise ValueError(
                    f"Source atom answer exposes {len(sections)} subsection(s) but --into lists {len(into_ids)} target ids. "
                    "Provide --section NEW_ATOM_ID:SECTION_HEADING for each target or align the counts."
                )
            return {
                target_id: (heading, content)
                for target_id, (heading, content) in zip(into_ids, sections, strict=True)
            }

        assignments: dict[str, tuple[str, str]] = {}
        for raw_flag in section_flags:
            target_id, separator, heading = str(raw_flag).partition(":")
            target_id = target_id.strip()
            heading = heading.strip()
            if not separator or not target_id or not heading:
                raise ValueError(
                    f"Invalid --section value '{raw_flag}'. Expected NEW_ATOM_ID:SECTION_HEADING."
                )
            if target_id not in into_ids:
                raise ValueError(
                    f"Section assignment references unknown target id '{target_id}'. Known ids: {', '.join(into_ids)}"
                )
            if target_id in assignments:
                raise ValueError(f"Section assignment for {target_id} was provided more than once.")
            if heading not in by_heading:
                available = ", ".join(heading_name for heading_name, _ in sections)
                raise ValueError(
                    f"Section heading '{heading}' was not found in the source atom answer. Available headings: {available}"
                )
            content = by_heading[heading]
            if any(existing_heading == heading for existing_heading, _ in assignments.values()):
                raise ValueError(f"Section heading '{heading}' was assigned more than once.")
            assignments[target_id] = (heading, content)

        missing = [target_id for target_id in into_ids if target_id not in assignments]
        if missing:
            raise ValueError(
                f"Missing --section assignment for target ids: {', '.join(missing)}"
            )
        return assignments

    def _render_atom_split_redirect_answer(self, atom_id: str, target_ids: list[str]) -> str:
        bullets = "\n".join(f"- atom:{target_id}" for target_id in target_ids)
        return (
            f"This atom has been split. Use the child atoms below instead of expanding atom:{atom_id} further.\n\n"
            "Redirect targets:\n"
            f"{bullets}\n\n"
            "The original atom is intentionally kept as a redirect stub so existing inbound references continue to resolve until callers are rerouted."
        )

    def _detect_atom_merge_ambiguities(
        self,
        source_payload: dict[str, Any],
        target_payload: dict[str, Any],
    ) -> list[str]:
        ambiguities: list[str] = []
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        target_question = str(target_payload.get("five_wh_one_plus") or "").strip()
        if source_question and target_question and source_question != target_question:
            ambiguities.append(
                f"five_wh_one_plus conflict ({source_question} vs {target_question})"
            )
        return ambiguities

    def _merge_atom_tags(self, target_tags: list[str], source_tags: list[str]) -> list[str]:
        merged: list[str] = []
        for tag in [*target_tags, *source_tags]:
            if tag not in merged:
                merged.append(tag)
        return merged

    def _merge_atom_answers(
        self,
        target_payload: dict[str, Any],
        source_payload: dict[str, Any],
    ) -> str:
        target_answer = str(target_payload.get("answer") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        if not target_answer:
            return source_answer
        if not source_answer:
            return target_answer
        if source_answer == target_answer or source_answer in target_answer:
            return target_answer
        appendix = self._render_atom_merge_appendix(source_payload)
        if appendix in target_answer:
            return target_answer
        return f"{target_answer}\n\n{appendix}".strip()

    def _render_atom_merge_appendix(self, source_payload: dict[str, Any]) -> str:
        source_id = str(source_payload.get("id") or "").strip()
        source_title = str(source_payload.get("title") or source_id).strip()
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        source_provenance = str(source_payload.get("provenance") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        metadata_lines = [
            f"Merged from atom:{source_id} ({source_title}).",
        ]
        if source_question:
            metadata_lines.append(f"Original question: `{source_question}`")
        if source_provenance:
            metadata_lines.append(f"Original provenance: `{source_provenance}`")
        metadata = "\n".join(f"- {line}" for line in metadata_lines)
        return f"### Merged from atom:{source_id}\n\n{metadata}\n\n{source_answer}".strip()

    def _render_atom_merge_redirect_answer(self, source_id: str, target_id: str) -> str:
        return (
            f"This atom has been merged into atom:{target_id}. Use atom:{target_id} instead of expanding atom:{source_id} further.\n\n"
            "The original atom is intentionally kept as a redirect stub so the old id remains traceable after inbound references are reconciled."
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

    def _rewrite_inbound_atom_references(
        self,
        source_id: str,
        target_id: str,
        *,
        excluded_paths: set[Path] | None = None,
    ) -> list[str]:
        needle = f"atom:{source_id}"
        replacement = f"atom:{target_id}"
        rewritten: list[str] = []
        excluded = {path.resolve() for path in (excluded_paths or set())}
        if not self.desk_root.exists():
            return rewritten
        for path in sorted(self.desk_root.rglob("*")):
            if path.resolve() in excluded:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                original_text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if needle not in original_text:
                continue
            pattern = re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])")
            updated_text = pattern.sub(replacement, original_text)
            if updated_text == original_text:
                continue
            changed_lines = [
                line_number
                for line_number, (before, after) in enumerate(
                    zip(original_text.splitlines(), updated_text.splitlines()), start=1
                )
                if before != after
            ]
            if not changed_lines:
                continue
            path.write_text(updated_text, encoding="utf-8")
            for line_number in changed_lines:
                rewritten.append(f"{path.relative_to(self.root)}:{line_number}")
        return rewritten

    def _retarget_atom_documents(self, retargets: dict[str, str]) -> bool:
        """Update tracked atom document paths in the .sldb store after moves.

        Retracking through SLDB's own track/untrack API keeps every derived index
        (semantic shards, sections, hashes, journal) consistent; editing the raw
        index files leaves the derived layers stale.
        """
        store_path = self.root / ".sldb"
        try:
            from sldb.api.documents.track_document_file import track_document_file
            from sldb.api.documents.untrack_document import untrack_document
            from sldb.store.layout import store_exists
        except ImportError:
            return False
        if not store_exists(store_path):
            return False

        pythonpath = str(Path(__file__).resolve().parents[1])
        changed = False
        for atom_id, new_path in retargets.items():
            try:
                untrack_document(store_path, atom_id, pythonpath)
                track_document_file(
                    store_path,
                    AtomDoc.__name__,
                    self.root / new_path,
                    name=atom_id,
                    pythonpath=pythonpath,
                    force=True,
                )
            except Exception:
                continue
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        store_path = self.root / ".sldb"
        try:
            from sldb.api.documents.untrack_document import untrack_document
            from sldb.store.layout import store_exists
        except ImportError:
            return False
        if not store_exists(store_path):
            return False

        try:
            untrack_document(store_path, atom_id, str(Path(__file__).resolve().parents[1]))
        except Exception:
            return False
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

    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _artifact_path(self, artifact_id: str, doc_id: str) -> Path:
        return self.desk_root / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        axis = DeskConfig.load(self.desk_root).atom_folder_axis
        if axis is None:
            return None
        axis = str(axis).strip()
        if not axis:
            return None
        namespaces = load_namespaces(default_registry_path(self.root))
        if axis not in namespaces:
            raise ValueError(
                f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
                "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
            )
        return axis

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        base = self.desk_root / "atoms"
        axis = self.atom_folder_axis()
        if axis is not None:
            value = folder_axis_value(tags, axis)
            if value is not None:
                return base / axis_folder_relpath(value) / f"{atom_id}.md"
        return base / f"{atom_id}.md"

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
        return resolve_selector(
            self.desk_root,
            [directory],
            selector,
            self._artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )

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
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        if self._write_through_store(path, model, payload):
            return
        return

    def _write_through_store(self, path: Path, model: type[Any], payload: dict[str, Any]) -> bool:
        """Write a tracked document through sldb so its stored hashes move with it.

        Writing the text directly leaves the store entry describing the previous
        content, which the next `sldb stores check` reports as a data mutation.
        """
        if not self._document_is_tracked(path, model):
            return False
        try:
            from sldb.api.documents.track_document_file import track_document_file
            from sldb.api.documents.untrack_document import untrack_document
            from sldb.store.layout import store_exists
        except ImportError:
            return False
        store_path = self.root / ".sldb"
        if not store_exists(store_path):
            return False
        pythonpath = str(Path(__file__).resolve().parents[1])
        try:
            untrack_document(store_path, path.stem, pythonpath)
            track_document_file(
                store_path,
                model.__name__,
                path,
                name=path.stem,
                pythonpath=pythonpath,
                force=True,
            )
        except Exception as exc:
            self.logger.debug(f"Store write-through failed for {path.name}, writing directly: {exc}")
            return False
        return True

    def _document_is_tracked(self, path: Path, model: type[Any]) -> bool:
        try:
            from sldb.store.io import load_documents_index, load_models_index, load_store_index
            from sldb.store.layout import store_exists
        except ImportError:
            return False
        store_path = self.root / ".sldb"
        if not store_exists(store_path):
            return False
        try:
            store_index = load_store_index(store_path)
            entry = next((item for item in store_index.models if item.name == model.__name__), None)
            if entry is None:
                return False
            models_index = load_models_index(self.root / entry.models_index)
            documents_index = load_documents_index(self.root / models_index.documents_index)
        except Exception:
            return False
        try:
            absolute = path if path.is_absolute() else (self.root / path)
            relative = str(absolute.resolve().relative_to(self.root.resolve()))
        except ValueError:
            return False
        return any(
            document.path == relative or document.name == path.stem
            for document in documents_index.documents
        )

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
        self._track_created_document(model, path, doc_id)

    def _track_created_document(self, model: type[Any], path: Path, doc_id: str) -> None:
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
            raise RuntimeError(
                f"Model {model.__name__} is not registered in store {store_path}; cannot track {path.relative_to(self.root)}"
            )

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
        raw_text = path.read_text(encoding="utf-8")
        payload = extract_model_data(model, raw_text)
        if model is TaskDoc:
            parsed_sections = parse_task_sections(raw_text)
            for field, content in parsed_sections["fields"].items():
                if field == "validation":
                    payload[field] = parse_validation_section(content)
                else:
                    payload[field] = content
        if "id" not in payload:
            payload["id"] = path.stem
        return payload
