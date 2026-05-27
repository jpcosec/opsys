from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from sldb.cli.utils import get_store_context, registered_model, resolve_model_ref
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.layout import project_root
from sldb.store.ops import track_document
from sldb.store.resolver import find_local_store


class RepoCLI:
    """Handle repository registration and discovery."""

    def run(self, args: Any) -> int:
        if args.repo_command == "register":
            return self.register(args)
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

        # Resolve registry root
        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        registry_dir.mkdir(parents=True, exist_ok=True)

        # Build filename
        filename = f"repo-{repo_id}.md"
        output_path = registry_dir / filename

        # Load model and render
        store_path, root = self._store_context(args)
        try:
            model_type, entry, idx = registered_model(
                store_path, "RepositoryDoc", args.pythonpath
            )
        except SLDBStoreError:
            print("Warning: RepositoryDoc model not registered. Registry will not be tracked.")
            # Fallback to direct write if model not found? 
            # Or better: require registration for opsys to be "healthy"
            return 1

        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Repository registration failed validation", details)

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
            return get_store_context(args.store)
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No store found to anchor the registry.")
        return local_store, project_root(local_store)
