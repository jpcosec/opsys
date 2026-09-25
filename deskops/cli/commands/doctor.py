from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.workspace import desk_doc_unmodeled_reason
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk
from deskops.workspace import unmodeled_desk_markdown_docs


class DoctorCLI:
    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        repair = getattr(args, "repair", False)

        findings: list[str] = []
        fixed: list[str] = []

        inspection = inspect_desk(root)
        desk_dir = root / "desk"
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

        if missing_desk_files:
            findings.append(f"Missing desk structure: {', '.join(missing_desk_files)}")
            if repair:
                scaffold_desk(root)
                fixed.append("Scaffolded missing desk/ structure.")

        if inspection.classification == "legacy":
            legacy_surfaces = [*inspection.missing_surfaces, *inspection.malformed_surfaces]
            findings.append(
                "Legacy desk detected: "
                + (", ".join(legacy_surfaces) if legacy_surfaces else "board/task/pill surfaces need explicit migration")
            )
            if repair:
                findings.append("Manual migration entrypoint: deskops desk migrate --root <repo>.")

        untracked: list[Path] = []
        invalid_docs: list[str] = []
        unmodeled_reasons: list[str] = []
        unregistered_models: list[str] = []
        store_index_unreadable = False

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
            unmodeled_mds = unmodeled_desk_markdown_docs(root, desk_dir)
            tracked_mds = set(inspection.tracked_surface_docs)

            tracked_mds: set[Path] = set()
            tracked_model_docs: list[tuple[str | None, Path]] = []

            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb"), "--format", "json"],
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

                            if doc_path.startswith("desk/"):
                                tracked_model_docs.append((model.get("name"), tracked_path))

                            if doc.get("note") not in ("ok", "benign_mutation") and doc_path.startswith("desk/"):
                                invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                except json.JSONDecodeError:
                    findings.append("Failed to parse SLDB store check output.")

            if result.returncode != 0 and not result.stdout:
                findings.append(f"SLDB store check crashed (likely malformed documents): {result.stderr.strip().split(chr(10))[0]}")

            store_dir = root / ".sldb"
            if store_dir.exists():
                try:
                    registered_models = SLDBBootstrap()._registered_model_names(store_dir)
                    unregistered_models = sorted(
                        name for name in MODEL_REFS if name not in registered_models
                    )
                except Exception:
                    store_index_unreadable = True

            untracked = [p for p in modeled_mds if p not in tracked_mds]

            unreadable_docs: list[str] = []
            for model_name, doc_path in tracked_model_docs:
                model = _resolve_deskops_model(model_name)
                if model is None or not doc_path.exists():
                    continue
                fields = is_unreadable_by_model(model, doc_path.read_text(encoding="utf-8"))
                if fields:
                    unreadable_docs.append(
                        f"{doc_path.relative_to(root)} ({model_name}: {', '.join(fields)})"
                    )

            unmodeled_reasons = sorted(
                {
                    reason
                    for path in unmodeled_mds
                    if (reason := desk_doc_unmodeled_reason(root, path)) is not None
                }
            )

            if result.returncode != 0 and not result.stdout:
                untracked = []

        if untracked:
            rel_untracked = [str(p.relative_to(root)) for p in untracked]
            finding = (
                "Untracked desk documents: "
                + ", ".join(rel_untracked)
                + ". These are SLDB-modeled surfaces with broken tracking/state, not intentionally unmodeled desk notes."
            )
            if unmodeled_reasons:
                finding += " Ignored by design: " + "; ".join(unmodeled_reasons)
            findings.append(finding)
            if repair:
                findings.append("Manual repair required to track documents (use sldb docs track).")

        if unreadable_docs:
            findings.append(
                "Documents whose model cannot read their own content: "
                + ", ".join(unreadable_docs)
                + ". The document states these fields, but extracting them yields nothing, "
                "so any edit through the model renders them back empty and erases the content."
            )
            if repair:
                findings.append(
                    "Manual repair required: rebuild each document from its text through sldb so the "
                    "renderer's fixed text is present, then retrack it."
                )

        if invalid_docs:
            findings.append(f"Invalid desk documents: {', '.join(invalid_docs)}")
            if repair:
                findings.append("Manual repair required for invalid documents (check syntax or run sldb stores update).")

        if store_index_unreadable:
            findings.append("Could not read the local .sldb store index; unregistered-model check skipped.")

        if unregistered_models:
            findings.append(
                "Unregistered models: "
                + ", ".join(unregistered_models)
                + ". Run `deskops desk update --apply` to register missing models and repair tracking."
            )
            if repair:
                try:
                    registered_ok = SLDBBootstrap().init_local_store(root) == 0
                except Exception:
                    registered_ok = False
                if registered_ok:
                    fixed.append("Registered missing models.")
                else:
                    findings.append("Manual repair required for unregistered models (run deskops desk update --apply).")

        if not findings:
            print("Desk is healthy. No issues found.")
            return 0

        print("Doctor Findings:")
        for finding in findings:
            print(f"- {finding}")

        if fixed:
            print("\nRepairs applied:")
            for fx in fixed:
                print(f"- {fx}")

        if repair and len(fixed) < len([f for f in findings if "Manual repair required" not in f]):
            print("\nSome issues could not be repaired automatically.")
            return 1
        if not repair:
            print("\nRun with --repair to attempt automatic fixes.")
            return 1

        return 0


def _resolve_deskops_model(name: str | None) -> type | None:
    """The deskops model registered under `name`, or None when it is not ours."""
    if not name:
        return None
    import deskops.models as models

    candidate = getattr(models, name, None)
    return candidate if isinstance(candidate, type) else None
