from __future__ import annotations


ABOUT_TEXT = """deskops

Workflow-domain CLI built on top of sldb.

What it manages:
- repo-local desk workspaces
- global and local sldb bootstrap flows
- workflow models such as tasks, boards, pills, rituals, messages, and repository registrations

First-use commands:
- deskops bootstrap
- deskops init .

First task, start to finish:
- deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest" --task-type code
  (a task declares at creation how it closes: --task-type code|implementation|test|docs|spec|design|external,
  or --evidence tests|commit|atom|materialization|document|external)
- deskops list tasks --root .
- deskops show task task-fix-thing --root .
- deskops advance task task-fix-thing --root .
- deskops closeout commit --root . --task task-fix-thing --no-run --reason "..."
  (verifies the declared evidence first; `deskops closeout verify --root . --task task-fix-thing` only checks)
- deskops doctor --root .

Useful commands:
- deskops faq
- deskops message send "Need follow-up" --to <registered-repo> --title "Follow-up"
- deskops promote inbox-to-drawer-task <inbox-selector> --root .
- deskops repo register <name> <path>
"""


def print_about() -> int:
    print(ABOUT_TEXT)
    return 0
