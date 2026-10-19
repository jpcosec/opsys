---
id: atom-workflow-role-model-routing
title: Workflow role model routing
five_wh_one_plus: how
tags:
- system:deskops
- topic:roles
- topic:model-routing
---

# Workflow role model routing

## Answer

Each deskops workflow role is bound to an explicit model in its installed agent frontmatter (~/.pi/agent/agents/), not left to inherit the pi default. Supervisor: anthropic/claude-opus-4-8 with fallback openai-codex/gpt-5.4 (routing and review). Executor: openai-codex/gpt-5.4 with fallback google-gemini-cli/gemini-3.1-pro-preview (implementation; supervisor may override per dispatch with model=). Tester: openrouter/nvidia/nemotron-3-super-120b-a12b:free with fallback openrouter/openai/gpt-oss-20b:free (mechanical validation).
