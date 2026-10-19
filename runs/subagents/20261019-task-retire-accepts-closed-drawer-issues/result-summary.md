# result summary: task-retire-accepts-closed-drawer-issues

Done by the supervisor directly.

- `deskops/services/retire.py`: `_is_retirable_drawer_issue` lets retire take a desk/drawer/issues file whose status is closed or resolved (issue_status) or that is an archived record (`record: true`). Open drawer issues are still refused, with a pointer to `issue close`. In the same DocTransaction, the issue's `- `<stem>`` bullets are removed from desk/drawer/tasks/Board.md, and that Board is reported and not counted as an inbound reference.
- `tests/test_retire_cli.py`: closed issue plus its Board bullet; refusal of an open issue; an archived record issue.

The first full run was lost when the disk filled up (ENOSPC), not to a test failure. The rerun used a private --basetemp: see validation.log.
