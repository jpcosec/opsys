FILE:desk/tasks/task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas.md
---
sldb:
  by: agent
  at: '2026-11-11T23:36:02Z'
  authority: generated
  via: create_document
id: task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas
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
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/identity.py
- deskops/cli/commands/closeout.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-c-digo-vive-en-otro-repo.md
---

# closeout resolved-by acepta referencias calificadas por repo (<repo>:<sha>, <repo>:<ruta de test>) verificadas contra un repo registrado, para cerrar una task.code cuyo código vive en otro repo

## Rationale

_Explain why this task exists or the business driver behind it._

Caso de AntonIA (inbox a79fe2d6): una task.code del desk de Governance cuyo código entró en Chatbot_Infra no puede cerrar, porque resolved-by exige un commit ancestro del repo del desk y un test .py de ese repo. La vía actual (tarea espejo en el repo del código, supersede en el desk coordinador) duplica tareas y pierde la traza.

## Goal

_Describe the concrete result this task must produce._

deskops closeout resolved-by cierra una tarea con --ref <repo>:<sha> y --test <repo>:<ruta>, donde <repo> es un repo del registro del ecosistema (deskops repo register), verificando en ese repo que el commit es ancestro de su HEAD y que el test existe y es un archivo de tests; con el mismo commit de cierre y los mismos trailers, que guardan la referencia calificada tal cual.

## Scope

_State what is in scope and what is out of scope._

En alcance: el parseo y la verificación de referencias calificadas en las compuertas de resolved-by (deskops/services/closeout_gates.py, deskops/services/closure.py), la resolución del repo por el registro (deskops/identity.py), la ayuda del CLI, tests, docs y CHANGELOG. Fuera: closeout verify y closeout commit (siguen exigiendo evidencia local); la sugerencia de task.external en add task o desk update (opción a de la nota, queda en el drawer); supersede (ya acepta una ruta o un commit local).

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox a79fe2d6 (AntonIA, 2026-11-11), opción b. Decisión del coordinador (revisable): se hace la opción b acotada a resolved-by; la opción a (sugerir task.external) queda en el drawer.

ESTADO ACTUAL: ClosureService.close_resolved_by exige al menos un --ref que sea un commit HEAD o ancestro del repo del desk (CloseoutGates.reference_points_to_commit, git rev-parse y merge-base con cwd en la raíz del desk) y al menos un --test que sea un .py existente bajo un directorio tests del repo del desk (reference_points_to_test). El registro de repos del ecosistema está en deskops/identity.py (load_repository_registry, RegisteredRepository con su raíz resuelta).

CAMBIO (c1-c5):
c1: una referencia calificada tiene la forma <repo-id>:<valor>, donde <repo-id> es la identidad de un repo del registro del ecosistema. Una referencia sin prefijo, o con un prefijo que no es un repo registrado, se trata como hoy. Una URL http(s) sigue siendo URL.
c2: --ref <repo-id>:<sha> cuenta como el commit exigido si, en la raíz registrada de ese repo, el sha resuelve a un commit que es ancestro de su HEAD (las mismas reglas que hoy: hex en minúscula, sin nombres simbólicos). Si la raíz registrada no existe en la máquina, se rechaza con un error que nombra el repo y la ruta.
c3: --test <repo-id>:<ruta> cuenta si la ruta existe en la raíz registrada de ese repo, con las mismas reglas que reference_points_to_test (un .py bajo un directorio tests, sin salir de la raíz). Los files de la tarea no amplían los tests de otro repo.
c4: los trailers del commit de cierre guardan cada referencia tal como se escribió (Closeout-Ref: Chatbot_Infra:87671716), y Closeout-Mode sigue siendo resolved-by.
c5: tests con dos repos git en tmp_path, registrados en el registro del ecosistema: cierra con commit y test del otro repo; rechaza un sha que no es ancestro del HEAD del otro repo, un test inexistente, un repo no registrado (se trata como local y falla como hoy) y una raíz registrada que no existe. Docs (operator-manual, sección de cierre) y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y, antes de entregar, la suite completa de a un archivo desde /dev/shm. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: resolved-by con --ref <repo>:<sha> y --test <repo>:<ruta> de otro repo registrado cierra con Closeout-Mode: resolved-by y guarda las referencias calificadas en los trailers
- Tests nuevos de rechazo: sha no ancestro, test inexistente, repo no registrado, raíz registrada ausente
- Los tests existentes de resolved-by y closeout siguen verdes; suite completa de a un archivo en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

