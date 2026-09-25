from __future__ import annotations

from pathlib import Path

from deskops.bootstrap import MODEL_REFS
from deskops.cli.main import main
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
    _mock_registered_missing(monkeypatch, "RoutineDoc")

    assert main(["doctor", "--root", str(root)]) == 1
    out, _ = capsys.readouterr()
    assert "Unregistered models: RoutineDoc" in out
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


def test_doctor_repair_registers_missing_models_idempotently(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    _mock_registered_missing(monkeypatch, "RoutineDoc")

    assert main(["doctor", "--root", str(root), "--repair"]) == 0
    out, _ = capsys.readouterr()
    assert "Registered missing models." in out
    assert "Unregistered models: RoutineDoc" in out

    assert main(["doctor", "--root", str(root), "--repair"]) == 0
    out, _ = capsys.readouterr()
    assert "Registered missing models." in out
