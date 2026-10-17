"""Write the deskops rewrite DAG as drawer TaskDocs.

Run from the deskops repo root:  python runs/planning/rewrite-plan/gen.py

Every task file it writes is fully regenerated; edit the TASKS table here, not the
generated Markdown. The existing drawer task `task-doctor-crashes-on-deskless-roots`
belongs to the plan too, but it is hand-maintained and not written by this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path.cwd()
DRAWER = ROOT / "desk" / "drawer" / "tasks"
INVENTORY = "runs/planning/deskops-rewrite-inventory.md"
P = "desk/contexts/"

OPS = "deskops/operations.py"
F0_DONE = [
    "task-rw-f0-closeout-amends-only-its-own-commit",
    "task-rw-f0-reject-ambiguous-selectors",
    "task-rw-f0-merge-retarget-whole-tokens",
    "task-rw-f0-closeout-commit-pathspec",
    "task-doctor-crashes-on-deskless-roots",
    "task-rw-f0-declare-runtime-dependencies",
    "task-rw-f0-graph-skips-vendored-trees",
    "task-rw-f0-pytest-collects-only-tests",
    "task-rw-f0-payload-from-drawer-resolves",
]
F1_DONE = [
    "task-rw-f1-model-contract-snapshot",
    "task-rw-f1-cli-contract-tests",
    "task-rw-f1-output-golden-files",
]

# Facts shared by many tasks, stated once so a zero-context executor does not guess.
SANDBOX_FACT = (
    "CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run "
    "`python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; "
    "the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with "
    "`subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in "
    "tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with "
    "`capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the "
    "repo's own `desk/`."
)
COMMIT_FACT = (
    "The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The "
    "executor does not commit; the supervisor reviews the diff and makes the closeout commit with "
    "`deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires "
    "`pytest tests` green in addition to the task's own Done When."
)
FIXTURE_TASKS_FACT = (
    "Create fixture tasks through the CLI so each is tracked and routed on the Board, e.g. "
    "`deskops add task --root <root> '{\"id\": \"task-foo\", \"title\": \"Foo\", \"goal\": \"g\", \"scope\": \"s\", "
    "\"implementation_path\": \"i\", \"done_when\": \"d\", \"validation\": [\"pytest\"]}'`; an explicit `id` "
    "overrides the title slug (deskops/specs/compiler.py:36). The task starts at the lifecycle node `ritual-execution`."
)
F1_CLI_TESTS = "tests/test_cli_contract.py (created by task-rw-f1-cli-contract-tests)"

TASKS: list[dict] = [
    # ---------------- F0: data-loss hotfixes ----------------
    dict(
        id="task-rw-f0-closeout-amends-only-its-own-commit",
        title="Closeout amends HEAD only when HEAD is the same task's closeout",
        phase="F0",
        why=(
            "Inventory finding D2. `DeskopsOperations._auto_commit_task_closure` (deskops/operations.py:1086) decides "
            "whether to amend with `head_subject.startswith(f\"closeout: {task_id}\")` (line 1123), so if HEAD is "
            "`closeout: task-foo-bar`, closing `task-foo` amends the other task's commit. (Finding D1, the primitive "
            "glob that deleted another task's files, disappeared with the per-task primitives in afdec7f.)"
        ),
        goal="Closing a task amends HEAD only when HEAD's `Task-Id` trailer is exactly that task's id; otherwise it makes a new commit.",
        scope=(
            "In scope: the amend decision in `_auto_commit_task_closure` and one regression test. Out of scope: the "
            "commit pathspec (task-rw-f0-closeout-commit-pathspec) and untrack/rollback transactions "
            "(task-rw-f2-transactional-doc-io)."
        ),
        implementation_path=(
            "1. Decide the amend from the trailer: amend only when "
            "`git log -1 --format=%(trailers:key=Task-Id,valueonly)` (stripped) equals `task_id`. The closeout commit "
            "message already carries `Task-Id: <id>` (operations.py:1115); a HEAD without that trailer never amends.\n"
            "2. Test in tests/test_lifecycle_end_to_end.py: make HEAD a commit whose subject is `closeout: task-foo-bar` "
            "with trailer `Task-Id: task-foo-bar`, then close `task-foo` through the CLI and assert HEAD~1 is that commit "
            "(a new commit was created)."
        ),
        resolved=[SANDBOX_FACT, FIXTURE_TASKS_FACT, COMMIT_FACT],
        validation=["pytest tests/test_lifecycle_end_to_end.py", "pytest tests"],
        done_when="The new test fails on the current code and passes after the fix, and `pytest tests` is green.",
        files=[OPS, "tests/test_lifecycle_end_to_end.py"],
        pills=[P + "pill-001-task-closure-commit.md", P + "pill-real-cli-surfaces-prove-operator-contracts.md"],
        depends_on=[],
        topics=["closeout", "git"],
    ),
    dict(
        id="task-rw-f0-reject-ambiguous-selectors",
        title="Prefix selectors fail on ambiguity instead of picking the first match",
        phase="F0",
        why=(
            "Inventory finding D5. `DeskopsOperations._resolve_glob` (deskops/operations.py:2077-2084) returns "
            "`matches[0]` of `{doc_id}*.md` when no exact file exists, so `advance task task-foo` can advance "
            "`task-foo-bar`, and `inherits_from` can inherit from the wrong parent. Its callers are at lines 674, 955 and 1964 (all "
            "resolve tasks). The other resolver, `_resolve_artifact_selector` (2112), already refuses ambiguity "
            "through `_one_artifact_match` (2203)."
        ),
        goal=(
            "`_resolve_glob` raises on more than one prefix match, naming every candidate, while an exact file name and a "
            "single prefix match keep resolving as today."
        ),
        scope=(
            "In scope: `_resolve_glob` and two CLI tests. Out of scope: merging the resolvers into one module "
            "(task-rw-f2-selector-resolution-module)."
        ),
        implementation_path=(
            "1. In `_resolve_glob`, after the exact-match check, if `len(matches) > 1` raise "
            "`ValueError(f\"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}\")`, the same "
            "shape as `_one_artifact_match`.\n"
            "2. `deskops.cli.main.main` already maps `ValueError` to `Invalid value: ...` on stderr and exit 1 "
            "(deskops/cli/main.py, `main`); no CLI change.\n"
            "3. Tests in tests/test_operational.py, importing `_make_repo` and `_cli` from "
            "tests/test_lifecycle_end_to_end.py (that module has the sandbox harness; test_operational.py does not): (a) with `task-foo-bar` and `task-foo-baz` only, "
            "`deskops advance task task-foo` exits 1, stderr names both stems, and both task files' text is unchanged "
            "(read before and after); (b) with `task-foo` and `task-foo-bar`, `deskops advance task task-foo` exits 0, "
            "its stdout contains `Task: task-foo`, and `task-foo-bar.md` is unchanged."
        ),
        resolved=[SANDBOX_FACT, FIXTURE_TASKS_FACT, COMMIT_FACT],
        validation=["pytest tests/test_operational.py", "pytest tests"],
        done_when="Both new tests pass and `pytest tests` is green.",
        files=[OPS, "tests/test_operational.py"],
        pills=[P + "pill-real-cli-surfaces-prove-operator-contracts.md", P + "pill-list-surfaces-must-expose-malformed-docs.md"],
        depends_on=["task-rw-f0-closeout-amends-only-its-own-commit"],
        topics=["selectors", "data-loss"],
    ),
    dict(
        id="task-rw-f0-merge-retarget-whole-tokens",
        title="Atom merge rewrites only whole `atom:<id>` tokens in referrers",
        phase="F0",
        why=(
            "Inventory finding D4. `DeskopsOperations._rewrite_inbound_atom_references` (deskops/operations.py:1706), "
            "called only by `merge_atom` (line 924), checks that a line holds the exact token `atom:<id>`, then runs "
            "`original_text.replace(needle, replacement)` on the whole file (line 1738). Merging `atom-foo` into another "
            "atom therefore also rewrites every `atom:atom-foo-bar` in the same file. `split_atom` only reads inbound "
            "references (its `_find_inbound_atom_references` call is at line 823) and is not affected. The finder "
            "(`_find_inbound_atom_references`, line 1685) has no token boundary, so it may list a line such as "
            "`xatom:atom-foo` that the bounded rewrite then leaves alone; that is acceptable (the report lists a "
            "candidate, the rewrite stays exact)."
        ),
        goal="`merge_atom` rewrites only exact `atom:<source id>` tokens in referrer files.",
        scope=(
            "In scope: the replace step of `_rewrite_inbound_atom_references` and one test. Out of scope: rollback of "
            "rewritten referrers on failure (task-rw-f3-atoms-service) and `split_atom`."
        ),
        implementation_path=(
            "1. Replace the global `str.replace` with `re.sub(rf\"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])\", "
            "replacement, original_text)`, the same token grammar as the matcher's `atom:[a-zA-Z0-9_.-]+`.\n"
            "2. The `rewritten` report (path:line) lists only lines whose text the substitution actually changed.\n"
            "3. Test in tests/test_atoms_merge.py: a referrer containing `atom:atom-foo` and `atom:atom-foo-bar`; merge "
            "`atom-foo` into a target; assert `atom:atom-foo-bar` is untouched and `atom:atom-foo` now names the target."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_atoms_merge.py tests/test_atoms_split.py", "pytest tests"],
        done_when="The new test fails before the fix and passes after; `pytest tests` is green.",
        files=[OPS, "tests/test_atoms_merge.py"],
        pills=[P + "pill-atom-lifecycle-preserves-provenance-and-materialization-links.md"],
        depends_on=["task-rw-f0-reject-ambiguous-selectors"],
        topics=["atoms", "data-loss"],
    ),
    dict(
        id="task-rw-f0-closeout-commit-pathspec",
        title="The advance closeout commit contains only the closing task's paths",
        phase="F0",
        why=(
            "Inventory finding D3. The commit `_auto_commit_task_closure` makes when `deskops advance` closes a task "
            "(deskops/operations.py:1125-1128) runs `git commit -m` without a pathspec, so anything the operator had "
            "staged for other work is swept into `closeout: <task>`. Its `git rm --cached` calls (line 1113) use "
            "`check=False` and ignore failures."
        ),
        goal=(
            "That commit includes exactly the removed task file, `desk/tasks/Board.md`, and those entries of the task's "
            "`files` list that have any change, new files included (`git status --porcelain -- <path>` prints "
            "something), with their working-tree content; unchanged listed paths are skipped; unrelated staged changes "
            "stay staged and out of the commit."
        ),
        scope=(
            "In scope: the staging and commit calls in `_auto_commit_task_closure`, and one test. Out of scope: the amend "
            "rule (task-rw-f0-closeout-amends-only-its-own-commit) and `deskops closeout commit` (deskops/cli/commands/closeout.py)."
        ),
        implementation_path=(
            "1. Build the path list: the removed task file, `desk/tasks/Board.md`, and each `files` entry for which "
            "`git status --porcelain -- <path>` prints something. Today the closeout `git add`s every listed file "
            "(operations.py:1104); keep that `git add -A -- <path>` for those paths only. The existing lifecycle test "
            "lists an untracked atom and test file and expects them in the commit; that must keep passing.\n"
            "2. A pathspec commit records the working tree, so the task file must already be deleted when it runs: keep "
            "its bytes in memory, `git rm -- <task path>` (checked; this deletes it from disk and the index) instead of "
            "`git rm --cached`, then commit with `git commit -m <msg> -- <paths>` (or `git commit --amend --no-edit -- "
            "<paths>`). On any failure restore the task file from memory, the Board, and the index (`git restore "
            "--staged`), and raise `RuntimeError` with git's stderr. The later untrack/unlink step then only untracks.\n"
            "3. Test in tests/test_lifecycle_end_to_end.py: stage an unrelated file, close a task through the CLI, assert "
            "the unrelated file is still staged (`git diff --cached --name-only`) and absent from "
            "`git show --name-only --format= HEAD`, and that HEAD's diff deletes the task file."
        ),
        resolved=[SANDBOX_FACT, FIXTURE_TASKS_FACT, COMMIT_FACT],
        validation=["pytest tests/test_lifecycle_end_to_end.py", "pytest tests"],
        done_when="The new test passes, the existing lifecycle test still commits the task's files, and `pytest tests` is green.",
        files=[OPS, "tests/test_lifecycle_end_to_end.py"],
        pills=[P + "pill-001-task-closure-commit.md"],
        depends_on=["task-rw-f0-merge-retarget-whole-tokens"],
        topics=["closeout", "git"],
    ),
    dict(
        id="task-rw-f0-declare-runtime-dependencies",
        title="pyproject declares kgdb as a dependency",
        phase="F0",
        why=(
            "deskops imports `sldb` throughout and `kgdb` in deskops/graph/snapshot.py:119 and deskops/cli/main.py:251, "
            "but pyproject.toml lists only pydantic and PyYAML, so a clean install of deskops cannot import itself."
        ),
        goal="pyproject.toml declares `kgdb` with a lower-bound version next to the existing `structuredLanguageDB>=0.1.9`, and a fresh venv that installs the sibling sldb checkout, kgdb and deskops imports the CLI.",
        scope=(
            "In scope: the `dependencies` list in pyproject.toml. Out of scope: publishing, upper bounds, and "
            "`ensure_sldb_available` in deskops/bootstrap.py."
        ),
        implementation_path=(
            "1. `dependencies` already holds `\"structuredLanguageDB>=0.1.9\"` (pyproject.toml:10, added by afdec7f); add "
            "`\"kgdb>=0.1.0\"` (the installed version) after it and change nothing else. In this machine's main "
            "environment the sldb metadata still says structuredLanguageDB 0.1.3 although `import sldb` loads ../sldb/src "
            "at 0.1.9, so `pip install -e .` there may need `pip install -e ../sldb` first; the throwaway venv below is "
            "the check that counts.\n"
            "2. Verify in a throwaway venv under /tmp: `python -m venv /tmp/deskops-venv && /tmp/deskops-venv/bin/pip install "
            "../sldb <kgdb source> . && /tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`. There is no sibling "
            "kgdb checkout; the installed kgdb 0.1.0 came from git (its dist-info `direct_url.json` records "
            "https://github.com/jpcosec/kgdb.git at commit 1247139), so `<kgdb source>` is "
            "`\"git+https://github.com/jpcosec/kgdb.git@1247139\"`. If that pip command exits non-zero, keep the "
            "declaration, and record the exact command and error in the closeout."
        ),
        resolved=[COMMIT_FACT],
        validation=["python -m deskops --help", "pytest tests"],
        done_when="pyproject.toml declares kgdb, and the throwaway-venv import check succeeds (or the pip error is recorded).",
        files=["pyproject.toml"],
        pills=[P + "pill-008-kgdb-sldb-boundary.md"],
        depends_on=[],
        topics=["packaging"],
    ),
    dict(
        id="task-rw-f0-graph-skips-vendored-trees",
        title="`graph build` ignores tools/, .tmp/ and .venv/",
        phase="F0",
        why=(
            "Inventory finding X4 (reproduced): `deskops graph build` puts 5 atoms from the untracked `tools/repopackage/` "
            "checkout into deskops' graph. Two walkers are involved: deskops/graph/extract_coverage.py excludes by "
            "`EXCLUDED_PATH_PARTS` (line 27, matched against any path part by `_is_excluded`, line 895), which lacks "
            "`tools` and `.tmp`; deskops/graph/extract_sources.py excludes by `EXCLUDED_DIRS` (lines 15-26), which lacks "
            "`tools` and `.tmp`."
        ),
        goal="After `deskops graph build --root .`, no node in the snapshot has a path under `tools/` or `.tmp/` (`.venv/` stays excluded).",
        scope=(
            "In scope: adding `tools` and `.tmp` to both exclusion sets (any-path-part matching stays as it is), and "
            "one test per extractor. Out of scope: whether the coverage extractor survives the rewrite "
            "(task-rw-f4-coverage-extractor-decision)."
        ),
        implementation_path=(
            "1. Add `\"tools\"` and `\".tmp\"` to `EXCLUDED_PATH_PARTS` in extract_coverage.py and to `EXCLUDED_DIRS` in "
            "extract_sources.py.\n"
            "2. Tests: in tests/test_graph_extract_coverage.py, an atom under `tools/x/desk/atoms/` produces no node; in "
            "tests/test_graph_extract_sources.py, a `.py` file under `tools/x/` produces no `source_file:` node.\n"
            "3. Rebuild and check: `python -m deskops graph build --root .`, then count snapshot nodes whose "
            "`semantics.path`, `identity.node_id` (after any `<kind>:` prefix) or any `source.provenance[*].path` "
            "starts with `tools/` or `.tmp/` (node layout: deskops/graph/snapshot.py:201-223); the count must be 0."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py", "deskops graph build --root .", "pytest tests"],
        done_when="Both tests pass and the rebuilt snapshot has zero nodes under `tools/` or `.tmp/`.",
        files=["deskops/graph/extract_coverage.py", "deskops/graph/extract_sources.py", "tests/test_graph_extract_coverage.py", "tests/test_graph_extract_sources.py"],
        pills=[P + "pill-010-graph-runtime-output-policy.md", P + "pill-009-source-file-graph-traceability.md"],
        depends_on=[],
        topics=["graph"],
    ),
    dict(
        id="task-rw-f0-pytest-collects-only-tests",
        title="Bare `pytest` collects only the tests/ directory",
        phase="F0",
        why=(
            "AGENTS.md names bare `pytest` as the minimum validation, but it also collects the untracked `tools/` "
            "checkout (another project's code), whose test fails, so the documented gate is red for reasons outside "
            "deskops. pyproject.toml already has a `[tool.pytest.ini_options]` table with `pythonpath` and "
            "`asyncio_default_fixture_loop_scope`."
        ),
        goal="Running `pytest` with no arguments from the repo root collects only `tests/`.",
        scope="In scope: one key in `[tool.pytest.ini_options]`. Out of scope: the contents of `tools/`, which deskops does not own.",
        implementation_path="Add `testpaths = [\"tests\"]` to the existing `[tool.pytest.ini_options]` table, keeping its other keys.",
        resolved=[COMMIT_FACT],
        validation=["pytest", "pytest tests"],
        done_when="Bare `pytest` reports the same passed count as `pytest tests` and both are green.",
        files=["pyproject.toml"],
        pills=[P + "pill-real-cli-surfaces-prove-operator-contracts.md"],
        depends_on=["task-rw-f0-declare-runtime-dependencies"],
        topics=["testing"],
    ),
    dict(
        id="task-rw-f0-graph-missing-ignores-archived-records",
        title="`graph missing` stops failing on paths quoted in archived drawer records",
        phase="F0",
        why=(
            "`deskops graph missing --root .` exits 1 on the repo desk (main at 56f49d5) with 102 findings, all "
            "`missing_declared_target` from the per-line path scanner (`source-file-reference` provenance) in "
            "deskops/graph/extract_edges.py: 98 come from desk/drawer/issues/diagnosis-archive.md (title line says "
            "'archived 2026-09-24'; no frontmatter) and 3 from "
            "desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md (a `## Status` section "
            "says 'resolved'; no frontmatter). The last one comes from "
            "desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md, which quotes "
            "deskops/runtime/primitives.py, deleted when afdec7f moved the lifecycle into the sldb graph; that issue "
            "is resolved by afdec7f and becomes a record too. They quote task and test paths that were closed or deleted. "
            "Today every finding prints and any finding exits 1 (`_graph_missing`, deskops/cli/main.py:280). While this gate is red on "
            "the real desk, no task can use it as validation."
        ),
        goal=(
            "`deskops graph missing --root .` exits 0 on the repo desk while a live issue with a dangling path still "
            "exits 1. With option A or C every document carrying the record marker is handled by one general rule (no "
            "per-file allowlist); with option B the three files no longer contain path-shaped references."
        ),
        scope=(
            "Blocked on the owner's choice (see Open Ambiguities). The record marker is checked on every extracted "
            "document, not only under desk/drawer/. With option C the output and exit code of `_graph_missing` in "
            "deskops/cli/main.py are in scope. Out of scope: other finding kinds and the sldb-backed graph rewrite "
            "(task-rw-f4-graph-on-sldb-edge-index). The 102 findings are all from the three files named in "
            "Rationale (checked 2026-10-16 with `deskops graph missing --root .` and grouping by provenance); if new "
            "non-record findings appear before this task runs, list them in the closeout and do not hide them."
        ),
        implementation_path=(
            "Option A or C: (1) mark all three files with the chosen record marker; (2) the path scanner in extract_edges.py "
            "tags each edge from a record document with `record: true` in its metadata (option A instead drops those "
            "edges there); `find_missing_graph_references` (deskops/graph/checks.py) copies the flag onto "
            "`GraphMissingFinding` as a new `record: bool | None = None` field, set to True only for record findings, so "
            "`to_dict` (which drops None) keeps today's dicts for live findings (tests/test_graph_checks.py:25,64); "
            "(3) option C only: `_graph_missing` (`_graph_missing`, deskops/cli/main.py:280) prints record findings under a separate "
            "`Informational (archived records):` heading after the failing ones, does not count them, exits 1 iff at "
            "least one non-record finding exists, and ends with `N missing, M informational`. "
            "Option B: rewrite each quoted path in the three files as plain text (for example drop the directory part or "
            "wrap it so it no longer matches the scanner), with no code change. "
            "Tests (all options), in tests/test_graph_declared_edges.py with a `tmp_path` desk: a live issue under "
            "desk/drawer/issues/ with a dangling path still yields a finding and exit 1 (the scanner only reads `task` "
            "and `issue` documents, extract_edges.py:93); for A or C, a marked record issue with the same path yields "
            "no failing finding."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py", "deskops graph missing --root .", "pytest tests"],
        done_when="`deskops graph missing --root .` exits 0 on the repo desk (with option C it may print informational record findings), the new tests for the chosen option pass, and `pytest tests` is green.",
        files=["deskops/graph/extract_edges.py", "deskops/graph/checks.py", "deskops/cli/main.py", "tests/test_graph_declared_edges.py", "desk/drawer/issues/diagnosis-archive.md",
               "desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md",
               "desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md"],
        pills=[P + "pill-009-source-file-graph-traceability.md", P + "pill-010-graph-runtime-output-policy.md"],
        depends_on=[],
        topics=["graph", "gates"],
        ambiguities=[
            "Owner decision, handling: A) skip record documents in the path scanner; B) edit the three files so the quoted "
            "paths stop looking like references (loses verbatim history); C) report record findings as informational "
            "with exit 0 (recommended; semantics in Implementation Path).",
            "Owner decision, marker: a `record: true` frontmatter key (recommended; both files need frontmatter added), "
            "the title containing 'archived', or a `## Status` section saying resolved/archived.",
        ],
        status="blocked",
    ),
    dict(
        id="task-rw-f0-payload-from-drawer-resolves",
        title="`from_drawer` given in a YAML or JSON payload is resolved like the flag",
        phase="F0",
        why=(
            "Found by the plan rehearsal (2026-10-16). `deskops add task --from-drawer <selector>` resolves the selector "
            "to a repo-relative drawer path in `OperationsCLI.run` (deskops/cli/commands/operations.py:21-27, through "
            "`DeskopsOperations.resolve_drawer_source` and `attach_drawer_source`, operations.py:493 and 525; the "
            "resolver already raises ValueError on an ambiguous selector, operations.py:520-522). The same "
            "key inside `--from-yaml` or an inline JSON payload skips that step: deskops/specs/compiler.py:57 copies the "
            "raw string, so the task records `from_drawer: rw-f0-x` instead of `desk/drawer/tasks/task-rw-f0-x.md`, and "
            "a missing or ambiguous selector is accepted silently."
        ),
        goal=(
            "A `from_drawer` value from the flag, a YAML payload or an inline JSON payload is resolved and stored as the "
            "same repo-relative drawer path; an unknown or ambiguous selector fails with exit 1 and creates nothing."
        ),
        scope=(
            "In scope: the add-task branch of `OperationsCLI.run` and one new test file. If both the flag and the payload "
            "carry a value, the flag wins and the payload value is ignored without being checked. A payload value that is "
            "absent, empty or null means no drawer source (as the flag's `if` at cli/commands/operations.py:21). Out of "
            "scope: the drawer routing service (task-rw-f3-drawer-routing-service)."
        ),
        implementation_path=(
            "1. In `OperationsCLI.run`, take the selector from `args.from_drawer`, else from `payload.get(\"from_drawer\")`, "
            "and run the existing resolve/attach step on it; keep the existing `Error: ...` message and `return 1` on "
            "`FileNotFoundError`/`ValueError`.\n"
            "2. New tests/test_add_task_from_drawer.py, all in one sandbox repo with one drawer entry (payloads need at "
            "least `title`; give each task its own `id`): (a) the same drawer stem given via `--from-drawer`, via "
            "`--from-yaml`, and via inline JSON produces three tasks with identical `from_drawer` paths; (b) an unknown "
            "selector in a JSON payload exits 1 and creates no `desk/tasks/` file; (c) with two drawer entries that "
            "share a fragment, that fragment in a JSON payload exits 1 and creates nothing."
        ),
        resolved=[SANDBOX_FACT, COMMIT_FACT],
        validation=["pytest tests/test_add_task_from_drawer.py", "pytest tests"],
        done_when="Both new tests pass and `pytest tests` is green.",
        files=["deskops/cli/commands/operations.py", "tests/test_add_task_from_drawer.py"],
        pills=[P + "pill-real-cli-surfaces-prove-operator-contracts.md", P + "pill-cli-gaps-become-tracked-work.md"],
        depends_on=[],
        topics=["drawer", "cli"],
    ),
    # ---------------- F1: freeze the contract ----------------
    dict(
        id="task-rw-f1-model-contract-snapshot",
        title="A test pins the sldb contract hash of every deskops model",
        phase="F1",
        why=(
            "24 stores on this machine track TaskDoc. sldb hashes each model's contract with `hash_model_contract` "
            "(../sldb/src/sldb/store/hashing.py:80, over field schemas with descriptions, `__template__`, `__family__`, "
            "semantics, base names, `__references__`, `__containment__`, `__compositions__`). An accidental change during "
            "the rewrite puts every one of those stores in FAIL, and nothing in deskops detects it today."
        ),
        goal=(
            "A test fails, naming the model, whenever a deskops model's contract hash differs from a committed snapshot, "
            "or when a model is added to or removed from the registered set."
        ),
        scope=(
            "In scope: one test module and its fixture. Out of scope: changing any model (F6). Import "
            "`sldb.store.hashing.hash_model_contract`; it is public by name although it is outside `sldb.api`."
        ),
        implementation_path=(
            "1. The model set is `deskops.bootstrap.MODEL_REFS` (a dict name -> `module:Class`) united with the model "
            "names listed in `.sldb/core/store_index.yaml`; import each class from its `model_ref` (the MODEL_REFS value, "
            "or the store index's `model_ref`; RelationTypeDoc and RelationDoc are `sldb.models.*` classes registered by "
            "the lifecycle graph and are snapshotted too).\n"
            "2. Fixture tests/fixtures/model_contract_hashes.json is a flat JSON object `{\"<ModelName>\": \"<sha256 hex>\"}` "
            "with sorted keys.\n"
            "3. tests/test_model_contract_snapshot.py asserts the fixture's key set equals the discovered set (listing "
            "missing and extra names) and each hash matches (listing changed names). The failure message says a change "
            "requires a store migration (task-rw-f6-migrate-tracking-stores) and prints the new hashes so the fixture "
            "can be updated deliberately.\n"
            "4. Generate the fixture once from the current code."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_model_contract_snapshot.py", "pytest tests"],
        done_when="The test passes on the current code, and fails naming the model when a TaskDoc field description is edited locally (check by hand, then revert).",
        files=["tests/test_model_contract_snapshot.py", "tests/fixtures/model_contract_hashes.json"],
        pills=[P + "pill-006-self-described-store-layout.md", P + "pill-legacy-desk-formats-need-explicit-adaptation.md"],
        depends_on=list(F0_DONE),
        topics=["contract", "testing"],
    ),
    dict(
        id="task-rw-f1-cli-contract-tests",
        title="Every CLI surface without a test gets one through main(argv)",
        phase="F1",
        why=(
            "The rewrite must not change the CLI. These subcommands have no test through `main` today (checked "
            "2026-10-16 by grepping tests/): `add faq-doc`, `atoms list`, `atoms show`, and `runtime "
            "init|status|attach|stop|supervise` (deskops/cli/parser.py:67-89). Already covered and out of this task: "
            "`add board|ritual|step` (tests/test_cli.py), `closeout commit` "
            "(tests/test_closeout.py), `bind pill` (tests/test_cli.py:1124), `atoms type` (tests/test_domain_tree.py:104) "
            "and `runtime workers` (tests/test_cli.py:2402)."
        ),
        goal=(
            "Each listed subcommand has one in-process test that calls `deskops.cli.main.main([...])` inside a sandbox "
            "repo and asserts the exit code and one stable line of output."
        ),
        scope=(
            "In scope: new tests only, one test per subcommand (parametrize where the shape repeats). Out of scope: fixing "
            "what the tests reveal: record each surprise as a new drawer task file and mark its test "
            "`pytest.mark.xfail(strict=True, reason='<task id>')`. `runtime` tests must not start Herdr: stub the Herdr "
            "client the way tests/test_herdr_runtime.py does."
        ),
        implementation_path=(
            "1. tests/test_cli_contract.py using the `lifecycle_desk` fixture from tests/conftest.py (a sandbox repo as "
            "`deskops init` leaves it).\n"
            "2. One test per subcommand listed in Rationale, calling `main([...])` with `--root <sandbox>`, capturing "
            "stdout/stderr via `capsys`.\n"
            "3. These tests call `main` in-process (like tests/test_cli.py:1124), not through a subprocess; the "
            "sandbox repo is still built as described in Resolved Decisions."
        ),
        resolved=[SANDBOX_FACT, COMMIT_FACT],
        validation=["pytest tests/test_cli_contract.py", "pytest tests"],
        done_when="Each of the 8 uncovered subcommands named in Rationale has its own test (a strict xfail tied to a new drawer task counts), and `pytest tests` is green.",
        files=["tests/test_cli_contract.py"],
        pills=[P + "pill-real-cli-surfaces-prove-operator-contracts.md", P + "pill-machine-readable-cli-output-needs-stable-contract.md"],
        depends_on=list(F0_DONE),
        topics=["contract", "cli", "testing"],
    ),
    dict(
        id="task-rw-f1-output-golden-files",
        title="Golden files pin the graph snapshot, run index, closeout trailers and --help text",
        phase="F1",
        why=(
            "Other tools read deskops outputs: `.sldb/runtime/graphs/deskops.kg.json` (schema "
            "`deskops_kgdb_graph_snapshot_v1`) and `deskops.nx.json`, `.sldb/runtime/self_reflection_findings.json`, "
            "`runs/subagents/index.jsonl`, and the trailers of closeout commits (`Task-Id`, `Run-Dir`, `Run-Id`, "
            "`Session-Sha256`, or `Closeout-Mode`/`Closeout-Reason` for `--no-run`). The CLI rewrite also needs every "
            "command's `--help` text pinned."
        ),
        goal="Tests compare those outputs, produced from a fixed fixture desk, against committed golden files with volatile values normalized.",
        scope="In scope: one fixture desk, the golden files listed below, the comparison tests, and a `--update-golden` pytest option. Out of scope: changing any output format.",
        implementation_path=(
            "1. Fixture desk tests/fixtures/golden_desk/ with 2 tasks, 2 atoms, 1 pill and 1 drawer task.\n"
            "2. Copy it into `tmp_path`, git init, run `graph build`, `graph reflect` (the only writer of "
            "self_reflection_findings.json), a `closeout commit --run-dir` and a "
            "`closeout commit --no-run`; normalize timestamps to `<ts>`, absolute paths to `<root>`, commit hashes to `<sha>`.\n"
            "3. Goldens in tests/fixtures/golden/: `graph_snapshot.kg.json`, `graph_snapshot.nx.json`, "
            "`self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (a list of `{route, trailers}` "
            "objects), and `help/deskops.txt` for the root plus `help/deskops_<sub>[_<subsub>].txt` for every command "
            "path reachable from `deskops --help`.\n"
            "4. tests/test_output_goldens.py compares; `--update-golden` (registered in tests/conftest.py) rewrites them."
        ),
        resolved=[SANDBOX_FACT, COMMIT_FACT, "tests/conftest.py already exists (the lifecycle_desk fixtures); add a `pytest_addoption` for `--update-golden` to it and keep the normalization helpers in tests/test_output_goldens.py."],
        validation=["pytest tests/test_output_goldens.py", "pytest tests"],
        done_when="The golden tests pass, and fail when a key is renamed in the snapshot writer (check by hand, then revert).",
        files=["tests/test_output_goldens.py", "tests/fixtures/golden/", "tests/fixtures/golden_desk/", "tests/conftest.py"],
        pills=[P + "pill-010-graph-runtime-output-policy.md", P + "pill-machine-readable-cli-output-needs-stable-contract.md"],
        depends_on=list(F0_DONE),
        topics=["contract", "graph", "testing"],
    ),
    # ---------------- F2: shared infrastructure (serial, all touch operations.py) ----------------
    dict(
        id="task-rw-f2-selector-resolution-module",
        title="One module resolves every desk selector",
        phase="F2",
        why=(
            "Four methods in deskops/operations.py resolve selectors: `_resolve_glob` (2077), "
            "`_resolve_artifact_selector_multi` (2086), `_resolve_artifact_selector` (2112) and `_one_artifact_match` "
            "(2203). After task-rw-f0-reject-ambiguous-selectors they share one rule (exact name or stem first, then a "
            "unique prefix, else an ambiguity error), but each keeps its own copy and message."
        ),
        goal="A new `deskops/desk_paths.py` implements that rule once; the four methods become one-line delegations to it.",
        scope=(
            "In scope: selector resolution only (desk layout constants such as `ARTIFACT_PATHS` stay where they are). "
            "Behavior is unchanged except two messages, which become one format for all callers: "
            "`Ambiguous <what> selector '<selector>': <candidates>` and `No <what> file found for selector '<selector>'`, "
            "where <candidates> are the matching paths relative to the desk root, sorted, joined with ', '."
        ),
        implementation_path=(
            "1. deskops/desk_paths.py: `resolve_selector(desk_root: Path, directories: list[Path], selector: str, pattern: str, "
            "what: str, recursive: bool) -> Path`; `recursive` keeps each caller's current search (`_resolve_glob` uses "
            "`glob`, the artifact selectors use `rglob`); `what` is the artifact id for the artifact selectors and the "
            "directory kind (`task`, the only one its callers use today) for `_resolve_glob` callers; "
            "with two tiers: (1) a file whose `name` or `stem` equals the selector; (2) a unique file whose name or stem "
            "starts with it; zero matches raise `FileNotFoundError` and more than one raise `ValueError`, with the messages "
            "above. Update any existing test that asserts the old wording, and list each one in the closeout.\n"
            "2. Make the four methods delegate.\n"
            "3. tests/test_desk_paths.py covers both tiers, zero matches and ambiguity."
        ),
        resolved=[COMMIT_FACT, f"The F1 CLI contract tests are {F1_CLI_TESTS}; they must pass unchanged."],
        validation=["pytest tests/test_desk_paths.py", "pytest tests"],
        done_when="`grep -n 'glob(\\|rglob(' deskops/operations.py` shows no selector-resolution loop outside the delegations, and `pytest tests` (including the F1 contract tests) is green.",
        files=["deskops/desk_paths.py", OPS, "tests/test_desk_paths.py"],
        pills=[P + "pill-real-cli-surfaces-prove-operator-contracts.md"],
        depends_on=list(F1_DONE),
        topics=["refactor", "selectors"],
    ),
    dict(
        id="task-rw-f2-typed-errors-and-exit-codes",
        title="Typed errors, a fixed exit-code table, and no swallowed tracebacks",
        phase="F2",
        why=(
            "Inventory findings X2 and X3. `deskops.cli.main.main` (deskops/cli/main.py:373-394) maps a few built-in "
            "exceptions to exit 1, classifies others by `exc.__class__.__name__`, and turns everything else into "
            "`SystemExit(\"Unexpected: ...\")` with no traceback; that hid both the doctor crash and the Governance CI "
            "SyntaxError. deskops/cli/commands/desk.py:149-171 ignores a failing `stores check` and prints "
            "'Desk is up to date.' with exit 0."
        ),
        goal=(
            "deskops raises typed errors from one module; the CLI maps them to exit codes 0 ok, 1 domain error, 2 usage "
            "error (argparse already uses 2), 3 environment error; an unexpected exception prints "
            "`Unexpected error: <type>: <message> (rerun with --debug for the traceback)` on stderr and exits 3; with "
            "`--debug` it prints the full traceback to stderr and still exits 3."
        ),
        scope=(
            "In scope: new deskops/errors.py, the handler in cli/main.py, a global `--debug` flag added to the root "
            "parser in `build_parser` (deskops/cli/parser.py:25) that also sets logging to DEBUG, and the `desk update` "
            "swallow. `--debug` is a root-only option parsed by argparse; `CLI.run` stores it on the CLI instance and "
            "`main()` (which handles exceptions outside `CLI.run`) reads it from that instance. Logging is unchanged "
            "(already DEBUG to a file); only delete the first `_setup_logging` definition (operations.py:322, dead and "
            "self-recursive) and keep the second (334). Typed errors print their message and exit with their code, with "
            "no traceback, with or without `--debug`, on stderr as today's exit-1 mappings do. `<type>` in the "
            "unexpected-error line is `type(exc).__name__`; with `--debug` the traceback prints first, then that line. `UsageError` replaces the hand-written `return 2` at "
            "cli/main.py:150-151 and :228-229 and cli/commands/drift.py:14; the handler prints the same text to the same stream "
            "those sites use today (stdout). Existing exit-1 mappings (FileNotFoundError, KeyError, ValueError, pydantic ValidationError, "
            "SLDBStoreError) stay exit 1. Out of scope: the JSON error envelope (task-rw-f5-output-renderer)."
        ),
        implementation_path=(
            "1. errors.py: `DeskopsError(Exception)` with `exit_code`, subclasses `DomainError` (1), `UsageError` (2), "
            "`DeskopsEnvironmentError` (3).\n"
            "2. main.py: `isinstance` checks instead of class-name strings (import pydantic's ValidationError and "
            "sldb's SLDBStoreError); unexpected exceptions exit 3 as described.\n"
            "3. desk.py: a failing `stores check` or unparseable JSON raises `DeskopsEnvironmentError`.\n"
            "4. Tests in tests/test_cli.py: an injected unexpected exception exits 3 and prints the one-line message "
            "without `--debug`, and exits 3 and prints a traceback with `--debug`; `desk update` whose `stores check` "
            "prints no parseable JSON (sldb missing, or output that is not JSON; a non-zero exit with JSON is a normal "
            "divergence report, see tests/test_desk_sync.py) "
            "exits 3. List every exit code that changes in the closeout."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_cli.py tests/test_desk_sync.py", "pytest tests"],
        done_when="No path prints `Unexpected:` without the `--debug` hint, the new tests pass, and `pytest tests` is green.",
        files=["deskops/errors.py", "deskops/cli/main.py", "deskops/cli/parser.py", "deskops/cli/commands/desk.py", OPS, "tests/test_cli.py"],
        pills=[P + "pill-machine-readable-cli-output-needs-stable-contract.md", P + "pill-doctor-separates-desk-repair-from-sldb-health.md"],
        depends_on=["task-rw-f2-selector-resolution-module"],
        topics=["errors", "cli"],
    ),
    dict(
        id="task-rw-f2-transactional-doc-io",
        title="One doc_io module talks to sldb through its public API, transactionally",
        phase="F2",
        why=(
            "Inventory findings D6, D7 and S6. deskops imports about 30 private sldb internals (for example "
            "`sldb.cli.commands.model.ModelCLI().add(SimpleNamespace)`, `DocCLI().untrack`, `sldb.store.ops.track_document` "
            "with 9 positional args, `sldb.store.io.*`). In `_auto_commit_task_closure` the untrack runs after the "
            "closeout commit and before each file's unlink, and a failure only logs a warning, so the file is deleted "
            "anyway (operations.py:1143-1156, with `store=None` and `pythonpath='.'`). The "
            "`create_task_bundle` rollback does not untrack, the `merge_atom` rollback does not restore rewritten "
            "referrers, and `_write_doc` untracks then tracks in two steps under `except Exception`."
        ),
        goal=(
            "Every sldb store write in deskops (track, untrack, model registration, document update) goes through "
            "`deskops/doc_io.py`, which imports only `sldb.api.*` plus the private names listed in its module-level "
            "tuple `PRIVATE_SLDB_IMPORTS`, and offers a `DocTransaction` that restores files and store entries when any "
            "step fails. Plain file writes that do not touch the store are out of this goal."
        ),
        scope=(
            "In scope: doc_io.py, migrating every sldb write call site, rollback tests, and an import-scan test. Closeout "
            "untrack moves before the commit, inside the transaction, and a failure aborts the closeout. Out of scope: "
            "editing sldb. When a needed operation has no `sldb.api` equivalent, keep the private call as a named helper "
            "in doc_io and append the gap (function, why, proposed API) to "
            "runs/planning/sldb-requests.md for the coordinator."
        ),
        implementation_path=(
            "1. `grep -rn 'from sldb\\|import sldb' deskops` lists the call sites.\n"
            "2. `DocTransaction(root)` is a re-entrant context manager (an inner `with` joins the outer transaction, so "
            "`create_task_bundle` -> `_write_doc` share one); "
            "`tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)` and `tx.delete(path)` record "
            "each path's original bytes and tracked state before acting; on exception it restores files and re-tracks or "
            "untracks to the recorded state, then re-raises. It replaces the `_with_rollback(write_fn, cleanup_fn)` "
            "helper that pill-012 prescribes; update that pill's How to name `DocTransaction`.\n"
            "3. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` and the closeout untrack.\n"
            "4. tests/test_doc_io.py injects a failure at each step (monkeypatch the sldb call to raise) and asserts file "
            "bytes and `sldb stores check` are as before; an import-scan test over the `deskops/` package only (tests "
            "may keep importing sldb internals) fails if any module other than doc_io imports a write-side sldb module: "
            "`sldb.cli.commands` (the CLI command classes, e.g. ModelCLI, DocCLI), `sldb.store.ops`, or a module (file) "
            "under `sldb.api.documents` whose name starts with "
            "`create_`, `delete_`, `update_`, `track_` or `untrack_`; and fails if doc_io imports a name outside "
            "`sldb.api` that is not in `PRIVATE_SLDB_IMPORTS`. Read-side imports (for example "
            "`sldb.store.io.load_store_index`, `sldb.store.resolver.find_local_store`, `sldb.store.layout`, "
            "`sldb.runtime.validation`, `sldb.core.exceptions`, `sldb.StructuredNLDoc`, and the read helpers "
            "`sldb.cli.model_utils`, `sldb.cli.store_context` and `sldb.cli.utils` used by identity.py, repo.py, message.py "
            "and operations.py) stay allowed everywhere.\n"
            "5. doc_io also offers plain helpers for one-off writes outside a transaction: `track(root, path, model)`, "
            "`untrack(root, path)`, `register_model(root, model_ref)` (wrapping `sldb.api.add_model`) and "
            "`is_tracked(root, path)`. An inner `with DocTransaction(root)` finds the outer one through a "
            "module-level stack keyed by root; only the outermost exit commits or rolls back; rollback restores store "
            "entries first, then file bytes, and if restoring fails it logs that and re-raises the original error.\n"
            "6. Store writes in operations.py beyond the four functions also move: `delete_atom` (719, via "
            "`_untrack_atom_document`, 1781) and `reorganize_atoms` (605, via `_retarget_atom_documents`, 1746). "
            "Writes outside operations.py also move: deskops/cli/commands/desk.py:256,280,291, "
            "deskops/cli/commands/repo.py:117, deskops/cli/commands/message.py:344, deskops/cli/commands/promote.py:86, "
            "deskops/bootstrap.py:138 and 156."
        ),
        resolved=[COMMIT_FACT, "Read-only sldb calls (model lookups, extraction such as `sldb.runtime.validation.extract_model_data`) may stay where they are; this task moves writes."],
        validation=["pytest tests/test_doc_io.py", "pytest tests", "sldb stores check --store .sldb"],
        done_when="The import-scan and injected-failure tests pass, `pytest tests` is green, and `sldb stores check --store .sldb` passes.",
        files=["deskops/doc_io.py", OPS, "deskops/identity.py", "deskops/bootstrap.py", "deskops/cli/commands/desk.py",
               "deskops/cli/commands/repo.py", "deskops/cli/commands/message.py", "deskops/cli/commands/promote.py",
               "tests/test_doc_io.py", "runs/planning/sldb-requests.md"],
        pills=[P + "pill-012-create-operations-transactional-rollback.md", P + "pill-008-kgdb-sldb-boundary.md"],
        depends_on=["task-rw-f2-typed-errors-and-exit-codes"],
        extra_files=["desk/contexts/pill-012-create-operations-transactional-rollback.md"],
        topics=["sldb-boundary", "transactions"],
    ),
    # ---------------- F3: domain services out of operations.py (serial) ----------------
    dict(
        id="task-rw-f3-drawer-routing-service",
        title="Drawer lookup moves to its own service",
        phase="F3",
        why=(
            "deskops/operations.py mixes many domains. Its drawer members are `DRAWER_INDEX_FILES` (491), "
            "`resolve_drawer_source` (493) and `attach_drawer_source` (525); inbox-to-drawer promotion lives in "
            "deskops/cli/commands/promote.py (`PromoteCLI`)."
        ),
        goal="`deskops/services/drawer.py` owns drawer lookup and promotion logic; `DeskopsOperations` and `PromoteCLI` delegate to it.",
        scope=(
            "In scope: moving those members and `PromoteCLI`'s helpers (`_inbox_to_drawer_task` minus its printing, "
            "`_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`) with unchanged "
            "behavior; `PromoteCLI.run` stays in the CLI and prints what the service returns. This task "
            "creates the `deskops/services/` package and sets its pattern: each service is a class constructed with "
            "`root: Path` that uses `deskops.desk_paths` and `deskops.doc_io` as modules; `DeskopsOperations.__init__` "
            "builds it lazily and its old methods become one-line wrappers. Out of scope: any new verb "
            "(task-rw-f3-drawer-entry-removal-verb)."
        ),
        implementation_path=(
            "1. Create deskops/services/__init__.py and deskops/services/drawer.py with `DrawerService(root)`.\n"
            "2. Move the members; leave wrappers in operations.py and promote.py.\n"
            "3. Run the named tests and the F1 contract tests unmodified."
        ),
        resolved=[COMMIT_FACT, f"The F1 CLI contract tests are {F1_CLI_TESTS}."],
        validation=["pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py", "pytest tests"],
        done_when="`def resolve_drawer_source` in deskops/operations.py is a one-line wrapper, `grep -n 'DrawerService(' deskops/cli/commands/promote.py` matches inside `PromoteCLI.run`, and the named tests pass unmodified.",
        files=["deskops/services/__init__.py", "deskops/services/drawer.py", OPS, "deskops/cli/commands/promote.py"],
        pills=[P + "pill-cli-gaps-become-tracked-work.md", P + "pill-operational-cli-grammar-follows-spoken-workflow.md"],
        depends_on=["task-rw-f2-transactional-doc-io"],
        topics=["refactor", "drawer"],
    ),
    dict(
        id="task-rw-f3-drawer-entry-removal-verb",
        title="A CLI verb removes a drawer entry",
        phase="F3",
        why=(
            "There is no deskops verb to delete a drawer entry. `deskops add task --from-drawer` keeps the entry 'for "
            "manual cleanup', so operators delete files by hand and nothing checks whether a task still records that "
            "entry in `from_drawer` (a provenance field that may dangle; see `PROVENANCE_FIELDS` in "
            "deskops/graph/extract_edges.py:31). desk/drawer/tasks/Board.md is hand-maintained prose: entries appear as "
            "bullets of the form ``- `<task-id>` — <summary>`` under several headings."
        ),
        goal="The approved verb removes one drawer file, untracks it if tracked, and deletes every Board.md bullet that starts with ``- `<its stem>` ``.",
        scope="Blocked on the owner decision (see Open Ambiguities). Uses `DrawerService` and `DocTransaction`.",
        implementation_path=(
            "1. Add the verb to deskops/cli/parser.py.\n2. Implement removal in `DrawerService` inside a `DocTransaction`.\n"
            "3. CLI test in a sandbox: the file is gone, its Board bullets are gone, other bullets are intact."
        ),
        resolved=[SANDBOX_FACT, COMMIT_FACT],
        validation=["pytest tests/test_inbox_promote_cli_gaps.py", "pytest tests"],
        done_when="The verb removes the entry and its Board bullets and the test passes.",
        files=["deskops/services/drawer.py", "deskops/cli/parser.py", "tests/test_inbox_promote_cli_gaps.py"],
        pills=[P + "pill-cli-gaps-become-tracked-work.md", P + "pill-operational-cli-grammar-follows-spoken-workflow.md"],
        depends_on=["task-rw-f3-drawer-routing-service"],
        topics=["drawer", "cli"],
        ambiguities=[
            "Owner decision: the verb's name (for example `deskops drawer remove <selector>`), and whether it refuses, "
            "warns, or proceeds silently when an active task's `from_drawer` points at the entry.",
        ],
        status="blocked",
    ),
    dict(
        id="task-rw-f3-closeout-gates-service",
        title="Closeout gates move to a service and verify real evidence",
        phase="F3",
        why=(
            "Inventory finding X6. The commit gate `_reference_points_to_commit` (deskops/operations.py:1818) accepts "
            "anything `git rev-parse --verify <ref>^{commit}` resolves, so `HEAD` or `main` pass; the tests gate "
            "`_reference_points_to_test` (1797-1816) strips `::node` and accepts any existing `.py` path. "
            "`references: [\"HEAD\", \"deskops/x.py\"]` passes closeout."
        ),
        goal=(
            "`deskops/services/closeout_gates.py` owns the gates and the closeout graph context; the commit gate accepts "
            "only a 7-40 character lowercase hex id that resolves to a commit that is HEAD or an ancestor of it (existing "
            "tests pass HEAD's own hash, tests/test_closeout.py:335 and tests/test_lifecycle_end_to_end.py:126); the tests gate "
            "accepts only a `.py` path inside `<root>/tests/` (optionally followed by `::node`, whose node part is not "
            "validated) that exists."
        ),
        scope=(
            "In scope: moving `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test` "
            "and `_build_closeout_graph_context` into the service with wrappers, tightening the two gates, and tests. "
            "Absolute paths and paths escaping `tests/` via `..` are rejected. Out of scope: the closure path itself "
            "(task-rw-f3-single-closure-path)."
        ),
        implementation_path=(
            "1. Move the functions (pattern from task-rw-f3-drawer-routing-service).\n"
            "2. Commit gate: `re.fullmatch(r'[0-9a-f]{7,40}', ref)`, then `git rev-parse --verify <ref>^{commit}` (an "
            "ambiguous abbreviation fails here and is rejected), then `git merge-base --is-ancestor <full sha> HEAD`.\n"
            "3. Tests gate: split off `::...`; reject the reference if `Path(ref).is_absolute()`; otherwise resolve it "
            "against root and require suffix `.py`, existence, and `resolved.is_relative_to((root / 'tests').resolve())`.\n"
            "4. tests/test_closeout.py: `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py` and `tests/../deskops/x.py` are "
            "rejected; a real ancestor hash and `tests/test_x.py::test_y` are accepted."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py", "pytest tests"],
        done_when="The new gate tests pass, the lifecycle test still closes its task, and `pytest tests` is green.",
        files=["deskops/services/closeout_gates.py", OPS, "tests/test_closeout.py"],
        pills=[P + "pill-closeout-knowledge-gates-require-traceable-evidence.md", P + "pill-001-task-closure-commit.md"],
        depends_on=["task-rw-f3-drawer-routing-service"],
        topics=["closeout", "gates"],
    ),
    dict(
        id="task-rw-f3-tasks-service",
        title="Task lifecycle moves to a service and reads TaskDoc only through sldb",
        phase="F3",
        why=(
            "Inventory finding S3: for TaskDoc only, `_read_doc` (deskops/operations.py:2366-2377) overlays the regex "
            "parser `parse_task_sections` (127-181) on `extract_model_data`, and the regex wins when they disagree. "
            "`parse_task_sections` is also used by deskops/cli/commands/promote.py:47 to read free-form inbox notes, "
            "which are not TaskDocs. CLI argument parsing (`parse_task_input` and `parse_artifact_input`, 991-1037) also lives in operations.py."
        ),
        goal=(
            "`deskops/services/tasks.py` owns create/advance/next for tasks; `_read_doc` reads TaskDoc only through "
            "`extract_model_data`; `parse_task_sections` remains only as an inbox-note helper used by promote.py; the "
            "`parse_*_input` functions move to deskops/cli/."
        ),
        scope=(
            "In scope: the move, removing the overlay, moving the parsers, and editing TaskDoc files under desk/tasks/ "
            "and desk/drawer/tasks/ when step 1 finds a divergence. Service methods keep today's signatures "
            "(`create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, the `next` report "
            "function) and CLI output for create, advance and next stays as pinned by the existing tests "
            "(tests/test_cli.py:650 add task, 1440 show/list/advance, 772 next). "
            "operations.py keeps no re-export of the moved parsers. Out of scope: the closure path "
            "(task-rw-f3-single-closure-path), changing how `list tasks` reports unreadable documents (today a stderr "
            "warning naming the file, operations.py:485-488), and TaskDoc contract changes (F6)."
        ),
        implementation_path=(
            "1. New tests/test_taskdoc_read_without_overlay.py compares overlay output with `extract_model_data` for "
            "every TaskDoc under desk/tasks/, desk/drawer/tasks/ (minus Board.md) and tests/fixtures/; fix any "
            "divergence by fixing the document, not by keeping the overlay. A document that `extract_model_data` "
            "cannot parse at all is listed by the test as a failure, never skipped.\n"
            "2. Remove the overlay branch from `_read_doc`; move `parse_task_sections` into "
            "deskops/cli/commands/promote.py as a private helper; delete `parse_validation_section` (operations.py:184), "
            "whose only caller is the overlay. Keep the new test as a regression guard that `_read_doc(TaskDoc)` equals "
            "`extract_model_data` for every TaskDoc.\n"
            "3. Move lifecycle methods into the service and `parse_*_input`, with the helpers only they use "
            "(`_load_yaml_mapping`, `_load_json_mapping`), into deskops/cli/parse_input.py; parse_input may import "
            "from operations.py (for `ARTIFACT_MODELS`), and operations.py must not import parse_input, so there is "
            "no cycle."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests", "deskops list tasks --root .", "deskops show task task-write-end-to-end-deskops-operator-manual --root ."],
        done_when="`grep -n 'parse_task_sections\\|def parse_.*_input' deskops/operations.py` is empty, deskops/services/tasks.py defines create, advance and next, both CLI checks print the task, and `pytest tests` is green.",
        files=["deskops/services/tasks.py", OPS, "deskops/cli/commands/operations.py", "deskops/cli/commands/promote.py", "deskops/cli/parse_input.py",
               "tests/test_taskdoc_read_without_overlay.py"],
        pills=[P + "pill-list-surfaces-must-expose-malformed-docs.md", P + "pill-007-phase-gated-task-flow.md"],
        depends_on=["task-rw-f3-closeout-gates-service"],
        topics=["refactor", "tasks"],
    ),
    dict(
        id="task-rw-f3-atoms-service",
        title="Atom operations move to a service; merge and split roll back fully",
        phase="F3",
        why="Atoms are the largest domain left in deskops/operations.py after the earlier F3 tasks; merge and split write several files and their rollbacks are partial (inventory D7).",
        goal=(
            "`deskops/services/atoms.py` (`AtomsService(root)`) owns atom create, edit, split, merge, retarget and delete; "
            "every write goes through doc_io; merge and split run inside one `DocTransaction` each; operations.py keeps "
            "only wrappers."
        ),
        scope=(
            "In scope: the move and the two transactions. 'Unchanged behavior' means tests/test_atoms_cli.py, "
            "tests/test_atoms_split.py, tests/test_atoms_create_from_source.py and tests/test_atoms_merge.py pass "
            "unmodified. Out of scope: new atom features."
        ),
        implementation_path=(
            "1. Move the atom methods and `_find_inbound_atom_references`/`_rewrite_inbound_atom_references`.\n"
            "2. Wrap `merge_atom` and `split_atom` each in one `DocTransaction`.\n"
            "3. Failure-injection tests: make the doc_io track step raise after the referrer rewrite (merge) and after "
            "the first new atom is written (split); assert every touched file's bytes equal the originals and "
            "`sldb stores check` is unchanged."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py", "pytest tests"],
        done_when="`grep -n 'def merge_atom' deskops/services/atoms.py` matches, operations.py only delegates, both injection tests pass, and `pytest tests` is green.",
        files=["deskops/services/atoms.py", OPS, "tests/test_atoms_merge.py", "tests/test_atoms_split.py"],
        pills=[P + "pill-atom-lifecycle-preserves-provenance-and-materialization-links.md", P + "pill-012-create-operations-transactional-rollback.md"],
        depends_on=["task-rw-f3-tasks-service"],
        topics=["refactor", "atoms"],
    ),
    dict(
        id="task-rw-f3-single-closure-path",
        title="One closure service behind every way of closing a task",
        phase="F3",
        why=(
            "Inventory finding S1: three ways to close a task. `deskops advance` at the closeout node runs gates and "
            "commits through `_auto_commit_task_closure`; `deskops advance task <id> --to complete` skips gates, does "
            "not commit and leaves the task on the Board; `deskops closeout commit` (deskops/cli/commands/closeout.py) "
            "makes the commit but runs no gates and does not touch the Board. Issue 2 is decided (owner, 2026-10-16): "
            "option A, shipped in 819a8b8 as `deskops closeout commit --no-run --reason <text>` (trailers "
            "`Closeout-Mode: manual` and `Closeout-Reason`, index entry with `run_dir: null` and `mode: manual`). Tasks "
            "closed before that use a fabricated run dir such as "
            "runs/subagents/20260901-manual-task-fix-sldb-deskops-cli-drift-breaking-11-tests; it stays as history."
        ),
        goal=(
            "`deskops/services/closure.py` performs every closure: gates (closeout_gates), Board update, bundle removal, "
            "exactly one commit with the route's trailers, and the index entry. `closeout commit` (both routes) uses it "
            "with its CLI unchanged."
        ),
        scope=(
            "In scope: closure.py, rewiring `closeout commit`, rewiring `advance` per the open decision, and updating "
            "desk/rituals/closeout.md so it names `deskops closeout commit` as the one entry point. Out of scope: the "
            "`--run-dir`/`--no-run` CLI contract, which is fixed."
        ),
        implementation_path=(
            "1. Implement closure.py on closeout_gates and doc_io, with both routes.\n"
            "2. Point `closeout commit` at it; its existing tests in tests/test_closeout.py pass unmodified. "
            "tests/test_lifecycle_end_to_end.py may change only where the decision changes what `advance` does.\n"
            "3. Rewire `advance` and `advance --to complete` per the decision.\n"
            "4. 'Same closure result' means: exit 0, task file gone, task removed from "
            "desk/tasks/Board.md, one new commit with the route's trailers, one new index line."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py", "pytest tests"],
        done_when="Every closing entry point produces the result defined in step 4, and desk/rituals/closeout.md names one entry point.",
        files=["deskops/services/closure.py", OPS, "deskops/cli/commands/closeout.py", "desk/rituals/closeout.md"],
        pills=[P + "pill-001-task-closure-commit.md", P + "pill-005-subagent-execution.md", P + "pill-closeout-knowledge-gates-require-traceable-evidence.md"],
        depends_on=["task-rw-f3-atoms-service"],
        topics=["closeout"],
        ambiguities=[
            "Owner decision: once closure is unified, what do `advance` at the closeout node and `advance --to complete` do? "
            "A) they stop closing and tell the operator to run `closeout commit` (recommended: one entry point); "
            "B) they call the closure service and accept `--run-dir` or `--no-run --reason`; "
            "C) `--to complete` is removed and `advance` keeps closing through the service.",
        ],
        status="blocked",
    ),
    # ---------------- F4: graph ----------------
    dict(
        id="task-rw-f4-request-sldb-unresolved-references",
        title="Write the sldb request for resolving bare ids and reporting unresolved references",
        phase="F4",
        why=(
            "deskops wants its declared graph edges from sldb's edge index instead of its own regex extractor. Two sldb "
            "behaviors block that: `_ids_in` (../sldb/src/sldb/store/edge_index/declared_references.py:66-74) keeps only "
            "values written `Model:name`, and deskops stores bare ids (`depends_on: [task-x]`, pill paths), so sldb emits "
            "no edge for any deskops reference; and `resolve_edges` (../sldb/src/sldb/store/edge_index/resolve.py:20-30) "
            "drops schema edges whose target is not tracked without reporting them, so `graph missing` cannot be "
            "computed from sldb."
        ),
        goal=(
            "runs/planning/sldb-request-unresolved-references.md contains a reproduction and a proposed public API for "
            "both gaps, and the coordinator's written reply is pasted into its `## Response` section."
        ),
        scope=(
            "In scope: the request document. The reproduction runs only in a throwaway repo under /tmp: git init, "
            "`deskops init .` (creates the store, registers the deskops models and scaffolds desk/), then "
            "`deskops add task` twice, one task with `depends_on: [task-nope]` and one with "
            "`depends_on: [TaskDoc:task-nope]`, then inspect sldb's edge index for both; never in ../sldb or its desk. "
            "Delivery: the supervisor of this deskops session pastes the file to the coordinator; the executor stops "
            "after writing the reproduction and proposal, and the supervisor pastes the reply. Out of scope: writing into the sldb repo or "
            "its inbox; the coordinator (the session that supervises deskops and owns sldb) routes it."
        ),
        implementation_path=(
            "1. Reproduce and paste commands and output under `## Reproduction`.\n"
            "2. Under `## Proposed API`: (a) how a declared reference field can resolve bare ids (for example a per-field "
            "allowed-model list, as `__containment__` already has); (b) a function such as "
            "`sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.\n"
            "3. Under `## deskops caller`: which deskops function will call it (`deskops graph missing`).\n"
            "4. Hand the file to the coordinator and paste the reply under `## Response`."
        ),
        resolved=[COMMIT_FACT],
        validation=[
            "test -f runs/planning/sldb-request-unresolved-references.md",
            "grep -q '^## Reproduction' runs/planning/sldb-request-unresolved-references.md",
            "grep -q '^## Proposed API' runs/planning/sldb-request-unresolved-references.md",
            "grep -q '^## deskops caller' runs/planning/sldb-request-unresolved-references.md",
            "grep -q '^## Response' runs/planning/sldb-request-unresolved-references.md",
        ],
        done_when="All validation checks pass and `## Response` holds the coordinator's reply, stating for each of the two gaps whether the proposed API is accepted, changed (with the agreed signature), or rejected.",
        files=["runs/planning/sldb-request-unresolved-references.md"],
        pills=[P + "pill-008-kgdb-sldb-boundary.md", P + "pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md"],
        depends_on=list(F1_DONE),
        topics=["graph", "cross-repo"],
    ),
    dict(
        id="task-rw-f4-graph-on-sldb-edge-index",
        title="Declared graph edges come from the sldb edge index",
        phase="F4",
        why=(
            "Inventory finding S4: deskops/graph/extract_edges.py re-implements with regex the declared edges sldb "
            "indexes, and deskops uses several node-id schemes (`task:`, `atom:`, `pill:`, `doc:`, `board:`, "
            "`drawer_task:<path>`, ... from deskops/graph/extract_docs.py:59-115, plus `source_file:`/`test_file:` from "
            "extract_sources.py:108-112), so promoting a drawer task changes its node id."
        ),
        goal=(
            "Edges declared by model fields come from sldb's public edge index (per the API agreed in "
            "task-rw-f4-request-sldb-unresolved-references); document nodes use one id scheme `<kind>:<id>` with "
            "`drawer_task` folded into `task`; file nodes keep `source_file:<path>`/`test_file:<path>`; `graph missing` "
            "uses sldb's unresolved-reference report. Id mapping: kinds keyed by frontmatter `id` today (atom, task, "
            "pill, board, and the rest in deskops/graph/extract_docs.py:183-193) keep `<kind>:<frontmatter id>`; "
            "`drawer_task:<path>` becomes `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) keep "
            "`<kind>:<path>`. Old ids get no alias."
        ),
        scope=(
            "In scope: extract_edges.py, extract_docs.py, snapshot.py, the closeout graph context in "
            "deskops/services/closeout_gates.py, and the graph tests listed below, which may be updated for the id "
            "change. Edges sldb cannot provide stay local: diagram `source:` edges (`_diagram_source_declarations`), "
            "section-declared atom refs (`_section_declarations`), YAML-fenced atom declarations in bodies "
            "(`_atom_declarations`, extract_edges.py:244), the per-line path scanner, and frontmatter fields of models "
            "that declare no `__references__`/`__containment__` (today MaterializationContractDoc's `source_atoms` and "
            "`target_identity`, read by `_declarations_from_mapping`, pinned by tests/test_materialization_contract.py:163), "
            "and the frontmatter edges of documents the store does not track (drawer tasks and any other untracked desk "
            "document; .sldb/core/documents/ holds only tracked ones), which keep the local extraction. Out of scope: the "
            "coverage extractor. Other code and fixtures that hard-code old ids are updated in this task: "
            "deskops/graph/self_reflection.py:164,173,450, deskops/operations.py:1304,1863 (or their moved copies), "
            "deskops/cli/parser.py:323, tests/fixtures/knowledge_graph/static_desk_source_graph.json and "
            "tests/test_graph_extract_docs.py:48-53."
        ),
        implementation_path=(
            "1. Before changing anything, save `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt` "
            "(a committed artifact).\n"
            "2. Switch declared-field edges to sldb; keep the local edges named in Scope.\n"
            "3. Keep today's edge roles: the local extractor uses the declaring field name as the role (for example "
            "`depends_on`, `pills`, tests/test_graph_declared_edges.py:78-92), while sldb emits `references`/`contains` "
            "with the field in its metadata; map each sldb edge back to role = its `field`, so roles do not change. "
            "Rename node ids; update tests/fixtures/golden/graph_snapshot.kg.json and the graph tests for the id "
            "change only (anything else that changes is a regression to fix), and write the old->new id table to runs/planning/graph-id-mapping.md.\n"
            "4. `graph missing` must report the same set of dangling references as the baseline: compare the sets of "
            "(kind, mapped source id, mapped target id) tuples, ignoring order."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py", "deskops graph missing --root .", "pytest tests"],
        done_when="extract_edges.py no longer parses the declared reference fields of store-tracked documents (the local cases listed in Scope remain), the dangling-reference set matches the baseline modulo the id mapping, and `pytest tests` is green.",
        files=["deskops/graph/extract_edges.py", "deskops/graph/extract_docs.py", "deskops/graph/snapshot.py", "deskops/services/closeout_gates.py",
               "tests/test_graph_cli.py", "tests/test_graph_declared_edges.py", "tests/test_graph_extract_edges.py", "runs/planning/graph-missing-baseline.txt",
               "tests/fixtures/golden/graph_snapshot.kg.json", "runs/planning/graph-id-mapping.md", "deskops/graph/self_reflection.py",
               "deskops/cli/parser.py", "tests/fixtures/knowledge_graph/static_desk_source_graph.json", "tests/test_graph_extract_docs.py"],
        pills=[P + "pill-008-kgdb-sldb-boundary.md", P + "pill-009-source-file-graph-traceability.md", P + "pill-010-graph-runtime-output-policy.md"],
        depends_on=["task-rw-f4-request-sldb-unresolved-references", "task-rw-f3-atoms-service", "task-rw-f3-closeout-gates-service", "task-rw-f0-graph-missing-ignores-archived-records", "task-rw-f1-output-golden-files"],
        topics=["graph", "sldb-boundary"],
    ),
    dict(
        id="task-rw-f4-single-snapshot-reader",
        title="One reader for the graph snapshot",
        phase="F4",
        why=(
            "Inventory finding S5: snapshot.py, checks.py and self_reflection.py in deskops/graph/ each parse the snapshot "
            "JSON with different keys and different errors (`GraphSnapshotReadError`, defined at snapshot.py:29 and "
            "raised at 53 and 58; `GraphMissingCheckError`, defined at checks.py:13, raised at 42 and caught by the CLI "
            "at cli/main.py:292 and 329; raw `JSONDecodeError` elsewhere)."
        ),
        goal=(
            "`deskops.graph.snapshot.read_graph_snapshot(path: Path) -> GraphSnapshot` (dataclasses "
            "`GraphSnapshot(nodes, edges)`, `Node(id, kind=None, path=None, identity=None, label=None)` with `identity` kept raw "
            "(dict or str, as stored), `Edge(source, target, role='related', provenance_path=None, "
            "provenance_locator=None, extractor=None)`, no caching) is "
            "the only snapshot parser; it raises `GraphSnapshotReadError` for a missing file, invalid JSON or a missing "
            "key; checks.py and self_reflection.py use it. The snapshot `graph build` writes has top-level `version`, "
            "`nodes` and `metadata` and nests each node's outgoing edges in `nodes[].edges` (snapshot.py:85-101); the "
            "reader flattens those into `GraphSnapshot.edges`, and also accepts a top-level `edges` list if present. "
            "Required: the `nodes` list, each node's id (`id` or `identity.node_id`), and each edge's target (`target` "
            "or `target_id`; its source is the enclosing node when nested); every other field is optional with "
            "the defaults above. Any other malformed shape (a non-list, a non-dict item) also raises "
            "`GraphSnapshotReadError`. checks.py's own `read_graph_snapshot` (checks.py:40) is removed; checks.py "
            "catches `GraphSnapshotReadError` from the snapshot reader and re-raises `GraphMissingCheckError` with the same "
            "message (`raise ... from exc`), so `_graph_missing`'s `except GraphMissingCheckError` (cli/main.py:292) keeps "
            "working; `_graph_reflect` (cli/main.py:321-333) reads the snapshot itself, so its `except` must also catch "
            "`GraphSnapshotReadError` (tests/test_graph_cli.py:233-240). Callers of the removed function (cli/main.py:321, "
            "self_reflection.py:422) and tests that pass raw dicts (tests/test_graph_checks.py:23,47, "
            "tests/test_graph_self_reflection.py:53,165) are updated: the check functions accept a `GraphSnapshot`."
        ),
        scope=(
            "In scope: the three modules and their tests. `read_graph_neighbors` keeps its signature and its output dicts "
            "byte-for-byte (keys node/incoming/outgoing/nodes and each node's `label`, which `deskops graph neighbors` "
            "prints, cli/main.py:341-364, tests/test_graph_cli.py:28,273); for that `Node` also carries "
            "`label: str | None` (semantics title, else label, else id, as snapshot.py:142 computes today). Out of "
            "scope: the snapshot format."
        ),
        implementation_path="1. Add the dataclasses and reader to snapshot.py; add reader tests (missing file, bad JSON, missing key, malformed shape, a valid snapshot) to the existing tests/test_graph_snapshot.py.\n2. Port checks.py and self_reflection.py.\n3. The golden snapshot test stays green.",
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py tests/test_output_goldens.py", "pytest tests"],
        done_when="`def read_graph_snapshot` exists only in deskops/graph/snapshot.py, checks.py and self_reflection.py contain no `json.load`/`json.loads` of the snapshot file (self_reflection.py:152 reads the separate decisions file and stays), the new reader tests pass, and `pytest tests` is green.",
        files=["deskops/graph/snapshot.py", "deskops/graph/checks.py", "deskops/graph/self_reflection.py", "tests/test_graph_snapshot.py",
               "deskops/cli/main.py", "tests/test_graph_checks.py", "tests/test_graph_self_reflection.py"],
        pills=[P + "pill-011-self-reflection-noise-control.md", P + "pill-010-graph-runtime-output-policy.md"],
        depends_on=["task-rw-f4-graph-on-sldb-edge-index", "task-rw-f1-output-golden-files"],
        topics=["graph"],
    ),
    dict(
        id="task-rw-f4-coverage-extractor-decision",
        title="Keep the coverage extractor as an optional report or delete it",
        phase="F4",
        why=(
            "Inventory finding S13: deskops/graph/extract_coverage.py (907 lines) scores matches with fixed thresholds; "
            "the tag-overlap (0.65, line 693) and token-overlap (0.60, line 727) scores fall below the 0.70 cutoff at line 636 "
            "and can never win; `confidence=\"high\"` is hard-coded at lines 192, 236, 248, 261 and 276 and written into "
            "snapshot edge metadata (snapshot.py:226); no deskops code reads it and no gate depends on the extractor."
        ),
        goal="The owner's choice is applied (see Open Ambiguities).",
        scope=(
            "Blocked on the owner decision. The supervisor records the choice under Resolved Decisions and lifts "
            "`blocked` when promoting. It runs after the F5 chain (the keep option adds a registry entry, and every F5 "
            "task edits deskops/cli/registry.py, created by task-rw-f5-command-registry, an ancestor through "
            "task-rw-f5-deprecated-aliases); with the delete option the supervisor may drop that dependency."
        ),
        implementation_path=(
            "Delete: remove the module, tests/test_graph_extract_coverage.py, its merge into the snapshot "
            "(snapshot.py:75-78) and its entry in `metadata.source_extractors` (snapshot.py:92, asserted by "
            "tests/test_graph_snapshot.py:43); update the golden snapshot. Keep: add "
            "`deskops graph coverage [--root] [--format text|json]` as a registry entry (task-rw-f5-command-registry) "
            "that prints one match per line (text) or a list (json) with fields element_id, atom_id, facet, score, basis, "
            "and always exits 0; remove coverage "
            "nodes, edges and the extractor entry from `graph build`; drop the two sub-cutoff scorers and the now-dead "
            "cutoff at line 636; compute `confidence` from the score (>=0.9 high, else medium)."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests", "deskops graph build --root ."],
        done_when="Delete: `grep -rn extract_coverage deskops/` is empty. Keep: `deskops graph coverage --help` exits 0 and the snapshot has no coverage nodes. Either way `pytest tests` is green.",
        files=["deskops/graph/extract_coverage.py", "tests/test_graph_extract_coverage.py", "deskops/graph/snapshot.py", "tests/test_graph_snapshot.py", "deskops/cli/registry.py"],
        pills=[P + "pill-010-graph-runtime-output-policy.md"],
        depends_on=["task-rw-f4-single-snapshot-reader", "task-rw-f5-deprecated-aliases"],
        topics=["graph"],
        ambiguities=["Owner decision: delete extract_coverage.py, or keep it as an opt-in `deskops graph coverage` report (semantics in Implementation Path)?"],
        status="blocked",
    ),
    # ---------------- F5: CLI ----------------
    dict(
        id="task-rw-f5-command-registry",
        title="The CLI is built from a declarative command registry",
        phase="F5",
        why="deskops/cli/parser.py is about 1,000 lines of hand-built argparse in which shared arguments (`--root`, selectors, `--format`) are redefined per command.",
        goal=(
            "deskops/cli/registry.py declares every command once (path, help, args, handler, `mutates: bool`); shared "
            "args are defined once; parser.py only walks the registry; every command's `--help` text stays "
            "byte-identical to the F1 help goldens, and exit codes stay as pinned by the F1 contract tests."
        ),
        scope=(
            "In scope: parser and dispatch. `--format` is two shared argument groups, not one: `text|json` "
            "(`_add_output_format_argument`, parser.py:839-845, and runtime workers) and `text|json|yaml` (inbox, "
            "message, faq); each command keeps its variant. Do not edit tests/test_cli*.py, tests/test_output_goldens.py, "
            "tests/conftest.py or anything under tests/fixtures/golden/, and do not run `--update-golden`. Out of scope: "
            "renaming commands or flags."
        ),
        implementation_path=(
            "1. Define the registry types as frozen dataclasses: `Arg(flags: tuple[str, ...], kwargs: dict, "
            "group: str | None = None, group_required: bool = False)` (args sharing a `group` go into one mutually "
            "exclusive group; required at parser.py:161 and 185, optional at 988) and `Command(path: tuple[str, ...], help: str, args: tuple[Arg, ...], "
            "handler: str, mutates: bool, epilog: str | None = None)`, where `handler` is a dotted "
            "`module:Class` path such as `deskops.cli.commands.runtime:RuntimeCLI`; commands generated from data "
            "today (the loops at parser.py:715, 780, 874 and 918, including the model-generated args) become "
            "factory functions that return `Command`s.\n2. Port commands group by group; after each group run the F1 contract tests "
            "and the `help/` goldens.\n3. Delete the per-command builder functions from parser.py; the walker's own "
            "`add_parser` call is the only one left.\n4. Add tests/test_command_registry.py asserting that the set of command paths declared in "
            "the registry equals the set of command paths that have a file in tests/fixtures/golden/help/ (written "
            "from the old parser by task-rw-f1-output-golden-files), so a dropped or extra command fails."
        ),
        resolved=[COMMIT_FACT, f"The F1 CLI contract tests are {F1_CLI_TESTS}; the help goldens are tests/fixtures/golden/help/ (task-rw-f1-output-golden-files)."],
        validation=["pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py", "python -m deskops --help", "deskops faq", "pytest tests"],
        done_when="registry.py exists, parser.py has no per-command builder functions, the registry-equality test passes, and the contract and golden tests pass with their files unmodified.",
        files=["deskops/cli/parser.py", "deskops/cli/main.py", "deskops/cli/registry.py", "tests/test_command_registry.py"],
        pills=[P + "pill-operational-cli-grammar-follows-spoken-workflow.md", P + "pill-real-cli-surfaces-prove-operator-contracts.md"],
        depends_on=["task-rw-f3-atoms-service", "task-rw-f4-single-snapshot-reader", "task-rw-f1-cli-contract-tests", "task-rw-f1-output-golden-files"],
        topics=["cli", "refactor"],
    ),
    dict(
        id="task-rw-f5-root-resolution-and-sandbox-guard",
        title="`--root` and the store resolve in one place, and the sandbox guard covers every mutating command",
        phase="F5",
        why=(
            "Inventory findings S7 and S8. `find_local_store()` (used by `resolve_store_context`, deskops/identity.py:36) "
            "walks up to `~/.sldb`, so a sandbox inside the repo uses the repo registry. The sandbox redirect "
            "`_apply_test_root_override` (deskops/cli/main.py:184-216) moves `--root .` to `DESKOPS_TEST_ROOT` or the "
            "configured sandbox root, but cannot tell an explicit `--root .` from the default, and its command list "
            "omits atoms, closeout, doctor and desk, which mutate the desk. "
            "`message` defaults `--root` to '.', so its `--store` branch (deskops/cli/commands/message.py:171-181) is "
            "unreachable."
        ),
        goal=(
            "One resolver turns `--root`/`--store`/cwd into `(desk_root, store)` for every command and stops searching at "
            "the nearest ancestor that contains `desk/` or `.git`; the redirect keeps its current action (it changes the "
            "root, it does not refuse) but applies to every command the registry marks `mutates=True` and only when "
            "`--root` was not given explicitly."
        ),
        scope=(
            "In scope: the resolver, the guard, message.py. Rules: `--root` sets desk_root; `--store` sets the store; if "
            "both are given and the store is not `<root>/.sldb`, fail with a usage error naming both. Mutating commands "
            "(known today): bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, "
            "atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, "
            "graph reflect, materialize, runtime init/stop, message send/ack, and the deprecated inbox alias. Read the "
            "handlers of atoms crossroad/proto/type and runtime workers/supervise and mark them too if they write files, "
            "the store or git; a test lists every `mutates=True` command so additions are deliberate. Out of scope: the "
            "registry format."
        ),
        implementation_path=(
            "1. `resolve_context(args) -> (desk_root, store)` in deskops/cli/registry.py.\n"
            "2. The upward search stops at the first ancestor with `desk/` or `.git`; if none exists up to the filesystem "
            "root, desk_root is the current directory and commands that need a store fail with the existing "
            "'No local store found' error.\n"
            "3. Mark the commands above `mutates=True`; the guard reads that flag.\n"
            "4. Tests: a sandbox nested inside a repo never reads the outer registry; `message list --store <s>` uses that store."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_message_cli.py tests/test_repo_identity.py", "pytest tests"],
        done_when="All new tests (nested sandbox, `message --store`, the mutating-command list) pass and `pytest tests` is green.",
        files=["deskops/identity.py", "deskops/cli/main.py", "deskops/cli/commands/message.py", "deskops/cli/registry.py"],
        pills=[P + "pill-project-local-config-carries-version-and-sandbox-policy.md", P + "pill-canonical-desk-identity-enables-horizontal-routing.md"],
        depends_on=["task-rw-f5-command-registry"],
        topics=["cli", "identity"],
    ),
    dict(
        id="task-rw-f5-output-renderer",
        title="One renderer for text, json and yaml output with an error envelope",
        phase="F5",
        why="Each command formats its own output; JSON shapes differ by command and errors have no machine-readable form.",
        goal=(
            "Handlers return data; deskops/cli/render.py prints it as text, json or yaml; with `--format json` an error "
            "prints `{\"ok\": false, \"error\": {\"code\": <exit code>, \"type\": \"<class name from deskops/errors.py, "
            "e.g. DomainError>\", \"message\": \"...\"}}` and exits with that code. argparse usage errors keep "
            "argparse's stderr text and exit 2 and are never wrapped, because they happen before `--format` is known."
        ),
        scope=(
            "Blocked on the owner decision about success shapes (see Open Ambiguities); the renderer, the port and the "
            "error envelope land together after it. Handlers return data plus, for text mode, a formatter that "
            "produces exactly today's stdout; before porting, record today's stdout for every format each command "
            "accepts as the output goldens (step 3), so byte-identity is checked against them. yaml is `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)` (PyYAML, already a "
            "dependency). The envelope prints to stdout, like the JSON it replaces. Streaming or progress output (for "
            "example `runtime supervise`) and `--help` bypass the renderer. Exit codes and class names come from "
            "deskops/errors.py (task-rw-f2-typed-errors-and-exit-codes)."
        ),
        implementation_path=(
            "1. Record the goldens of step 3 from the current code.\n2. Implement the renderer and the error envelope, "
            "then port commands; success JSON follows the decision.\n"
            "3. Goldens in tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml> for every command "
            "that accepts `--format`, compared by tests/test_output_goldens.py and refreshed only with `--update-golden`."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests", "deskops list tasks --root . --format json", "deskops list tasks --root ."],
        done_when="Every command with `--format` prints through the renderer and, for each format that command already accepts (text|json or text|json|yaml; no command gains a format), its output matches the golden recorded before porting (under option B the json comparison is between the golden and the envelope's `data`); `pytest tests` is green.",
        files=["deskops/cli/render.py", "deskops/cli/main.py", "deskops/cli/registry.py"],
        pills=[P + "pill-machine-readable-cli-output-needs-stable-contract.md"],
        depends_on=["task-rw-f5-root-resolution-and-sandbox-guard"],
        topics=["cli", "output"],
        ambiguities=["Owner decision: success JSON A) keeps today's per-command shapes (no break for external consumers), or B) is wrapped as `{\"ok\": true, \"data\": <today's shape>}`."],
        status="blocked",
    ),
    dict(
        id="task-rw-f5-deprecated-aliases",
        title="Duplicate commands become warned aliases or are removed",
        phase="F5",
        why="`inbox` duplicates `message`, `status` overlaps `doctor` (both run DoctorCLI, deskops/cli/main.py:80), and `atoms list/show` duplicate `list atoms`/`show atom`. The canonical side is `message`, `doctor` and `list atoms`/`show atom`.",
        goal="The owner's choice is applied to each duplicate.",
        scope=(
            "Blocked on the owner decision. Alias behavior: before any output, print "
            "``Deprecated: use `deskops <canonical>` `` on stderr, then run the canonical command. Removal behavior: argparse "
            "rejects the name (`invalid choice`, exit 2). Aliases stay listed in `--help` with their deprecation note "
            "(today's behavior, parser.py:500-505, asserted by tests/test_cli.py:42 and tests/test_message_cli.py:35). "
            "`inbox` has its own flag grammar (`--list/--show/--ack`) that `MessageCLI._run_legacy` "
            "(deskops/cli/commands/message.py:32,57) translates; that translation stays. Docs, skills, README.md, "
            "desk/atoms and desk/contexts that recommend an old name are updated in the same task; for a surviving "
            "alias, notes that say it is deprecated stay; for a removed name, every mention is rewritten to the "
            "canonical command. desk/drawer/ is history (use cases, stress tests) and is not edited."
        ),
        implementation_path=(
            "Aliases: add a field `deprecated_for: tuple[str, ...] | None = None` (the canonical command path, e.g. "
            "`(\"message\",)`) to the `Command` dataclass in deskops/cli/registry.py, which "
            "task-rw-f5-command-registry creates; the dispatcher (deskops/cli/main.py) prints the warning when it is set. Tests run the alias and the canonical command with equivalent args in the same test and assert "
            "the stderr line and byte-identical stdout, or exit 2 for each removed name (and update the command-set "
            "assertion in tests/test_cli.py:42 for removed names). Review every hit of the "
            "validation grep and rewrite the recommending ones."
        ),
        resolved=[COMMIT_FACT],
        validation=[
            "pytest tests",
            "deskops faq",
            "grep -rn 'deskops inbox\\|deskops status\\|deskops atoms list\\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts",
        ],
        done_when="Each duplicate behaves per the decision and every remaining grep hit is a deprecation note, not a recommendation.",
        files=["deskops/cli/registry.py", "deskops/cli/main.py", "deskops/cli/parser.py", "deskops/cli/commands/message.py", "tests/test_cli.py",
               "tests/test_message_cli.py", "docs/faq.md", ".pi/skills/use-deskops/SKILL.md", ".opencode/skills/use-deskops/SKILL.md", "README.md",
               "desk/atoms", "desk/contexts"],
        pills=[P + "pill-operational-cli-grammar-follows-spoken-workflow.md"],
        depends_on=["task-rw-f5-output-renderer", "task-rw-f5-command-registry"],
        topics=["cli"],
        ambiguities=["Owner decision, per duplicate (`inbox`, `status`, `atoms list`, `atoms show`): warned alias, or removal?"],
        status="blocked",
    ),
    # ---------------- F6: model contract changes ----------------
    dict(
        id="task-rw-f6-bootstrap-registers-all-models",
        title="Bootstrap registers every deskops model, and only bootstrap/init install sldb",
        phase="F6",
        why=(
            "Inventory finding S9: `MODEL_REFS` in deskops/bootstrap.py lists 12 models while the repo store registers 15 "
            "deskops models (plus sldb's RelationTypeDoc and RelationDoc, registered by the lifecycle graph), so a fresh "
            "`deskops init` does not register MaterializationContractDoc, RunDoc or RuntimeProfileDoc. "
            "`ensure_sldb_available` (bootstrap.py:36-62) can run `pip install -e ../sldb` from `list`, `show` or `add`."
        ),
        goal=(
            "`MODEL_REFS` stays a `dict[name, 'deskops.models:<Class>']`, built from every `StructuredNLDoc` subclass in "
            "`deskops.models.__all__` except the base classes `PrimitiveDoc` and `OperationalArtifactDoc`; a fresh init "
            "registers the same 15 deskops models as the repo store; only `bootstrap` and `init` may install sldb; other commands "
            "print the existing 'Error: sldb is not installed...' message and exit 1."
        ),
        scope="In scope: bootstrap.py, its callers' install flag, and two tests (A and B below) in tests/test_doctor_model_registration.py. Out of scope: model contract changes. Importers rely on the dict shape (deskops/cli/commands/desk.py:142, doctor.py:118, domain_tree.py:249-250, tests/test_doctor_model_registration.py:17).",
        implementation_path=(
            "1. Build MODEL_REFS as described.\n2. Add an `allow_install` parameter to `ensure_sldb_available`, true only "
            "from bootstrap and init.\n3. Test A: `deskops init` in a `tmp_path` repo, then assert "
            "`<tmp>/.sldb/core/store_index.yaml` exists and its model-name set equals the set derived from "
            "`deskops.models.__all__` minus the two bases, plus `RelationTypeDoc` and `RelationDoc` that the lifecycle "
            "graph registers during init (no hard-coded count).\n4. Test B (in-process, so monkeypatch works): monkeypatch sldb as not "
            "importable and spy on the install runner; `deskops list tasks` prints the error, exits 1, and the spy "
            "was not called."
        ),
        resolved=[SANDBOX_FACT, COMMIT_FACT],
        validation=["pytest tests/test_doctor_model_registration.py", "pytest tests"],
        done_when="Tests A and B pass and `pytest tests` is green.",
        files=["deskops/bootstrap.py", "tests/test_doctor_model_registration.py"],
        pills=[P + "pill-006-self-described-store-layout.md", P + "pill-doctor-separates-desk-repair-from-sldb-health.md"],
        depends_on=["task-rw-f5-command-registry"],
        topics=["models", "bootstrap"],
    ),
    dict(
        id="task-rw-f6-taskdoc-contract-cleanup",
        title="TaskDoc contract cleanup",
        phase="F6",
        why=(
            "Inventory finding S10, in deskops/models/task.py (afdec7f already dropped `routine` and `checklists` and "
            "pointed `current_node` at RitualDoc): TaskDoc sets `extra: allow`; the `frontmatter` field "
            "(`exclude=True`) is repopulated by `render_payload` from a hand-kept body-field list, the only deskops model "
            "using the dict-frontmatter template marker; `from_drawer` sits in `__references__` although it is "
            "provenance; and the `_omit_unset_from_drawer` docstring claims that omitting an empty `from_drawer` kept "
            "the contract hash stable, which is false (the field itself is hashed)."
        ),
        goal=(
            "TaskDoc uses `extra: ignore`, drops the `frontmatter` field, its `_merge_frontmatter` validator and the "
            "`render_payload` override, declares each frontmatter field with its own template marker (as PillDoc does), "
            "keeps `from_drawer` as a plain field outside `__references__`, and the docstring says it keeps "
            "documents byte-identical, not the contract hash; tests/fixtures/model_contract_hashes.json is updated deliberately."
        ),
        scope=(
            "Blocked on the owner deciding that F6 enters this cycle. The store migration is "
            "task-rw-f6-migrate-tracking-stores. `PROVENANCE_FIELDS` in deskops/graph/extract_edges.py stays: it also "
            "stops the line scanner from reading the `from_drawer` path (lines 340-346)."
        ),
        implementation_path=(
            "1. Before changing the model, save `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` for "
            "every file in desk/tasks/*.md and desk/drawer/tasks/*.md except Board.md, and every task file in the "
            "golden fixture desk (the round trip used in tests/test_composition.py:66).\n"
            "2. Pre-scan the stores found by task-rw-f6-migrate-tracking-stores' discovery rule for TaskDoc files with "
            "top-level frontmatter keys not in `TaskDoc.model_fields` (null values count) and list them in "
            "runs/planning/taskdoc-unknown-keys.md; with `extra: ignore` those keys are dropped, so those files are "
            "exempt from the byte-identical check and handled by the migration task.\n"
            "3. Change the model. Removing `from_drawer` from `__references__` drops the frontmatter `from_drawer` edge "
            "(deskops/graph/extract_edges.py:181-190); update tests/test_graph_declared_edges.py:131 to expect no edge.\n"
            "4. Run tests/test_model_contract_snapshot.py and copy the printed TaskDoc hash into the fixture.\n"
            "5. Re-render and compare with step 1; every file not listed in step 2 must be byte-identical."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py", "deskops graph missing --root .", "pytest tests"],
        done_when="`pytest tests` is green with the updated fixture and every TaskDoc not listed in runs/planning/taskdoc-unknown-keys.md renders byte-identically.",
        files=["deskops/models/task.py", "tests/fixtures/model_contract_hashes.json", "tests/test_graph_declared_edges.py", "runs/planning/taskdoc-unknown-keys.md"],
        pills=[P + "pill-legacy-desk-formats-need-explicit-adaptation.md", P + "pill-006-self-described-store-layout.md"],
        depends_on=["task-rw-f6-bootstrap-registers-all-models", "task-rw-f4-graph-on-sldb-edge-index", "task-rw-f1-model-contract-snapshot"],
        topics=["models", "contract"],
        ambiguities=["Owner decision: does F6 (TaskDoc contract change plus migrating the 24 stores that track it) enter this cycle, or is it postponed?"],
        status="blocked",
    ),
    dict(
        id="task-rw-f6-migrate-tracking-stores",
        title="Migrate every store that tracks deskops models",
        phase="F6",
        why="About 24 stores on this machine track TaskDoc; a contract change leaves each in FAIL until it runs `sldb models update` and `deskops desk update --apply`.",
        goal="scripts/migrate_desk_stores.py migrates every discovered store and logs per-store before/after `sldb stores check` results; every store passes afterwards.",
        scope=(
            "Blocked by the same owner decision as task-rw-f6-taskdoc-contract-cleanup. Discovery: directories named "
            "`.sldb` under $HOME whose `core/models/TaskDoc.yaml` exists, excluding paths containing `/.tmp/`, `/.venv/`, "
            "`/node_modules/`, `/tools/` or `/tmp/` (matched on whole path segments of the `.sldb` path relative to the "
            "discovery root, so a test tree under pytest's `tmp_path` is not excluded by its own location), and only when `git -C <parent of .sldb> rev-parse --is-inside-work-tree` prints `true`. Walk with "
            "`os.walk(followlinks=False)`, skip directories that raise PermissionError, and do not descend into a "
            "matched store. Each store's repo commit is its owner's."
        ),
        implementation_path=(
            "1. `--dry-run` (default) lists stores and the commands it would run and exits 0 iff at least one store was "
            "found; `--apply` runs them. `--home <dir>` (default `~`) sets the discovery root so tests can use a fake "
            "tree. Each command gets a 300 s timeout; a timeout is a FAIL.\n"
            "2. Per store (`<store>` = the `.sldb` dir, `<target>` = its parent repo, `<deskops>` = this deskops "
            "checkout, so `deskops.models` imports): `sldb stores check --store <store>`, then "
            "`sldb models update <Model> --store <store> --pythonpath <deskops>` for each deskops model whose contract "
            "hash changed (TaskDoc for task-rw-f6-taskdoc-contract-cleanup), then "
            "`deskops desk update --root <target> --apply`, then check again; on failure record FAIL and continue.\n"
            "3. Exit 0 only if at least one store was found and every store passes; re-running is safe.\n"
            "4. Log to runs/planning/store-migration-<YYYYMMDD>.md, starting with the full discovered list and its count.\n"
            "5. tests/test_migrate_desk_stores.py covers discovery and exclusion on a fake tree in `tmp_path`."
        ),
        resolved=[COMMIT_FACT],
        validation=["pytest tests/test_migrate_desk_stores.py", "python scripts/migrate_desk_stores.py --dry-run", "python scripts/migrate_desk_stores.py --apply", "sldb stores check --store .sldb", "pytest tests"],
        done_when="The log shows every discovered store PASS after `--apply`.",
        files=["scripts/migrate_desk_stores.py", "tests/test_migrate_desk_stores.py"],
        pills=[P + "pill-legacy-desk-formats-need-explicit-adaptation.md"],
        depends_on=["task-rw-f6-taskdoc-contract-cleanup"],
        topics=["models", "migration"],
        ambiguities=["Blocked by the same owner decision as task-rw-f6-taskdoc-contract-cleanup: does F6 enter this cycle?"],
        status="blocked",
    ),
]


def render(task: dict) -> str:
    front = {
        "id": task["id"],
        "status": task.get("status", "deferred"),
        "references": [],
        "depends_on": task["depends_on"],
        "pills": task["pills"],
        "files": task["files"] + task.get("extra_files", []),
        "task_type": "implementation",
        "tags": ["workspace:desk", "artifact:task", "source:drawer", "plan:deskops-rewrite", f"phase:{task['phase'].lower()}"]
        + [f"topic:{t}" for t in task["topics"]],
    }
    amb = task.get("ambiguities") or []
    amb_text = "\n".join(f"- {a}" for a in amb) if amb else "None."
    resolved = task.get("resolved") or []
    resolved_text = "\n".join(f"- {r}" for r in resolved) if resolved else "None."
    validation = "\n".join(f"- {v}" for v in task["validation"])
    return (
        "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n"
        f"# {task['title']}\n\n"
        "## Rationale\n\n_Explain why this task exists or the business driver behind it._\n\n"
        f"{task['why']}\n\nPlan: phase {task['phase']} of `{INVENTORY}`.\n\n"
        "## Goal\n\n_Describe the concrete result this task must produce._\n\n"
        f"{task['goal']}\n\n"
        "## Scope\n\n_State what is in scope and what is out of scope._\n\n"
        f"{task['scope']}\n\n"
        "## Implementation Path\n\n_Outline the expected implementation route or affected surface._\n\n"
        f"{task['implementation_path']}\n\n"
        "## Validation\n\n_List the checks required before this task can close._\n\n"
        f"{validation}\n\n"
        "## Done When\n\n_Name the observable condition that makes the task complete._\n\n"
        f"{task['done_when']}\n\n"
        "## Resolved Decisions\n\n"
        f"{resolved_text}\n\n"
        "## Open Ambiguities\n\n"
        f"{amb_text}\n"
    )


BOARD_HEADING = "### Deskops rewrite plan (2026-10-16)"
BOARD_ANCHOR = "\nPromoted to active desk tasks:"
HAND_MAINTAINED = {"task-doctor-crashes-on-deskless-roots": ("F0", "Doctor no longer crashes on roots without `desk/` (finding X1)")}


def render_board_section() -> str:
    rows: dict[str, list[str]] = {}
    for tid, (phase, title) in HAND_MAINTAINED.items():
        rows.setdefault(phase, []).append(f"- `{tid}` — {title}")
    for task in TASKS:
        flag = " (**blocked**)" if task.get("status") == "blocked" else ""
        rows.setdefault(task["phase"], []).append(f"- `{task['id']}` — {task['title']}{flag}")
    out = [
        "", BOARD_HEADING, "",
        f"Every node of the DAG in `{INVENTORY}`, one deferred task each, generated by",
        "`runs/planning/rewrite-plan/gen.py`. `depends_on` carries the order; tasks marked **blocked**",
        "wait on an owner decision named in their `## Open Ambiguities`. Tasks that edit",
        "`deskops/operations.py` run in series.", "",
    ]
    for phase in ["F0", "F1", "F2", "F3", "F4", "F5", "F6"]:
        out += [f"{phase}:", "", *rows.get(phase, []), ""]
    return "\n".join(out)


def update_board() -> None:
    board = DRAWER / "Board.md"
    text = board.read_text(encoding="utf-8")
    section = render_board_section()
    if BOARD_HEADING in text:
        start = text.index("\n" + BOARD_HEADING)
        end = text.index(BOARD_ANCHOR, start)
        text = text[:start] + section + text[end:]
    else:
        text = text.replace(BOARD_ANCHOR, section + BOARD_ANCHOR, 1)
    board.write_text(text, encoding="utf-8")


def main() -> int:
    ids = {t["id"] for t in TASKS}
    for stale in DRAWER.glob("task-rw-*.md"):
        if stale.stem not in ids:
            stale.unlink()
            print(f"removed stale {stale.name}")
    for task in TASKS:
        (DRAWER / f"{task['id']}.md").write_text(render(task), encoding="utf-8")
    update_board()
    print(f"wrote {len(TASKS)} tasks and the drawer Board plan section")
    return 0


if __name__ == "__main__":
    sys.exit(main())
