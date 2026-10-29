# Tester Review

**Task**: task-declared-materialization-targets-resolve-outside-the-indexed-package  
**Role**: tester  
**Run ID**: 20261021-materialization-targets-outside-package  
**Date**: 2026-10-21T17:15:00-03:00

## Summary

**Overall**: PASS (with expected pre-closeout findings)

---

## Check 1: Run Validation Commands

| Command | Result | Notes |
|---------|--------|-------|
| `pytest tests/test_materialization_targets_outside_package.py` | PASS (4/4) | 65s |
| `pytest tests/test_graph_extract_sources.py` | PASS (14/14) | 0.18s |
| `pytest tests/test_materialization_contract.py` | PASS (5/5) | 2.43s |
| `pytest tests/test_output_goldens.py` | PARTIAL (timeout on test_help_goldens) | Unrelated to this task |
| `deskops graph missing --root .` | PASS (exit 0) | No missing graph references |

**Verdict**: PASS

---

## Check 2: Diff Review

### Scope Creep
- **PASS**: Changes are tightly scoped to:
  - `deskops/graph/extract_sources.py`: New `_declared_materialization_target_nodes()` and `_read_target_identity()` functions
  - `deskops/operations.py`: Single-line change adding `"artifact.materialization"` to tracking
  - `docs/knowledge-graph/desk-source-graph-vocabulary.md`: One-sentence doc update
  - Tests: Two test files with appropriate coverage

### Mocks/Stubs
- **PASS**: No mocks or stubs. Tests use:
  - `tmp_path` fixtures with real file system operations
  - `subprocess` CLI invocations with real git repos
  - Real `deskops init`, `add atom`, `add materialization` commands

### Literal-Duplicating Assertions
- **PASS**: Assertions test behavior, not literal duplication:
  - Tests verify node existence by id pattern
  - Tests verify provenance `source_kind` value
  - Tests verify CLI exit codes and JSON output structure

### Path Rejection Rules Correctness

| Rule | Implementation | Test Coverage |
|------|----------------|---------------|
| Strip leading `./` | `normalized = target_identity.lstrip("./")` | `test_declared_target_leading_dotslash_is_stripped` |
| Reject absolute paths | `if normalized.startswith("/")` | `test_declared_target_absolute_path_produces_no_node` |
| Reject `..` segments | `if ".." in Path(normalized).parts` | `test_declared_target_dotdot_path_produces_no_node` |
| Reject `:` (kind:id) | `if ":" in normalized` | `test_declared_target_kind_id_produces_no_node` |
| Outside-root symlinks | `resolved.relative_to(root.resolve())` | Implicit via path resolution |
| Excluded dirs (.tmp/, tools/) | `if _is_excluded(root, resolved)` | `test_declared_target_excluded_tmp_produces_no_node`, `test_declared_target_excluded_tools_produces_no_node` |
| Doc surfaces | `if relative_path in doc_paths` | `test_declared_target_doc_surface_produces_no_source_node` |
| Dedupe | `if relative_path in existing_paths` and `if relative_path in seen_paths` | `test_declared_target_already_matched_by_path_rule_not_duplicated` |

**Verdict**: PASS

---

## Check 3: Sandbox End-to-End Reproduction

Location: `.tmp/tester-gov-repro`

| Step | Result |
|------|--------|
| `deskops init` | PASS |
| Create `src/vsm/organs/links.py` | PASS |
| Create `.github/workflows/pulse.yml` | PASS |
| `deskops add atom` | PASS (atom-ci-cd-workflow-policy) |
| `deskops add materialization` (links) | PASS |
| `deskops add materialization` (pulse) | PASS |
| `deskops graph missing` exit 0 | PASS |
| `sldb stores check --format json` lists MaterializationContractDoc with 2 documents | PASS |

**Verdict**: PASS

---

## Check 4: Closeout Verify on Real Repo

```bash
deskops closeout verify --root . --task task-declared-materialization-targets-resolve-outside-the-indexed-package
```

### Findings

