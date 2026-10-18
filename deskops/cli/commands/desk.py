from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from deskops import doc_io
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import migrate_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        doc_io.register_model(root, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        doc_io.track(root, document.path, FAQ_MODEL, name=document.name, pythonpath=pythonpath)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    doc_io.remove_model_from(
        root, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True
    )
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


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
        return models.DeskFAQDoc
    if len(parts) == 2 and parts[0] == "lifecycle":
        return None  # written and tracked by deskops.lifecycle.ensure_lifecycle_graph
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

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import ensure_lifecycle_graph

            for change in ensure_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
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

        from deskops.lifecycle_migration import inspect_legacy_lifecycle
        from deskops.lifecycle_migration import migrate_legacy_lifecycle

        legacy = inspect_legacy_lifecycle(root) if desk_dir.exists() else None
        legacy_pending = bool(legacy and (legacy.needs_migration or legacy.registered_legacy_models))
        if legacy_pending and apply:
            from deskops.lifecycle_migration import LegacyMigrationBlocked

            print("Migrating the task lifecycle to the desk's sldb graph...")
            if store_dir.exists() and "RitualDoc" not in SLDBBootstrap()._registered_model_entries(store_dir):
                # The lifecycle states are RitualDocs; a store that never registered the
                # model (an early desk) gets the deskops models before the graph is written.
                SLDBBootstrap().init_local_store(root)
                print("- registered the deskops models the lifecycle graph needs")
            try:
                for change in migrate_legacy_lifecycle(root):
                    print(f"- {change}")
            except LegacyMigrationBlocked as exc:
                print(f"Error: {exc}")
                return 1
            legacy_pending = False

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
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        tracked_mds: set[Path] = set()
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None:
                if result.returncode != 0:
                    raise DeskopsEnvironmentError(
                        f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}"
                    )
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
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

        if not legacy_pending and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if legacy_pending and legacy is not None:
            print(
                "- Legacy task lifecycle: "
                f"{len(legacy.primitive_docs)} routine/primitive documents to delete, "
                f"{len(legacy.tasks_to_rewrite)} tasks to rewrite, "
                f"lifecycle graph {'missing' if legacy.graph_missing else 'present'}, "
                f"retired models still registered: {', '.join(legacy.registered_legacy_models) or 'none'}"
            )
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
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

        if unregistered_models or copied_models:
            bootstrap.init_local_store(root)
            print("Registered missing models and converted copied deskops models.")

        if untracked_docs:
            pythonpath = package_pythonpath()
            for p in untracked_docs:
                model = guess_model_for_path(desk_dir, p)
                if model:
                    try:
                        doc_io.track(
                            root,
                            p,
                            model,
                            name=p.stem,
                            pythonpath=pythonpath,
                        )
                        print(f"Tracked {p.relative_to(root)} as {model.__name__}.")
                    except Exception as e:
                        print(f"Failed to track {p.relative_to(root)}: {e}")
                else:
                    print(f"Could not guess model for {p.relative_to(root)}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    doc_io.untrack(root, name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs:
            pythonpath = package_pythonpath()
            doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
            print("Updated store derived indexes.")

        if store_dir.exists():
            from deskops.lifecycle import ensure_lifecycle_graph
            from deskops.lifecycle import lifecycle_graph_present

            if not lifecycle_graph_present(root):
                for change in ensure_lifecycle_graph(root):
                    print(f"Lifecycle graph: {change}")

        return 0
