from __future__ import annotations


ABOUT_TEXT = """deskops

Workflow-domain CLI built on top of sldb.

What it manages:
- repo-local desk workspaces
- global and local sldb bootstrap flows
- workflow models such as tasks, boards, pills, rituals, inbox notes, and repository registrations

First-use commands:
- deskops bootstrap
- deskops init .

Useful commands:
- deskops faq
- deskops inbox
- deskops repo register
"""


def print_about() -> int:
    print(ABOUT_TEXT)
    return 0
