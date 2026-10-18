from __future__ import annotations

from pathlib import Path

from deskops import paths
from deskops.bootstrap import MODEL_REFS
from deskops.bootstrap import SLDBBootstrap
from deskops.specs.loader import SpecRegistry


def test_package_pythonpath_is_the_directory_containing_deskops() -> None:
    package_parent = Path(paths.package_pythonpath())

    assert (package_parent / "deskops" / "paths.py").is_file()
    assert SLDBBootstrap().default_pythonpath() == paths.package_pythonpath()


def test_runtime_specs_and_faq_ship_inside_the_package() -> None:
    assert paths.data_path("spec", "workflows", "task_lifecycle.yaml").is_file()
    assert paths.data_path("data", "faq.md").is_file()
    registry = SpecRegistry.load(paths.data_path("spec"))
    assert "artifact.task" in registry.artifacts
    assert "field.goal" in registry.fields


def test_packaged_faq_matches_the_human_copy() -> None:
    repo_faq = Path(__file__).resolve().parents[1] / "docs" / "faq.md"

    assert paths.data_path("data", "faq.md").read_text(encoding="utf-8") == repo_faq.read_text(encoding="utf-8")


def test_register_models_falls_back_when_no_owner_store_is_installed(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    root = tmp_path / "repo"
    root.mkdir()

    assert SLDBBootstrap().init_local_store(root) == 0

    from sldb.store.io import load_store_index

    entries = {entry.name: entry for entry in load_store_index(root / ".sldb").models}
    for name, model_ref in MODEL_REFS.items():
        assert entries[name].origin is None
        assert entries[name].model_ref == model_ref
    assert "registering the models directly" in capsys.readouterr().out


def test_desk_update_is_clean_with_directly_registered_models(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out
