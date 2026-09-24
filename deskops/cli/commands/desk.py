from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import migrate_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
import deskops.models as models

def guess_model_for_path(desk_dir: Path, path: Path) -> type | None:
    rel = path.relative_to(desk_dir)
    parts = rel.parts
    if len(parts) == 2 and parts[0] == "tasks" and parts[1] == "Board.md":
        return models.BoardDoc
    if len(parts) == 2 and parts[0] == "tasks":
        return models.TaskDoc
    if len(parts) == 2 and parts[0] == "contexts":
        return models.PillDoc
    if len(parts) == 2 and parts[0] == "rituals":
        return models.RitualDoc
    if len(parts) == 2 and parts[0] == "atoms":
        if path.stem.startswith("proto-"):
            return models.ProtoAtomDoc
        return models.AtomDoc
    if len(parts) == 2 and parts[0] == "roles":
        return models.RoleDoc
    if len(parts) == 2 and parts[0] == "inbox":
        return models.InboxNoteDoc
    if len(parts) == 2 and parts[0] == "registry":
        return models.RepositoryDoc
    if len(parts) == 2 and parts[0] == "steps":
        return models.StepDoc
    if len(parts) == 2 and parts[0] == "faq":
        return models.FAQDoc
    if len(parts) == 2 and parts[0] == "routines":
        return models.RoutineDoc
    if len(parts) == 3 and parts[0] == "primitives":
        if parts[1] == "conditions": return models.ConditionDoc
        if parts[1] == "operators": return models.OperatorDoc
        if parts[1] == "checklists": return models.ChecklistDoc
        if parts[1] == "hooks": return models.HookDoc
        if parts[1] == "edges": return models.EdgeDoc
    return None

class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = scaffold_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")

        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"
        inspection = inspect_desk(root)

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")

        bootstrap = SLDBBootstrap()
        registered_models: set[str] = set()
        if store_dir.exists():
            try:
                registered_models = bootstrap._registered_model_names(store_dir)
            except Exception:
                pass

        unregistered_models: list[str] = []
        for model_name in MODEL_REFS.keys():
            if model_name not in registered_models:
                unregistered_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        tracked_mds: set[Path] = set()
        result = subprocess.run(
            [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout:
            try:
                payload = json.loads(result.stdout)
                for model in payload.get("models", []):
                    for doc in model.get("documents", []):
                        doc_path = doc.get("path")
                        if not doc_path:
                            continue
                        tracked_path = (root / doc_path).resolve()
                        tracked_mds.add(tracked_path)
                        
                        if doc.get("note") not in ("ok",):
                            invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                            if doc.get("note") == "missing":
                                missing_docs.append(doc.get("name") or Path(doc_path).stem)
            except json.JSONDecodeError:
                pass

        untracked_docs: list[Path] = []
        if desk_dir.exists():
            ignored_modeled_names = {
                "Board.md",
                "pills.md",
                "execution.md",
                "testing.md",
                "closeout.md",
                "phase.md",
                "README.md",
                "tag-namespaces.yaml",
            }
            modeled_mds = {
                path.resolve()
                for path in modeled_desk_markdown_docs(root, desk_dir)
                if path.name not in ignored_modeled_names
            }
            untracked_docs = [p for p in modeled_mds if p not in tracked_mds]

        if not missing_desk_files and not unregistered_models and not untracked_docs and not invalid_docs:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if untracked_docs:
            rel_untracked = [str(p.relative_to(root)) for p in untracked_docs]
            print(f"- Untracked desk documents: {', '.join(rel_untracked)}")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")

        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")
        
        if missing_desk_files:
            scaffold_desk(root)
            print("Scaffolded missing desk structure.")

        if unregistered_models:
            bootstrap.init_local_store(root)
            print("Registered missing models.")

        if untracked_docs:
            try:
                from sldb.api.documents.track_document_file import track_document_file
                pythonpath = str(Path(__file__).resolve().parents[2])
                for p in untracked_docs:
                    model = guess_model_for_path(desk_dir, p)
                    if model:
                        try:
                            track_document_file(
                                store_dir,
                                model.__name__,
                                p,
                                name=p.stem,
                                pythonpath=pythonpath,
                                force=True,
                            )
                            print(f"Tracked {p.relative_to(root)} as {model.__name__}.")
                        except Exception as e:
                            print(f"Failed to track {p.relative_to(root)}: {e}")
                    else:
                        print(f"Could not guess model for {p.relative_to(root)}.")
            except ImportError:
                print("Failed to import sldb API for tracking documents.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            try:
                from sldb.api.documents.untrack_document import untrack_document
                pythonpath = str(Path(__file__).resolve().parents[2])
                for name in missing_docs:
                    try:
                        untrack_document(store_dir, name, pythonpath)
                        print(f"Untracked {name}: its file is gone.")
                    except Exception as e:
                        print(f"Failed to untrack {name}: {e}")
            except ImportError:
                print("Failed to import sldb API for untracking documents.")

        if invalid_docs:
            try:
                from sldb.api.stores.update_store_indexes import update_store_indexes
                pythonpath = str(Path(__file__).resolve().parents[2])
                update_store_indexes(store_dir, pythonpath, wait=False)
                print("Updated store derived indexes.")
            except ImportError:
                print("Failed to import sldb API for updating store.")

        return 0
