"""Message delivery must not depend on the target desk registering the sender.

These are the three failures reported on 2026-10-18:

* a target without ``project_identity`` refused the note,
* a sender was resolved against the target's registry (so a repo that only
  registered itself made every foreign sender unresolvable),
* ``ack`` stopped finding the repo itself once its registry registered some
  other repo.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.models import InboxNoteDoc
from deskops.models import RepositoryDoc
from sldb.runtime.validation import render_model_markdown


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    result = _cli(path, "init", str(path))
    assert result.returncode == 0, result.stderr or result.stdout
    return path


def _register(repo: Path, repo_id: str, repo_path: str) -> None:
    registry_dir = repo / "desk" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": repo_id,
        "name": repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    (registry_dir / f"repo-{repo_id}.md").write_text(
        render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8"
    )


def _write_note(repo: Path, stem: str, *, target_project: str) -> Path:
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "suggestion",
        "sender_project": "sender-repo",
        "target_project": target_project,
        "created_at": "2026-01-01T00:00:00",
        "status": "open",
        "title": "Ack me",
        "body": "Please acknowledge this note.",
    }
    note = inbox / f"{stem}.md"
    note.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
    return note


def test_send_to_target_without_project_identity_uses_directory_name(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "TraderBot")
    (target / "desk" / "config.json").write_text("{}\n", encoding="utf-8")

    result = _cli(
        sender,
        "message",
        "send",
        "A note for an unconfigured desk.",
        "--title",
        "No identity",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["sender_project"] == "sender-repo"
    assert payload["target_project"] == "TraderBot"
    assert "no project_identity" in result.stderr
    assert len(list((target / "desk" / "inbox").glob("*.md"))) == 1


def test_send_resolves_sender_from_sender_repo_not_target_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "target-repo")
    # The target's local registry knows only itself, exactly like the reported case.
    _register(target, "target-repo", str(target))

    without_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "No sender override",
        "--root",
        str(target),
        "--format",
        "json",
    )
    with_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "Explicit sender",
        "--from",
        "sender-repo",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert without_from.returncode == 0, without_from.stderr or without_from.stdout
    assert with_from.returncode == 0, with_from.stderr or with_from.stdout
    assert json.loads(without_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(with_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(without_from.stdout)["target_project"] == "target-repo"


def test_ack_falls_back_to_config_when_registry_lacks_itself(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "graph-repo")
    # Registering somebody else used to hide the repo's own identity from ack.
    _register(repo, "graph_ui", str(tmp_path / "elsewhere"))
    note = _write_note(repo, "20260101-000000-suggestion-ackme", target_project="graph-repo")

    result = _cli(
        repo,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "closed"
    assert payload["acknowledged_by"] == "graph-repo"
    assert payload["target_project"] == "graph-repo"
