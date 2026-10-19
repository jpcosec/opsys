from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.migrate_desk_stores as migrate


def _git_init(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)


def _make_store(
    repo: Path,
    *,
    taskdoc: bool = True,
    contract_hash: str = "0" * 64,
) -> Path:
    store = repo / ".sldb"
    models_dir = store / "core" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    if taskdoc:
        (models_dir / "TaskDoc.yaml").write_text(
            yaml.safe_dump(
                {
                    "name": "TaskDoc",
                    "model_ref": "deskops.models:TaskDoc",
                    "documents_index": ".sldb/core/documents/TaskDoc.yaml",
                    "contract_hash": contract_hash,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (store / "core" / "store_index.yaml").write_text(
            yaml.safe_dump(
                {
                    "stores": [],
                    "models": [
                        {
                            "name": "TaskDoc",
                            "model_ref": "deskops.models:TaskDoc",
                            "models_index": ".sldb/core/models/TaskDoc.yaml",
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
    else:
        (models_dir / "Other.yaml").write_text("name: Other\n", encoding="utf-8")
    return store


def test_discovery_uses_segments_relative_to_the_home_root(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    repo = home / "repo"
    _git_init(repo)
    store = _make_store(repo)

    # tmp_path itself lives under /tmp; only segments relative to --home count.
    assert migrate.discover_stores(home) == [store.resolve()]


@pytest.mark.parametrize(
    "segment", [".cache", ".claude", ".tmp", ".venv", "node_modules", "tools", "tmp"]
)
def test_excluded_segments_are_not_discovered(tmp_path: Path, segment: str) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    repo = home / segment / "repo"
    _git_init(repo)
    _make_store(repo)

    assert migrate.discover_stores(home) == []


def test_stores_under_kimun_are_never_discovered(tmp_path: Path) -> None:
    """The owner forbids the migration to touch kimun (incident of 2026-10-19)."""
    regular = tmp_path / "proyectos" / "regular"
    _git_init(regular)
    kept = _make_store(regular)
    _git_init(tmp_path / "proyectos" / "kimun")
    _make_store(tmp_path / "proyectos" / "kimun" / "docs" / "archive" / "architecture" / "spec2viz")

    assert migrate.discover_stores(tmp_path) == [kept.resolve()]


def test_the_real_kimun_checkout_is_protected_by_absolute_path() -> None:
    kimun_store = Path("/home/jp/proyectos/kimun/docs/archive/architecture/spec2viz/.sldb")

    assert migrate.is_protected(kimun_store, Path("/somewhere/else"))
    assert not migrate.is_protected(Path("/home/jp/proyectos/SLDB_1/deskops/.sldb"), Path("/home/jp"))


def test_store_outside_a_git_work_tree_is_not_discovered(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    _make_store(home / "plain")

    assert migrate.discover_stores(home) == []


def test_store_without_a_tracked_taskdoc_is_not_discovered(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    repo = home / "repo"
    _git_init(repo)
    _make_store(repo, taskdoc=False)

    assert migrate.discover_stores(home) == []


def test_discovery_does_not_descend_into_a_matched_store(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    repo = home / "repo"
    _git_init(repo)
    store = _make_store(repo)
    _make_store(store / "nested")

    assert migrate.discover_stores(home) == [store.resolve()]


def test_changed_contract_plans_a_model_update_and_desk_update(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _git_init(repo)
    store = _make_store(repo, contract_hash="0" * 64)

    models, commands = migrate.plan_store(store)
    rendered = [migrate.format_command(command) for command in commands]

    assert models == ["TaskDoc"]
    assert any("models update TaskDoc" in line for line in rendered)
    assert any(f"--pythonpath {ROOT}" in line for line in rendered)
    assert any(
        "desk update --root" in line and "--apply" in line for line in rendered
    )
    assert rendered[0].endswith(f"stores check --store {store.resolve()}")
    assert rendered[-1].endswith(f"stores check --store {store.resolve()}")


def test_unchanged_contract_skips_the_model_update(tmp_path: Path) -> None:
    from sldb.store.hashing import hash_model_contract

    from deskops.models import TaskDoc

    repo = tmp_path / "repo"
    _git_init(repo)
    store = _make_store(repo, contract_hash=hash_model_contract(TaskDoc))

    models, commands = migrate.plan_store(store)
    rendered = [migrate.format_command(command) for command in commands]

    assert models == []
    assert not any("models update" in line for line in rendered)
    assert any("desk update --root" in line for line in rendered)


def test_dry_run_exits_zero_only_when_a_store_was_found(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    monkeypatch.setattr(migrate, "LOG_DIR", tmp_path / "logs")

    assert migrate.main(["--home", str(home), "--dry-run"]) == 1

    repo = home / "repo"
    _git_init(repo)
    _make_store(repo)

    assert migrate.main(["--home", str(home), "--dry-run"]) == 0
