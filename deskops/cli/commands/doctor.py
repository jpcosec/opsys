from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.doctor_findings import REGISTER, Findings, moved_documents, print_findings, read_store_check
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk


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
            self._check_models(root, repair, findings)
        return self._report(findings, repair)

    def _check_structure(self, root: Path, desk_dir: Path, inspection, repair: bool, findings: Findings) -> None:
        missing = [rel for rel, exists in (
            ("desk/tasks/Board.md", (desk_dir / "tasks" / "Board.md").exists()),
            ("desk/drawer/", (desk_dir / "drawer").exists()),
            ("desk/rituals/phase.md", (desk_dir / "rituals" / "phase.md").exists()),
        ) if desk_dir.exists() and not exists]
        if missing and repair:
            scaffold_desk(root)
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
