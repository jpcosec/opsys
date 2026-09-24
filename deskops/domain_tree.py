"""Domain tree: crossroads order a knowledge base and protoatoms hang from them.

A ``domain:a.b.c`` tag places a document under the path ``a.b.c``. Every prefix
of that path (``a``, ``a.b``, ``a.b.c``) needs a CrossroadDoc with written
content: the system is forced to write the parent before it can describe the
children. Protoatoms are free atoms; typing one into another sldb model keeps it
as a redirect stub whose ``typed_as`` names the typed document.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.atom_tags import TAG_PATTERN
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.bootstrap import MODEL_REFS
from deskops.models.atom import AtomDoc
from deskops.models.crossroad import DOMAIN_PATH_PATTERN
from deskops.models.crossroad import CrossroadDoc
from deskops.models.protoatom import ProtoAtomDoc
from deskops.operations import ARTIFACT_MODELS
from deskops.operations import ARTIFACT_PATHS
from deskops.operations import DeskopsOperations
from deskops.operations import slugify

DOMAIN = "domain"
PROTO_PREFIX = "proto-"
CROSSROAD_PREFIX = "crossroad-"
_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)


def domain_paths(tags: list[str]) -> list[str]:
    """Values of the ``domain:`` tags, in order."""
    values: list[str] = []
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == DOMAIN:
            values.append(str(tag).split(":", 1)[1])
    return values


def prefixes(path: str) -> list[str]:
    """``a.b.c`` -> ``['a', 'a.b', 'a.b.c']``."""
    parts = path.split(".")
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def crossroad_id(path: str) -> str:
    return CROSSROAD_PREFIX + path.replace(".", "--")


def read_crossroads(atoms_dir: Path) -> dict[str, dict[str, Any]]:
    """Written crossroads by path. An unreadable or empty one does not count as written."""
    found: dict[str, dict[str, Any]] = {}
    for file in sorted(atoms_dir.rglob(f"{CROSSROAD_PREFIX}*.md")):
        try:
            payload = extract_model_data(CrossroadDoc, file.read_text(encoding="utf-8"))
            CrossroadDoc(**payload)
        except Exception:
            continue
        found[str(payload["path"])] = {**payload, "file": file}
    return found


def missing_parents(tags: list[str], crossroads: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for value in domain_paths(tags):
        for prefix in prefixes(value):
            if prefix not in crossroads and prefix not in missing:
                missing.append(prefix)
    return missing


def require_domain_parents(atoms_dir: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix."""
    for value in domain_paths(tags):
        if not _DOMAIN_PATH.fullmatch(value):
            raise ValueError(f"Invalid domain path '{value}': use lowercase segments separated by dots.")
    missing = missing_parents(tags, read_crossroads(atoms_dir))
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


@dataclass
class Created:
    doc_id: str
    path: Path


@dataclass
class Typed:
    protoatom_id: str
    protoatom_path: Path
    model: str
    doc_id: str
    path: Path


