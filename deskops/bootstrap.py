from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

from sldb import StructuredNLDoc

from deskops import doc_io
from deskops import models as deskops_models


DESKOPS_STORE_LINK = "deskops"

#: Base classes that are never registered as models in a store.
BASE_MODEL_NAMES = frozenset({"PrimitiveDoc", "OperationalArtifactDoc"})

#: Every deskops model is inherited from the owner store by name and model ref.
MODEL_REFS = {
    name: f"deskops.models:{name}"
    for name in deskops_models.__all__
    if name not in BASE_MODEL_NAMES
    and isinstance(getattr(deskops_models, name, None), type)
    and issubclass(getattr(deskops_models, name), StructuredNLDoc)
}


class SLDBBootstrap:
    def ensure_sldb_available(self, *, allow_install: bool = False) -> int:
        """Check that sldb is importable.

        Only ``deskops bootstrap`` and ``deskops init`` may install it; every other
        command fails with the install hint instead of running pip behind the user's back.
        """
        if self._sldb_importable():
            if shutil.which("sldb") is None:
                print("sldb is importable but no shell entrypoint was found; using python -m sldb.")
            return 0

        if not allow_install:
            print(
                "Error: sldb is not installed. Run 'deskops bootstrap' or 'deskops init' to install it."
            )
            return 1

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

        return 0

    def ensure_machine_ready(self) -> int:
        ready = self.ensure_sldb_available(allow_install=True)
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
                self._init_store(Path.home())
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        result = self._register_models(global_store)
        if result != 0:
            return result

        print("Global deskops model registry is ready.")
        return 0

    def init_local_store(self, target_path: Path) -> int:
        local_store = target_path / ".sldb"
        if local_store.exists():
            print(f"Local store already exists at {local_store}.")
        else:
            print(f"Initializing local store at {local_store}...")
            try:
                self._init_store(target_path)
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        return self._register_models(local_store)

    def _register_models(self, store_path: Path) -> int:
        """Link the deskops owner store and inherit the model set from it.

        A model registered here as a copy of the deskops class is converted in place by
        `inherit_model`, keeping its documents and signed contract.
        """
        try:
            owner = self._deskops_owner_store()
            link_state = self._ensure_owner_link(store_path, owner)
            if link_state is None:
                # The name is already taken by another checkout. sldb cannot replace a
                # link, so leave this store as it is instead of inheriting from it.
                print(
                    f"Skipping model registration in {store_path}: '{DESKOPS_STORE_LINK}' is linked elsewhere."
                )
                return 0
            if link_state:
                print(f"Linked {owner} as {DESKOPS_STORE_LINK} in {store_path}.")

            entries = self._registered_model_entries(store_path)
            for model_name, model_ref in MODEL_REFS.items():
                entry = entries.get(model_name)
                if entry is not None:
                    origin = getattr(entry, "origin", None)
                    if origin == DESKOPS_STORE_LINK:
                        continue
                    if origin or getattr(entry, "model_ref", None) != model_ref:
                        continue
                print(f"Inheriting {model_name} in {store_path}...")
                self._inherit_model(model_name, store_path)

            self._init_relations(store_path)
            self._update_store_indexes(store_path)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1

        return 0

    def _deskops_owner_store(self) -> Path:
        owner = self._package_root() / ".sldb"
        if not owner.exists():
            raise RuntimeError(
                f"deskops owner store not found at {owner}; the deskops models must be registered in the deskops repo's .sldb"
            )
        return owner

    def _ensure_owner_link(self, store_path: Path, owner: Path) -> bool | None:
        """Link `owner` as `deskops` unless the store already links that name.

        Returns True when the link was added, False when it already points at `owner`,
        and None when the name is linked to a different (stale) store.
        """
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                existing = next(
                    (link for link in idx.stores if link.name == DESKOPS_STORE_LINK),
                    None,
                )
                if existing is not None:
                    target = (store_path.parent / existing.path).resolve()
                    if target == owner.resolve():
                        return False
                    print(
                        f"Warning: {store_path} already links '{DESKOPS_STORE_LINK}' to {target}, "
                        f"not to {owner}."
                    )
                    return None
                doc_io.link_store_alias(store_path.parent, owner, DESKOPS_STORE_LINK)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            existing = self._store_link_names(store_path)
            if DESKOPS_STORE_LINK in existing:
                return False
            self.run_sldb([
                "stores",
                "add",
                str(owner),
                "--name",
                DESKOPS_STORE_LINK,
                "--store",
                str(store_path),
            ])
        return True

    def _inherit_model(self, model_name: str, store_path: Path) -> None:
        ref = f"{DESKOPS_STORE_LINK}:{model_name}"
        if self._sldb_importable():
            try:
                doc_io.inherit_model_from(store_path.parent, ref, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "models",
                "inherit",
                ref,
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _init_relations(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_relations_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "edges",
                "init",
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _update_store_indexes(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.update_store_indexes_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "update", "--store", str(store_path)])

    def run_sldb(self, args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        return self._run([sys.executable, "-m", "sldb", *args], capture_output=capture_output)

    def _init_store(self, target_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_store_at(target_path)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "init", "--path", str(target_path)])

    def _registered_model_entries(self, store_path: Path) -> dict[str, Any]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {m.name: m for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"]: entry for entry in payload.get("models", [])}

    def _store_link_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {link.name for link in idx.stores}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["stores", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("stores", [])}

    def _registered_model_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index
            try:
                idx = load_store_index(store_path)
                return {m.name for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

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
