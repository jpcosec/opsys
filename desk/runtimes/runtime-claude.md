---
# runtime-xxx
id: runtime-claude
# draft | active | archived
status: active
# Runtime binary identifier matching RoleDoc.kind values, e.g. pi, claude, codex
kind: claude
binary: claude
# Empty means this runtime does not support that capability
model_flag: --model
fallback_models_flag: ''
# comma | space | repeat
fallback_models_join: comma
tools_flag: --allowedTools
# comma | space | repeat
tools_join: repeat
system_prompt_flag: --append-system-prompt
# inline | file
system_prompt_delivery: file
session_flag: --resume
extra_args:
- --print
# RoleDoc fields this runtime cannot honor
unsupported_role_fields:
- fallback_models
# e.g. system:deskops
tags:
- system:deskops
---

# Claude Code Runtime

## Summary

_Summarize what this runtime is and when to use it._

Claude Code CLI runtime.

## Notes

_Operational notes such as authentication requirements or version pins._

Requires ANTHROPIC_API_KEY or an active `claude login` session.
