from pathlib import Path
from deskops.config import DeskConfig

def test_load_desk_config_defaults(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    config = DeskConfig.load(desk)
    assert config.project_identity == "unknown-project"
    assert config.versions.desk_format == "1.0.0"
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
    # The sandbox_root should remain from the main config because of dict update
    assert config.sandbox.sandbox_root == "/tmp/test"
