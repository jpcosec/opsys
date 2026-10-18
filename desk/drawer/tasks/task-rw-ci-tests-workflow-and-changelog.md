---
id: task-rw-ci-tests-workflow-and-changelog
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- .github/workflows/tests.yml
- CHANGELOG.md
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- topic:packaging
- topic:ci
---

# CI runs pytest on every push, and the repo has a CHANGELOG

## Rationale

_Explain why this task exists or the business driver behind it._

Packaging audit of 2026-10-17 (desk/inbox/20261017-233236-suggestion-auditor-a-de-empaquetado-2026-10-17-kgdb-no-declarado-rutas-file-dependientes-del-checkout.md); the owner asked for it on 2026-10-18 through the SLDB_1 coordinator. deskops has no `.github/workflows` and no CHANGELOG; the owner's rule is that the remote always holds the best stable version, and nothing checks that a pushed main is green.

## Goal

_Describe the concrete result this task must produce._

A GitHub Actions workflow runs `pytest tests` on push and pull request to main, and CHANGELOG.md records the changes since the last tag.

## Scope

_State what is in scope and what is out of scope._

In scope: one workflow file and CHANGELOG.md. Out of scope: publishing, release tags, and kgdb's own packaging defect (see Implementation Path).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `.github/workflows/tests.yml`: on `push` and `pull_request` to `main`; one job on `ubuntu-latest`, Python 3.12 (`actions/setup-python`); steps: checkout this repo, `pip install "git+https://github.com/jpcosec/sldb.git@main"` (public; distribution `structuredLanguageDB`), `pip install --no-deps "git+https://github.com/jpcosec/kgdb.git@1247139"` (`--no-deps` because kgdb 0.1.0 requires a distribution named `sldb` that does not exist; found while closing task-rw-f0-declare-runtime-dependencies), `pip install -e . pytest pytest-asyncio` (check which pytest plugins tests/ needs, e.g. `asyncio_default_fixture_loop_scope` in pyproject), set git user.name/user.email (tests make commits), then `pytest tests -q`. The `.pi/skills` tree is gitignored, so a test that needs it must skip when `.pi/` is absent: find such tests (tests/test_skill_cli_drift.py) and make them `pytest.skip` with a reason when the directory does not exist, without weakening them when it exists.
2. Reproduce the job locally in a throwaway venv under /tmp and a fresh `git clone` of this repo (no `.pi/`, no `tools/`), running the same commands; record the result.
3. CHANGELOG.md in Keep a Changelog format: `## [Unreleased]` with the user-visible changes since tag `v-stable-2026.08.29` (`git log --oneline v-stable-2026.08.29..HEAD`), grouped (Added / Changed / Removed / Fixed), one line each, the lifecycle-in-the-graph change and the F0 fixes included.

## Validation

_List the checks required before this task can close._

- pytest tests
- the local reproduction of the CI job (step 2) is green

## Done When

_Name the observable condition that makes the task complete._

The workflow file exists, its local reproduction in a fresh clone is green, and CHANGELOG.md exists with an Unreleased section.

## Resolved Decisions

- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): add CI with pytest and a CHANGELOG.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
