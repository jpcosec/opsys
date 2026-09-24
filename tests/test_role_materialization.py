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
    "kind": "pi",
    "model": "anthropic/claude-opus-4-8",
    "fallback_models": ["openai-codex/gpt-5.4"],
    "tools": ["read", "grep", "find", "ls", "bash"],
    "system_prompt_mode": "replace",
    "inherit_project_context": True,
    "inherit_skills": True,
    "default_context": "fresh",
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
    # A tracked RuntimeProfileDoc for the role's kind is required for a clean
    # drift check (see drift_check_runtime_bindings); without one the check
    # correctly reports "missing runtime profile for kind 'pi'".
    runtime_dir = tmp_path / "desk" / "runtimes"
    runtime_dir.mkdir(parents=True)
    (runtime_dir / "runtime-pi.md").write_text(
        "---\nid: runtime-pi\nstatus: active\nkind: pi\nbinary: pi\nmodel_flag: --model\n"
        "fallback_models_flag: ''\nfallback_models_join: comma\ntools_flag: --tools\ntools_join: comma\n"
        "system_prompt_flag: --append-system-prompt\nsystem_prompt_delivery: inline\nsession_flag: --session\n"
        "extra_args: []\nunsupported_role_fields:\n- fallback_models\ntags: []\n---\n\n"
        "# Pi Runtime\n\n## Summary\n\nPi runtime.\n\n## Notes\n\nNone.\n",
        encoding="utf-8",
    )

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
    assert "No drift found." in clean_out.out

    output_path.write_text(output_path.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
    drifted = main(["drift", "check", "--root", str(tmp_path), "--out", str(out_dir)])
    drifted_out = capsys.readouterr()
    assert drifted == 1
    assert "Drift findings:" in drifted_out.out
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


def test_render_pi_agent_markdown_omits_empty_tools_and_empty_model() -> None:
    """Regression: an empty tools list or empty model must be omitted, not
    emitted as `tools: []` / `model: ''`.

    A role with no declared tool allowlist (like the executor, the only role
    allowed to write code) must materialize with NO `tools:` key at all, so
    the runtime falls back to its own default toolset. Emitting `tools: []`
    would instead grant zero tools and silently disable the role.
    """
    executor_role = {
        "id": "role-deskops-executor",
        "name": "deskops-executor",
        "description": "Use when acting as the executor.",
        "kind": "pi",
        "model": "openai-codex/gpt-5.4",
        "fallback_models": [],
        "tools": [],
        "system_prompt_mode": "replace",
        "inherit_project_context": True,
        "inherit_skills": True,
        "default_context": "fresh",
        "body": "# Workflow Executor",
    }

    rendered = render_pi_agent_markdown(executor_role)
    frontmatter = rendered.split("---")[1]

    assert "tools" not in frontmatter
    assert "fallbackModels" not in frontmatter
    assert "model: openai-codex/gpt-5.4" in frontmatter


def test_render_pi_agent_markdown_keeps_non_empty_tools() -> None:
    rendered = render_pi_agent_markdown(SUPERVISOR_ROLE)
    frontmatter = rendered.split("---")[1]

    assert "tools:" in frontmatter
    assert "- read" in frontmatter


def test_render_pi_agent_markdown_keeps_false_booleans() -> None:
    """A False boolean is a meaningful, explicit value and must never be
    dropped by the same filter that omits empty strings and empty lists."""
    role = dict(SUPERVISOR_ROLE, inherit_project_context=False)

    rendered = render_pi_agent_markdown(role)
    frontmatter = rendered.split("---")[1]

    assert "inheritProjectContext: false" in frontmatter
