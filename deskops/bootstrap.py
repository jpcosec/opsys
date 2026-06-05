from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


MODEL_REFS = {
    "BoardDoc": "deskops.models:BoardDoc",
    "TaskDoc": "deskops.models:TaskDoc",
    "PillDoc": "deskops.models:PillDoc",
    "RitualDoc": "deskops.models:RitualDoc",
    "InboxNoteDoc": "deskops.models:InboxNoteDoc",
    "RepositoryDoc": "deskops.models:RepositoryDoc",
    "StepDoc": "deskops.models:StepDoc",
    "AtomDoc": "deskops.models:AtomDoc",
    "FAQDoc": "deskops.models:FAQDoc",
}


class SLDBBootstrap:
    def ensure_sldb_available(self) -> int:
        if not self._sldb_importable():
            install_path = self._resolve_sldb_checkout()
            if install_path is None:
                print("Error: sldb is not installed and no sibling checkout was found.")
                print(
                    "Set DESKOPS_SLDB_PATH or keep the sibling checkout at ../sldb before running deskops init."
                )
                return 1
            print(f"Installing sldb from {install_path}...")
            try:
                self._run([
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-e",
                    str(install_path),
                ])
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1
            importlib.invalidate_caches()
        elif shutil.which("sldb") is None:
            print("sldb is importable but no shell entrypoint was found; using python -m sldb.")

        return 0

    def ensure_machine_ready(self) -> int:
        ready = self.ensure_sldb_available()
        if ready != 0:
            return ready

        return self.ensure_global_store_and_models()

    def default_pythonpath(self) -> str:
        return str(self._package_root())

    def ensure_global_store_and_models(self) -> int:
        global_store = Path.home() / ".sldb"
        if not global_store.exists():
            print(f"Initializing global store at {global_store}...")
            try:
                self.run_sldb(["stores", "init", "--path", str(Path.home())])
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        try:
            registered = self._registered_model_names(global_store)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1

        for model_name, model_ref in MODEL_REFS.items():
            if model_name in registered:
                continue
            print(f"Registering {model_name} in {global_store}...")
            try:
                self.run_sldb(["models", "add", model_ref, "--store", str(global_store)])
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        print("Global deskops model registry is ready.")
        return 0

    def init_local_store(self, target_path: Path) -> int:
        local_store = target_path / ".sldb"
        if local_store.exists():
            print(f"Local store already exists at {local_store}.")
        else:
            print(f"Initializing local store at {local_store}...")
            try:
                self.run_sldb(["stores", "init", "--path", str(target_path)])
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        try:
            registered = self._registered_model_names(local_store)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1

        for model_name, model_ref in MODEL_REFS.items():
            if model_name in registered:
                continue
            print(f"Registering {model_name} in {local_store}...")
            try:
                self.run_sldb(["models", "add", model_ref, "--store", str(local_store)])
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        return 0

    def run_sldb(self, args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        return self._run([sys.executable, "-m", "sldb", *args], capture_output=capture_output)

    def _registered_model_names(self, store_path: Path) -> set[str]:
        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("models", [])}

    def _sldb_importable(self) -> bool:
        return importlib.util.find_spec("sldb") is not None

    def _resolve_sldb_checkout(self) -> Path | None:
        candidates: list[Path] = []
        env_path = (os.environ.get("DESKOPS_SLDB_PATH") or "").strip()
        if env_path:
            candidates.append(Path(env_path).expanduser())

        package_root = self._package_root()
        repo_root = package_root.parent
        candidates.append(repo_root.parent / "sldb")
        candidates.append(Path.cwd().resolve().parent / "sldb")

        seen: set[Path] = set()
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            if (resolved / "pyproject.toml").exists() and (resolved / "src" / "sldb").exists():
                return resolved
        return None

    def _package_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    def _run(self, command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=capture_output,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise RuntimeError(detail)
        return result