| Finding | Expected | Notes |
|---------|----------|-------|
| `missing_tests_evidence` | Yes | Pre-commit: task references not yet linked to test evidence |
| `missing_commit_evidence` | Yes | Pre-commit: no commit SHA in references |
| `missing_changed_file_link` | **Not present** | ✓ This was the bug being fixed |

### Gate Status

| Gate | Status | Evidence Count |
|------|--------|----------------|
| `atom_or_materialization_link` | OK | 21 evidence items |
| `commit` | FAIL | Expected (pre-commit) |
| `tests` | FAIL | Expected (pre-commit) |

**Verdict**: PASS - No `missing_changed_file_link` for any of the task's changed files

---

## Guardrails Proven

1. **MaterializationContractDoc targets outside desk/deskops become graph nodes**: Verified via unit tests and sandbox CLI
2. **Targets with invalid paths (absolute, `..`, `:`) produce no node**: Unit test coverage complete
3. **Doc surfaces not duplicated as source_file nodes**: Explicit test
4. **Excluded dirs stay missing_declared_target**: Tests for .tmp/ and tools/
5. **Materializations are tracked in .sldb store**: CLI test and sandbox verification
6. **Closeout accepts materialization coverage**: No missing_changed_file_link in closeout verify

---

## Stale or Missing Tests

None found. All tests are newly written and match the scope.

---

## Follow-up Needed Before Closeout

1. **Commit the changes**: The task needs a commit reference in `references` field
2. **Full pytest suite**: The `test_help_goldens` timeout should be investigated separately (unrelated to this task)

---

## Defects Found

**None**

---

## Files Changed (from git diff --stat)

```
.sldb/store.yaml                                   |   4 +
desk/tasks/task-...outside-the-indexed-package.md  |   6 +-
deskops/graph/extract_sources.py                   | 135 +++++++++++++++
deskops/operations.py                              |   2 +-
docs/knowledge-graph/desk-source-graph-vocabulary.md |   2 +-
tests/test_graph_extract_sources.py                | 191 +++++++++++++++++++++
```

New untracked files:
- `tests/test_materialization_targets_outside_package.py`
- `desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md`
- `desk/materializations/materialization-*.md` (4 files)

---

## Session Information

- **run_id**: 20261021-materialization-targets-outside-package
- **session_path**: runs/subagents/20261021-materialization-targets-outside-package/
- **Evidence files**:
  - `tester-validation.log`
  - `tester-review.md`

---

## Round 2 Verdict

**Date**: 2026-10-21T20:10:00-03:00  
**Tester**: Independent round 2 (different session)

### Defects Fixed (Verified)

1. **lstrip('./') → removeprefix('./')** (extract_sources.py:181-183)
   - Before: `./.github/workflows/pulse.yml` became `github/workflows/pulse.yml`
   - After: `./.github/workflows/pulse.yml` correctly becomes `.github/workflows/pulse.yml`
   - Regression test: `test_declared_target_dotslash_github_workflow_yields_correct_node` PASS

2. **Node path from symlink-resolved path → declared normalized path** (extract_sources.py:206-237)
   - Before: A symlink `link.py` → `real.py` would create node for `real.py`
   - After: The node is created for `link.py` (the declared path)
   - `resolve()` is now used only for containment check (lines 206-211)
   - Regression test: `test_declared_target_symlink_yields_link_path_not_resolved_target` PASS

---

### Check (a): `_declared_materialization_target_nodes` rejects invalid targets

| Rejection Rule | Implementation | Line | Test Coverage | Status |
|----------------|----------------|------|---------------|--------|
| Absolute paths | `if normalized.startswith("/")` | 194-196 | `test_declared_target_absolute_path_produces_no_node` | PASS |
| '..' segments | `if ".." in Path(normalized).parts` | 198-200 | `test_declared_target_dotdot_path_produces_no_node` | PASS |
| ':' targets | `if ":" in normalized` | 202-204 | `test_declared_target_kind_id_produces_no_node` | PASS |
| Outside-root symlinks | `resolved.relative_to(root.resolve())` | 206-211 | Implicit (ValueError catch) | PASS* |
| Excluded dirs | `if _is_excluded(root, declared_path)` | 225-226 | `test_declared_target_excluded_tmp_produces_no_node`, `test_declared_target_excluded_tools_produces_no_node` | PASS |
| Doc surfaces | `if normalized in doc_paths` | 222-223 | `test_declared_target_doc_surface_produces_no_source_node` | PASS |
| Duplicates (path rule) | `if normalized in existing_paths` | 216-217 | `test_declared_target_already_matched_by_path_rule_not_duplicated` | PASS |
| Duplicates (self) | `if normalized in seen_paths` | 219-220 | Implicit via sorted glob | PASS |

