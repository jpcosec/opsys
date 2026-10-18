# result summary: task-closed-issues-count-as-records-in-graph-missing

Done by the supervisor directly.

- `deskops/graph/extract_edges.py`: `_is_closed_issue(kind, text)` uses `issue_status` from deskops/services/issues.py. A closed issue counts as an archived record both for document declarations and for store-unresolved findings, so its stale Resolution refs are informational.
- `tests/test_graph_cli.py`: `test_graph_missing_treats_a_closed_issue_as_a_record[closed|open]`. On the unfixed code, closed fails.
- `deskops graph missing --root .`: 10 missing before, 0 missing now (134 informational).

Full suite: see validation.log.
