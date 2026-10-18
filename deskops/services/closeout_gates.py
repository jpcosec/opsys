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
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": []}
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
        return evidence

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
