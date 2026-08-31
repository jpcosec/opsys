from __future__ import annotations

import json
from pathlib import Path

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.identity import infer_sender_project_identity
from deskops.identity import load_repository_registry
from deskops.identity import resolve_registered_desk
from deskops.models import RepositoryDoc


def _write_repo_doc(registry_dir: Path, *, repo_id: str, repo_path: str, name: str | None = None, filename: str | None = None) -> Path:
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


def test_repo_identity_resolver_returns_single_registered_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    (repo_root / "desk").mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="sender-repo", name="Sender Repo")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    assert resolve_registered_desk("sender-repo", str(store_path)) == (repo_root / "desk").resolve()
    assert infer_sender_project_identity(repo_root / "subdir", str(store_path)) == "sender-repo"


def test_repo_identity_resolver_fails_on_duplicate_id(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-one", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-two", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository id 'shared-id'"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_identity_resolver_fails_on_duplicate_root(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="repo-one", repo_path="shared-root", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="repo-two", repo_path="shared-root", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository root"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_whoami_prints_canonical_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "deskops-child"
    _write_config(repo_root, "deskops-child")
    _write_repo_doc(registry_dir, repo_id="deskops-child", repo_path="deskops-child")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    result = main(["repo", "whoami", "--root", str(repo_root), "--store", str(store_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "deskops-child"