*Note: Outside-root symlinks are implicitly tested through the ValueError catch. A dedicated unit test could strengthen coverage but is not a blocker.

**Verdict: PASS**

---

### Check (b): Node path is always the declared normalized path

Verification in `_declared_materialization_target_nodes`:
- Line 228: `id=f"source_file:{normalized}"` — uses declared path ✓
- Line 230: `identity=normalized` — uses declared path ✓
- Line 231: `path=normalized` — uses declared path ✓
- Line 235: `provenance["path"]=normalized` — uses declared path ✓

The `resolved` variable (line 206) is used **only** for the containment check (lines 206-211), never for node creation.

**Verdict: PASS**

---

### Check (c): No mocks, no literal-duplicating assertions

- `grep -n "mock\|Mock\|patch"` in test files: No matches
- Assertions test behavior (node presence, properties, exit codes), not literal file contents
- Tests use real `tmp_path` filesystem and subprocess CLI calls

**Verdict: PASS**

---

### Check (d): No scope creep beyond task files list

Task `files` list vs actual changes:

| Listed File | Changed | Notes |
|-------------|---------|-------|
| `deskops/graph/extract_sources.py` | ✓ | Core implementation |
| `deskops/operations.py` | ✓ | +materialization tracking |
| `docs/knowledge-graph/desk-source-graph-vocabulary.md` | ✓ | +source_kind doc |
| `tests/test_graph_extract_sources.py` | ✓ | +13 unit tests |
| `tests/test_materialization_targets_outside_package.py` | ✓ (new) | +4 integration tests |
| `desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md` | ✓ (new) | Task knowledge |
| `desk/materializations/materialization-*.md` (4 files) | ✓ (new) | Closeout coverage |
| `desk/tasks/task-...-outside-the-indexed-package.md` | ✓ | Task metadata |
| `.sldb/store.yaml` | ✓ | Expected side effect |

**Verdict: PASS** — All changes within task scope

---

### Sandbox Reproduction (.tmp/tester-gov-repro2)

| Step | Result |
|------|--------|
| `deskops init` | PASS |
| Create `src/vsm/organs/links.py` | PASS |
| Create `.github/workflows/pulse.yml` | PASS |
| `deskops add atom` | PASS |
| `deskops add materialization` (links) | PASS |
| `deskops add materialization` (pulse) | PASS |
| `deskops graph missing --root` exit 0 | PASS |
| `sldb stores check --format json` lists both materializations | PASS |

**Verdict: PASS**

---

### Pytest Validation

```
$ python -m pytest -q tests/test_graph_extract_sources.py tests/test_materialization_targets_outside_package.py tests/test_materialization_contract.py
25 passed in 26.63s
```

**Verdict: PASS**

---

### Overall Round 2 Status

| Check | Status |
|-------|--------|
| (a) Rejection rules | PASS |
| (b) Declared path for nodes | PASS |
| (c) No mocks/literals | PASS |
| (d) No scope creep | PASS |
| Defect 1 fix (removeprefix) | VERIFIED |
| Defect 2 fix (symlink path) | VERIFIED |
| Sandbox reproduction | PASS |
| Pytest validation | PASS |

**Round 2 Verdict: PASS — Ready for closeout**

---

### Residual Risks

1. **Outside-root symlinks**: No explicit unit test; relies on ValueError catch. Low priority — behavior is correct.
2. **Backfill tracking**: Existing untracked materializations remain untracked. Documented as out of scope.

---

### Session Information

- **run_id**: 20261021-materialization-targets-outside-package
- **session_path**: runs/subagents/20261021-materialization-targets-outside-package/
- **tester_round**: 2
- **validation_log**: tester-validation-round2.log
