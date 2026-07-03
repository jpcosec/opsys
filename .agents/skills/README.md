# Repo-local agent skills

These skills generalize the workflow-role pattern used in other repos into `deskops` itself.

They are not product features. They are operational prompts for Pi-style agents so the agent can:

- recover real desk state from repo artifacts
- separate supervisor and executor behavior
- preserve evidence for subagent runs
- respect execution, testing, and closeout gates
- use `sldb` correctly for structured-document work

Available skills:

- `deskops-workflow`
- `workflow-executor`
- `workflow-supervisor`
- `workflow-tester`
- `subagent-execution`
- existing structured-doc skill: `.skills/sldb/SKILL.md`
