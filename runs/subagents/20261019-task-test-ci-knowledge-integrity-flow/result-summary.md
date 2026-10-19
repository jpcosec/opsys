# result summary: task-test-ci-knowledge-integrity-flow

Done by the supervisor directly. The pi worker's lane was lost when the machine rebooted and wiped /tmp before it committed.

- `scripts/ci-knowledge-check.sh [root]`: `deskops doctor`, `sldb stores check` and `deskops graph missing` gate the run, and the first non-zero exit fails with `FAILED: <cmd>` on stderr. `deskops drift check` runs as an advisory step with `--out` pointed at a temp dir, so CI never writes ~/.pi.
- `tests/test_ci_integration.py`: a fresh `deskops init` sandbox (isolated HOME) exits 0; a doc with a dangling `source_atoms` reference exits non-zero and names the failing gate.
- `.github/workflows/tests.yml`: a new "Check knowledge integrity" step after pytest.
- The script exits 0 on this repository.
- Drawer: st-15 and uc-15, the gap this task closes, were retired, and the drawer README and Board were updated to match.

Full suite: see validation.log.