class DomainTree:
    """Crossroads, protoatoms and typing over one repository's desk/atoms."""

    def __init__(self, root: Path) -> None:
        self.ops = DeskopsOperations(root)
        self.root = self.ops.root
        self.atoms_dir = self.ops.desk_root / "atoms"

    def create_crossroad(self, path: str, *, title: str, content: str) -> Created:
        self.ops.ensure_workspace()
        if not _DOMAIN_PATH.fullmatch(path):
            raise ValueError(f"Invalid domain path '{path}': use lowercase segments separated by dots.")
        parent = path.rpartition(".")[0]
        if parent:
            require_domain_parents(self.atoms_dir, [f"{DOMAIN}:{parent}"])
        if path in read_crossroads(self.atoms_dir):
            raise FileExistsError(f"A crossroad for '{path}' already exists.")
        payload = CrossroadDoc(id=crossroad_id(path), path=path, title=title, content=content).model_dump(mode="json")
        return self._create(CrossroadDoc, payload, [f"{DOMAIN}:{path}"])

    def create_protoatom(self, doc_id: str, *, title: str, content: str = "", tags: list[str]) -> Created:
        self.ops.ensure_workspace()
        slug = doc_id.removeprefix(PROTO_PREFIX)
        if not doc_id.startswith(PROTO_PREFIX) or not slug or slug != slugify(slug):
            raise ValueError(f"Protoatom id must follow slug convention proto-<slug>: {doc_id}")
        tags = list(tags)
        validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        if len(domain_paths(tags)) > 1:
            raise ValueError("A protoatom hangs from one place in the domain tree: use a single domain:<path> tag.")
        require_domain_parents(self.atoms_dir, tags)
        payload = ProtoAtomDoc(id=doc_id, title=title, content=content, tags=tags).model_dump(mode="json")
        return self._create(ProtoAtomDoc, payload, tags)

    def type_protoatom(
        self,
        selector: str,
        *,
        model_name: str,
        doc_id: str | None = None,
        content_field: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Typed:
        """Create the typed document, then turn the protoatom into its redirect stub."""
        self.ops.ensure_workspace()
        proto_path = self._find_protoatom(selector)
        proto = self.ops._read_doc(proto_path, ProtoAtomDoc)
        if proto.get("typed_as"):
            raise ValueError(f"{proto['id']} was already typed as {proto['typed_as']}.")
        model = self._resolve_model(model_name)
        slug = str(proto["id"]).removeprefix(PROTO_PREFIX)
        target_id = doc_id or f"{model.__name__.removesuffix('Doc').lower()}-{slug}"
        payload = model(**self._typed_payload(model, target_id, proto, content_field, data or {})).model_dump(mode="json")
        stub = ProtoAtomDoc(**{**proto, "typed_as": f"{model.__name__}:{target_id}",
                               "content": _redirect_content(model.__name__, target_id)})
        # Rendered before any write, so a stub that cannot be written never leaves a typed orphan.
        stub_text = render_model_markdown(ProtoAtomDoc, stub.model_dump(mode="json")) + "\n"
        target_path = self._typed_path(model, target_id, list(proto.get("tags") or []))
        self._write_and_track(target_path, model, payload, target_id)
        proto_path.write_text(stub_text, encoding="utf-8")
        return Typed(str(proto["id"]), proto_path, model.__name__, target_id, target_path)

    def check(self) -> list[dict[str, Any]]:
        """Domain-tree errors per document under desk/atoms."""
        crossroads = read_crossroads(self.atoms_dir)
        records: list[dict[str, Any]] = []
        for path in sorted(self.atoms_dir.rglob("*.md")):
            if path.name.startswith(CROSSROAD_PREFIX):
                doc_id, errors = self._check_crossroad(path, crossroads)
            elif path.name.startswith(PROTO_PREFIX):
                doc_id, errors = self._check_protoatom(path, crossroads)
            else:
                doc_id, errors = path.stem, self._check_atom(path, crossroads)
            records.append({"id": doc_id, "path": str(path), "errors": errors})
        return records

    def tree(self) -> dict[str, Any]:
        """Crossroads nested by path, with the documents hanging from each one."""
        crossroads = read_crossroads(self.atoms_dir)
        nodes = {
            path: {"path": path, "id": item["id"], "title": item["title"], "children": [], "items": []}
            for path, item in crossroads.items()
        }
        roots: list[dict[str, Any]] = []
        for path in sorted(nodes):
            parent = path.rpartition(".")[0]
            (nodes[parent]["children"] if parent in nodes else roots).append(nodes[path])
        orphans: list[dict[str, Any]] = []
        unplaced: list[dict[str, Any]] = []
        for file in sorted(self.atoms_dir.rglob("*.md")):
            if file.name.startswith(CROSSROAD_PREFIX):
                continue
            model = ProtoAtomDoc if file.name.startswith(PROTO_PREFIX) else AtomDoc
            try:
                payload = self.ops._read_doc(file, model)
            except Exception:
                continue
            item = {"id": payload.get("id") or file.stem, "title": payload.get("title"),
                    "model": model.__name__, "typed_as": payload.get("typed_as")}
            places = domain_paths(list(payload.get("tags") or []))
            if not places:
                unplaced.append(item)
            for place in places:
                (nodes[place]["items"] if place in nodes else orphans).append({**item, "domain": place})
        return {"roots": roots, "orphans": orphans, "unplaced": unplaced}

    def _create(self, model: type[Any], payload: dict[str, Any], tags: list[str]) -> Created:
        doc_id = str(payload["id"])
        if any(self.atoms_dir.rglob(f"{doc_id}.md")):
            raise FileExistsError(f"Refusing to overwrite existing document {doc_id}.")
        path = self.ops._atom_doc_path(doc_id, tags)
        self._write_and_track(path, model, payload, doc_id)
        return Created(doc_id, path)

    def _write_and_track(self, path: Path, model: type[Any], payload: dict[str, Any], doc_id: str) -> None:
        self.ops._write_new_doc(path, model, payload)
        try:
            self.ops._track_created_document(model, path, doc_id)
        except Exception:
            self.ops._remove_created_file(path)
            raise

    def _find_protoatom(self, selector: str) -> Path:
        matches = [path for path in self.atoms_dir.rglob(f"{PROTO_PREFIX}*.md") if selector in {path.stem, path.name}]
        if not matches:
            raise FileNotFoundError(f"No protoatom '{selector}' under {self.atoms_dir}.")
        if len(matches) > 1:
            raise ValueError(f"Protoatom selector '{selector}' is ambiguous: {', '.join(map(str, matches))}")
        return matches[0]

    def _resolve_model(self, name: str) -> type[Any]:
        from sldb.cli.model_utils import resolve_model_ref
        from sldb.store.io import load_store_index
        from sldb.store.layout import store_exists

        store = self.root / ".sldb"
        if store_exists(store):
            entry = next((model for model in load_store_index(store).models if model.name == name), None)
            if entry is None:
                raise ValueError(f"Model '{name}' is not registered in {store}; register it before typing into it.")
            return resolve_model_ref(entry.model_ref, str(self.root))
        if name in MODEL_REFS:
            return resolve_model_ref(MODEL_REFS[name])
        raise ValueError(f"Unknown model '{name}': there is no local store and it is not a deskops model.")

    def _typed_payload(
        self, model: type[Any], target_id: str, proto: dict[str, Any], content_field: str | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        fields = model.model_fields
        carried = {"id": target_id, "title": proto.get("title"),
                   "tags": list(proto.get("tags") or []), "provenance": proto.get("provenance")}
        payload = {name: value for name, value in carried.items() if name in fields and value is not None}
        content = str(proto.get("content") or "")
        target = content_field or ("content" if "content" in fields else None)
        if target is not None:
            if target not in fields:
                raise ValueError(f"{model.__name__} has no field '{target}' to receive the protoatom content.")
            payload[target] = content
        elif content.strip():
            raise ValueError(
                f"{model.__name__} has no 'content' field: pass --content-field to choose where the protoatom "
                "content goes (for AtomDoc, answer)."
            )
        return {**payload, **data}

    def _typed_path(self, model: type[Any], doc_id: str, tags: list[str]) -> Path:
        if model.__name__ == AtomDoc.__name__:
            return self.ops._atom_doc_path(doc_id, tags)
        artifact = next((key for key, known in ARTIFACT_MODELS.items() if known.__name__ == model.__name__), None)
        folder = Path(ARTIFACT_PATHS[artifact]) if artifact else Path("typed") / model.__name__
        return self.ops.desk_root / folder / f"{doc_id}.md"

    def _check_crossroad(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload = self.ops._read_doc(path, CrossroadDoc)
            CrossroadDoc(**payload)
        except Exception as exc:
            return path.stem, [f"crossroad is invalid: {_first_line(exc)}"]
        doc_id, errors = str(payload["id"]), []
        if doc_id != crossroad_id(payload["path"]):
            errors.append(f"crossroad id must be {crossroad_id(payload['path'])}")
        if path.stem != doc_id:
            errors.append(f"filename must match crossroad id '{doc_id}'")
        parent = str(payload["path"]).rpartition(".")[0]
        if parent:
            errors.extend(self._domain_errors([f"{DOMAIN}:{parent}"], crossroads))
        return doc_id, errors

    def _check_protoatom(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload = self.ops._read_doc(path, ProtoAtomDoc)
            ProtoAtomDoc(**payload)
        except Exception as exc:
            return path.stem, [f"protoatom is invalid: {_first_line(exc)}"]
        doc_id, tags, errors = str(payload["id"]), list(payload.get("tags") or []), []
        if path.stem != doc_id:
            errors.append(f"filename must match protoatom id '{doc_id}'")
        try:
            validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        except ValueError as exc:
            errors.append(str(exc))
        if len(domain_paths(tags)) > 1:
            errors.append("a protoatom takes a single domain:<path> tag")
        errors.extend(self._domain_errors(tags, crossroads))
        typed_as = str(payload.get("typed_as") or "")
        if typed_as and not any(self.ops.desk_root.rglob(f"{typed_as.split(':', 1)[-1]}.md")):
            errors.append(f"typed_as target not found: {typed_as}")
        return doc_id, errors

    def _check_atom(self, path: Path, crossroads: dict[str, Any]) -> list[str]:
        try:
            tags = list(self.ops._read_doc(path, AtomDoc).get("tags") or [])
        except Exception:
            return []  # atoms validate already reports unreadable atoms
        return self._domain_errors(tags, crossroads)

    def _domain_errors(self, tags: list[str], crossroads: dict[str, Any]) -> list[str]:
        errors = [f"invalid domain path '{value}'" for value in domain_paths(tags) if not _DOMAIN_PATH.fullmatch(value)]
        valid = [f"{DOMAIN}:{value}" for value in domain_paths(tags) if _DOMAIN_PATH.fullmatch(value)]
        errors.extend(f"no written crossroad for domain path '{path}'" for path in missing_parents(valid, crossroads))
        return errors


def _redirect_content(model_name: str, doc_id: str) -> str:
    return (
        f"Typed as {model_name} {doc_id}. This protoatom is kept as a redirect stub so its id keeps "
        "resolving; its content now lives in the typed document."
    )


def _first_line(exc: Exception) -> str:
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return " ".join(lines[:3]) if lines else exc.__class__.__name__
