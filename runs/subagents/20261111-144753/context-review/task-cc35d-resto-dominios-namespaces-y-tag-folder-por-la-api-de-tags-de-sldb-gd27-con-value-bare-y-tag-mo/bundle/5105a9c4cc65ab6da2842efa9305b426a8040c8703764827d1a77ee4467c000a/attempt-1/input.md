FILE:desk/tasks/task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo.md
---
sldb:
  by: agent
  at: '2026-11-11T14:46:59Z'
  authority: generated
  via: create_document
id: task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/domain_tree.py
- deskops/atom_tags.py
- deskops/doc_access.py
- deskops/services/atoms.py
- deskops/cli/commands/atoms.py
- deskops/cli/commands/doctor.py
- deskops/models/atom.py
- deskops/data/desk_declaration.yaml
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cc35d-resto-rbol-de-dominios-require-domain-parents-tag-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-cuando-sldb-resuelva-h1-h3.md
---

# CC35d resto: dominios, namespaces y tag_folder por la API de tags de sldb (GD27 con value bare y tag_models)

## Rationale

_Explain why this task exists or the business driver behind it._

Resto de CC35d cortado por DO7, ahora desbloqueado por GD27 para deskops en sldb. Cierra CC35 entero y con eso abre CC51-53.

## Goal

_Describe the concrete result this task must produce._

domain_tree, atom_tags y los chequeos de namespaces y padres de dominio pasan a la API de tags de sldb (declaración, reglas, tag_tree, tag_folder); se borran require_domain_parents, _domain_errors y validate_atom_tag_namespaces; goldens idénticos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/domain_tree.py, deskops/atom_tags.py, deskops/doc_access.py, deskops/services/atoms.py, deskops/cli/commands/atoms.py, deskops/cli/commands/doctor.py, deskops/models/atom.py, deskops/data/desk_declaration.yaml, tests/, docs/, CHANGELOG.md. Fuera: desk replace (ya entró) y vistas (CC34).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO: es el resto de CC35d (DO7, decisiones.md de deskops-como-config), con el scope de CC35d del dag (rev 3) para tags: namespaces, domain_tree y la API de tags de sldb (GD27), menos lo que ya entró (a4, desk replace por sldb.replace_text, 6d55bb40). Drawer de origen: 'CC35d resto'. Informe de CC35d: runs/subagents/cc35d-worker-report.md (en la rama wt/cc35d, 568d2140 y 1b3ad660).

LO QUE DESBLOQUEA (sldb, tarea GD27 para deskops, en sldb main antes de despachar):
- anchored_by admite value: bare, para que CrossroadDoc.path 'a.b' ancle 'domain:a.b' (B1/H1).
- La declaración del store admite tag_models: la familia builtin:tag_namespace solo evalúa esos modelos y sus descendientes; las anclas no se filtran (B2/H2).
- tag_folder sigue estricto con segmentos vacíos (H3): deskops se adapta.

ALCANCE (e1-e7):
e1 (declaración): tag-namespaces.yaml del desk se lleva a la declaración del store con la API de declaración de sldb (load_declaration/save_declaration o stores declare), nunca a mano. tag_models = [AtomDoc] y sus descendientes que deskops usa, más CrossroadDoc y ProtoAtomDoc si llevan tags del namespace. domain se declara con anchored_by {model: CrossroadDoc, field: path, value: bare}. Lo escribe desk update --apply de forma idempotente; si archivo y declaración difieren, gana el archivo.
e2 (domain_tree.py): queda solo la creación de crossroads y protoatoms. require_domain_parents y _domain_errors se borran; los padres de dominio los exige la regla builtin:tag_namespace:domain de sldb (fila 5 del inventario de CC38).
e3 (atom_tags.py): validate_atom_tag_namespaces (fila 3 del inventario de CC38, namespace declarado) se borra; lo cubre la regla de sldb. La forma del tag sigue en el modelo.
e4 (H3): ATOM_TAG_PATTERN (deskops/models/atom.py) prohíbe segmentos vacíos ('a..b', 'a.', '.a') para que tag_folder de sldb nunca reciba uno; folder axis pasa a tag_folder de sldb. Antes de cambiarlo, el informe cuenta cuántos átomos de los 6 desks tienen ese patrón (copias en /dev/shm). Si alguno lo tiene, el worker para y avisa.
e5 (B3): doc_access.py, services/atoms.py, cli/commands/atoms.py y cli/commands/doctor.py dejan de llamar a lo borrado y usan la API de sldb (rules check sobre la familia, tag_tree, tag_folder) con el mismo texto de error y exit que hoy (goldens).
e6 (aceptación): grep de require_domain_parents, _domain_errors y validate_atom_tag_namespaces en deskops/ vacío; 'domain:a.b' sin crossroad sigue fallando con el mismo exit y texto; goldens de ayuda y salida idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; desk update --apply idempotente; tests de los archivos tocados verdes; CHANGELOG y docs.
e7 (sldb): lo que falte se deja como hipótesis en el informe; el coordinador abre la nota. No se escribe en sldb.

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

4 PASOS: sldb stores build --store .sldb; pytest de a uno; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio. Si el nodo registra o cambia un modelo del store, tests/test_model_contract_snapshot.py va en la lista.

## Validation

_List the checks required before this task can close._

- grep de require_domain_parents, _domain_errors y validate_atom_tag_namespaces en deskops/ vacío
- domain:a.b sin crossroad falla igual; goldens idénticos
- desk update --apply idempotente con la declaración de tags
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

e1-e7 hechos con tests verdes; CHANGELOG y docs.

FILE:deskops/domain_tree.py
"""Domain tree: crossroads order a knowledge base and protoatoms hang from them.

A ``domain:a.b.c`` tag places a document under the path ``a.b.c``. Every prefix
of that path (``a``, ``a.b``, ``a.b.c``) needs a CrossroadDoc with written
content: the system is forced to write the parent before it can describe the
children. Protoatoms are free atoms; typing one into another sldb model keeps it
as a redirect stub whose ``typed_as`` names the typed document.

What one document must satisfy on its own (the form of its id, its tags and its
domain paths, one ``domain:`` tag per protoatom, a crossroad id naming its path)
is a validator of its model in ``deskops.models``. What is checked here needs
other documents or the file tree: the written parents of a domain path, the file
name of a document, the tag namespace registry and the target of ``typed_as``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.bootstrap import MODEL_REFS
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.models.atom import DOMAIN_NAMESPACE as DOMAIN
from deskops.models.atom import AtomDoc
from deskops.models.atom import domain_paths
from deskops.models.crossroad import CROSSROAD_PREFIX
from deskops.models.crossroad import DOMAIN_PATH_PATTERN
from deskops.models.crossroad import CrossroadDoc
from deskops.models.crossroad import crossroad_id
from deskops.models.protoatom import PROTO_PREFIX
from deskops.models.protoatom import ProtoAtomDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated

__all__ = ["DOMAIN", "PROTO_PREFIX", "CROSSROAD_PREFIX", "domain_paths", "crossroad_id", "DomainTree"]

_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)


def prefixes(path: str) -> list[str]:
    """``a.b.c`` -> ``['a', 'a.b', 'a.b.c']``."""
    parts = path.split(".")
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def read_crossroads(atoms_dir: Path) -> dict[str, dict[str, Any]]:
    """Written crossroads by path. An unreadable or invalid one does not count as written."""
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
    """Refuse domain tags whose path lacks a written crossroad for some prefix.

    The form of each path is the model's invariant (``AtomDoc.tags``); this only asks
    the file tree whether the parents are written.
    """
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
        self.root = Path(root).resolve()
        self.desk_root = doc_access.desk_root(self.root)
        self.atoms_dir = self.desk_root / "atoms"

    def create_crossroad(self, path: str, *, title: str, content: str) -> Created:
        doc_access.ensure_workspace(self.root)
        payload = validated(
            CrossroadDoc, {"id": crossroad_id(path), "path": path, "title": title, "content": content}
        ).model_dump(mode="json")
        parent = path.rpartition(".")[0]
        if parent:
            require_domain_parents(self.atoms_dir, [f"{DOMAIN}:{parent}"])
        if path in read_crossroads(self.atoms_dir):
            raise FileExistsError(f"A crossroad for '{path}' already exists.")
        return self._create(CrossroadDoc, payload, [f"{DOMAIN}:{path}"])

    def create_protoatom(self, doc_id: str, *, title: str, content: str = "", tags: list[str]) -> Created:
        doc_access.ensure_workspace(self.root)
        tags = list(tags)
        payload = validated(ProtoAtomDoc, {"id": doc_id, "title": title, "content": content, "tags": tags}).model_dump(
            mode="json"
        )
        validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        require_domain_parents(self.atoms_dir, tags)
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
        doc_access.ensure_workspace(self.root)
        proto_path = self._find_protoatom(selector)
        proto = doc_access.read_doc(proto_path, ProtoAtomDoc)
        if proto.get("typed_as"):
            raise ValueError(f"{proto['id']} was already typed as {proto['typed_as']}.")
        model = self._resolve_model(model_name)
        slug = str(proto["id"]).removeprefix(PROTO_PREFIX)
        target_id = doc_id or f"{model.__name__.removesuffix('Doc').lower()}-{slug}"
        payload = validated(model, self._typed_payload(model, target_id, proto, content_field, data or {})).model_dump(
            mode="json"
        )
        stub = validated(ProtoAtomDoc, {**proto, "typed_as": f"{model.__name__}:{target_id}",
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
                payload = doc_access.read_doc(file, model)
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
        path = doc_access.atom_doc_path(self.root, doc_id, tags)
        self._write_and_track(path, model, payload, doc_id)
        return Created(doc_id, path)

    def _write_and_track(self, path: Path, model: type[Any], payload: dict[str, Any], doc_id: str) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)
        try:
            doc_access.track_created_document(self.root, model, path, doc_id)
        except Exception:
            doc_access.remove_created_file(path)
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
            return doc_access.atom_doc_path(self.root, doc_id, tags)
        artifact = next((key for key, known in ARTIFACT_MODELS.items() if known.__name__ == model.__name__), None)
        folder = Path(ARTIFACT_PATHS[artifact]) if artifact else Path("typed") / model.__name__
        return self.desk_root / folder / f"{doc_id}.md"

    def _check_crossroad(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(CrossroadDoc, path.read_text(encoding="utf-8"), invalid="crossroad is invalid")
        except Exception as exc:
            return path.stem, [f"crossroad is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        if path.stem != doc_id:
            errors.append(f"filename must match crossroad id '{doc_id}'")
        parent = str(payload.get("path") or "").rpartition(".")[0]
        if parent:
            errors.extend(self._domain_errors([f"{DOMAIN}:{parent}"], crossroads))
        return doc_id, errors

    def _check_protoatom(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(ProtoAtomDoc, path.read_text(encoding="utf-8"), invalid="protoatom is invalid")
        except Exception as exc:
            return path.stem, [f"protoatom is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        tags = list(payload.get("tags") or []) if isinstance(payload.get("tags"), list) else []
        if path.stem != doc_id:
            errors.append(f"filename must match protoatom id '{doc_id}'")
        try:
            validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        except ValueError as exc:
            errors.append(str(exc))
        errors.extend(self._domain_errors(tags, crossroads))
        typed_as = str(payload.get("typed_as") or "")
        if typed_as and not any(self.desk_root.rglob(f"{typed_as.split(':', 1)[-1]}.md")):
            errors.append(f"typed_as target not found: {typed_as}")
        return doc_id, errors

    def _check_atom(self, path: Path, crossroads: dict[str, Any]) -> list[str]:
        try:
            tags = check_document(AtomDoc, path.read_text(encoding="utf-8"))[0].get("tags")
        except Exception:
            return []  # atoms validate already reports unreadable atoms
        return self._domain_errors(list(tags) if isinstance(tags, list) else [], crossroads)

    def _domain_errors(self, tags: list[str], crossroads: dict[str, Any]) -> list[str]:
        """The domain paths of ``tags`` without a written crossroad. A malformed path is the
        model's error (reported with the document), so it is left out here."""
        valid = [f"{DOMAIN}:{value}" for value in domain_paths(tags) if _DOMAIN_PATH.fullmatch(value)]
        return [f"no written crossroad for domain path '{path}'" for path in missing_parents(valid, crossroads)]