c1-c5 hechos, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados; la opción a de la nota queda como ítem de drawer.

FILE:deskops/services/closeout_gates.py
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

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})


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


def order_evidence_kinds(kinds: list[str]) -> list[str]:
    """Deduplicate a declared evidence list in the vocabulary order, keeping the kinds that
    are declared on a type but not in the CLI vocabulary (``children``, ``goldens``) last.
    """
    seen: list[str] = []
    for kind in [*CLOSEOUT_EVIDENCE_VOCABULARY, *kinds]:
        if kind in kinds and kind not in seen:
            seen.append(kind)
    return seen


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
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref, files=files):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
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

    def reference_points_to_test(self, reference: str, files: list[Any] | None = None) -> bool:
        """True only for an existing .py file inside the repository that is a test location.

        After dropping an optional ``::node`` suffix (the node is not validated) and the
        ``pytest <path>`` form, the reference must name an existing file, relative to the
        root, whose suffix is exactly ``.py`` and which resolves inside the root. It counts
        when one of its directories (relative to the root) is named ``tests`` (``tests/``,
        ``runtime/foo/tests/``, ``ops/tests/sub/``) or when its path is declared in
        ``files``, the evaluated TaskDoc's ``files``: they widen where tests may live but
        are not evidence by themselves. Absolute paths, paths that leave the root through
        ``..`` or a symlink, and files under a directory starting with ``.`` or named
        ``site-packages`` or ``node_modules`` (third-party code) are not evidence. Each
        reference is checked on its own; the disk is not walked.
        """
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path_text or path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if not resolved.is_relative_to(self.root):
                continue
            directories = resolved.relative_to(self.root).parts[:-1]
            if any(part.startswith(".") or part in {"site-packages", "node_modules"} for part in directories):
                continue
            if "tests" in directories:
                return True
            for entry in files or []:
                declared = str(entry).strip()
                if declared and not Path(declared).is_absolute() and (self.root / declared).resolve() == resolved:
                    return True
        return False

    def full_commit_sha(self, reference: str) -> str:
        """The full id of a commit reference that passes ``reference_points_to_commit``, else ''."""
        if not self.reference_points_to_commit(reference):
            return ""
        resolved = subprocess.run(
            ["git", "rev-parse", "--verify", f"{reference.strip()}^{{commit}}"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        return resolved.stdout.strip() if resolved.returncode == 0 else ""

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

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The declared-edge graph the closeout link gate reads, built lazily.

        Nodes come from one pass over the repository's document surfaces and file tree,
        tracked documents and schema edges from one read of the sldb index; the declared
        edges of a document are read only when the gate asks about it.
        """
        from deskops.graph.desk_graph import desk_graph

        return CloseoutGraph(desk_graph(self.root))

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


class CloseoutGraph:
    """What the closeout link gate asks of the declared-edge graph.

    The gate needs, for a changed file, the edges leaving its node and the edges a
    materialization points at it, plus the edges that link test files to atoms or
    materializations. Only the materialization documents and the documents the gate asks
    about are read; ``edges_around`` and ``test_link_edges`` return supersets of what the
    gate keeps, in the order a full scan of the sorted edge list would visit them, so the
    gate's own conditions produce the same evidence in the same order.
    """

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        lookup = graph.nodes.lookup
        self.node_ids_by_path = {path: node.id for path, node in lookup.by_path.items()}
        materializations = sorted(
            node_id for node_id in lookup.existing_ids | graph.node_ids() if node_id.startswith("materialization:")
        )
        self.invalid_materializations = {node_id for node_id in materializations if graph.missing_from(node_id)}
        self._materialization_edges_to: dict[str, list[Any]] = {}
        for node_id in materializations:
            for edge in graph.edges_from(node_id):
                self._materialization_edges_to.setdefault(edge.target_id, []).append(edge)

    def node_id(self, relative_path: str) -> str | None:
        return self.node_ids_by_path.get(relative_path)

    def edges_around(self, node_id: str) -> list[Any]:
        """Edges leaving ``node_id`` and materialization edges into it, sorted and unique."""
        return _sorted_unique([*self.graph.edges_from(node_id), *self._materialization_edges_to.get(node_id, [])])

    def test_link_edges(self) -> list[Any]:
        """Edges leaving a test file, and materialization edges into a test file."""
        edges = [
            edge
            for node_id in sorted(self.graph.node_ids())
            if node_id.startswith("test_file:")
            for edge in self.graph.edges_from(node_id)
        ]
        edges += [
            edge
            for target_id, into in self._materialization_edges_to.items()
            if target_id.startswith("test_file:")
            for edge in into
        ]
        return _sorted_unique(edges)


def _sorted_unique(edges: list[Any]) -> list[Any]:
    unique = {(edge.source_id, edge.target_id, edge.role, edge.provenance_locator): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]

FILE:deskops/identity.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root
from sldb.store.layout import store_exists

from deskops.config import DeskConfig
from deskops.models import RepositoryDoc

UNKNOWN_PROJECT_IDENTITY = "unknown-project"


@dataclass(frozen=True)
class RegisteredRepository:
    id: str
    name: str | None
    source_path: Path
    relative_path: str | None
    repo_root: Path | None

    @property
    def desk_root(self) -> Path | None:
        if self.repo_root is None:
            return None
        return self.repo_root / "desk"


def find_context_root(start: Path | None = None) -> Path:
    """Return the nearest ancestor that looks like a project boundary.

    The upward walk stops at the first directory containing ``desk/`` or
    ``.git``. Nothing above that boundary is considered, so a sandbox nested
    inside a repository never falls through to the repository's store or
    registry. With no matching ancestor the current directory is the boundary.
    """
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for directory in [current, *current.parents]:
        if (directory / "desk").is_dir() or (directory / ".git").exists():
            return directory
    return current


def find_local_store(start: Path | None = None) -> Path | None:
    """Return the store at the project boundary, never an ancestor's store."""
    candidate = find_context_root(start) / ".sldb"
    return candidate if store_exists(candidate) else None


def resolve_store_context(store_arg: str | None) -> tuple[Path, Path]:
    if store_arg:
        return get_store_context(store_arg)
    local_store = find_local_store()
    if local_store is None:
        raise SLDBStoreError("No local store found. Use --store to anchor the repo lookup.")
    return local_store, project_root(local_store)


def load_repository_registry(registry_desk_root: Path, ecosystem_root: Path) -> list[RegisteredRepository]:
    registry_dir = registry_desk_root / "registry"
    if not registry_dir.exists():
        return []

    entries: list[RegisteredRepository] = []
    for path in sorted(registry_dir.glob("repo-*.md")):
        payload = extract_model_data(RepositoryDoc, path.read_text(encoding="utf-8"))
        repo_id = str(payload.get("id") or path.stem.removeprefix("repo-"))
        repo_path = payload.get("path")
        resolved_root = _resolve_registered_root(ecosystem_root, repo_path)
        entries.append(
            RegisteredRepository(
                id=repo_id,
                name=payload.get("name"),
                source_path=path.resolve(),
                relative_path=repo_path,
                repo_root=resolved_root,
            )
        )

    _raise_on_duplicate_ids(entries)
    _raise_on_duplicate_roots(entries)
    return entries


def resolve_registered_repo(
    entries: list[RegisteredRepository],
    repo_id: str,
    *,
    registry_dir: Path | None = None,
) -> RegisteredRepository:
    matches = [entry for entry in entries if entry.id == repo_id]
    if not matches:
        raise SLDBStoreError(_missing_repository_message(repo_id, entries, registry_dir=registry_dir))
    if len(matches) > 1:
        raise SLDBStoreError(_duplicate_id_message(repo_id, matches))
    return matches[0]


def resolve_registered_repo_by_root(
    entries: list[RegisteredRepository],
    repo_root: Path,
) -> RegisteredRepository | None:
    candidate = repo_root.resolve()
    matches = [
        entry
        for entry in entries
        if entry.repo_root is not None
        and (candidate == entry.repo_root or _is_relative_to(candidate, entry.repo_root))
    ]
    if not matches:
        return None
    if len(matches) > 1:
        joined = ", ".join(f"{entry.id} ({entry.repo_root})" for entry in matches)
        raise SLDBStoreError(
            f"Repository root '{candidate}' is ambiguous in registry; matches: {joined}."
        )
    return matches[0]


class EcosystemIdentity:
    """Canonical resolution path answering 'what repository am I in right now' and 'how do I find another'."""
    def __init__(self, store_arg: str | None) -> None:
        self.store_path, self.ecosystem_root = resolve_store_context(store_arg)
        self.registry_desk_root = self.ecosystem_root / "desk"
        self.registry_dir = self.registry_desk_root / "registry"
        self.entries = load_repository_registry(self.registry_desk_root, self.ecosystem_root)

    def what_repository_am_i_in(
        self,
        repo_root: Path,
        *,
        require_registry_match: bool,
        allow_unregistered: bool = False,
        default_to_directory_name: bool = False,
    ) -> str | None:
        """Resolve the identity of the repo at ``repo_root``.

        ``allow_unregistered`` lets a repo whose desk config names it fall back
        to that config when the local registry does not list it at all. That is
        the `message ack` case: creating a register for somebody else must not
        hide the repo's own identity.

        ``default_to_directory_name`` resolves a desk without
        ``project_identity`` from its directory name instead of failing, which
        lets a message be delivered to a desk that never configured itself.
        """
        repo_root = repo_root.resolve()
        desk_root = repo_root / "desk"
        config_identity = UNKNOWN_PROJECT_IDENTITY
        if desk_root.exists():
            config = DeskConfig.load(desk_root)
            config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY

        entry_by_root = resolve_registered_repo_by_root(self.entries, repo_root)

        if not self.entries:
            if require_registry_match and config_identity == UNKNOWN_PROJECT_IDENTITY:
                if default_to_directory_name:
                    return repo_root.name
                raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
            return config_identity if config_identity != UNKNOWN_PROJECT_IDENTITY else None

        if require_registry_match:
            if config_identity == UNKNOWN_PROJECT_IDENTITY:
                if not default_to_directory_name:
                    raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
                return entry_by_root.id if entry_by_root is not None else repo_root.name
            matches = [entry for entry in self.entries if entry.id == config_identity]
            if not matches and allow_unregistered:
                if entry_by_root is not None:
                    raise SLDBStoreError(
                        f"Desk config project_identity '{config_identity}' disagrees with registry root match '{entry_by_root.id}' for '{repo_root}'."
                    )
                return config_identity
            repo_by_id = resolve_registered_repo(
                self.entries, config_identity, registry_dir=self.registry_dir
            )
            if entry_by_root is None:
                raise SLDBStoreError(
                    _unregistered_current_repo_message(repo_root, registry_dir=self.registry_dir)
                )
            if repo_by_id.id != entry_by_root.id:
                raise SLDBStoreError(
                    f"Desk config project_identity '{config_identity}' disagrees with registry root match '{entry_by_root.id}' for '{repo_root}'."
                )
            return config_identity
        else:
            if entry_by_root is None:
                if allow_unregistered and config_identity != UNKNOWN_PROJECT_IDENTITY:
                    return config_identity
                return None
            if config_identity != UNKNOWN_PROJECT_IDENTITY and config_identity != entry_by_root.id:
                raise SLDBStoreError(
                    f"Desk config project_identity '{config_identity}' disagrees with registry id '{entry_by_root.id}' for '{entry_by_root.repo_root}'."
                )
            return entry_by_root.id

    def how_do_i_find_another(self, repo_id: str) -> Path:
        entry = resolve_registered_repo(self.entries, repo_id, registry_dir=self.registry_dir)
        if entry.desk_root is None:
            raise SLDBStoreError(f"Repository id '{repo_id}' has no registered root path.")
        return entry.desk_root.resolve()


def _raise_on_duplicate_ids(entries: list[RegisteredRepository]) -> None:
    by_id: dict[str, list[RegisteredRepository]] = {}
    for entry in entries:
        by_id.setdefault(entry.id, []).append(entry)
    for repo_id, matches in by_id.items():
        if len(matches) > 1:
            raise SLDBStoreError(_duplicate_id_message(repo_id, matches))


def _raise_on_duplicate_roots(entries: list[RegisteredRepository]) -> None:
    by_root: dict[Path, list[RegisteredRepository]] = {}
    for entry in entries:
        if entry.repo_root is None:
            continue
        by_root.setdefault(entry.repo_root, []).append(entry)
    for root, matches in by_root.items():
        if len(matches) > 1:
            ids = ", ".join(f"{entry.id} [{entry.source_path}]" for entry in matches)
            raise SLDBStoreError(f"Duplicate repository root '{root}' in registry: {ids}.")


def _duplicate_id_message(repo_id: str, matches: list[RegisteredRepository]) -> str:
    locations = ", ".join(str(entry.source_path) for entry in matches)
    return f"Duplicate repository id '{repo_id}' in registry: {locations}."


def _missing_repository_message(repo_id: str, entries: list[RegisteredRepository], *, registry_dir: Path | None) -> str:
    registry_hint = f" at '{registry_dir}'" if registry_dir is not None else ""
    found = ", ".join(sorted(e.id for e in entries)) if entries else "none"
    return (
        f"Repository id '{repo_id}' not found in registry{registry_hint} (found: {found}). "
        "Supported path: run 'deskops repo register <name> --path <abs>' "
        "or add an entry to the ecosystem registry."
    )


def _unregistered_current_repo_message(repo_root: Path, *, registry_dir: Path | None) -> str:
    registry_hint = f" at '{registry_dir}'" if registry_dir is not None else ""
    return (
        f"Current repository root '{repo_root}' is not registered in the ecosystem registry{registry_hint}. "
        f"Supported path: run 'deskops repo register <name> --path {repo_root}' "
        "or add an entry to the ecosystem registry."
    )


def _resolve_registered_root(ecosystem_root: Path, repo_path: str | None) -> Path | None:
    if not repo_path:
        return None
    candidate = Path(repo_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (ecosystem_root / candidate).resolve()


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
    except ValueError:
        return False
    return True

FILE:deskops/cli/commands/closeout.py
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService


class CloseoutCLI:
    """Tool-made closing commits, linked to run evidence or marked manual.

    The closing commit is created by ``ClosureService``, not by agent
    discretion. With --run-dir the commit message carries immutable trailers
    linking it to the run evidence directory; with --no-run it carries
    Closeout-Mode: manual and the stated reason instead. ``supersede`` closes a
    task whose subject no longer exists, with a reason and a resolvable ref
    instead of run evidence; ``retire`` removes a task that was already resolved
    before the ritual lifecycle, keeping its status; ``resolved-by`` closes a task
whose work already entered the history, with an ancestor commit and an accepted
test instead of an atom per file. Either way an append-only
    index records the task
    and run, committed together with the closing commit; the commit hash is
    resolved from its Task-Id trailer.
    """

    def run(self, args: Any) -> int:
        command = getattr(args, "closeout_command", None)
        if command == "commit":
            return self._commit(args)
        if command == "supersede":
            return self._supersede(args)
        if command == "retire":
            return self._retire(args)
        if command == "resolved-by":
            return self._resolved_by(args)
        if command == "verify":
            return self._verify(args)
        print("Usage: deskops closeout {commit|supersede|retire|resolved-by|verify} ...")
        return 1

    def _retire(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_retired(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _resolved_by(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_resolved_by(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
            tests=getattr(args, "test", None),
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _supersede(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_superseded(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _verify(self, args: Any) -> int:
        root = Path(args.root).resolve()
        # verify also writes the evidence receipts (CC33a); the envelope is unchanged.
        report = DeskopsOperations(root).closure.verify_task_closeout(args.task, write_receipts=True)
        print(json.dumps(report, indent=2, sort_keys=True))
        # The JSON stays machine-readable on stdout; the declared/found line and the
        # alerts are always said aloud on stderr, never silently folded into the report.
        print(f"Closeout gate: {report['summary']}", file=sys.stderr)
        for alert in report.get("alerts") or []:
            print(f"ALERTA {alert['code']}: {alert['message']}", file=sys.stderr)
        return 0 if report["ok"] else 1

    def _commit(self, args: Any) -> int:
        run_dir_arg = getattr(args, "run_dir", None)
        no_run = bool(getattr(args, "no_run", False))
        reason = getattr(args, "reason", None)
        if run_dir_arg and no_run:
            print("Pass either --run-dir or --no-run, not both.")
            return 1
        if not run_dir_arg and not no_run:
            print(
                "Closing a task needs one of two routes: --run-dir <runs/subagents/dir> to link the "
                "commit to a subagent run, or --no-run --reason \"<why>\" to close it manually."
            )
            return 1
        if no_run:
            return self._commit_manual(args, reason)
        if reason is not None:
            print("--reason applies only to --no-run; a --run-dir closeout takes its evidence from the run.")
            return 1
        return self._commit_with_run(args)

    def _commit_manual(self, args: Any, reason: str | None) -> int:
        root = Path(args.root).resolve()
        run_only = [flag for flag, attr in (("--run-id", "run_id"), ("--session", "session")) if getattr(args, attr, None)]
        if run_only:
            print(f"{', '.join(run_only)} applies only to --run-dir; a --no-run closeout has no run to record.")
            return 1
        if not " ".join((reason or "").split()):
            print("--no-run needs a non-empty --reason saying why the task closes without a subagent run.")
            return 1

        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_manual(
            args.task,
            reason=reason or "",
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _commit_with_run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_with_run(
            args.task,
            run_dir=args.run_dir,
            paths=getattr(args, "paths", None),
            run_id=getattr(args, "run_id", None),
            session=getattr(args, "session", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

A task its model rejects (its `status`, `current_node` and `history` are not a state
the lifecycle can produce) is an error of its own, one line per task with the file and
the validator's text, read from the task's frontmatter: `sldb stores check` stops at the
first such document, so doctor names every one and still runs the other checks
(structure, store, models). A task the legacy migration decides says
`Migrate it with deskops desk update --apply`; any other one says what its owner can
do (`decide its state: deskops closeout supersede --task <id> --reason ... --ref ...`).

`doctor` also compares the desk's managed seeds (the lifecycle graph and its rules
under `desk/lifecycle/`) with the ones the installed deskops ships, by the same
comparison `deskops desk update --apply` makes before rewriting them. Each copy
that differs is one finding, naming the top-level frontmatter fields that differ
(`body` when only the text below the frontmatter does; the `sldb:` write
provenance is named only when nothing else differs):

```text
lifecycle seed out of date: desk/lifecycle/execution-task_activates.md differs from the deskops package (attributes). Fix: deskops desk update --apply
```

It is an **error** when a lifecycle edge's transition fields differ (`source_id`,
`target_id`, `relation_type`, `condition`, `attributes`): `deskops advance` refuses
that edge. Any other difference (a rule, the body or notes of a seed) is an
**alert**. A desk seeded before CC31 has `attributes: {}` on its edges and shows
up here; `deskops desk update --apply` restores the managed seeds.

`--repair` acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.
- `desk update` also migrates the tasks a desk migrated before CC31 left in a
  state no transition produces: an empty history with a terminal or drawer
  status at a node. The dry run lists them as `Legacy task states to migrate`;
  `--apply` writes them first, one line per changed field
  (`desk/tasks/<task>.md: history [] -> [superseded]`). The table:
  `superseded` gets `history [superseded]` (its node stays); `closed`,
  `resolved`, `done`, `complete` and `cancelled` (pre-lifecycle resolved), and
  `deferred` and `candidate` (drawer), get `current_node ''`, outside the
  lifecycle. A non-terminal status with an empty history (any status that is
  not `draft` nor one of those above, nor a closeout status: `active`,
  `ready_for_testing`, `blocked`...) is backed by no transition, so it gets
  `status draft` at the entry node `ritual-execution` (an empty
  `current_node` stays empty), reported as
  `desk/tasks/<task>.md: status active -> draft` plus
  `current_node <node> -> ritual-execution` when the node moves, and its
  `summary` gets one line in front, `Migrada a draft por deskops desk update:
  estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).`, followed by the
  previous summary. A non-empty history with an incoherent status is not
  migrated. Any other task the model rejects is listed under
  `Invalid task documents (not written)` with the validator's text and what its
  owner can do; it is never written. The write goes to the frontmatter, not
  through sldb (sldb rebuilds every task of the store on each write and stops at
  the invalid one), and the new text is validated with `TaskDoc`; a task it
  still rejects is restored. While `sldb stores check` cannot read the store,
  `--apply` reports it and skips every other repair (structure, lifecycle
  graph, models, tracking, task types, indexes) instead of leaving the store
  half written. `--apply` exits 0
  when nothing is left and 1 while a task waits for its owner; a second run
  migrates nothing.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`deskops inbox` is a deprecated alias for the same storage. Its flag grammar
(`--list`, `--show`, `--ack`) still works:

```bash runnable
deskops inbox --list --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity (`--sender` is the deprecated `inbox` spelling).
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed. Any other reference to the entry is left as it is.
Each file that holds one is reported on stderr as
`alert: <entry> still referenced by <file>`, and the exit code does not change.
These references are what `sldb.api.referrers` finds over the desk graph: a
drawer-board bullet in another form, such as `` `tasks/<id>.md` ``, or a task
that names the entry. `deskops closeout` reports the files that still name the
closed task in the same way.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. The declared fields that name the document lose that entry
in the transaction that deletes it. For a pill, these are the `pills` of the
Board and of every task. A mention in prose, such as a path in a task body, is
never rewritten, so retire refuses while one remains unless `--force` is passed.
Both kinds of reference are what `sldb.api.referrers` finds: the store's field
index, and the mention patterns of the desk graph. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

Before applying an edge, `advance` checks it against the lifecycle the installed
deskops ships: same `relation_type`, same target ritual and same
`attributes.sets.status`. An edge that differs (a desk seeded before CC31 has
`attributes: {}`) would write a state the task model rejects, so `advance` stops
first, exits 1 and leaves the task unchanged:

```text
Error: Cannot advance task-x via task_activates: the edge desk/lifecycle/execution-task_activates.md does not set status active (attributes.sets.status is missing). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.
```

`deskops doctor` reports the same seed; `deskops desk update --apply` restores it.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`,
`complete` or `cancelled`, as pre-lifecycle tasks are, or `superseded`,
`deferred` or `candidate` with an empty history (what a desk migrated before
CC31 left; a `superseded` task with only its `superseded` record, what
`desk update --apply` makes of it, too). Retire reads the task's frontmatter, so it also removes a task its
model rejects; in a desk with a store it waits until no other task is invalid
(`deskops desk update --apply` first). `closeout supersede` also closes a task
its model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads and writes the frontmatter, with the same
commit and trailers, and waits the same way while another task is invalid. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject. Like supersede, it also closes a task its
model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads the task's `files` and history from the
frontmatter, applies the same ref and test gates, writes `status: resolved` and
the `resolved-by` record into the frontmatter (validated with `TaskDoc`, restored
if it fails) and makes the same closing commit with the same trailers. In a desk
with a store, supersede, retire and resolved-by refuse before writing anything
while another task is invalid: sldb re-extracts the whole model on every write
(sldb H2, note 3895e9f7). Migrate the others with `deskops desk update --apply`,
decide them by hand, or close each with `closeout supersede` or `closeout retire`
once it is the only invalid task, then run the close again.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb. The write is sldb's
`replace_text` inside the desk transaction: a store-tracked file (a role prompt)
must still validate under its model after the replacement, or nothing is written
and the command exits 1 with `Refusing to replace in <path>: ...`.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites every reference to the source atom so that it names the target,
in the same transaction as the merge. It covers fields such as a task's
`atoms`, `atom:atom-<source>` anywhere in a task or issue, and a bare
`atom-<source>` under a Related Atoms heading. The source stays as a redirect
stub. `atoms delete` and `atoms split` find the same references. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-e-0123456789ab

# A tester is its own role and mode, with separate scope and completion rules.
deskops runtime template deskops-tester --root . --harness claude \
  --mode tester --task task-fix-thing --agent deskops-t-0123456789ab \
  --task-root . --run-dir runs/subagents/20261110-120000-task-fix-thing-testing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task, `--mode tester` writes the independent verification instructions,
and `--mode coordinator` writes it for an agent that owns a desk. An explicit
mode always wins; otherwise only the selected role's own name/id is inspected
(a name or id ending in `-tester` chooses tester; a selected name or id naming a
supervisor/coordinator chooses coordinator; anything else executor). With
`--task` and `--agent` it also records the in_progress RunDoc launch intent under
`runs/subagents/`; its summary says it is intent, not proof of start.
`--task-root` names the repository whose desk owns the task (default `--root`)
and `--run-dir` points at the evidence directory. An existing RunDoc is reused
for reconciliation but never overwritten: a retry gets a new run_dir, and
attempts and their evidence are immutable.

`--context-file` accepts JSON with exactly `project`, `workspace_root`,
`desk_root`, `source_root` and `sldb_root`. `project` is a non-empty Scion slug
or UUID, never a filesystem path; the other four are absolute directories inside
`workspace_root`, where `desk_root` contains `desk/`, `source_root` contains the
`deskops` package and `sldb_root` is sldb's `src` directory. Missing, unknown,
relative, out-of-workspace or invalid values are refused before any template is
written. A valid context emits `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`
and `PYTHONPATH=source_root:sldb_root`, plus a volume whose source and target are
`workspace_root`. It carries no secrets. Omitting the flag preserves CLI, path
and environment compatibility; the corrected prompt text is intentionally not
byte-identical to the faulty earlier wording.

The coordinator derives a stable child identity from the task contract:
`deskops-e-<12hex>` for an executor or `deskops-t-<12hex>` for a tester, where
the hex is SHA-256 of `task_id + NUL + contract_sha256 + NUL + role`.
`contract_sha256` is the SLDB `TaskDoc.__contract__` digest. Attempt 1 uses the
base name, attempt 2 appends `-a2`, and there is no attempt 3; labels are
`deskops.task_id`, `deskops.contract_sha256`, `deskops.role` and
`deskops.attempt`. The runtime helper `scion_child_identity(task_path, role,
attempt)` returns that name and label set, and `scion_start_argv` builds the
explicit native start argv. These helpers only derive identity/argv; native
Scion orchestration remains Scion, not a DeskOps scheduler.

Native labels must be printable ASCII and at most 63 characters. The helper
preserves the full canonical task id and 64-hex contract hash in its returned
identity and name derivation; `deskops.contract_sha256` carries the 63-hex prefix.
A long or non-ASCII task-id label uses a bounded hash descriptor while TaskDoc
and RunDoc retain the full id. Copy the helper label map exactly rather than
pasting a full 64-hex digest into `--label`.

The generated coordinator reconciles its own existing executor/tester lanes and
completed handoffs before selecting new work; a restart or successful child
completion must not skip its own task or duplicate a child. It reads Scion
activity first and phase only as fallback, because the native bridge can report
`activity=completed` while `phase=running`. A dependency-ready task missing its
preflight/bundle receipt is routine work: run the cheap context review and
adjudicate factual findings before dispatch. Implementation and validation run
from the configured `desk_root`, with template artifacts and evidence under the
assigned desk `runs/` path rather than `/tmp`. Closeout runs
`deskops closeout verify`, reviews the diff, and commits only scoped
implementation/evidence/review paths with `closeout commit --paths` (never
`git add -A`). The coordinator signals `task_completed` only after all authorized
work is closed, declared evidence verified and required phase integration/commit
done; an external blocker is recorded and signalled as blocked, and only an
actual owner decision uses `ask_user`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

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
- Incoming references (CC35c, sldb GD22): `deskops atoms delete`, `split` and `merge`, `deskops retire`, `deskops drawer remove` and the closeouts that delete a task now find references to a document with sldb. They use `resolve_target` and `find_hits` of `sldb.api.edges.referrers` with the desk graph built in process (`deskops/services/references.py`, DO8). Fields come from the store's edge index, and prose mentions from the graph's `MentionPattern` rules. Merge rewrites through `rewrite_references` (fields), and through `rewritten_line` plus `replace_text` (mentions), inside the merge's `desk_transaction`. Retire removes the retired document from the declared fields that name it, such as the Board's `pills` and every task's `pills`, inside the transaction that deletes it, so a failure leaves every file as it was. A mention in prose still refuses retire unless `--force` is given. `drawer remove` and closeout do not rewrite: each file that still names the deleted document is reported on stderr as `alert: <document> still referenced by <file>`, and the exit code does not change. The desk graph gains two patterns. `ATOM_ID` (`atom:atom-<slug>` as a whole token) is read in Related Atoms sections and on every line of tasks and issues. `DRAWER_BULLET` (`` - `tasks/<id>.md` `` or `` - `<id>` ``) is read on the drawer Board. The old searches are gone: `_find_inbound_atom_references`, `_rewrite_inbound_atom_references` and retire's `_inbound_references`. Files that are neither tracked documents nor desk graph nodes have no referrers, so retire no longer refuses a file such as a `desk/logbook/` note because a doc names its path. A desk without a store has no field references, so retire leaves its Board untouched (`tests/test_atoms_merge.py`, `tests/test_retire_cli.py`, `tests/test_inbox_promote_cli_gaps.py`).
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

- `deskops closeout resolved-by` closes a task its model rejects (for example a `draft` after `task_activates, task_hands_to_closeout`, as the two drafts of shared_llm-gateway), which used to exit 1 with `Validation error: ... lifecycle is inconsistent`. Like `closeout supersede`, it reads the task from its frontmatter when the model rejects it, applies the same `--ref` and `--test` gates (the tests gate uses the frontmatter's `files`), writes `status: resolved` and appends `resolved-by` to the history with `workspace.rewrite_task_fields` (validated with `TaskDoc`, restored if it fails), and makes the same closing commit with the same trailers as for a valid task. Supersede and resolved-by share that path (`ClosureService._read_closing_task` and `_record_closing_status`). With a store, it refuses before writing anything while another task is invalid, as supersede and retire do; the refusal of the three now names sldb H2 (note 3895e9f7: sldb re-extracts the whole model on every write) and the manual route (decide the other task by hand, or close it with supersede or retire once it is the only invalid one) (`tests/test_closeout_resolved_by.py`, `tests/test_legacy_task_states.py`).
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
Cold-bundle de la tarea task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test nuevo: resolved-by con --ref <repo>:<sha> y --test <repo>:<ruta> de otro repo registrado cierra con Closeout-Mode: resolved-by y guarda las referencias calificadas en los trailers
- Tests nuevos de rechazo: sha no ancestro, test inexistente, repo no registrado, raíz registrada ausente
- Los tests existentes de resolved-by y closeout siguen verdes; suite completa de a un archivo en verde
- 4 pasos del CI de deskops en clon limpio

