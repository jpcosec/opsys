from __future__ import annotations

import json
from pathlib import Path
import re
from types import SimpleNamespace

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.identity import load_repository_registry
from deskops.identity import resolve_canonical_project_identity
from deskops.identity import resolve_registered_desk
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


def test_resolve_registered_desk_reports_actionable_missing_registry_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "desk" / "registry").mkdir(parents=True)
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="Supported path: run 'deskops repo register <name> --path <abs>'"):
        resolve_registered_desk("deskops", str(store_path))



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
        resolve_canonical_project_identity(repo_root, str(store_path))



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