def _redirect_content(model_name: str, doc_id: str) -> str:
    return (
        f"Typed as {model_name} {doc_id}. This protoatom is kept as a redirect stub so its id keeps "
        "resolving; its content now lives in the typed document."
    )


def _first_line(exc: Exception) -> str:
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return " ".join(lines[:3]) if lines else exc.__class__.__name__

FILE:deskops/atom_tags.py
from __future__ import annotations

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


def axis_folder_relpath(value: str) -> Path:
    """Map a dot-notated axis value to a nested folder path.

    Example: 'mepu.licitaciones' -> Path('mepu/licitaciones').
    """
    parts = [part for part in str(value).split(".") if part]
    if not parts:
        raise ValueError(f"Axis value '{value}' does not produce a valid folder path.")
    return Path(*parts)


def validate_atom_tag_namespaces(tags: list[str], path: Path) -> None:
    """Every tag's namespace is declared in the registry at ``path`` (a rule between the
    document and ``tag-namespaces.yaml``). The form of a tag is the model's own invariant
    (``AtomDoc.tags``), so a malformed tag is not this function's error.
    """
    namespaces = load_namespaces(path)
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is None:
            continue
        namespace = match.group("namespace")
        if namespace not in namespaces:
            raise ValueError(f"Unknown atom tag namespace '{namespace}' for tag '{tag}'.")


def _write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(registry, sort_keys=True), encoding="utf-8")

FILE:deskops/doc_access.py
"""Reading, writing and resolving the documents of one desk.

Every function takes the repository ``root`` (the directory that holds ``desk/``) and
works on the desk documents under it: parse a document into its model payload, write
one through ``sldb.api.transaction``, resolve a selector to a file, read a task with
its inherited context, or list the artifacts of one kind. ``DeskopsOperations`` is a
facade over these functions and the services; the services call them directly.

Writes: every document write of deskops goes through the desk's ``sldb.api.transaction``
(``desk_transaction``), so a service that writes several documents wraps them in one block
and a failure anywhere restores them all. An update of a tracked document carries
``expected_source_hash``: the hash the store had indexed for the document when
``read_doc`` read it (``index_entry``, from the store's indexes alone), so a document the
store rewrote in between is refused with the deskops conflict message and nothing is
written. A document edited by hand and not reindexed keeps its indexed hash, so the next
deskops edit of it goes through.
"""

from __future__ import annotations

from contextlib import contextmanager
import copy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterator

import yaml
from sldb.api import AmbiguousSelectionError
from sldb.api import ConflictError
from sldb.api import Transaction
from sldb.api import store_fingerprint
from sldb.api import tracked_documents
from sldb.api import select_documents
from sldb.api import transaction
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.layout import store_exists
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
# CC35b-a3: untracked surface, resolved on disk
from deskops.desk_paths import resolve_selector
from deskops.desk_paths import relative_candidates
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.errors import DomainError
from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import DeskFAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import ReviewDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.paths import package_pythonpath
from deskops.runtime import Task
from deskops.specs import compile_artifact_spec
from deskops.specs import compile_task_spec
from deskops.workspace import seed_desk


ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.materialization": MaterializationContractDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.review": ReviewDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": DeskFAQDoc,
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
    "artifact.review": "reviews",
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
    "artifact.review": {"subject": "review", "list_subject": "reviews", "create": False},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}

# Fields whose value is an effect of a workflow command, not a free edit. The
# value names who writes the field, so the refusal teaches the correct entry
# point instead of only saying no.
_TASK_OWNED_FIELDS = {
    "status": "deskops advance (transition effects) and deskops closeout commit",
    "current_node": "deskops advance",
    "history": "deskops advance and deskops closeout (append-only)",
    "task_type": "deskops add task --task-type (create a new task to change the type)",
    "closeout_evidence": "the task type, and deskops add task --evidence at creation",
}

# Artifacts whose documents are named by hand: their files are not `<id_pattern>.md`.
_FREE_NAMED_ARTIFACTS = {"artifact.inbox_note", "artifact.board", "artifact.ritual", "artifact.review"}

# Artifacts tracked in the desk's store on creation whatever their surface; ``create_artifact``
# also tracks every other artifact it writes on a tracked surface (``_tracked_surface``).
_TRACKED_ON_CREATE = {"artifact.atom", "artifact.pill", "artifact.materialization"}

# (absolute path, model) -> (text, payload): ``read_doc`` parses a document once per text.
_DOC_PAYLOADS: dict[tuple[str, Any], tuple[str, dict[str, Any]]] = {}

# absolute path -> the source hash the store had indexed for the document when ``read_doc``
# last read it (None: not tracked then): the ``expected_source_hash`` of its next update.
_READ_HASHES: dict[str, str | None] = {}

# resolved store path -> (store index signature, {relative path: IndexEntry}).
_INDEX_ENTRIES: dict[str, tuple[tuple[int, int], dict[str, "IndexEntry"]]] = {}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


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


def desk_root(root: Path) -> Path:
    return root / "desk"


# ---------------------------------------------------------------- workspace
def ensure_workspace(root: Path) -> None:
    """The desk scaffold: its declared folders (the artifact directories among them), seed files
    and default tag namespaces, whichever are missing (``seed_desk``)."""
    seed_desk(root)


# ---------------------------------------------------------------- store
@dataclass(frozen=True)
class IndexEntry:
    """What the desk's store records about one tracked document: its model, its name and
    the ``source_hash`` of the text it last indexed."""

    model: str
    name: str
    source_hash: str


def store_path(root: Path) -> Path:
    return root / ".sldb"


def has_store(root: Path) -> bool:
    """Whether the root has an sldb store: a ``.sldb/`` that only holds runtime files
    (graph snapshots, caches) is not one."""
    return store_exists(store_path(root))


