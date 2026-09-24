from __future__ import annotations

from pathlib import Path

from deskops.materializers.runtime_profiles import (
    build_agent_spec_args,
    drift_check_runtime_bindings,
    load_runtime_profiles,
)

PI_PROFILE = {
    "kind": "pi",
    "model_flag": "--model",
    "fallback_models_flag": "",
    "fallback_models_join": "comma",
    "tools_flag": "--tools",
    "tools_join": "comma",
    "system_prompt_flag": "--append-system-prompt",
    "system_prompt_delivery": "inline",
    "session_flag": "--session",
    "extra_args": [],
    "unsupported_role_fields": ["fallback_models"],
}

CLAUDE_PROFILE = {
    "kind": "claude",
    "model_flag": "--model",
    "fallback_models_flag": "",
    "fallback_models_join": "comma",
    "tools_flag": "--allowedTools",
    "tools_join": "repeat",
    "system_prompt_flag": "--append-system-prompt",
    "system_prompt_delivery": "file",
    "session_flag": "--resume",
    "extra_args": ["--print"],
    "unsupported_role_fields": ["fallback_models"],
}

EXECUTOR_ROLE = {
    "name": "deskops-executor",
    "kind": "pi",
    "model": "openai-codex/gpt-5.4",
    "fallback_models": ["google-gemini-cli/gemini-3.1-pro-preview"],
    "tools": [],
    "body": "# Workflow Executor",
}

SUPERVISOR_ROLE = {
    "name": "deskops-supervisor",
    "kind": "pi",
    "model": "anthropic/claude-opus-4-8",
    "fallback_models": [],
    "tools": ["read", "grep", "find", "ls", "bash"],
    "body": "# Workflow Supervisor",
}


def test_build_agent_spec_args_omits_flags_for_empty_role_values() -> None:
    """The executor has no declared tools; its --tools flag must not appear
    at all, matching the render_pi_agent_markdown fix for the same bug."""
    args = build_agent_spec_args(EXECUTOR_ROLE, PI_PROFILE)

    assert args == ("--model", "openai-codex/gpt-5.4", "--append-system-prompt", "# Workflow Executor")


def test_build_agent_spec_args_comma_joins_tools() -> None:
    args = build_agent_spec_args(SUPERVISOR_ROLE, PI_PROFILE)

    assert "--tools" in args
    assert args[args.index("--tools") + 1] == "read,grep,find,ls,bash"


def test_build_agent_spec_args_repeat_joins_tools() -> None:
    args = build_agent_spec_args(SUPERVISOR_ROLE, CLAUDE_PROFILE, system_prompt_path="/tmp/prompt.md")

    tools_positions = [i for i, a in enumerate(args) if a == "--allowedTools"]
    assert len(tools_positions) == 5
    assert [args[i + 1] for i in tools_positions] == ["read", "grep", "find", "ls", "bash"]


def test_build_agent_spec_args_file_delivery_needs_a_path() -> None:
    """system_prompt_delivery=file must not inline the body as a flag value,
    and must not emit the flag at all when no file path was written yet."""
    without_path = build_agent_spec_args(SUPERVISOR_ROLE, CLAUDE_PROFILE)
    assert "--append-system-prompt" not in without_path

    with_path = build_agent_spec_args(SUPERVISOR_ROLE, CLAUDE_PROFILE, system_prompt_path="/tmp/prompt.md")
    assert "--append-system-prompt" in with_path
    assert with_path[with_path.index("--append-system-prompt") + 1] == "/tmp/prompt.md"
    assert "# Workflow Supervisor" not in with_path


def test_build_agent_spec_args_inline_delivery_passes_body_directly() -> None:
    args = build_agent_spec_args(SUPERVISOR_ROLE, PI_PROFILE)

    assert "--append-system-prompt" in args
    assert args[args.index("--append-system-prompt") + 1] == "# Workflow Supervisor"


def test_build_agent_spec_args_appends_session_and_extra_args() -> None:
    args = build_agent_spec_args(SUPERVISOR_ROLE, CLAUDE_PROFILE, session_path="runs/subagents/x/session.jsonl", system_prompt_path="/tmp/p.md")

    assert "--resume" in args
    assert args[args.index("--resume") + 1] == "runs/subagents/x/session.jsonl"
    assert args[-1] == "--print"


def test_build_agent_spec_args_respects_unsupported_and_missing_flags() -> None:
    """fallback_models has no flag on either profile; it must never surface,
    regardless of whether the role declares it."""
    args = build_agent_spec_args(EXECUTOR_ROLE, PI_PROFILE)

    assert "--fallback-models" not in " ".join(args)
    assert "google-gemini-cli/gemini-3.1-pro-preview" not in args


def test_load_runtime_profiles_keys_by_kind(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/runtimes/runtime-pi.md",
        """---
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
unsupported_role_fields: []
tags: []
---

# Pi Runtime

## Summary

Pi runtime.

## Notes

None.
""",
    )

    profiles = load_runtime_profiles(tmp_path)

    assert set(profiles) == {"pi"}
    assert profiles["pi"]["binary"] == "pi"


def test_drift_check_runtime_bindings_flags_missing_profile(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/roles/deskops-executor.md",
        role_doc_markdown("deskops-executor", kind="codex", tools=[], fallback_models=[]),
    )

    findings = drift_check_runtime_bindings(tmp_path)

    assert any("missing runtime profile for kind 'codex'" in f for f in findings)


def test_drift_check_runtime_bindings_flags_silent_tool_loss(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/runtimes/runtime-pi.md",
        """---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: ''
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: inline
session_flag: --session
extra_args: []
unsupported_role_fields: []
tags: []
---

# Pi Runtime

## Summary

Pi runtime with no tools flag and no acknowledgement of that gap.

## Notes

None.
""",
    )
    write(
        tmp_path / "desk/roles/deskops-supervisor.md",
        role_doc_markdown("deskops-supervisor", kind="pi", tools=["read", "grep"], fallback_models=[]),
    )

    findings = drift_check_runtime_bindings(tmp_path)

    assert any("silent capability loss" in f and "tools" in f for f in findings)


def test_drift_check_runtime_bindings_accepts_declared_unsupported_field(tmp_path: Path) -> None:
    """The same gap as above, but the profile explicitly lists 'tools' as
    unsupported: this must not be reported, since it is acknowledged."""
    write(
        tmp_path / "desk/runtimes/runtime-pi.md",
        """---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: ''
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: inline
session_flag: --session
extra_args: []
unsupported_role_fields:
- tools
tags: []
---

# Pi Runtime

## Summary

Pi runtime that deliberately does not support tools.

## Notes

None.
""",
    )
    write(
        tmp_path / "desk/roles/deskops-supervisor.md",
        role_doc_markdown("deskops-supervisor", kind="pi", tools=["read", "grep"], fallback_models=[]),
    )

    findings = drift_check_runtime_bindings(tmp_path)

    assert findings == []


def role_doc_markdown(name: str, *, kind: str, tools: list[str], fallback_models: list[str]) -> str:
    tools_yaml = "[]" if not tools else "\n" + "\n".join(f"- {t}" for t in tools)
    fallback_yaml = "[]" if not fallback_models else "\n" + "\n".join(f"- {m}" for m in fallback_models)
    return f"""---
id: role-{name}
name: {name}
description: Test role.
kind: {kind}
model: some/model
fallback_models: {fallback_yaml}
tools: {tools_yaml}
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Test role
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
