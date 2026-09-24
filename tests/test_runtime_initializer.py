from __future__ import annotations

from pathlib import Path

from deskops.runtime.initializer import build_role_agent_panes

RUNTIME_PI = """---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: inline
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags: []
---

# Pi Runtime

## Summary

Pi runtime.

## Notes

None.
"""


def role_doc(name: str, *, kind: str, tools: str = "[]", model: str = "some/model") -> str:
    return f"""---
id: role-{name}
name: {name}
description: Test role.
kind: {kind}
model: {model}
fallback_models: []
tools: {tools}
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Role {name}
"""


def test_build_role_agent_panes_derives_specs_from_role_and_runtime_docs(tmp_path: Path) -> None:
    """No fixed pair of role names is assumed: this desk has three roles and
    all three get a pane, none of them hardcoded anywhere in the code."""
    write(tmp_path / "desk/runtimes/runtime-pi.md", RUNTIME_PI)
    write(tmp_path / "desk/roles/deskops-executor.md", role_doc("deskops-executor", kind="pi", model="exec/model"))
    write(tmp_path / "desk/roles/deskops-supervisor.md", role_doc("deskops-supervisor", kind="pi", tools="\n- read\n- bash", model="sup/model"))
    write(tmp_path / "desk/roles/deskops-tester.md", role_doc("deskops-tester", kind="pi", tools="\n- read", model="test/model"))

    panes = build_role_agent_panes(tmp_path)

    names = {pane.id for pane in panes}
    assert names == {"deskops-executor", "deskops-supervisor", "deskops-tester"}
    by_name = {pane.id: pane for pane in panes}
    assert by_name["deskops-executor"].agent.kind == "pi"
    assert "--model" in by_name["deskops-executor"].agent.args
    assert "exec/model" in by_name["deskops-executor"].agent.args
    # No declared tools on the executor -> no --tools flag at all.
    assert "--tools" not in by_name["deskops-executor"].agent.args
    assert "--tools" in by_name["deskops-supervisor"].agent.args


def test_build_role_agent_panes_skips_roles_with_no_matching_runtime_profile(tmp_path: Path) -> None:
    """A role naming a kind with no tracked RuntimeProfileDoc is skipped
    rather than guessed at; deskops drift check reports the gap separately."""
    write(tmp_path / "desk/runtimes/runtime-pi.md", RUNTIME_PI)
    write(tmp_path / "desk/roles/deskops-executor.md", role_doc("deskops-executor", kind="pi"))
    write(tmp_path / "desk/roles/deskops-mystery.md", role_doc("deskops-mystery", kind="no-such-runtime"))

    panes = build_role_agent_panes(tmp_path)

    assert {pane.id for pane in panes} == {"deskops-executor"}


def test_build_role_agent_panes_all_parent_root_and_alternate_direction(tmp_path: Path) -> None:
    write(tmp_path / "desk/runtimes/runtime-pi.md", RUNTIME_PI)
    write(tmp_path / "desk/roles/role-a.md", role_doc("role-a", kind="pi"))
    write(tmp_path / "desk/roles/role-b.md", role_doc("role-b", kind="pi"))

    panes = build_role_agent_panes(tmp_path)

    assert all(pane.parent == "root" for pane in panes)
    directions = [pane.direction for pane in panes]
    assert directions == ["right", "down"]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
