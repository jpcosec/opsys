from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

import yaml


from deskops.models.atom import ATOM_TAG_PATTERN

NAMESPACE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
# The tag form is the model's (AtomDoc.tags); this is the same pattern with the namespace named.
TAG_PATTERN = re.compile(ATOM_TAG_PATTERN.replace("^[a-z][a-z0-9_]*:", "^(?P<namespace>[a-z][a-z0-9_]*):"))

DEFAULT_ATOM_TAG_NAMESPACES: dict[str, dict[str, Any]] = {
    "system": {
        "meaning": "System, project, or tool the atom belongs to.",
        "use_when": "The atom is about a specific system.",
        "do_not_use_when": "The tag is only a general topic.",
        "examples": ["system:deskops", "system:sldb"],
    },
    "topic": {
        "meaning": "Subject area discussed by the atom.",
        "use_when": "The atom is about a conceptual topic.",
        "do_not_use_when": "The atom describes a reusable implementation shape.",
        "examples": ["topic:atoms", "topic:composition"],
    },
    "layer": {
        "meaning": "Architectural layer where the atom applies.",
        "use_when": "The atom is scoped to a layer of the system.",
        "do_not_use_when": "The tag names only a broad topic or system.",
        "examples": ["layer:document-model", "layer:runtime", "layer:cli"],
    },
    "domain": {
        "meaning": "Problem domain or durable area of concern.",
        "use_when": "The atom belongs to a reusable problem domain.",
        "do_not_use_when": "A more specific system, topic, layer, or pattern tag applies.",
        "examples": ["domain:knowledge-management", "domain:task-execution"],
    },
}


def default_registry_path(root: Path) -> Path:
    return root / "desk" / "atoms" / "tag-namespaces.yaml"


