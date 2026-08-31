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


def resolve_registered_repo(entries: list[RegisteredRepository], repo_id: str) -> RegisteredRepository:
    matches = [entry for entry in entries if entry.id == repo_id]
    if not matches:
        raise SLDBStoreError(f"Repository id '{repo_id}' not found in registry.")
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


def resolve_registered_desk(repo_id: str, store_arg: str | None) -> Path:
    _store_path, ecosystem_root = resolve_store_context(store_arg)
    entries = load_repository_registry(ecosystem_root / "desk", ecosystem_root)
    entry = resolve_registered_repo(entries, repo_id)
    if entry.desk_root is None:
        raise SLDBStoreError(f"Repository id '{repo_id}' has no registered root path.")
    return entry.desk_root.resolve()


def resolve_canonical_project_identity(repo_root: Path, store_arg: str | None) -> str:
    repo_root = repo_root.resolve()
    desk_root = repo_root / "desk"
    config = DeskConfig.load(desk_root)
    config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY
    if config_identity == UNKNOWN_PROJECT_IDENTITY:
        raise SLDBStoreError(
            "Desk config project_identity is not established (found 'unknown-project')."
        )

    _store_path, ecosystem_root = resolve_store_context(store_arg)
    entries = load_repository_registry(ecosystem_root / "desk", ecosystem_root)
    repo_by_id = resolve_registered_repo(entries, config_identity)
    repo_by_root = resolve_registered_repo_by_root(entries, repo_root)
    if repo_by_root is None:
        raise SLDBStoreError(
            f"Current repository root '{repo_root}' is not registered in the ecosystem registry."
        )
    if repo_by_id.id != repo_by_root.id:
        raise SLDBStoreError(
            "Desk config project_identity "
            f"'{config_identity}' disagrees with registry root match '{repo_by_root.id}' for '{repo_root}'."
        )
    return config_identity


def infer_sender_project_identity(sender_root: Path, store_arg: str | None) -> str | None:
    _store_path, ecosystem_root = resolve_store_context(store_arg)
    entries = load_repository_registry(ecosystem_root / "desk", ecosystem_root)
    entry = resolve_registered_repo_by_root(entries, sender_root.resolve())
    if entry is None:
        return None

    desk_root = entry.desk_root
    if desk_root is not None and desk_root.exists():
        config_identity = DeskConfig.load(desk_root).project_identity.strip() or UNKNOWN_PROJECT_IDENTITY
        if config_identity != UNKNOWN_PROJECT_IDENTITY and config_identity != entry.id:
            raise SLDBStoreError(
                "Desk config project_identity "
                f"'{config_identity}' disagrees with registry id '{entry.id}' for '{entry.repo_root}'."
            )
    return entry.id


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
