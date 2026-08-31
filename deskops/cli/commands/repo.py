from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from sldb.cli.model_utils import registered_model, resolve_model_ref
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.layout import project_root
from sldb.store.ops import track_document
from sldb.store.resolver import find_local_store

from deskops.identity import load_repository_registry
from deskops.identity import resolve_canonical_project_identity


class RepoCLI:
    """Handle repository registration and discovery."""

    def run(self, args: Any) -> int:
        if args.repo_command == "register":
            return self.register(args)
        if args.repo_command == "whoami":
            return self.whoami(args)
        return 1

    def register(self, args: Any) -> int:
        name = args.name
        path = args.path
        repo_id = args.id or self._slug(name)
        description = args.description or f"Repository for {name}."
        tags = [t.strip() for p in (args.tags or "").split(",") if (t := p.strip())]

        payload = {
            "name": name,
            "id": repo_id,
            "path": path,
            "status": "active",
            "description": description,
            "tags": tags,
        }

        # Preflight: resolve store context and model before any mutation
        try:
            store_path, root = self._store_context(args)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        try:
            model_type, entry, idx = registered_model(
                store_path, "RepositoryDoc", args.pythonpath
            )
        except SLDBStoreError:
            print("Error: RepositoryDoc model is not registered in the store.")
            print("Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>")
            return 1
        except (FileNotFoundError, OSError) as e:
            print(f"Error: cannot read store at {store_path}: {e}")
            return 1

        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        filename = f"repo-{repo_id}.md"
        output_path = registry_dir / filename

        if output_path.exists():
            print(f"Error: Repository file already exists at {output_path}")
            return 1

        try:
            existing_entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        resolved_repo_root = self._resolve_registered_root(root, path)
        for entry in existing_entries:
            if entry.id == repo_id:
                print(
                    f"Error: Repository id '{repo_id}' is already registered by {entry.source_path}."
                )
                return 1
            if entry.repo_root is not None and resolved_repo_root == entry.repo_root:
                print(
                    "Error: Repository root "
                    f"'{resolved_repo_root}' is already registered as '{entry.id}' by {entry.source_path}."
                )
                return 1

        from sldb.store.io import load_models_index, load_documents_index
        models_idx = load_models_index(root / entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        if any(d.name == f"repo-{repo_id}" for d in docs_idx.documents):
            print(f"Error: Repository repo-{repo_id} is already registered in the store.")
            return 1

        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            print("Error: Repository registration failed validation.")
            for issue in details:
                print(f"  - {issue}")
            return 1

        # All prerequisites verified — mutate filesystem
        registry_dir.mkdir(parents=True, exist_ok=True)
        
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")

        # Track in store
        track_document(
            store_path,
            root,
            idx,
            model_type,
            entry,
            output_path,
            f"repo-{repo_id}",
            resolve_model_ref,
            args.pythonpath,
        )
        print(f"Tracked 'repo-{repo_id}'")

        return 0

    def whoami(self, args: Any) -> int:
        try:
            project_id = resolve_canonical_project_identity(Path(args.root), args.store)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1
        print(project_id)
        return 0

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "repo"

    def _desk_root(self, args: Any) -> Path:
        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()
        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()
        return (Path.cwd() / "desk").resolve()

    def _store_context(self, args: Any) -> tuple[Path, Path]:
        if args.store:
            try:
                return get_store_context(args.store)
            except (SLDBStoreError, FileNotFoundError, OSError) as e:
                raise SLDBStoreError(str(e))
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No store found to anchor the registry.")
        return local_store, project_root(local_store)

    def _resolve_registered_root(self, ecosystem_root: Path, repo_path: str) -> Path:
        candidate = Path(repo_path)
        if candidate.is_absolute():
            return candidate.resolve()
        return (ecosystem_root / candidate).resolve()
