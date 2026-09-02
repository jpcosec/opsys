# Workflow role system prompts

These files are reference prompts for workflow roles.

They are intentionally **not** stored as auto-discovered repo-local skills.
Workflow roles such as supervisor, executor, and tester are global/system-prompt concerns rather than per-task surface skills.

The canonical tracked role sources now live under `desk/roles/` and materialize into installed pi-agent files. This directory keeps only reference documentation about the role system prompt surface:

- `deskops-workflow.md` — legacy local workflow skill text kept as reference after consolidation into the global `use-deskops` skill
