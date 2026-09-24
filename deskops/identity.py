from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root
from sldb.store.resolver import find_local_store

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

    def what_repository_am_i_in(self, repo_root: Path, *, require_registry_match: bool) -> str | None:
        repo_root = repo_root.resolve()
        desk_root = repo_root / "desk"
        config_identity = UNKNOWN_PROJECT_IDENTITY
        if desk_root.exists():
            config = DeskConfig.load(desk_root)
            config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY

        entry_by_root = resolve_registered_repo_by_root(self.entries, repo_root)

        if not self.entries:
            if require_registry_match and config_identity == UNKNOWN_PROJECT_IDENTITY:
                raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
            return config_identity if config_identity != UNKNOWN_PROJECT_IDENTITY else None

        if require_registry_match:
            if config_identity == UNKNOWN_PROJECT_IDENTITY:
                raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
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
