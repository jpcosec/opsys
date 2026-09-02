from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from deskops.graph.extract_docs import extract_doc_nodes
from deskops.materializers.roles import render_pi_agent_markdown
from deskops.models import RoleDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


SUPERVISOR_ROLE = {
    "id": "role-deskops-supervisor",
    "name": "deskops-supervisor",
    "description": "Use when acting as the desk workflow supervisor in this repository.",
    "body": "# Workflow Supervisor\n\nUse this skill when your role is **supervisor**.",
}


def test_role_doc_roundtrips_and_preserves_body() -> None:
    rendered = render_model_markdown(RoleDoc, SUPERVISOR_ROLE)
    extracted = extract_model_data(RoleDoc, rendered)

    assert extracted == SUPERVISOR_ROLE
    assert rendered.startswith("---\nid: role-deskops-supervisor\nname: deskops-supervisor\n")
    assert "# Workflow Supervisor" in rendered
    assert "Use this skill when your role is **supervisor**." in rendered


def test_materialize_renders_role_docs_to_out_dir_and_drift_checks(tmp_path: Path, capsys) -> None:
    role_dir = tmp_path / "desk" / "roles"
    role_dir.mkdir(parents=True)
    (role_dir / "deskops-supervisor.md").write_text(render_model_markdown(RoleDoc, SUPERVISOR_ROLE) + "\n", encoding="utf-8")

    out_dir = tmp_path / "agents"
    materialize = main(["materialize", "--root", str(tmp_path), "--out", str(out_dir)])
    materialized = capsys.readouterr()

    assert materialize == 0
    assert "Materialized desk/roles/deskops-supervisor.md" in materialized.out

    output_path = out_dir / "deskops-supervisor.md"
    assert output_path.exists()
    expected = render_pi_agent_markdown(SUPERVISOR_ROLE)
    assert output_path.read_text(encoding="utf-8") == expected
    assert "tools:" in expected
    assert "model: anthropic/claude-opus-4-8" in expected

    clean = main(["drift", "check", "--root", str(tmp_path), "--out", str(out_dir)])
    clean_out = capsys.readouterr()
    assert clean == 0
    assert "No role-agent drift found." in clean_out.out

    output_path.write_text(output_path.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
    drifted = main(["drift", "check", "--root", str(tmp_path), "--out", str(out_dir)])
    drifted_out = capsys.readouterr()
    assert drifted == 1
    assert "Role-agent drift findings:" in drifted_out.out
    assert str(output_path) in drifted_out.out


def test_extract_doc_nodes_includes_role_docs(tmp_path: Path) -> None:
    role_path = tmp_path / "desk" / "roles" / "deskops-supervisor.md"
    role_path.parent.mkdir(parents=True)
    role_path.write_text(render_model_markdown(RoleDoc, SUPERVISOR_ROLE) + "\n", encoding="utf-8")

    nodes = extract_doc_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "role:role-deskops-supervisor" in by_id
    assert by_id["role:role-deskops-supervisor"].path == "desk/roles/deskops-supervisor.md"
    assert by_id["role:role-deskops-supervisor"].document_id == "role-deskops-supervisor"
