from pathlib import Path

import pytest

from deskops.config import DeskConfig
from deskops.constants import CURRENT_DESK_FORMAT

def test_load_desk_config_defaults(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    config = DeskConfig.load(desk)
    assert config.project_identity == "unknown-project"
    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert not config.sandbox.enabled

def test_load_desk_config_from_json(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": true,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"

def test_load_desk_config_local_override(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": false,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "sandbox": {
            "enabled": true
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"


def test_load_desk_config_deep_merges_nested_versions(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "versions": {
            "desk_format": "1.0.0",
            "model_version": "1.0.0"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "versions": {
            "model_version": "2.0.0"
        }
    }
    ''')

    config = DeskConfig.load(desk)

    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert config.versions.model_version == "2.0.0"


def test_load_desk_config_surfaces_malformed_json_warning(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('{"sandbox": {"enabled": true}')

    with pytest.warns(UserWarning, match="Failed to parse desk config"):
        config = DeskConfig.load(desk)

    assert config.has_load_warnings is True
    assert config.load_warnings
    assert config.sandbox.enabled is False
