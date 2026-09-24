---
# runtime-xxx
id: runtime-pi
# draft | active | archived
status: active
# Runtime binary identifier matching RoleDoc.kind values, e.g. pi, claude, codex
kind: pi
binary: pi
# Empty means this runtime does not support that capability
model_flag: --model
fallback_models_flag: ''
# comma | space | repeat
fallback_models_join: comma
tools_flag: --tools
# comma | space | repeat
tools_join: comma
system_prompt_flag: --append-system-prompt
# inline | file
system_prompt_delivery: inline
session_flag: --session
extra_args: []
# RoleDoc fields this runtime cannot honor
unsupported_role_fields:
- fallback_models
# e.g. system:deskops
tags:
- system:deskops
---

# Pi Runtime

## Summary

_Summarize what this runtime is and when to use it._

Pi CLI agent runtime, invoked with role-derived flags.

## Notes

_Operational notes such as authentication requirements or version pins._

Requires PI_API_KEY in the environment.
