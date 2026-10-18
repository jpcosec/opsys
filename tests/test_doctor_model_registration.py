from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

from deskops import models as deskops_models
from deskops.bootstrap import MODEL_REFS
from deskops.cli.main import main
from deskops.paths import package_pythonpath
from deskops.workspace import scaffold_desk


def _init_repo(root: Path, capsys) -> None:
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()


def _mock_registered_missing(monkeypatch, missing: str) -> None:
    registered = set(MODEL_REFS) - {missing}
    monkeypatch.setattr(
        "deskops.cli.commands.doctor.SLDBBootstrap._registered_model_names",
        lambda self, store: registered,
    )


def test_doctor_reports_unregistered_models_with_proposal(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    _mock_registered_missing(monkeypatch, "StepDoc")

    assert main(["doctor", "--root", str(root)]) == 1
    out, _ = capsys.readouterr()
    assert "Unregistered models: StepDoc" in out
    assert "deskops desk update --apply" in out
    assert "Run with --repair to attempt automatic fixes." in out


def test_doctor_skips_model_check_when_index_unreadable(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)

    def _boom(self, store):  # type: ignore[no-untyped-def]
        raise RuntimeError("broken index")

    monkeypatch.setattr(
        "deskops.cli.commands.doctor.SLDBBootstrap._registered_model_names",
        _boom,
    )

    assert main(["doctor", "--root", str(root)]) == 1
    out, _ = capsys.readouterr()
    assert "Could not read the local .sldb store index; unregistered-model check skipped." in out
    assert "Unregistered models:" not in out


def test_doctor_skips_model_check_without_store(tmp_path: Path, capsys) -> None:
    root = tmp_path / "project"
    root.mkdir()
    scaffold_desk(root)

    assert main(["doctor", "--root", str(root)]) == 1
    out, _ = capsys.readouterr()
    assert "SLDB store check crashed" in out
    assert "Unregistered models:" not in out


def _git(root: Path, *argv: str) -> None:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_init_registers_every_deskops_model(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "seed.txt")
    _git(root, "commit", "-q", "-m", "seed")

    env = {**os.environ, "HOME": str(tmp_path / "home")}
    result = subprocess.run(
        [sys.executable, "-m", "deskops", "init", str(root)],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr or result.stdout

    store_index = root / ".sldb" / "core" / "store_index.yaml"
    assert store_index.exists()
    names = {
        entry["name"]
        for entry in (yaml.safe_load(store_index.read_text(encoding="utf-8")) or {}).get("models") or []
    }
    expected = (
        set(deskops_models.__all__) - {"PrimitiveDoc", "OperationalArtifactDoc"}
    ) | {"RelationTypeDoc", "RelationDoc"}
    assert names == expected


def test_non_bootstrap_command_does_not_install_sldb(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr("deskops.bootstrap.SLDBBootstrap._sldb_importable", lambda self: False)
    monkeypatch.setattr(
        "deskops.bootstrap.SLDBBootstrap._resolve_sldb_checkout",
        lambda self: tmp_path / "sldb",
    )
    install_calls: list[list[str]] = []

    def spy(self, command, *, capture_output=False):  # type: ignore[no-untyped-def]
        install_calls.append(command)
        raise AssertionError(f"unexpected command: {command}")

    monkeypatch.setattr("deskops.bootstrap.SLDBBootstrap._run", spy)

    assert main(["list", "tasks", "--root", str(tmp_path)]) == 1
    out, _ = capsys.readouterr()
    assert "Error: sldb is not installed" in out
    assert install_calls == []


def test_doctor_repair_registers_missing_models_idempotently(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    _mock_registered_missing(monkeypatch, "StepDoc")

    assert main(["doctor", "--root", str(root), "--repair"]) == 0
    out, _ = capsys.readouterr()
    assert "Registered missing models." in out
    assert "Unregistered models: StepDoc" in out

    assert main(["doctor", "--root", str(root), "--repair"]) == 0
    out, _ = capsys.readouterr()
    assert "Registered missing models." in out


def _store_index(root: Path) -> dict:
    path = root / ".sldb" / "core" / "store_index.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _deskops_link(root: Path) -> dict:
    return next(entry for entry in _store_index(root)["stores"] if entry["name"] == "deskops")


def _point_deskops_link_at(root: Path, target: Path) -> None:
    path = root / ".sldb" / "core" / "store_index.yaml"
    index = _store_index(root)
    for entry in index["stores"]:
        if entry["name"] == "deskops":
            entry["path"] = os.path.relpath(target, root)
    path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")


def _sldb_stores_check(store: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store), "--quiet"],
        capture_output=True,
        text=True,
        env={**os.environ},
    )


def test_init_repairs_a_broken_deskops_link(tmp_path: Path, capsys) -> None:
    root = tmp_path / "repo"
    _init_repo(root, capsys)
    owner = (Path(package_pythonpath()) / ".sldb").resolve()

    deleted = tmp_path / "deleted" / ".sldb"
    deleted.mkdir(parents=True)
    _point_deskops_link_at(root, deleted)
    shutil.rmtree(tmp_path / "deleted")

    assert main(["init", str(root)]) == 0
    out, _ = capsys.readouterr()
    assert "Replaced broken 'deskops' link" in out
    assert (root / _deskops_link(root)["path"]).resolve() == owner

    check = _sldb_stores_check(root / ".sldb")
    assert check.returncode == 0, check.stdout + check.stderr


def test_init_leaves_a_healthy_deskops_link_to_another_store(tmp_path: Path, capsys) -> None:
    root = tmp_path / "repo"
    _init_repo(root, capsys)
    other = tmp_path / "other"
    _init_repo(other, capsys)
    other_store = (other / ".sldb").resolve()

    _point_deskops_link_at(root, other_store)

    assert main(["init", str(root)]) == 0
    out, _ = capsys.readouterr()
    assert "already links 'deskops'" in out
    assert (root / _deskops_link(root)["path"]).resolve() == other_store
