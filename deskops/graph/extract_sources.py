from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXTRACTOR_NAME = "desk_source_file_nodes_v1"

SOURCE_SUFFIXES = {".py"}
CONFIG_SUFFIXES = {".cfg", ".ini", ".json", ".toml", ".yaml", ".yml"}
SPEC_SUFFIXES = {".md", ".yaml", ".yml"}

EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
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

    for path in _iter_candidate_paths(project_root):
        relative_path = _relative_path(project_root, path)
        classification = _classify_path(relative_path, path)
        if classification is None:
            continue

        kind, file_kind = classification
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
    return path.resolve().relative_to(root).as_posix()
