from pydantic import Field

from .base import PrimitiveDoc


class RuntimeProfileDoc(PrimitiveDoc):
    """Declares how one agent runtime kind translates abstract role settings
    (model, tools, system prompt, session) into that binary's CLI flags.

    Adding support for a new runtime is writing one of these documents, not
    editing Python. The vocabulary is deliberately closed: a flag name per
    capability plus an enumerated join/delivery mode, never an expression
    language or per-flag scripting.
    """

    __semantics__ = {"type": ["workflow", "runtime_profile"], "workspace": ["desk", "runtimes"]}
    __template__ = """---
# runtime-xxx
id: ⸢rev•id⸥
# draft | active | archived
status: ⸢rev•status⸥
# Runtime binary identifier matching RoleDoc.kind values, e.g. pi, claude, codex
kind: ⸢rev•kind⸥
binary: ⸢rev•binary⸥
# Empty means this runtime does not support that capability
model_flag: ⸢rev•model_flag⸥
fallback_models_flag: ⸢rev•fallback_models_flag⸥
# comma | space | repeat
fallback_models_join: ⸢rev•fallback_models_join⸥
tools_flag: ⸢rev•tools_flag⸥
# comma | space | repeat
tools_join: ⸢rev•tools_join⸥
system_prompt_flag: ⸢rev•system_prompt_flag⸥
# inline | file
system_prompt_delivery: ⸢rev•system_prompt_delivery⸥
session_flag: ⸢rev•session_flag⸥
extra_args: ⸢rev•extra_args⸥
# RoleDoc fields this runtime cannot honor
unsupported_role_fields: ⸢rev•unsupported_role_fields⸥
# e.g. system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this runtime is and when to use it._

⸢rev•summary⸥

## Notes

_Operational notes such as authentication requirements or version pins._

⸢rev•notes⸥
""".strip()

    kind: str = Field(
        description="Runtime binary identifier this profile targets, matching RoleDoc.kind values (e.g. 'pi', 'claude', 'codex')."
    )
    binary: str = Field(description="Executable name or path Herdr invokes to start this runtime kind.")
    model_flag: str = Field(
        default="", description="CLI flag used to pass the primary model id; empty means this runtime has no model flag."
    )
    fallback_models_flag: str = Field(
        default="", description="CLI flag used to pass fallback model ids; empty means unsupported."
    )
    fallback_models_join: str = Field(
        default="comma",
        description="How multiple fallback model values are combined for fallback_models_flag: 'comma', 'space', or 'repeat'.",
    )
    tools_flag: str = Field(
        default="", description="CLI flag used to pass the tool allowlist; empty means unsupported."
    )
    tools_join: str = Field(
        default="comma", description="How multiple tool values are combined for tools_flag: 'comma', 'space', or 'repeat'."
    )
    system_prompt_flag: str = Field(
        default="", description="CLI flag used to append or override the system prompt; empty means unsupported."
    )
    system_prompt_delivery: str = Field(
        default="inline",
        description="How the system prompt text reaches the flag: 'inline' passes it directly as the flag value, "
        "'file' writes it to a session-scoped file and passes the file path.",
    )
    session_flag: str = Field(
        default="",
        description="CLI flag used to pass the session/transcript file path; empty means this runtime has no resumable session concept.",
    )
    extra_args: list[str] = Field(
        default_factory=list, description="Static CLI arguments always appended for this runtime, independent of role fields."
    )
    unsupported_role_fields: list[str] = Field(
        default_factory=list,
        description="RoleDoc field names this runtime cannot honor; used to warn instead of silently dropping role settings.",
    )
    notes: str = Field(
        default="", description="Operational notes such as authentication requirements or version pins for this runtime."
    )