def ensure_default_namespaces(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_registry(path, {"namespaces": DEFAULT_ATOM_TAG_NAMESPACES})


def load_namespaces(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    namespaces = loaded.get("namespaces") or {}
    if not isinstance(namespaces, dict):
        raise ValueError(f"Invalid atom tag namespace registry at {path}")
    return dict(namespaces)


def add_namespace(
    path: Path,
    namespace: str,
    *,
    meaning: str,
    use_when: str,
    do_not_use_when: str,
    examples: list[str],
) -> None:
    namespace = namespace.strip()
    if not NAMESPACE_PATTERN.fullmatch(namespace):
        raise ValueError("Namespace must match ^[a-z][a-z0-9_]*$.")

    path.parent.mkdir(parents=True, exist_ok=True)
    registry = {"namespaces": load_namespaces(path)}
    if namespace in registry["namespaces"]:
        raise ValueError(f"Atom tag namespace '{namespace}' already exists.")

    for example in examples:
        match = TAG_PATTERN.fullmatch(example)
        if match is None or match.group("namespace") != namespace:
            raise ValueError(f"Example '{example}' must use namespace '{namespace}'.")

    registry["namespaces"][namespace] = {
        "meaning": meaning,
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
        "examples": examples,
    }
    _write_registry(path, registry)


def axis_values(tags: list[str], axis: str) -> list[str]:
    """Return the sorted unique values carried by tags of the axis namespace."""
    values: set[str] = set()
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == axis:
            values.add(str(tag).split(":", 1)[1])
    return sorted(values)


def folder_axis_value(tags: list[str], axis: str) -> str | None:
    """Return the single folder-axis value for an atom, or None when absent.

    Raises ValueError when the atom carries more than one value of the axis
    namespace, because the physical folder placement must be deterministic.
    """
    values = axis_values(tags, axis)
    if len(values) > 1:
        raise ValueError(
            f"Atom carries multiple '{axis}' axis values: {', '.join(values)}. "
            f"The folder axis requires exactly one '{axis}:<value>' tag; "
            "remove the extra axis tags or split the atom."
        )
    return values[0] if values else None


def axis_folder(value: str) -> Path:
    """The folder an axis value places an atom in: sldb's ``tag_folder`` (``a.b`` -> ``a/b``).

    An empty segment (``a..b``, ``a.``) is a ``ValueError``; the atom model never lets one in
    (``check_atom_tags``).
    """
    from sldb.api import tag_folder

    return Path(tag_folder(value))


# --- The tag declaration of the store (CC35d resto, e1) ------------------------------------
#
# ``desk/atoms/tag-namespaces.yaml`` is the desk's registry; the store declares the same
# namespaces in ``.sldb/store.yaml`` (``tag_namespaces``), and sldb checks them as the rule
# family ``builtin:tag_namespace:<name>`` (docs/architecture/tags.md in sldb). The file wins:
# ``sync_tag_declaration`` rewrites the declaration only when it differs.

#: The models whose tags the family checks: atoms and protoatoms (the protoatom exists to hang
#: from a domain). Tasks, pills and the rest carry namespaces the registry does not declare.
TAG_MODELS = ["AtomDoc", "ProtoAtomDoc"]
#: A ``domain:a.b`` tag is anchored by the CrossroadDoc whose ``path`` is ``a.b``.
DOMAIN_ANCHOR = {"model": "CrossroadDoc", "field": "path", "value": "bare"}
_SEEN = "(seen: "


def tag_store(root: Path) -> Path | None:
    """The desk's store, or None when the repository has none (then nothing is checked)."""
    from sldb.store.layout import store_exists

    store = Path(root) / ".sldb"
    return store if store_exists(store) else None


def wanted_tag_declaration(root: Path) -> tuple[list[Any], list[str]]:
    """``(tag_namespaces, tag_models)`` the store must declare for the registry file.

    ``folder_axis`` is not declared: the atom folder axis is ``desk/config.json``'s
    ``atom_folder_axis``, which ``config.local.json`` may override per machine, and the
    committed ``store.yaml`` must not depend on the machine.
    """
    from sldb.api import TagNamespace

    from deskops.models.atom import DOMAIN_NAMESPACE

    root = Path(root)
    namespaces = [
        TagNamespace(name=name, anchored_by=dict(DOMAIN_ANCHOR) if name == DOMAIN_NAMESPACE else None)
        for name in sorted(load_namespaces(default_registry_path(root)))
    ]
    return namespaces, list(TAG_MODELS) if namespaces else []


def sync_tag_declaration(root: Path, *, apply: bool = True) -> bool:
    """Whether the store's tag declaration differs from ``tag-namespaces.yaml``; with ``apply``,
    rewrite it (sldb's ``save_declaration``). Idempotent: a second run finds nothing to do.

    A store without ``store.yaml`` (``deskops init`` creates none) starts from the declaration its
    index implies (sldb's ``declare_store``) once there is a namespace to declare.
    """
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import declaration_path
    from sldb.api.stores.store_declaration import load_declaration
    from sldb.api.stores.store_declaration import save_declaration

    root = Path(root)
    store = tag_store(root)
    if store is None:
        return False
    namespaces, models = wanted_tag_declaration(root)
    if declaration_path(store).is_file():
        current = load_declaration(store)
    elif namespaces:
        current = None
    else:
        return False
    if current is not None and current.tag_namespaces == namespaces and current.tag_models == models:
        return False
    if apply:
        base = current if current is not None else declare_store(store, Path(root).resolve())
        save_declaration(store, base.model_copy(update={"tag_namespaces": namespaces, "tag_models": models}))
    return True


# --- Bridge until sldb H4 ---------------------------------------------------------------
#
# Puente hasta sldb H4 (q18: create/track evalúan on_write). sldb's ``create_document`` and
# ``track_document_file`` do not evaluate ``on_write``, so the family cannot refuse a document
# deskops is about to create, and a CrossroadDoc carries no tag for it to check. Until they do,
# deskops refuses before writing from sldb's data only: the declared namespaces
# (``tag_namespaces``), the anchors (``tag_tree``) and what each tag requires
# (``TagNamespace.required``). Without a store or a declaration nothing is checked.


def declared_namespaces(store: Path) -> dict[str, Any]:
    """The namespaces the store declares, by name (``sldb.api.tag_namespaces``)."""
    from sldb.api import TagNamespace
    from sldb.api import tag_namespaces

    return {item["name"]: TagNamespace(**item) for item in tag_namespaces(store)}


def _anchored(store: Path, namespace: str) -> set[str]:
    from sldb.api import tag_tree

    found: set[str] = set()
    pending = list(tag_tree(store, namespace)["roots"])
    while pending:
        node = pending.pop()
        if node["document"] is not None:
            found.add(node["tag"])
        pending.extend(node["children"])
    return found


def refuse_undeclared_namespaces(root: Path, tags: list[str]) -> None:
    """Refuse a tag whose namespace the store does not declare (bridge until sldb H4)."""
    store = tag_store(root)
    declared = declared_namespaces(store) if store is not None else {}
    if not declared:
        return
    for tag in tags:
        namespace = str(tag).split(":", 1)[0]
        if ":" in str(tag) and namespace not in declared:
            raise ValueError(f"Unknown atom tag namespace '{namespace}' for tag '{tag}'.")


def unanchored_tags(root: Path, tags: list[str]) -> list[str]:
    """The tags ``tags`` require (``TagNamespace.required``) that no document anchors, top-down
    and once each; empty without a store or without anchored namespaces (bridge until sldb H4)."""
    store = tag_store(root)
    declared = declared_namespaces(store) if store is not None else {}
    missing: list[str] = []
    for name, namespace in declared.items():
        own = [str(tag) for tag in tags if str(tag).split(":", 1)[0] == name]
        if namespace.anchored_by is None or not own:
            continue
        anchored = _anchored(store, name)
        for tag in own:
            missing += [need for need in namespace.required(tag) if need not in anchored and need not in missing]
    return missing


def refuse_unanchored_domains(root: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix (bridge until
    sldb H4); the message names the crossroads to write, top-down."""
    missing = [tag.split(":", 1)[1] for tag in unanchored_tags(root, tags)]
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


def refuse_unplaced_tags(root: Path, tags: list[str]) -> None:
    """The bridge for a document about to be created: declared namespaces, then anchored domains."""
    refuse_undeclared_namespaces(root, tags)
    refuse_unanchored_domains(root, tags)


# --- The family's findings, in deskops' words ----------------------------------------------


def tag_findings(root: Path) -> dict[str, dict[str, list[str]]]:
    """The findings of sldb's ``tag_check`` by document path (absolute, as ``str``), split in
    ``namespace`` (an undeclared namespace) and ``anchor`` (a domain path without crossroad),
    with the texts ``atoms validate`` printed before sldb checked them. Empty without a store or
    a declaration. Only the documents the store tracks are checked.
    """
    from sldb.api import tag_check

    store = tag_store(root)
    if store is None or not declared_namespaces(store):
        return {}
    base = Path(root).resolve()
    found: dict[str, dict[str, list[str]]] = {}
    for finding in tag_check(store):
        if not finding.document or _SEEN not in finding.what:
            continue
        seen = json.loads(finding.what.split(_SEEN, 1)[1][:-1])
        record = found.setdefault(str(base / finding.document), {"namespace": [], "anchor": []})
        if "missing" in seen:
            record["anchor"] += [
                f"no written crossroad for domain path '{tag.split(':', 1)[1]}'" for tag in seen["missing"]
            ]
        else:
            record["namespace"] += [
                f"Unknown atom tag namespace '{seen['namespace']}' for tag '{tag}'." for tag in seen["tags"][:1]
            ]
    return found


def _write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(registry, sort_keys=True), encoding="utf-8")
