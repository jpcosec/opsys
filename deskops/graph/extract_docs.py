from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml


EXTRACTOR_NAME = "desk_doc_nodes_v1"


@dataclass(frozen=True)
class DocGraphNode:
    id: str
    kind: str
    identity: str
    path: str
    label: str
    provenance: dict[str, str]
    document_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_doc_nodes(root: Path) -> list[DocGraphNode]:
    project_root = root.resolve()
    nodes: list[DocGraphNode] = []

    for path, kind in _iter_doc_paths(project_root):
        relative_path = _relative_path(project_root, path)
        metadata = _read_metadata(path)
        document_id = metadata.get("id")
        label = metadata.get("title") or _title_from_path(path)
        identity = _identity_for(kind, relative_path, document_id, label, path)

        nodes.append(
            DocGraphNode(
                id=f"{kind}:{identity}",
                kind=kind,
                identity=identity,
                path=relative_path,
                label=label,
                document_id=document_id,
                provenance={
                    "path": relative_path,
                    "source_kind": "file_metadata",
                    "extractor": EXTRACTOR_NAME,
                },
            )
        )

    return sorted(nodes, key=lambda node: node.id)


def _iter_doc_paths(root: Path) -> list[tuple[Path, str]]:
    candidates: list[tuple[Path, str]] = []
    candidates.extend((path, "atom") for path in _glob(root / "desk" / "atoms", "**/*.md"))
    candidates.extend((path, "materialization") for path in _glob(root / "desk" / "materializations", "**/*.md"))
    candidates.extend((path, "role") for path in _glob(root / "desk" / "roles", "**/*.md"))
    candidates.extend((path, "pill") for path in _glob(root / "desk" / "contexts", "*.md"))
    candidates.extend(
        (path, "task")
        for path in _glob(root / "desk" / "tasks", "*.md")
        if path.name != "Board.md"
    )
    candidates.extend(
        (path, "issue") for path in _glob(root / "desk" / "drawer" / "issues", "*.md")
    )
    candidates.extend(
        (path, "question") for path in _glob(root / "desk" / "drawer" / "questions", "*.md")
    )
    candidates.extend(
        (path, "drawer_task")
        for path in _glob(root / "desk" / "drawer" / "tasks", "*.md")
        if path.name != "Board.md"
    )
    candidates.extend(
        (path, "feature") for path in _glob(root / "desk" / "drawer" / "features", "*.md")
    )
    candidates.extend(
        (path, "use_case") for path in _glob(root / "desk" / "drawer" / "use-cases", "*.md")
    )
    candidates.extend(
        (path, "stress_test") for path in _glob(root / "desk" / "drawer" / "stress-tests", "**/*.md")
    )
    candidates.extend(
        (path, "diagram")
        for path in _glob(root / "docs" / "diagrams", "**/*")
        if path.suffix in {".md", ".mmd"}
    )
    candidates.extend(
        (path, "doc")
        for path in _glob(root / "docs", "**/*.md")
        if "diagrams" not in path.relative_to(root / "docs").parts
    )
    candidates.extend(
        (path, "spec")
        for path in _glob(root / "spec", "**/*")
        if path.suffix in {".md", ".yaml", ".yml"}
    )
    return candidates


def _glob(root: Path, pattern: str) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.glob(pattern) if path.is_file())


def _read_metadata(path: Path) -> dict[str, str]:
    if path.suffix in {".yaml", ".yml"}:
        return _read_yaml_metadata(path)
    frontmatter = _read_frontmatter_metadata(path)
    if frontmatter:
        metadata = _read_text_metadata(path)
        metadata.update(frontmatter)
        return metadata
    return _read_text_metadata(path)


def _read_frontmatter_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return {}
    loaded = yaml.safe_load(block) or {}
    if not isinstance(loaded, dict):
        return {}
    return _metadata_from_mapping(loaded)


def _read_yaml_metadata(path: Path) -> dict[str, str]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {}
    return _metadata_from_mapping(loaded)


def _metadata_from_mapping(loaded: dict[str, Any]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for key in ("id", "title"):
        value = loaded.get(key)
        if isinstance(value, str) and value.strip():
            metadata[key] = value.strip()
    return metadata


def _read_text_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and "title" not in metadata:
            metadata["title"] = stripped.removeprefix("# ").strip()
        if stripped.startswith("ID:") and "id" not in metadata:
            metadata["id"] = stripped.removeprefix("ID:").strip()
        if "id" in metadata and "title" in metadata:
            break
    return metadata


def _identity_for(
    kind: str,
    relative_path: str,
    document_id: str | None,
    label: str,
    path: Path,
) -> str:
    if kind in {"atom", "materialization", "pill", "role", "task"} and document_id:
        return document_id
    if kind == "issue":
        return document_id or _slugify(label) or path.stem
    return relative_path


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _title_from_path(path: Path) -> str:
    return re.sub(r"[-_]+", " ", path.stem).strip().title()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)
