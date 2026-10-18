from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import re
from types import SimpleNamespace

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.bootstrap import SLDBBootstrap
from deskops.cli.main import main
from deskops import doc_io
from deskops.identity import load_repository_registry
from deskops.identity import EcosystemIdentity
from deskops.models import RepositoryDoc


def _write_repo_doc(
    registry_dir: Path,
    *,
    repo_id: str,
    repo_path: str,
    name: str | None = None,
    filename: str | None = None,
) -> Path:
    payload = {
        "id": repo_id,
        "name": name or repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    path = registry_dir / (filename or f"repo-{repo_id}.md")
    path.write_text(render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8")
    return path


def _write_config(repo_root: Path, project_identity: str) -> None:
    desk_root = repo_root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": project_identity}, indent=2) + "\n",
        encoding="utf-8",
    )


def _init_ecosystem(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(root) == 0
    desk_root = root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": "graph_ui"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return root / ".sldb"


def test_repo_remove_then_register_same_path_under_correct_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A mis-registered id is removable so the same root can be registered again."""
    root = tmp_path / "ecosystem"
    store_path = _init_ecosystem(root)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)

    register_wrong = main([
        "repo", "register", "graph-ui", str(root), "--store", str(store_path),
    ])
    capsys.readouterr()
    assert register_wrong == 0

    registry_file = root / "desk" / "registry" / "repo-graph-ui.md"
    assert registry_file.exists()
    assert doc_io.is_tracked(root, registry_file)

    removed = main(["repo", "remove", "graph-ui", "--store", str(store_path)])
    remove_out = capsys.readouterr().out
    assert removed == 0
    assert str(registry_file) in remove_out
    assert not registry_file.exists()
    assert not doc_io.is_tracked(root, registry_file)

    missing = main(["repo", "remove", "not-registered", "--store", str(store_path)])
    missing_out = capsys.readouterr().out
    assert missing == 1
    assert "not-registered" in missing_out
    assert "(none)" in missing_out

    register_right = main([
        "repo",
        "register",
        "graph_ui",
        str(root),
        "--id",
        "graph_ui",
        "--store",
        str(store_path),
    ])
    capsys.readouterr()
    assert register_right == 0
    assert (root / "desk" / "registry" / "repo-graph_ui.md").exists()

    whoami = main(["repo", "whoami", "--root", str(root), "--store", str(store_path)])
    whoami_out = capsys.readouterr().out
    assert whoami == 0
    assert whoami_out.strip() == "graph_ui"


def test_repo_remove_missing_id_lists_existing_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="graph-ui", repo_path="graph-ui")
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    result = main(["repo", "remove", "ghost", "--store", str(store_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Repository 'ghost' is not registered" in captured.out
    assert "graph-ui" in captured.out
    assert (registry_dir / "repo-graph-ui.md").exists()


def test_resolve_registered_desk_reports_actionable_missing_registry_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "desk" / "registry").mkdir(parents=True)
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="Supported path: run 'deskops repo register <name> --path <abs>'"):
        EcosystemIdentity(str(store_path)).how_do_i_find_another("deskops")



def test_resolve_canonical_project_identity_reports_actionable_unregistered_root_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    _write_config(repo_root, "sender-repo")
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="other-root")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    expected = f"Supported path: run 'deskops repo register <name> --path {repo_root.resolve()}'"
    with pytest.raises(SLDBStoreError, match=re.escape(expected)):
        EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True)



def test_repo_register_accepts_optional_path_flag_and_does_not_crash_on_registry_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "ecosystem"
    desk_root = root / "desk"
    registry_dir = desk_root / "registry"
    registry_dir.mkdir(parents=True)
    store_path = root / ".sldb"
    store_path.mkdir(parents=True)

    _write_repo_doc(registry_dir, repo_id="existing-repo", repo_path="tools/existing-repo")

    tracked: list[str] = []

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.cli.commands.repo.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.cli.commands.repo.find_local_store", lambda: store_path)
    monkeypatch.setattr(
        "deskops.cli.commands.repo.registered_model",
        lambda store, name, pythonpath: (RepositoryDoc, SimpleNamespace(models_index=Path("models-index.yaml")), "documents-idx"),
    )

    class FakeModelsIndex:
        documents_index = Path("documents-index.yaml")

    class FakeDocumentsIndex:
        documents: list[object] = []

    monkeypatch.setattr("sldb.store.io.load_models_index", lambda _path: FakeModelsIndex())
    monkeypatch.setattr("sldb.store.io.load_documents_index", lambda _path: FakeDocumentsIndex())
    monkeypatch.setattr(
        "deskops.cli.commands.repo.track_document",
        lambda store_path_arg, root_arg, idx, model_type, entry, path, note_name, resolver, pythonpath: tracked.append(note_name),
    )

    repo_root = (tmp_path / "external" / "deskops").resolve()
    result = main([
        "repo",
        "register",
        "deskops",
        "--path",
        str(repo_root),
        "--store",
        str(store_path),
    ])

    captured = capsys.readouterr()
    output_path = registry_dir / "repo-deskops.md"

    assert result == 0
    assert output_path.exists()
    assert tracked == ["repo-deskops"]
    assert "Unexpected:" not in captured.out
    assert f"Wrote {output_path}" in captured.out

    entries = load_repository_registry(desk_root, root)
    deskops_entry = next(entry for entry in entries if entry.id == "deskops")
    assert deskops_entry.repo_root == repo_root
