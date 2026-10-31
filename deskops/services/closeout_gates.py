"""Closeout evidence gates.

Closeout verification accepts only real evidence: a lowercase commit id naming
a commit in HEAD's history, and a Python test file inside the repository's
``tests/`` directory. A front-matter string that merely looks like evidence is
not evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
from typing import Any
from typing import Callable


COMMIT_ID_PATTERN = re.compile(r"[0-9a-f]{7,40}")
URL_PATTERN = re.compile(r"https?://\S+")

# Closed vocabulary for a task's declared closeout evidence. `atom` and
# `materialization` are alternatives of one gate: either link satisfies it.
CLOSEOUT_EVIDENCE_VOCABULARY = ("tests", "commit", "atom", "materialization", "document", "external")

CODE_EVIDENCE = ("tests", "commit", "atom", "materialization")
DOCUMENT_EVIDENCE = ("commit", "document")
EXTERNAL_EVIDENCE = ("external",)

# task_type -> evidence declared when --evidence is absent.
TASK_TYPE_EVIDENCE: dict[str, tuple[str, ...]] = {
    "code": CODE_EVIDENCE,
    "implementation": CODE_EVIDENCE,
    "test": CODE_EVIDENCE,
    "docs": DOCUMENT_EVIDENCE,
    "spec": DOCUMENT_EVIDENCE,
    "design": DOCUMENT_EVIDENCE,
    "external": EXTERNAL_EVIDENCE,
}

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})

HOW_TO_DECLARE_EVIDENCE = (
    "Declare how this task closes: pass --evidence <kind>... "
    f"(kinds: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}) or --task-type "
    f"({', '.join(TASK_TYPE_EVIDENCE)}) so the evidence is filled from the type "
    "(code: tests+commit+atom|materialization; docs|spec|design: commit+document; external: external)."
)


class CloseoutEvidenceError(ValueError):
    """The declared closeout evidence is invalid or missing."""


def normalize_declared_evidence(value: Any) -> list[str]:
    """Validate a declared evidence list against the closed vocabulary, keeping order."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    declared: list[str] = []
    for item in items:
        kind = str(item).strip().lower()
        if not kind:
            continue
        if kind not in CLOSEOUT_EVIDENCE_VOCABULARY:
            raise CloseoutEvidenceError(
                f"Unknown closeout evidence '{item}'. Allowed: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}."
            )
        if kind not in declared:
            declared.append(kind)
    return declared


def evidence_for_task_type(task_type: str) -> list[str]:
    return list(TASK_TYPE_EVIDENCE.get(str(task_type or "").strip().lower(), ()))


def resolve_new_task_evidence(payload: dict[str, Any], *, require: bool) -> list[str]:
    """Evidence a new task declares: explicit --evidence, else filled from task_type.

    With ``require`` set and neither source available (or the task_type unknown),
    raises ``CloseoutEvidenceError`` explaining how to declare it.
    """
    declared = normalize_declared_evidence(payload.get("closeout_evidence"))
    if declared:
        return declared
    task_type = str(payload.get("task_type") or "").strip()
    filled = evidence_for_task_type(task_type)
    if filled:
        return filled
    if require:
        if task_type:
            raise CloseoutEvidenceError(
                f"Task type '{task_type}' does not imply closeout evidence. " + HOW_TO_DECLARE_EVIDENCE
            )
        raise CloseoutEvidenceError("This task declares no closeout evidence. " + HOW_TO_DECLARE_EVIDENCE)
    return []


def collapse_link_kinds(kinds: list[str]) -> list[str]:
    """Show atom and materialization as the one alternative gate they are."""
    if "atom" in kinds and "materialization" in kinds:
        out: list[str] = []
        for kind in kinds:
            label = "atom|materialization" if kind in {"atom", "materialization"} else kind
            if label not in out:
                out.append(label)
        return out
    return list(kinds)


def gate_summary(declared: list[str], found: list[str]) -> str:
    declared_text = ", ".join(collapse_link_kinds(declared)) or "nada"
    found_text = ", ".join(found) or "nada"
    return f"esta tarea declaró {declared_text}; encontré {found_text}"


class CloseoutGatesService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def closeout_reference_evidence(
        self,
        payload: dict[str, Any],
        *,
        points_to_atom: Callable[[str], bool],
        points_to_routed_follow_up: Callable[[str], bool],
    ) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": [], "document": [], "external": []}
        references = payload.get("references") or []
        if not isinstance(references, list):
            references = [references]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for candidate in [*references, *files]:
            ref = str(candidate).strip()
            if ref and self.reference_points_to_document(ref) and ref not in evidence["document"]:
                evidence["document"].append(ref)
        return evidence

    @staticmethod
    def reference_points_to_url(reference: str) -> bool:
        """True for an http(s) URL: the record of work done outside this repository."""
        return bool(URL_PATTERN.fullmatch(reference.strip()))

    def reference_points_to_document(self, reference: str) -> bool:
        """True only for an existing document file inside the repository.

        Documents are prose or spec files (``DOCUMENT_SUFFIXES``). Test sources and
        the task bundle itself, which closure removes, are not documents.
        """
        path = Path(reference.split("::", 1)[0].strip())
        if not str(path) or path.is_absolute():
            return False
        resolved = (self.root / path).resolve()
        if resolved.suffix.lower() not in DOCUMENT_SUFFIXES or not resolved.is_file():
            return False
        if not resolved.is_relative_to(self.root):
            return False
        excluded = ((self.root / "tests").resolve(), (self.root / "desk" / "tasks").resolve())
        return not any(resolved.is_relative_to(parent) for parent in excluded)

    def reference_points_to_test(self, reference: str) -> bool:
        """True only for an existing .py file under <root>/tests/.

        Accepts an optional ``::node`` suffix (the node is not validated) and
        the ``pytest <path>`` form. Absolute paths and paths that escape
        ``tests/`` through ``..`` are not evidence.
        """
        tests_root = (self.root / "tests").resolve()
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if resolved.is_relative_to(tests_root):
                return True
        return False

    def reference_points_to_commit(self, reference: str) -> bool:
        """True only for a lowercase hex id resolving to HEAD or an ancestor.

        The pattern rejects symbolic names such as ``HEAD`` or ``main``; an
        ambiguous abbreviation fails ``rev-parse --verify``; an unrelated or
        descendant commit fails the ancestor check.
        """
        candidate = reference.strip()
        if not COMMIT_ID_PATTERN.fullmatch(candidate):
            return False
        try:
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            if resolved.returncode != 0:
                return False
            full_sha = resolved.stdout.strip()
            if not full_sha:
                return False
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", full_sha, "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return ancestor.returncode == 0

    def build_closeout_graph_context(self) -> dict[str, Any]:
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

    def _test_path_candidates(self, reference: str) -> list[str]:
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
        return candidates
