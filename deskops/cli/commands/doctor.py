from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

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

                            if doc.get("note") not in ("ok", "benign_mutation") and doc_path.startswith("desk/"):
                                invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                except json.JSONDecodeError:
                    findings.append("Failed to parse SLDB store check output.")

            if result.returncode != 0 and not result.stdout:
                findings.append(f"SLDB store check crashed (likely malformed documents): {result.stderr.strip().split(chr(10))[0]}")

            untracked = [p for p in modeled_mds if p not in tracked_mds]

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

        if invalid_docs:
            findings.append(f"Invalid desk documents: {', '.join(invalid_docs)}")
            if repair:
                findings.append("Manual repair required for invalid documents (check syntax or run sldb stores update).")

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