def _absolute(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def relative_path(root: Path, path: Path | str) -> str:
    """``path`` relative to the project root with ``/`` separators, as the store records it."""
    absolute = _absolute(root, path).resolve()
    try:
        return absolute.relative_to(root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _model_name(model: Any) -> str:
    return model if isinstance(model, str) else str(getattr(model, "__name__", model))


@contextmanager
def desk_transaction(root: Path) -> Iterator[Transaction | None]:
    """``sldb.api.transaction`` over the desk's store, importing its models from the deskops package.

    Nested blocks over the same root join the open one, so a service that writes several
    documents wraps them in one block and a failure anywhere restores them all. A root
    without a store (a desk before ``deskops init``, the desks some tests build) has no
    transaction: the block runs with ``None`` and each write is a plain file write.
    """
    if not has_store(root):
        yield None
        return
    with transaction(store_path(root), pythonpath=package_pythonpath()) as tx:
        yield tx


def _index_signature(root: Path) -> tuple[int, int]:
    try:
        stat = (store_path(root) / "core" / "store_index.yaml").stat()
    except OSError:
        return (0, 0)
    return (stat.st_mtime_ns, stat.st_size)


def index_entries(root: Path) -> dict[str, IndexEntry]:
    """Relative path -> index entry of every document the desk's store tracks.

    Read from the store's indexes alone (``store_fingerprint`` for the hashes,
    ``tracked_documents`` for the paths): no model is imported and no document is extracted.
    Kept per process while the store index keeps its signature: every sldb write moves it, a
    hand edit of a document does not, which is what the update guard needs (the hash of the
    text the store indexed, not of the file on disk).
    """
    if not has_store(root):
        return {}
    store = store_path(root)
    key = str(store.resolve())
    signature = _index_signature(root)
    hit = _INDEX_ENTRIES.get(key)
    if hit is not None and hit[0] == signature:
        return hit[1]
    fingerprint = store_fingerprint(store)
    refs = {key.replace(":", "/", 1): key for key in fingerprint.documents}
    statuses = tracked_documents(store, list(refs))
    entries = {
        str(status.path): IndexEntry(
            model=str(status.model),
            name=str(status.name),
            source_hash=fingerprint.documents[refs[ref]].source_hash,
        )
        for ref, status in statuses.items()
    }
    _INDEX_ENTRIES[key] = (signature, entries)
    return entries


def forget_index(root: Path) -> None:
    _INDEX_ENTRIES.pop(str(store_path(root).resolve()), None)


def index_entry(root: Path, path: Path | str) -> IndexEntry | None:
    """The store's entry for ``path``, or None when it is not tracked (or there is no store)."""
    return index_entries(root).get(relative_path(root, path))


def _store_root_of(path: Path) -> Path | None:
    """The root whose store may track ``path``: the nearest parent with a store, unless a
    desk without one (``desk/`` and no ``.sldb``) comes first."""
    for parent in path.resolve().parents:
        if has_store(parent):
            return parent
        if (parent / "desk").is_dir():
            return None
    return None


def _note_read(path: Path) -> None:
    """Keep the source hash the store has for ``path`` as of this read."""
    root = _store_root_of(path)
    entry = index_entry(root, path) if root is not None else None
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _note_written(root: Path, path: Path) -> None:
    forget_index(root)
    entry = index_entry(root, path)
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def conflict_error(root: Path, path: Path | str) -> DomainError:
    """The deskops conflict: the store rewrote the document after deskops read it."""
    return DomainError(
        f"Error: {relative_path(root, path)} changed since deskops read it; nothing was written. Re-run the command."
    )


def update_tracked_doc(tx: Transaction, root: Path, path: Path, entry: IndexEntry, payload: dict[str, Any]) -> None:
    """``Transaction.update`` of the tracked document at ``path``, guarded by the source hash
    deskops read for it (``read_doc``; ``entry.source_hash`` when the caller read it another
    way). A failed guard raises the deskops conflict, and the transaction writes nothing."""
    key = os.path.abspath(path)
    expected = _READ_HASHES.get(key, entry.source_hash)
    try:
        tx.update(relative_path(root, path), payload, expected_source_hash=expected)
    except ConflictError as exc:
        raise conflict_error(root, path) from exc
    _note_written(root, path)


def delete_doc(root: Path, path: Path) -> None:
    """Delete a document: ``Transaction.delete`` when the store tracks it (entry and file),
    else the file alone, recorded so the transaction restores it on failure."""
    with desk_transaction(root) as tx:
        if tx is not None and index_entry(root, path) is not None:
            tx.delete(relative_path(root, path))
        else:
            if tx is not None:
                tx.record(relative_path(root, path))
            if path.exists():
                path.unlink()
    _READ_HASHES.pop(os.path.abspath(path), None)
    forget_index(root)


def untrack_doc(root: Path, ref: Path | str) -> bool:
    """``Transaction.untrack`` by path or document name. A document the store does not
    track, or a root without a store, is left alone (False)."""
    with desk_transaction(root) as tx:
        if tx is None:
            return False
        if isinstance(ref, Path):
            entry = index_entry(root, ref)
            name = entry.name if entry is not None else None
        else:
            name = next((entry.name for entry in index_entries(root).values() if entry.name == ref), None)
        if name is None:
            return False
        tx.untrack(name)
    forget_index(root)
    return True


# ---------------------------------------------------------------- read / write
def read_doc(path: Path, model: type[Any]) -> dict[str, Any]:
    """The model payload of a document, parsed once per text of the file.

    The parse is kept for the whole process under (path, model) with the text it came
    from, and handed out as a copy: a reader that builds a new ``DeskopsOperations`` per
    request (the UI's server) does not re-parse unchanged documents, and a caller that
    edits the payload it got does not edit the kept one.
    """
    raw_text = path.read_text(encoding="utf-8")
    _note_read(path)
    key = (os.path.abspath(path), model)
    hit = _DOC_PAYLOADS.get(key)
    if hit is not None and hit[0] == raw_text:
        return copy.deepcopy(hit[1])
    payload = extract_model_data(model, raw_text)
    if "id" not in payload:
        payload["id"] = path.stem
    _DOC_PAYLOADS[key] = (raw_text, copy.deepcopy(payload))
    return payload


def write_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
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
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
            return
        entry = index_entry(root, path)
        if entry is None:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))
            return
        update_tracked_doc(tx, root, path, entry, payload)


def write_new_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    """A new document the store does not track yet, as a file the desk's transaction restores
    on failure (``write_file``); ``track_created_document`` tracks it when its kind is tracked."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    rendered = render_model_markdown(model, payload) + "\n"
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
        else:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))


def create_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any], name: str) -> None:
    """A new tracked document: ``Transaction.create`` renders it under its registered model
    and tracks it in one step. Without a store, the file alone."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, render_model_markdown(model, payload) + "\n")
            return
        tx.create(_model_name(model), name, payload, relative_path(root, path))
    _note_written(root, path)


def remove_created_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def track_created_document(root: Path, model: type[Any], path: Path, doc_id: str) -> None:
    """``Transaction.track`` of a document deskops just wrote, if the root has a store."""
    with desk_transaction(root) as tx:
        if tx is not None:
            tx.track(relative_path(root, path), _model_name(model), doc_id)
    _note_written(root, path)


