from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


EXTRACTOR_NAME = "desk_source_file_nodes_v1"

SOURCE_SUFFIXES = {".py"}
CONFIG_SUFFIXES = {".cfg", ".ini", ".json", ".toml", ".yaml", ".yml"}
SPEC_SUFFIXES = {".md", ".yaml", ".yml"}

EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "tools",
    "venv",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_PATH_PREFIXES = {
    ".sldb/runtime",
    "tests/fixtures",
}
EXCLUDED_GRAPH_OUTPUT_SUFFIXES = {
    ".graph.json",
    ".kgdb.json",
    ".snapshot.json",
}


@dataclass(frozen=True)
class SourceFileGraphNode:
    id: str
    kind: str
    identity: str
    path: str
    file_kind: str
    provenance: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_source_file_nodes(root: Path) -> list[SourceFileGraphNode]:
    project_root = root.resolve()
    nodes: list[SourceFileGraphNode] = []
    existing_paths: set[str] = set()

    for path in _iter_candidate_paths(project_root):
        relative_path = _relative_path(project_root, path)
        classification = _classify_path(relative_path, path)
        if classification is None:
            continue

        kind, file_kind = classification
        existing_paths.add(relative_path)
        nodes.append(
            SourceFileGraphNode(
                id=f"{kind}:{relative_path}",
                kind=kind,
                identity=relative_path,
                path=relative_path,
                file_kind=file_kind,
                provenance={
                    "path": relative_path,
                    "source_kind": "path_rule",
                    "extractor": EXTRACTOR_NAME,
                },
            )
        )

    # Add declared materialization targets that are not already nodes
    for node in _declared_materialization_target_nodes(project_root, existing_paths):
        nodes.append(node)

    return sorted(nodes, key=lambda node: node.id)


def _iter_candidate_paths(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file() and not _is_excluded(root, path))


def _is_excluded(root: Path, path: Path) -> bool:
    relative_path = _relative_path(root, path)
    parts = Path(relative_path).parts
    if any(part in EXCLUDED_DIRS for part in parts):
        return True
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    if any(_has_path_prefix(relative_path, prefix) for prefix in EXCLUDED_PATH_PREFIXES):
        return True
    return any(relative_path.endswith(suffix) for suffix in EXCLUDED_GRAPH_OUTPUT_SUFFIXES)


def _classify_path(relative_path: str, path: Path) -> tuple[str, str] | None:
    parts = Path(relative_path).parts
    suffix = path.suffix

    if parts and parts[0] == "spec" and suffix in SPEC_SUFFIXES:
        return "spec", "spec"
    if len(parts) >= 3 and parts[:3] == ("docs", "architecture", "spec2viz") and suffix in SPEC_SUFFIXES:
        return "spec", "spec"
    if parts and parts[0] == "tests" and suffix in SOURCE_SUFFIXES:
        return "test_file", "test"
    if _is_config_file(relative_path, path):
        return "config_file", "config"
    if suffix in SOURCE_SUFFIXES and _is_source_path(parts):
        return "source_file", "source"
    return None


def _is_config_file(relative_path: str, path: Path) -> bool:
    if path.suffix not in CONFIG_SUFFIXES:
        return False
    if relative_path == "pyproject.toml":
        return True
    if path.name.startswith(".") and path.suffix in {".json", ".yaml", ".yml"}:
        return True
    stem = path.stem.lower()
    if "config" in stem or "namespace" in stem or "registry" in stem:
        return True
    return path.suffix in {".toml", ".ini", ".cfg"}


def _is_source_path(parts: tuple[str, ...]) -> bool:
    return bool(parts) and parts[0] in {"desk", "deskops"}


def _has_path_prefix(relative_path: str, prefix: str) -> bool:
    return relative_path == prefix or relative_path.startswith(f"{prefix}/")


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _declared_materialization_target_nodes(
    root: Path, existing_paths: set[str]
) -> list[SourceFileGraphNode]:
    """Emit source_file nodes for declared materialization targets.

    Each MaterializationContractDoc under desk/materializations/**/*.md may declare
    a target_identity in its frontmatter. When that value is a plain repo-relative
    POSIX path to an existing regular file and no exclusion rule applies, this
    function creates a source_file node for it.
    """
    from deskops.graph.extract_docs import _iter_doc_paths

    materializations_dir = root / "desk" / "materializations"
    if not materializations_dir.exists():
        return []

    # Compute doc paths to avoid creating source_file nodes for doc surfaces
    doc_paths = {_relative_path(root, path) for path, _kind in _iter_doc_paths(root)}

    nodes: list[SourceFileGraphNode] = []
    seen_paths: set[str] = set()

    for md_path in sorted(materializations_dir.rglob("*.md")):
        if not md_path.is_file():
            continue

        target_identity = _read_target_identity(md_path)
        if target_identity is None:
            continue

        # Normalize: strip leading ./ using removeprefix (not lstrip, which strips
        # every leading '.' and '/')
        normalized = target_identity.removeprefix("./")

        # Reject absolute paths
        if normalized.startswith("/"):
            continue

        # Reject paths with '..' segments
        if ".." in Path(normalized).parts:
            continue

        # Reject kind:id targets (contain ':')
        if ":" in normalized:
            continue

        # Require resolved location to be inside root (containment check only)
        resolved = (root / normalized).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue

        # Require the declared path to be an existing regular file
        # (Use the declared normalized path, not the resolved symlink target)
        declared_path = root / normalized
        if not declared_path.is_file():
            continue

        # Skip if already produced by a path rule
        if normalized in existing_paths:
            continue

        # Skip if already seen from another materialization
        if normalized in seen_paths:
            continue

        # Skip if this is a doc surface
        if normalized in doc_paths:
            continue

        # Skip if excluded (check the declared path, not resolved)
        if _is_excluded(root, declared_path):
            continue

        seen_paths.add(normalized)
        nodes.append(
            SourceFileGraphNode(
                id=f"source_file:{normalized}",
                kind="source_file",
                identity=normalized,
                path=normalized,
                file_kind="source",
                provenance={
                    "path": normalized,
                    "source_kind": "declared_materialization_target",
                    "extractor": EXTRACTOR_NAME,
                },
            )
        )

    return nodes


def _read_target_identity(path: Path) -> str | None:
    """Read target_identity from the frontmatter of a Markdown file.

    Returns None if the file is unreadable, malformed, or has no string
    target_identity at the top level of its frontmatter.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not text.startswith("---\n"):
        return None

    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return None

    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return None

    if not isinstance(loaded, dict):
        return None

    target = loaded.get("target_identity")
    if not isinstance(target, str):
        return None

    return target.strip() if target.strip() else None
