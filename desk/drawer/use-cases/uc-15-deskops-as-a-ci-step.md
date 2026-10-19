# UC-15: Deskops as a CI step — "Check my PR for knowledge integrity"

The team wants PRs to maintain knowledge integrity. Deskops runs in CI to catch issues before merge.

**Interaction flow:**

1. Developer opens a PR with atom changes
2. CI runs: `python -m pytest tests -q`
3. CI runs: `deskops graph missing`
4. CI runs: `deskops drift check`
5. CI runs: `deskops closeout verify --task <id>`
6. If any fail → PR is blocked with a clear report
7. Developer sees in CI logs: "2 missing references, 1 drift item"
8. Fixes issues, pushes, CI passes

**What this user is trying to do:**
Enforce knowledge quality automatically. The same commands they run locally are reproducible in CI. No special CI configuration beyond running deskops.

**When this breaks:**
- CI mode is different from local mode (different results)
- Exit codes don't distinguish "found issues" from "crashed"
- Output is too verbose (scrolls past the important bits)
- Deskops requires interactive terminal or user config to run
- Graph build is too slow for CI turnaround
- Secrets or local paths leak into CI output