def track_created_artifact(root: Path, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
    if artifact_id not in _TRACKED_ON_CREATE:
        return
    track_created_document(root, model, path, doc_id)


# ---------------------------------------------------------------- values
def coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def merge_unique(*values: list[str]) -> list[str]:
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


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    YAML folds the line breaks of multi-line text and reads `**bold` as an alias,
    so a text field (`str` or `str | None`) takes the raw value as written. A JSON
    string literal (`"..."`) is still decoded, for callers that quote their text.
    """
    annotation = model.model_fields[field_name].annotation
    if annotation in (str, str | None):
        if raw_value.startswith('"'):
            try:
                decoded = json.loads(raw_value)
            except ValueError:
                return raw_value
            if isinstance(decoded, str):
                return decoded
        return raw_value
    return parse_data_value(raw_value)


# ---------------------------------------------------------------- paths and selectors
def artifact_path(root: Path, artifact_id: str, doc_id: str) -> Path:
    return desk_root(root) / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"


def artifact_glob_pattern(artifact_id: str) -> str:
    if artifact_id in _FREE_NAMED_ARTIFACTS:
        return "*.md"
    id_pattern = str(getattr(ARTIFACT_MODELS[artifact_id], "__artifact__", {})["id_pattern"])
    return id_pattern.replace("{slug}", "*") + ".md"


def atom_folder_axis(root: Path) -> str | None:
    """Return the configured folder axis namespace for atoms, or None (flat)."""
    axis = DeskConfig.load(desk_root(root)).atom_folder_axis
    if axis is None:
        return None
    axis = str(axis).strip()
    if not axis:
        return None
    namespaces = load_namespaces(default_registry_path(root))
    if axis not in namespaces:
        raise ValueError(
            f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
            "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
        )
    return axis


def atom_doc_path(root: Path, atom_id: str, tags: list[str]) -> Path:
    base = desk_root(root) / "atoms"
    axis = atom_folder_axis(root)
    if axis is not None:
        value = folder_axis_value(tags, axis)
        if value is not None:
            return base / axis_folder_relpath(value) / f"{atom_id}.md"
    return base / f"{atom_id}.md"


# Desk folders the store does not track (CC35b-a3): the include of
# ``deskops/data/desk_declaration.yaml`` declares neither, so their documents resolve on disk.
_UNTRACKED_DESK_FOLDERS = ("drawer", "issues")


def _tracked_surface(root: Path, directory: Path) -> bool:
    """Whether documents under ``directory`` resolve through the store: the root has one and
    the directory is not one of the desk folders it leaves untracked."""
    if not has_store(root):
        return False
    try:
        relative = directory.resolve().relative_to(desk_root(root).resolve())
    except ValueError:
        return True
    return not (relative.parts and relative.parts[0] in _UNTRACKED_DESK_FOLDERS)


def _select_one(root: Path, query: dict[str, str], selector: str, what: str) -> Path | None:
    """The one document ``query`` names (``select_documents``, ``expect="one"``), or None.

    Several matches raise the deskops ambiguity message, its candidates the rows of the same
    query (``expect="many"``) that ``AmbiguousSelectionError`` names, relative to ``desk/``.
    """
    store = store_path(root)
    try:
        rows = select_documents(store, query, expect="one")
    except AmbiguousSelectionError as error:
        named = set(error.candidates)
        paths = [root / row["path"] for row in select_documents(store, query) if row["export_id"] in named]
        raise ValueError(f"Ambiguous {what} selector '{selector}': {relative_candidates(desk_root(root), paths)}") from None
    except SLDBDocumentTargetError:
        return None
    return root / rows[0]["path"]


def resolve_document(
    root: Path,
    directory: Path,
    selector: str,
    what: str,
    *,
    pattern: str = "*.md",
    recursive: bool = True,
    model: str | None = None,
) -> Path:
    """The document ``selector`` names under ``directory`` (``pattern``; ``recursive`` reaches subfolders).

    A tracked surface asks ``sldb.api.select_documents`` twice, in order (TaskDoc c3): by
    name (``prefix``, where an exact name wins over the unique prefix match), then, only if
    that found nothing, by file name (``path_glob`` of ``<selector>*.md``), which keeps the
    files whose name differs from their document's (``desk/rituals/execution.md`` is
    ``ritual-execution``). An ambiguous query stops there. Zero matches raise
    ``FileNotFoundError``, several ``ValueError``, with the messages the disk rule uses.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")
    if not _tracked_surface(root, directory):
        # CC35b-a3: untracked surface, resolved on disk
        return resolve_selector(desk_root(root), [directory], selector, pattern, what, recursive=recursive)
    base = relative_path(root, directory) + ("/**/" if recursive else "/")
    by_name = {"prefix": selector, "path_glob": base + pattern}
    if model is not None:
        by_name["model"] = model
    for query in (by_name, {"path_glob": f"{base}{selector}*.md"}):
        found = _select_one(root, query, selector, what)
        if found is not None:
            return found
    raise FileNotFoundError(f"No {what} file found for selector '{selector}'")


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_document(root, directory, doc_id, "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    """``resolve_artifact_selector`` over several directories, in order: the first that
    names the selector wins (a review resolves by its id, the name the store tracks it by)."""
    for directory in directories:
        try:
            return resolve_artifact_selector(root, artifact_id, directory, selector)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_document(root, directory, selector, artifact_id, pattern=artifact_glob_pattern(artifact_id))
    except FileNotFoundError:
        if artifact_id != "artifact.task" or not _tracked_surface(root, directory):
            raise
    # Tasks written before the `task-*` naming are still tracked: every task type extends
    # TaskDoc, so its model family names them whatever their file is called.
    return resolve_document(root, directory, selector, artifact_id, model="TaskDoc")


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    return resolve_artifact_selector(root, "artifact.ritual", directory, selector)


def editable_artifact(root: Path, subject: str, selector: str) -> tuple[type[Any], Path, str]:
    """The model, file and kind of the document `deskops edit <subject> <selector>` names."""
    if subject == "task":
        try:
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "tasks", selector)
        except FileNotFoundError:
            # Drawer candidates are tasks too; an active task with the same
            # selector wins because it resolved before this fallback.
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "drawer" / "tasks", selector)
        return TaskDoc, path, "task"
    artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
    if subject not in artifact_subjects:
        raise ValueError(f"Unsupported edit subject: {subject}")
    artifact_id = artifact_subjects[subject]
    model = ARTIFACT_MODELS[artifact_id]
    if artifact_id == "artifact.ritual":
        return model, resolve_ritual_selector(root, selector), subject
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    path = resolve_artifact_selector_multi(root, artifact_id, directories, selector)
    return model, path, subject


# ---------------------------------------------------------------- tasks
def resolve_task_payload(root: Path, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
    """The normalized payload of a task with its inherited context (``effective_*``)."""
    if task_id in stack:
        chain = " -> ".join([*stack, task_id])
        raise ValueError(f"Task inheritance cycle detected: {chain}")
    path = resolve_glob(root, desk_root(root) / "tasks", task_id)
    payload = compile_task_spec(read_doc(path, TaskDoc), entry_node="").task_payload
    inherited_ids = coerce_list(payload.get("inherits_from") or [])
    inherited_payloads = [resolve_task_payload(root, parent_id, (*stack, task_id)) for parent_id in inherited_ids]

    payload["effective_references"] = merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
        payload.get("references", []),
    )
    payload["effective_pills"] = merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
        payload.get("pills", []),
    )
    payload["effective_tags"] = merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
        payload.get("atoms", []),
    )

    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = merge_unique(
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
        payload["effective_validation"] = coerce_list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    return payload


def hydrate_task(payload: dict[str, Any]) -> Task:
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
        closeout_evidence=list(payload.get("closeout_evidence") or []),
        effective_references=list(payload.get("effective_references") or payload.get("references") or []),
        effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
        effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
        effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
        effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
        effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
    )


def load_task(root: Path, task_id: str) -> Task:
    return hydrate_task(resolve_task_payload(root, task_id))


# ---------------------------------------------------------------- artifacts
def list_artifacts(root: Path, artifact_id: str) -> list[dict[str, Any]]:
    model = ARTIFACT_MODELS[artifact_id]
    directory = desk_root(root) / ARTIFACT_PATHS[artifact_id]
    if not directory.exists():
        if not desk_root(root).exists():
            raise FileNotFoundError(f"Desk root not found at {desk_root(root)}. Run 'deskops init' to initialize.")
        return []
    pattern = artifact_glob_pattern(artifact_id)
    results = []
    for path in sorted(directory.rglob(pattern)):
        try:
            results.append(read_doc(path, model))
        except Exception as e:
            print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
    return results


def show_artifact(root: Path, artifact_id: str, doc_id: str) -> dict[str, Any]:
    if not doc_id:
        raise ValueError(f"No {artifact_id} ID provided")
    model = ARTIFACT_MODELS[artifact_id]
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    return read_doc(resolve_artifact_selector_multi(root, artifact_id, directories, doc_id), model)


def create_artifact(root: Path, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
    ensure_workspace(root)
    model = ARTIFACT_MODELS[artifact_id]
    compiled = compile_artifact_spec(artifact_id, raw_payload, model_fields=model.model_fields.keys())
    validated(model, compiled.artifact_payload)
    doc_id = compiled.artifact_payload["id"]
    if artifact_id == "artifact.atom":
        tags = list(compiled.artifact_payload.get("tags") or [])
        validate_atom_tag_namespaces(tags, default_registry_path(root))
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(desk_root(root) / "atoms", tags)
        path = atom_doc_path(root, doc_id, tags)
    else:
        path = artifact_path(root, artifact_id, doc_id)
    # Every artifact `add` writes on a tracked surface is tracked as it is created: since CC35b
    # the selectors of `show`/`edit` resolve those surfaces through the store only, so a
    # document `add` left untracked could not be shown or edited until `desk update --apply`.
    if artifact_id in _TRACKED_ON_CREATE or _tracked_surface(root, path.parent):
        create_doc(root, path, model, compiled.artifact_payload, doc_id)
    else:
        write_new_doc(root, path, model, compiled.artifact_payload)
    return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=doc_id, path=path)


def edit_artifact_field(root: Path, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
    ensure_workspace(root)
    model, path, kind = editable_artifact(root, subject, selector)
    field_name = field.replace("-", "_")
    if field_name not in model.model_fields:
        raise ValueError(f"Unknown field '{field_name}' for {subject}")
    if field_name == "id":
        raise ValueError("Cannot edit immutable field 'id'")
    if subject == "task" and field_name in _TASK_OWNED_FIELDS:
        raise ValueError(
            f"{field_name} is not editable with edit task; "
            f"it is written by {_TASK_OWNED_FIELDS[field_name]}."
        )
    if subject == "review" and field_name in {"verdict", "reason", "disposed_at", "disposed_by"}:
        raise ValueError(
            "verdict is written by deskops review dispose (GC03); a new review is a new document"
        )
    payload = read_doc(path, model)
    payload[field_name] = _parse_field_value(model, field_name, raw_value)
    write_doc(root, path, model, payload)
    return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)


# ---------------------------------------------------------------- registry
def registered_repositories(root: Path) -> list[dict[str, Any]]:
    """The repositories of ``desk/registry/repo-*.md``: the documents the store tracks there
    (``select_documents``), or the files on disk in a desk without a store."""
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    if has_store(root):
        pattern = relative_path(root, registry_dir) + "/repo-*.md"
        paths = [root / row["path"] for row in select_documents(store_path(root), {"path_glob": pattern})]
    else:
        # CC35b-a3: untracked surface, resolved on disk
        paths = sorted(registry_dir.glob("repo-*.md"))
    repositories = []
    for path in paths:
        try:
            repositories.append(read_doc(path, RepositoryDoc))
        except Exception as e:
            print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
            continue
    return repositories


def repository_root(root: Path, repository: dict[str, Any]) -> Path:
    repo_path = Path(str(repository["path"]))
    if repo_path.is_absolute():
        return repo_path.resolve()
    return (root / repo_path).resolve()


def _resolve_repo_board_task_path(repo_root: Path, task_ref: str) -> Path | None:
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


def _task_route_summary(task_path: Path) -> dict[str, str]:
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


def list_repo_task_routes(root: Path) -> list[RepoTaskRoute]:
    routes: list[RepoTaskRoute] = []
    for repository in registered_repositories(root):
        repo_root = repository_root(root, repository)
        board_path = repo_root / "desk" / "tasks" / "Board.md"
        if not board_path.exists():
            continue
        try:
            board_payload = read_doc(board_path, BoardDoc)
        except Exception:
            continue
        for task_ref in board_payload.get("tasks") or []:
            task_path = _resolve_repo_board_task_path(repo_root, str(task_ref))
            if task_path is None:
                continue
            try:
                summary = _task_route_summary(task_path)
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

FILE:deskops/services/atoms.py
"""Atom domain service: create, validate, reorganize, split, merge, retarget, delete.

Every atom write goes through ``deskops.doc_access`` and the desk's
``sldb.api.transaction``; split and merge each run inside one ``desk_transaction``
block so a failure restores the original files and store entries.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from sldb.api import Transaction

from deskops import doc_access
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import axis_values
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.doc_access import DocumentRecord
from deskops.models import AtomDoc
from deskops.models import PillDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


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


def reference_points_to_atom(root: Path, reference: str) -> bool:
    """Whether a task reference names an atom document of this desk (by path or by id)."""
    candidate = reference.strip()
    if not candidate:
        return False
    path_text = candidate.split("::", 1)[0]
    path = Path(path_text)
    if not path.is_absolute():
        path = root / path
    atoms_dir = doc_access.desk_root(root) / "atoms"
    if path.suffix == ".md" and path.exists():
        try:
            path.relative_to(atoms_dir)
            return True
        except ValueError:
            pass
    atom_id = candidate.removeprefix("atom:")
    if not atom_id.startswith("atom-"):
        return False
    return any(atom_path.stem == atom_id for atom_path in atoms_dir.rglob("*.md"))


class AtomsService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Document access is ``deskops.doc_access``; these keep the service's own vocabulary.
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_doc(self.root, path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)

    def _remove_created_file(self, path: Path) -> None:
        doc_access.remove_created_file(path)

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        doc_access.track_created_artifact(self.root, artifact_id, model, path, doc_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return doc_access.resolve_artifact_selector(self.root, artifact_id, directory, selector)

    def _reference_points_to_atom(self, reference: str) -> bool:
        return reference_points_to_atom(self.root, reference)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return doc_access.resolve_artifact_selector_multi(self.root, artifact_id, directories, selector)

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
        untracked = doc_access.index_entry(self.root, path) is not None
        doc_access.delete_doc(self.root, path)
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
        normalized_question = str(five_wh_one_plus).strip()
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

        validated(AtomDoc, payload)
        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        doc_access.create_doc(self.root, path, AtomDoc, payload, atom_id)
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

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])
        new_payloads: dict[str, dict[str, Any]] = {}
        for target_id in normalized_ids:
            heading, content = assignments[target_id]
            new_payloads[target_id] = {
                "id": target_id,
                "title": f"{payload['title']} — {heading}",
                "five_wh_one_plus": payload["five_wh_one_plus"],
                "answer": content,
                "tags": list(payload.get("tags") or []),
                "provenance": payload.get("provenance"),
            }
            validated(AtomDoc, new_payloads[target_id])

        created: list[DocumentRecord] = []

        with doc_access.desk_transaction(self.root):
            for target_id in normalized_ids:
                new_payload = new_payloads[target_id]
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                doc_access.create_doc(self.root, new_path, AtomDoc, new_payload, target_id)
                created.append(DocumentRecord(kind="atom", doc_id=target_id, path=new_path))

            payload["answer"] = self._render_atom_split_redirect_answer(atom_id, normalized_ids)
            self._write_doc(path, AtomDoc, payload)

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

        validated(AtomDoc, source_payload)
        validated(AtomDoc, target_payload)

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        inbound_references = self._find_inbound_atom_references(source_id, excluded_path=source_path)
        rewritten_references: list[str] = []

        with doc_access.desk_transaction(self.root) as transaction:
            rewritten_references = self._rewrite_inbound_atom_references(
                source_id,
                target_id,
                excluded_paths={source_path, target_path},
                transaction=transaction,
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

        return AtomMergeResult(
            source_id=source_id,
            source_path=source_path,
            target_id=target_id,
            target_path=target_path,
            redirect_kept=True,
            rewritten_references=rewritten_references,
            ambiguities=ambiguities,
        )

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
        try:
            payload, errors = check_document(AtomDoc, path.read_text(encoding="utf-8"), invalid="model validation failed")
        except Exception as exc:
            return AtomValidationRecord(doc_id=path.stem, path=path, errors=[f"model validation failed: {exc}"])
        doc_id = str(payload.get("id") or path.stem)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")

        tags = payload.get("tags")
        try:
            validate_atom_tag_namespaces(
                list(tags) if isinstance(tags, list) else [],
                default_registry_path(self.root),
            )
        except ValueError as exc:
            errors.append(str(exc))

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

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
        transaction: Transaction | None = None,
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
            if transaction is not None:
                transaction.record(path)
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
        if not (self.root / ".sldb").is_dir():
            return False

        changed = False
        for atom_id, new_path in retargets.items():
            try:
                with doc_access.desk_transaction(self.root) as transaction:
                    doc_access.untrack_doc(self.root, atom_id)
                    transaction.track(self.root / new_path, "AtomDoc", atom_id)
            except Exception:
                continue
            doc_access.forget_index(self.root)
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        if not (self.root / ".sldb").is_dir():
            return False
        try:
            doc_access.untrack_doc(self.root, atom_id)
        except Exception:
            return False
        return True

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        return doc_access.atom_folder_axis(self.root)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:deskops/cli/commands/atoms.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.atom_tags import add_namespace
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.domain_tree import DomainTree
from deskops.operations import DeskopsOperations


class AtomsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        registry_path = default_registry_path(root)
        operations = DeskopsOperations(root)

        if args.atoms_command == "add-namespace":
            ensure_default_namespaces(registry_path)
            try:
                add_namespace(
                    registry_path,
                    args.namespace,
                    meaning=args.meaning,
                    use_when=args.use_when,
                    do_not_use_when=args.do_not_use_when,
                    examples=list(args.example or []),
                )
            except ValueError as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Added atom tag namespace {args.namespace}")
            print(f"Path: {registry_path}")
            return 0

        if args.atoms_command == "validate":
            try:
                results = operations.validate_atoms(args.doc_id if not getattr(args, "all", False) else None)
                if getattr(args, "all", False):
                    results = _with_domain_checks(results, DomainTree(root).check())
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            invalid = False
            for record in results:
                print(f"Atom: {record['id']}")
                print(f"Path: {record['path']}")
                if record["errors"]:
                    invalid = True
                    for error in record["errors"]:
                        print(f"- {error}")
                else:
                    print("- valid")
            return 1 if invalid else 0

        if args.atoms_command == "create":
            try:
                result = operations.create_atom_from_source(
                    args.doc_id,
                    five_wh_one_plus=args.five_wh_one_plus,
                    title=getattr(args, "title", None),
                    tags=list(args.tag or []),
                    from_pill=getattr(args, "from_pill", None),
                    from_graph=getattr(args, "from_graph", None),
                    from_diagram=getattr(args, "from_diagram", None),
                    graph_path=getattr(args, "graph", None),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Created atom {result.doc_id}")
            print(f"Path: {result.path}")
            print(f"Source kind: {result.source_kind}")
            print(f"Source selector: {result.source_selector}")
            print(f"Source provenance: {result.provenance}")
            return 0

        if args.atoms_command == "delete":
            try:
                record = operations.delete_atom(args.doc_id, force=bool(getattr(args, "force", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Deleted atom {record.doc_id}")
            print(f"Path: {record.path}")
            print(f"Store untracked: {'yes' if record.kind == 'atom-untracked' else 'no'}")
            return 0

        if args.atoms_command == "split":
            try:
                result = operations.split_atom(
                    args.doc_id,
                    into_ids=list(args.into or []),
                    section_flags=list(args.section or []),
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Split atom {result.original_id}")
            print(f"Original path: {result.original_path}")
            for record in result.created:
                print(f"Created atom {record.doc_id} at {record.path}")
            print(f"Original kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            if result.inbound_references:
                print("Inbound references acknowledged:")
                for item in result.inbound_references:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "merge":
            try:
                result = operations.merge_atom(
                    args.doc_id,
                    into_selector=args.into,
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Merged atom {result.source_id} into {result.target_id}")
            print(f"Source path: {result.source_path}")
            print(f"Target path: {result.target_path}")
            print(f"Source kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            print(f"Inbound references rewritten: {len(result.rewritten_references)}")
            if result.rewritten_references:
                for item in result.rewritten_references:
                    print(f"- {item}")
            if result.ambiguities:
                print("Merge ambiguities acknowledged:")
                for item in result.ambiguities:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "reorganize":
            try:
                report = operations.reorganize_atoms(dry_run=bool(getattr(args, "dry_run", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Would move" if report["dry_run"] else "Moved"
            print(f"Folder axis: {report['axis']}")
            if not report["moves"]:
                print("No atoms need to move.")
            for move in report["moves"]:
                print(f"{verb} {move['id']}: {move['from']} -> {move['to']}")
            for error in report["errors"]:
                print(f"Skipped: {error}")
            return 1 if report["errors"] else 0

        if args.atoms_command == "list":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    getattr(args, "format", "text"),
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                getattr(args, "format", "text"),
                lambda _data: _format_atom_list(payloads, axis),
            )

        if args.atoms_command in {"crossroad", "proto", "type", "tree"}:
            return self._run_domain_tree(args, root)

        if args.atoms_command == "show":
            args.command = "show"
            args.subject = "atom"
            from deskops.cli.commands.operations import OperationsCLI
            return OperationsCLI().run(args)

        return 1

    def _run_domain_tree(self, args: Any, root: Path) -> int:
        tree = DomainTree(root)
        try:
            if args.atoms_command == "crossroad":
                created = tree.create_crossroad(args.path, title=args.title, content=args.content)
                print(f"Created crossroad {created.doc_id}")
                print(f"Path: {created.path}")
                return 0
            if args.atoms_command == "proto":
                created = tree.create_protoatom(
                    args.doc_id, title=args.title, content=args.content, tags=list(args.tag or [])
                )
                print(f"Created protoatom {created.doc_id}")
                print(f"Path: {created.path}")
                return 0
            if args.atoms_command == "type":
                typed = tree.type_protoatom(
                    args.doc_id,
                    model_name=args.model,
                    doc_id=args.new_id,
                    content_field=args.content_field,
                    data=json.loads(args.data) if args.data else {},
                )
                print(f"Typed protoatom {typed.protoatom_id} as {typed.model} {typed.doc_id}")
                print(f"Path: {typed.path}")
                print(f"Protoatom kept as redirect stub: {typed.protoatom_path}")
                return 0
            report = tree.tree()
        except (FileNotFoundError, FileExistsError, ValueError, RuntimeError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )
        return render(
            report,
            getattr(args, "format", "text"),
            _format_tree,
        )


def _with_domain_checks(results: list[dict[str, Any]], domain: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add domain-tree errors to atom records and append crossroad and protoatom records."""
    merged = [dict(record, errors=list(record["errors"])) for record in results]
    by_path = {record["path"]: record for record in merged}
    for record in domain:
        if record["path"] in by_path:
            by_path[record["path"]]["errors"].extend(record["errors"])
        else:
            merged.append(record)
    return merged


def _format_atom_list(payloads: list[dict[str, Any]], axis: str | None) -> str:
    lines: list[str] = []
    for payload in payloads:
        label = payload.get("title") or payload["id"]
        if axis:
            values = ",".join(payload.get("axis_values") or []) or "-"
            lines.append(f"{payload['id']} | {label} | {axis}:{values}")
        else:
            lines.append(f"{payload['id']} | {label}")
    return "\n".join(lines)


def _format_tree(report: dict[str, Any]) -> str:
    lines: list[str] = []

    def walk(node: dict[str, Any], depth: int) -> None:
        pad = "  " * depth
        lines.append(f"{pad}{node['path']} — {node['title']}")
        for item in node["items"]:
            target = f" -> {item['typed_as']}" if item.get("typed_as") else ""
            lines.append(f"{pad}  · {item['id']}  {item['title']}{target}")
        for child in node["children"]:
            walk(child, depth + 1)

    for node in report["roots"]:
        walk(node, 0)
    if report["orphans"]:
        lines.append("Without a written crossroad:")
        for item in report["orphans"]:
            lines.append(f"  · {item['id']} (domain:{item['domain']})")
    if report["unplaced"]:
        lines.append(f"Without a domain tag: {len(report['unplaced'])} document(s)")
    return "\n".join(lines)

FILE:deskops/cli/commands/doctor.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.doctor_findings import REGISTER, Findings, invalid_task_findings, moved_documents, print_findings, read_store_check, seed_drift
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import desk_seed_text
from deskops.workspace import seed_desk


_IGNORED_MODELED_NAMES = {
    "Board.md",
    "pills.md",
    "execution.md",
    "testing.md",
    "closeout.md",
    "phase.md",
    "README.md",
    "tag-namespaces.yaml",
}


class DoctorCLI:
    """Report what breaks the desk (errors) apart from what only moved (alerts).

    Exit 1 only when an error is left; alerts alone exit 0 and are always printed. `--repair`
    acts on errors only: an alert is not damage, it is registered with `deskops desk update
    --apply`. See `deskops.doctor_findings`.
    """

    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        repair = getattr(args, "repair", False)
        inspection = inspect_desk(root)
        desk_dir = root / "desk"
        if inspection.classification == "absent" and not (desk_dir / "config.json").exists():
            print(f"No desk at {root}: this repository has no desk/ (run deskops init to create one).")
            return 0
        findings = Findings()
        self._check_structure(root, desk_dir, inspection, repair, findings)
        if desk_dir.exists():
            self._check_documents(root, desk_dir, repair, findings)
            self._check_managed_seeds(root, findings)
            self._check_models(root, repair, findings)
        return self._report(findings, repair)

    def _check_structure(self, root: Path, desk_dir: Path, inspection, repair: bool, findings: Findings) -> None:
        missing = [rel for rel, exists in (
            ("desk/tasks/Board.md", (desk_dir / "tasks" / "Board.md").exists()),
            ("desk/drawer/", (desk_dir / "drawer").exists()),
            ("desk/rituals/phase.md", (desk_dir / "rituals" / "phase.md").exists()),
        ) if desk_dir.exists() and not exists]
        if missing and repair:
            seed_desk(root)
            findings.fixed.append(f"Scaffolded missing desk/ structure: {', '.join(missing)}")
        elif missing:
            findings.errors.append(f"Missing desk structure: {', '.join(missing)}")
        if inspection.classification == "legacy":
            surfaces = [*inspection.missing_surfaces, *inspection.malformed_surfaces]
            findings.errors.append(
                "Legacy desk detected: "
                + (", ".join(surfaces) if surfaces else "board/task/pill surfaces need explicit migration")
                + ". Migrate with: deskops desk migrate --root <repo>."
            )

    def _check_documents(self, root: Path, desk_dir: Path, repair: bool, findings: Findings) -> None:
        findings.errors += invalid_task_findings(root)
        payload = self._store_check(root, findings)
        if payload is None:
            return
        docs = read_store_check(root, payload)
        modeled = {p.resolve() for p in modeled_desk_markdown_docs(root, desk_dir) if p.name not in _IGNORED_MODELED_NAMES}
        untracked = sorted(p for p in modeled if p not in docs.tracked)
        moves, gone, untracked = moved_documents(root, docs.missing, untracked)
        findings.alerts += [f"Edited: {d}" for d in docs.changed]
        findings.alerts += [f"Moved: {m}" for m in moves]
        findings.alerts += [f"Not tracked yet: {p.relative_to(root)}" for p in untracked]
        findings.alerts += docs.store_alerts
        findings.errors += [f"Tracked document is gone: {p.relative_to(root)} (restore it, or untrack it with {REGISTER})" for p in gone]
        findings.errors += [f"Invalid desk document: {d}" for d in docs.unknown]
        findings.errors += docs.store_errors
        findings.errors += self._unreadable(root, docs.by_model)

    def _check_managed_seeds(self, root: Path, findings: Findings) -> None:
        """The managed seeds (the lifecycle graph and its rules) whose desk copy differs from the
        package: what ``deskops desk update --apply`` would rewrite, by the same comparison
        (``seed_desk(apply=False, restore_managed=True)``). One finding per file; an error when a
        lifecycle edge's transition fields differ (``advance`` refuses it), else an alert (b1)."""
        try:
            rewritten = seed_desk(root, apply=False, restore_managed=True).rewritten_paths
        except Exception as exc:
            findings.errors.append(f"Could not compare the desk's managed seeds with the deskops package: {exc}")
            return
        for path in rewritten:
            rel = path.resolve().relative_to(root).as_posix()
            drift = seed_drift(rel, desk_seed_text(root.name, rel), path.read_text(encoding="utf-8"))
            (findings.errors if drift.governs_transition else findings.alerts).append(drift.line)

    def _store_check(self, root: Path, findings: Findings) -> dict | None:
        result = subprocess.run(
            [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb"), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not result.stdout:
            if result.returncode != 0:
                first = result.stderr.strip().split("\n")[0]
                findings.errors.append(f"SLDB store check crashed (likely malformed documents): {first}")
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            findings.errors.append("Failed to parse SLDB store check output.")
            return None

    def _unreadable(self, root: Path, by_model: list[tuple[str | None, Path]]) -> list[str]:
        """Documents whose model cannot read their own content: an edit through the model erases it."""
        out = []
        for model_name, doc_path in by_model:
            model = _resolve_deskops_model(model_name)
            if model is None or not doc_path.exists():
                continue
            if fields := is_unreadable_by_model(model, doc_path.read_text(encoding="utf-8")):
                out.append(
                    f"Model cannot read its own document: {doc_path.relative_to(root)} ({model_name}: {', '.join(fields)}). "
                    "Any edit through the model renders these fields back empty; rebuild the text through sldb and retrack it."
                )
        return out

    def _check_models(self, root: Path, repair: bool, findings: Findings) -> None:
        store_dir = root / ".sldb"
        if not store_dir.exists():
            return
        try:
            registered = SLDBBootstrap()._registered_model_names(store_dir)
        except Exception:
            findings.errors.append("Could not read the local .sldb store index; unregistered-model check skipped.")
            return
        if not (unregistered := sorted(name for name in MODEL_REFS if name not in registered)):
            return
        if repair and self._register_models(root):
            findings.fixed.append(f"Registered missing models: {', '.join(unregistered)}")
        else:
            findings.errors.append(f"Unregistered models: {', '.join(unregistered)}. Register them with {REGISTER}.")

    def _register_models(self, root: Path) -> bool:
        try:
            return SLDBBootstrap().init_local_store(root) == 0
        except Exception:
            return False

    def _report(self, findings: Findings, repair: bool) -> int:
        if not findings.errors and not findings.alerts and not findings.fixed:
            print("Desk is healthy. No issues found.")
            return 0
        print_findings(findings, repair=repair)
        if not findings.errors:
            print(f"\nDesk is healthy{f', with {len(findings.alerts)} alert(s)' if findings.alerts else ''}.")
            return 0
        return 1


def _resolve_deskops_model(name: str | None) -> type | None:
    """The deskops model registered under `name`, or None when it is not ours."""
    if not name:
        return None
    import deskops.models as models

    candidate = getattr(models, name, None)
    return candidate if isinstance(candidate, type) else None

FILE:deskops/models/atom.py
from enum import StrEnum
import re
from typing import Annotated

from pydantic import Field, field_validator

from sldb import StructuredNLDoc

from .crossroad import check_domain_path

ATOM_TAG_PATTERN = r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$"
DOMAIN_NAMESPACE = "domain"
_ATOM_TAG = re.compile(ATOM_TAG_PATTERN)


class AtomQuestion(StrEnum):
    WHAT = "what"
    WHY = "why"
    HOW = "how"
    HOW_NOT = "how_not"
    WHEN = "when"
    WHERE = "where"
    FOR_WHOM = "for_whom"


AtomTag = Annotated[
    str,
    Field(
        pattern=ATOM_TAG_PATTERN,
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


def check_slug_id(value: object, prefix: str, label: str) -> object:
    """``<prefix><slug>``, where the slug is already in slug form. Anything else is left to pydantic."""
    if not isinstance(value, str):
        return value
    # Lazy: doc_access imports the models, and the slug form is defined once, there.
    from deskops.doc_access import slugify

    slug = value.removeprefix(prefix)
    if not value.startswith(prefix) or not slug or slug != slugify(slug):
        raise ValueError(f"{label} id must follow slug convention {prefix}<slug>: {value}")
    return value


def check_atom_tags(tags: object) -> object:
    """Each tag is ``namespace:value``; each ``domain:`` value is a domain path. Anything that is
    not a list of strings is left to pydantic."""
    if not isinstance(tags, list):
        return tags
    for tag in tags:
        if not isinstance(tag, str):
            continue
        if _ATOM_TAG.fullmatch(tag) is None:
            raise ValueError(f"Invalid atom tag '{tag}'. Expected namespace:value.")
        namespace, value = tag.split(":", 1)
        if namespace == DOMAIN_NAMESPACE:
            check_domain_path(value)
    return tags


def domain_paths(tags: list[str]) -> list[str]:
    """Values of the ``domain:`` tags, in order."""
    values: list[str] = []
    for tag in tags:
        match = _ATOM_TAG.fullmatch(str(tag))
        if match is not None and str(tag).split(":", 1)[0] == DOMAIN_NAMESPACE:
            values.append(str(tag).split(":", 1)[1])
    return values


class AtomDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "atom-{slug}",
        "status_default": None,
        "tags": ["system:deskops", "topic:atoms"],
    }
    __semantics__ = {
        "type": ["knowledge", "atom"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
five_wh_one_plus: ⸢rev•five_wh_one_plus⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Answer

⸢rev•answer⸥
""".strip()

    id: str = Field(
        description="Stable, unique atom identifier, conventionally 'atom-<slug>'."
    )
    title: str = Field(
        description="Short, descriptive title for the atomic knowledge unit."
    )
    five_wh_one_plus: AtomQuestion = Field(
        description=(
            "The single 5WH1+ question this atom answers: one of "
            "what, why, how, how_not, when, where, for_whom."
        )
    )
    answer: str = Field(
        description=(
            "The curated raw answer to the selected 5WH1+ question, written as "
            "one stable knowledge unit."
        )
    )
    tags: list[AtomTag] = Field(
        default_factory=list,
        description=(
            "Namespaced semantic tags used for retrieval and grouping, each in the "
            "form namespace:value (e.g. system:deskops, topic:templates). Tags do "
            "not encode lifecycle, relations, evidence, or materialization."
        ),
    )
    provenance: str | None = Field(
        default=None,
        description=(
            "Optional URL or path to the authoritative source of this atom's "
            "knowledge. Used for traceability and provenance tracking."
        ),
    )

    @field_validator("id", mode="before")
    @classmethod
    def _id_follows_the_slug_convention(cls, value: object) -> object:
        return check_slug_id(value, "atom-", "atom")

    @field_validator("tags", mode="before")
    @classmethod
    def _tags_are_namespaced(cls, tags: object) -> object:
        return check_atom_tags(tags)

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/` (`templates/` for the desk's own files,
#   `lifecycle/` for the lifecycle graph);
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# A desk's own files are `if_missing` seeds: a desk that already has the file keeps its own.
# The task lifecycle graph (CC31, GO09) is `managed`: the three RelationTypeDoc and the three
# RelationDoc under `desk/lifecycle/` are deskops' documents, written from `lifecycle/` and
# rewritten whenever a desk's copy differs (`deskops desk update --apply` reports it). Each
# RelationDoc carries the transition's effects in `attributes`: `sets` (the fields written on
# the task when the edge is taken) and `terminal` (the task closes). The activation gate of
# each factory task type (CC32, GO06/GO08) is a `managed` RuleDoc too, written from `rules/`
# to `desk/lifecycle/rule-activation-<type>.md`: `on_transition` over `ritual-execution`, with
# subject `model <= <TypeDoc>` so a desk subtype inherits it, it requires the review receipts
# the type asks for (accepted and intact) and the task's dependencies closed; sldb evaluates
# it when `deskops advance` asks for the holding edges. The closeout gate of each factory type
# (CC33b) is the same kind of managed RuleDoc, written from `rules/` to
# `desk/lifecycle/rule-closeout-<type>.md`: `on_transition` over `ritual-closeout`, it requires
# the evidence receipts `deskops closeout verify` writes (kinds in `rules/closeout-evidence.yaml`),
# accepted and intact, and `deskops closeout commit` evaluates it; the two
# `rule-closeout-alert-*.md` are `on_write` alerts over the task's own fields. The `include` rules say
# which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`): the lifecycle documents, the rules,
# the three lifecycle rituals by their ids (`RitualDoc:ritual-<x>`, what the graph's edges
# name), the seeded Board (`BoardDoc:Board`) and phase ritual (`RitualDoc:ritual-phase`), which
# the selectors resolve through the store (CC35b d1), and one glob per desk folder. The tasks
# are tracked by their own paths.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: templates/config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: templates/contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: templates/rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: templates/rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: templates/rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: templates/rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: templates/drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: templates/atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
- path: desk/lifecycle/type-task_activates.md
  mode: managed
  file: lifecycle/type-task_activates.md
- path: desk/lifecycle/type-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/type-task_hands_to_closeout.md
- path: desk/lifecycle/type-task_completes.md
  mode: managed
  file: lifecycle/type-task_completes.md
- path: desk/lifecycle/execution-task_activates.md
  mode: managed
  file: lifecycle/execution-task_activates.md
- path: desk/lifecycle/testing-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/testing-task_hands_to_closeout.md
- path: desk/lifecycle/closeout-task_completes.md
  mode: managed
  file: lifecycle/closeout-task_completes.md
- path: desk/lifecycle/rule-activation-task-code.md
  mode: managed
  file: rules/rule-activation-task-code.md
- path: desk/lifecycle/rule-activation-task-docs.md
  mode: managed
  file: rules/rule-activation-task-docs.md
- path: desk/lifecycle/rule-activation-task-debug.md
  mode: managed
  file: rules/rule-activation-task-debug.md
- path: desk/lifecycle/rule-activation-task-refactor.md
  mode: managed
  file: rules/rule-activation-task-refactor.md
- path: desk/lifecycle/rule-activation-task-decision.md
  mode: managed
  file: rules/rule-activation-task-decision.md
- path: desk/lifecycle/rule-activation-task-aggregate.md
  mode: managed
  file: rules/rule-activation-task-aggregate.md
- path: desk/lifecycle/rule-activation-task-external.md
  mode: managed
  file: rules/rule-activation-task-external.md
- path: desk/lifecycle/rule-closeout-task-code.md
  mode: managed
  file: rules/rule-closeout-task-code.md
- path: desk/lifecycle/rule-closeout-task-docs.md
  mode: managed
  file: rules/rule-closeout-task-docs.md
- path: desk/lifecycle/rule-closeout-task-debug.md
  mode: managed
  file: rules/rule-closeout-task-debug.md
- path: desk/lifecycle/rule-closeout-task-refactor.md
  mode: managed
  file: rules/rule-closeout-task-refactor.md
- path: desk/lifecycle/rule-closeout-task-decision.md
  mode: managed
  file: rules/rule-closeout-task-decision.md
- path: desk/lifecycle/rule-closeout-task-aggregate.md
  mode: managed
  file: rules/rule-closeout-task-aggregate.md
- path: desk/lifecycle/rule-closeout-task-external.md
  mode: managed
  file: rules/rule-closeout-task-external.md
- path: desk/lifecycle/rule-closeout-alert-implicit-code.md
  mode: managed
  file: rules/rule-closeout-alert-implicit-code.md
- path: desk/lifecycle/rule-closeout-alert-pill-graduation.md
  mode: managed
  file: rules/rule-closeout-alert-pill-graduation.md
include:
- model: RelationTypeDoc
  glob: desk/lifecycle/type-*.md
- model: RelationDoc
  paths:
  - desk/lifecycle/execution-task_activates.md
  - desk/lifecycle/testing-task_hands_to_closeout.md
  - desk/lifecycle/closeout-task_completes.md
- model: RuleDoc
  glob: desk/lifecycle/rule-activation-*.md
- model: RuleDoc
  glob: desk/lifecycle/rule-closeout-*.md
- model: BoardDoc
  paths:
  - desk/tasks/Board.md
- model: RitualDoc
  paths:
  - path: desk/rituals/phase.md
    name: ritual-phase
  - path: desk/rituals/execution.md
    name: ritual-execution
  - path: desk/rituals/testing.md
    name: ritual-testing
  - path: desk/rituals/closeout.md
    name: ritual-closeout
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Closeout rules (CC33b): the closeout gate of each factory task type is a `RuleDoc` seed, `deskops/data/rules/rule-closeout-task-<type>.md`, written as a managed seed to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`, glob `rule-closeout-*.md`; a second `--apply` changes nothing). Each is `on_transition`, `severity: error`, `where current_node = "ritual-closeout"` (the source of `task_completes`), subject `model <= <TypeDoc>`, and asks for the evidence receipts of CC33a, accepted and intact: `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")` per kind, `atom|materialization` as an `or` of two. `task.refactor` adds the `goldens` review receipt (`deskops review record --kind goldens`) to the `task.code` rule its family gets; `task.aggregate` asks only for `commit` (no `children` field yet). The kinds per type are data, `deskops/data/rules/closeout-evidence.yaml`, which `deskops closeout verify` and `deskops add task` read (a desk subtype reads its nearest factory ancestor's entry); `tests/test_closeout_rules.py` checks the rules against it. Two `on_write` alert rules cover task fields: `rule-closeout-alert-implicit-code` and `rule-closeout-alert-pill-graduation`.
- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
- Scion autonomy contract (task-scion-autonomy-coordinator-contract): runtime templates add independent `--mode tester`, strict `--context-file` and separate task-data `--task-root`. Coordinators reconcile their own children and Scion activity before selecting work, prepare missing reviews, require independent passing tests, and verify scoped closeout before continuing through phases. Child identities use the full canonical SLDB contract; native label descriptors fit Scion ASCII/63-character limits. RunDocs record immutable launch intent, and the supervisor may mutate modeled workflow through CLIs while implementation stays with executors.
- `deskops review record --kind preflight|bundle --operator <name>` (main en verde, decisión B del coordinador de proyecto con las condiciones del overlord): a desk without a model (CI scenarios, the quickstart) records those receipts by hand. `--operator` is required for both kinds (without it nothing is written); the receipt keeps `engine: human`, names the operator as `actor` and says `no model available` in its title and summary. Real desk tasks still get them from `deskops review preflight|bundle`.
- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).
- `deskops closeout resolved-by --task <id> --reason "..." --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] [--paths ...] [--message ...]` closes a task whose work already entered the history (for example through a PR) before its closeout (`ClosureService.close_resolved_by`). It does not ask for an atom per changed file: at least one `--ref` must be a commit that is HEAD or an ancestor of the `--root` repository, the other refs may be ancestor commits or http(s) URLs, and at least one `--test` is required, each one accepted by the tests gate for the task's `files`. Any ref or test that does not resolve, or a blank reason, is refused with exit 1 and writes nothing. It makes one closing commit with `Task-Id`, `Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and one `Closeout-Test` per test, marks the task `resolved` with `resolved-by` in its history, takes it off the Board and records the index entry with `mode: resolved-by` (`tests/test_closeout_resolved_by.py`).

### Changed

- `deskops view board|task` from sldb ViewDocs (CC34): the views are the seed ViewDocs `deskops/data/views/board.md` and `task.md` (only in the package, DA4), tracked as `ViewDoc` in the deskops repo's own store (`.sldb/store.yaml`, written with `sldb stores declare --write`), evaluated by `sldb.api.run_view` and projected to the unchanged contract of `docs/deskops-ui.md` by `deskops.cli.commands.view.project`, a public function graph_ui calls in process on what `GET /views/<view>` of `sldb serve` returns. The task view's `revision` is now the ETag of the view (GD25): it moves whenever the task, the Board, a pill or an atom the view read changes; the key and its optimistic guard are the same. What the ViewDoc model does not express yet is added by the CLI from the read operations that already existed (gates from `show_task`, closeout from a read-only `verify_task_closeout`, `next` and the columns' phase from the lifecycle spec, inherited fields from `resolve_task_payload`; sldb hypotheses H1-H8), and drawer and inbox still read the desk's files (H10: those folders are not tracked in a desk's store). The agents view moved to `deskops/runtime/desk_agents.py`. `deskops/services/desk_view.py` (`DeskView`, `task_revision`, `note_revision`) and the private aliases `_read_doc`, `_resolve_glob`, `_registered_repositories` and `_repository_root` of `DeskopsOperations` are gone; an error that stops a view is the envelope type `ViewError` (was `DeskViewError`). Until sldb resolves a ViewDoc of a linked store (H9), `deskops view board|task` works only on a desk whose own store tracks the ViewDocs (the deskops repo); elsewhere it exits 1 with `Unknown view: <view>`. JSON goldens of the four views are in `tests/fixtures/golden/output/view_*.json` (`tests/test_view_goldens.py`, `tests/test_view.py`).
- `deskops desk replace` writes through `sldb.api.replace_text` (CC35d a4, GD27) inside the desk transaction (`doc_access.desk_transaction`), instead of writing the bytes and untracking and re-tracking the document itself. deskops keeps which files the verb reaches (modeled subjects are still pointed at `deskops edit`) and the count guard with its message (`Refusing to replace in <path>: found N occurrence(s) of --old, expected M. The file is unchanged.`), checked before sldb is called. A plain file (a drawer note, an issue body, `tag-namespaces.yaml`) is rewritten as before. A store-tracked file (a role prompt) is now validated under its model and the store's `on_write` rules before it is rewritten and tracked again, and a replacement that breaks it is refused with `Refusing to replace in <path>: <sldb error> The file is unchanged.` (exit 1), the transaction rolled back. A desk without a store still writes the file directly. The rest of CC35d (tag namespaces, the domain tree, `tag_folder`) waits on sldb (H1-H3) (`tests/test_desk_replace.py`).
- `deskops closeout commit` writes no receipt and no longer gates on verify's result: it evaluates the task type's closeout rule on the receipts `deskops closeout verify` wrote (task read at `ritual-closeout`). A blocked commit prints `Closeout gate blocked <task>; the closing commit was not made.`, the declared/found line and alerts of a read-only verify, one `- error: [rules/rule-closeout-<type>] ...` line per finding and `Run 'deskops closeout verify --task <task>' ...`; a task the store does not track cannot be evaluated and is blocked with that reason. The `task_completes` edge condition is `status = "ready_for_testing"` (the `has(closeout_evidence_verified)` fact is gone), so `deskops show task`, `next` and `advance` show the rule's findings on that gate. Editing a contract field after verify leaves the receipts `changed` and blocks again.
- `deskops closeout verify`: the task's `closeout_evidence` only adds kinds to its type's (DA5): an added kind is verified and gets its receipt, and a failure is the alert `added_closeout_evidence_not_verified` instead of a blocking finding; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`. `goldens` is read by the rule from the review receipt, not produced by verify, and `children` is no longer declared, so `closeout_evidence_not_verifiable` is gone. When the atom|materialization gate passes without a linking document (exempt desk, follow-up only, skill guard test) verify writes an accepted `atom` receipt with `value: exempt: <why>` (b3). The `closeout_evidence_not_declared` alert moved to the `rule-closeout-alert-implicit-code` rule.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
- `deskops graph neighbors|missing|reflect` and `deskops drift check` read sldb's project graph of the desk (CC33c, GD21: `sldb.api.edges.project_graph.ProjectGraph` with the configuration of `deskops/graph/desk_graph.py`) instead of a snapshot deskops built and read back. Without `--graph`, `graph neighbors` and `graph reflect` no longer need a prior `graph build` and no longer read `.sldb/runtime/graphs/deskops.kg.json` or the legacy `.sldb/runtime/knowledge_graph.kg.json`; `drift check` reads the graph's edges and its dangling edge targets whether or not a snapshot was built. `--graph <path>` still reads that graph file (`deskops/graph/view.py`, `read_graph_file`). `deskops graph build` still writes the KGDB GraphSnapshot and its NetworkX sibling, unchanged, from the same graph (`deskops/graph/export.py`). `deskops/graph/snapshot.py` is gone (its runtime-path fallback and `read_graph_neighbors` with it), and the atom-reference check of `drift check` reads the frontmatter of the project graph's documents under `desk/` and `docs/` instead of an `rglob` (`grep rglob deskops/graph/` is empty). `graph neighbors` and `graph missing` were compared with the frozen v1 extractors over a copy of the real desk (619 nodes, 296 edges, the same `(source, target, role)` sets and the same missing findings), and `tests/graph_oracle_v1/` was then removed; `tests/closeout_graph_oracle.py` keeps only the lifecycle-transitions oracle.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. CC33c lo decidió (a4): el grafo de proyecto de sldb sigue sin nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json`, así que la excepción queda. Tests en `tests/test_graph_missing_existing_files.py`.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or `deferred`, what a drawer task holds, when `current_node` is empty); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or, when `current_node` is empty (a task outside the lifecycle), `deferred` (a drawer task) or `resolved`/`closed`/`done`/`complete` (a task resolved before the lifecycle, what `closeout retire` removes)); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- Selectors of tracked desk documents resolve through `sldb.api.select_documents` (CC35b, GD23). `doc_access.resolve_document` asks the store twice, in order: by name (`prefix`, where an exact name wins over the one prefix match) under the directory's pattern, then, only if that found nothing, by file name (`path_glob` of `<selector>*.md`), so a ritual tracked as `ritual-execution` in `desk/rituals/execution.md` resolves as `ritual-execution` and as `execution`; an ambiguous query stops there. `resolve_glob`, `resolve_artifact_selector[_multi]`, `resolve_ritual_selector`, `registered_repositories` and the task and pill lookups of `deskops review` use it; the messages are the same (`No <what> file found for selector '<s>'`, `Ambiguous <what> selector '<s>': <paths relative to desk/>`), the ambiguity candidates being the rows sldb names. Gone: `_tracked_task_paths` (which read `.sldb/core/documents/` directly) and the frontmatter-id fallbacks of reviews and rituals (`frontmatter_id`): a legacy task resolves by the `TaskDoc` model family, a review and a ritual by the name the store tracks them by. A file on a tracked surface that the store does not track no longer resolves. The drawer and `desk/issues`, which the store does not track, and a desk without a store keep the disk rule of `desk_paths.resolve_selector` (marked `CC35b-a3`); the `operations.py` aliases graph_ui calls are marked `CC34`. `resolve_artifact_selector_multi` tries its directories in order (an active pill before a drawer pill of the same selector) instead of one candidate set across them. The desk declaration's `include` now names the seeded Board (`desk/tasks/Board.md` as `BoardDoc:Board`) and phase ritual (`desk/rituals/phase.md` as `RitualDoc:ritual-phase`), so `deskops init` and `deskops desk update --apply` track them and a new desk's `deskops edit board Board` resolves (CC35b d1); the Board seed keeps `track: false`.
- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- `__activation_receipts__` and `task_type_activation_receipts` are gone from `deskops/models/task_types.py`: the receipts a type requires live only in its activation `RuleDoc` (CC32). `ReviewDoc`'s docstring says what sldb does with `subject` now that GO07 is in (pins it on save, computes `anchor_state` on read); the model is unchanged. The tests that activate a task write its receipts first with `tests/activation_receipts.py` (accepted and pinned through `sldb.api.transaction`).
- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.
- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).

### Fixed

- `deskops desk update --apply` migrates a task with a non-terminal status and an empty history (`active`, `ready_for_testing`, `blocked`..., left by desks migrated before CC31) instead of listing it as not migratable and skipping every other repair (task.debug of non-terminal tasks, decision of the overlord, 2026-11-11). `legacy_state_migration` had no row for it and returned `None`. It now gives `status draft` and, when `current_node` is set and is not the entry node, the entry node `ritual-execution` (an empty node stays empty); a status is terminal when it is `superseded`, a `CLOSEOUT_STATES` key, a `LEGACY_RESOLVED_STATUSES` or a `DRAWER_STATUSES` status. The task's `summary` gets the line `Migrada a draft por deskops desk update: estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).` in front of its previous text, on one line. The report prints `<file>: status <before> -> draft` and `<file>: current_node <before> -> ritual-execution` when the node moves; a second run changes nothing, and doctor points the task to `deskops desk update --apply`. A non-empty history with an incoherent status still waits for its owner (`tests/test_legacy_task_states.py`, golden `desk_update_nonterminal_migration.text`).

- Tasks left by desks migrated before CC31 with a terminal or drawer status, an empty history and `current_node: ritual-execution` (shared_llm-gateway, the Chatbot_Infra kit, Governance, labchile) no longer break the desk (task.debug of legacy states). `deskops desk update` migrates them by a table (`superseded`: `history [superseded]`; `closed`, `resolved`, `done`, `complete`, `cancelled`, `deferred`, `candidate`: `current_node ''`), dry-run by default and written with `--apply` before the models are registered, one `<file>: <field> <before> -> <after>` line per field; the write goes to the frontmatter and is validated with `TaskDoc`, and a second run changes nothing. Any other task the model rejects is reported with the validator's text and a fixed suggestion, never written, and `--apply` exits 1 while one remains. `desk update` no longer raises when `sldb stores check` cannot read the store because of an invalid task (sldb stops at the first invalid document): it reports it and skips every repair but the migration (the scaffold re-tracks the lifecycle graph too); a store check without JSON and without an invalid task is still an environment error (exit 3). `deskops doctor` reports each invalid task as an error (file, validator text, fix) and runs every other check. `cancelled` joins `LEGACY_RESOLVED_STATUSES`. `deskops closeout retire` reads the task's frontmatter instead of the model and also retires `cancelled`, and `superseded`, `deferred` or `candidate` with an empty history (and `superseded` with only `history [superseded]`, what the migration leaves); with a store, it refuses while another task is invalid (sldb rebuilds every task when one is untracked). `deskops closeout supersede` closes a task its model rejects (for example a `draft` after `task_hands_to_closeout`) by reading and writing its frontmatter, with the same commit and trailers and the same wait. The suggestion for an undecided task uses the real grammar (`deskops closeout supersede --task <id> --reason ... --ref ...`, `deskops closeout resolved-by --task <id> --reason ... --ref <commit> --test <file>`). Its help changes only in that list of statuses (`tests/test_legacy_task_states.py`, `tests/test_closeout.py`, `tests/test_task_lifecycle_validator.py`).
- A desk whose lifecycle seeds predate CC31 (edges with `attributes: {}`, as the Chatbot_Infra kit has) is reported and no longer fails with a pydantic error (task.debug, nota de inbox 5106e3f8). `deskops doctor` compares the desk's managed seeds with the package by the comparison `deskops desk update --apply` makes (`seed_desk(apply=False, restore_managed=True)`) and reports each copy that differs: `lifecycle seed out of date: desk/lifecycle/<file> differs from the deskops package (<top-level frontmatter keys, without the `sldb:` write provenance>). Fix: deskops desk update --apply`, an error when a lifecycle edge's transition fields differ (`source_id`, `target_id`, `relation_type`, `condition`, `attributes`), an alert otherwise (rules, body or notes). `deskops advance` compares the edge it is about to apply with the package's lifecycle table (`lifecycle_table()`, cached): an edge with another `relation_type`, target or `attributes.sets.status` fails before any effect is applied with `Error: Cannot advance <task> via <relation_type>: the edge desk/lifecycle/<file> does not set status <expected> (attributes.sets.status is <seen|missing>). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.` (exit 1, the task unchanged) instead of `Validation error: ... lifecycle is inconsistent` (`tests/test_lifecycle_seed_drift.py`).
- `deskops review status` preserves current accepted/rejected dispositions, selects matching exact-input receipts before applying verdict priority, and groups pinned task subjects by task id. Older receipts no longer mask a current acceptance or turn a changed input into a technical failure.

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

### Removed

- `__closeout_evidence__` on the task type classes, the `closeout_evidence_verified` and `pill_graduation_verified` facts, `TasksService.add_closeout_facts`, `ClosureService.has_verified_task_closeout_evidence` and `has_verified_task_pill_graduation`, `task_type_closeout_evidence` and `NOT_YET_VERIFIABLE_EVIDENCE` (CC33b).

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep de require_domain_parents, _domain_errors y validate_atom_tag_namespaces en deskops/ vacío
- domain:a.b sin crossroad falla igual; goldens idénticos
- desk update --apply idempotente con la declaración de tags
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

