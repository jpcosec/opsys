# Deskops UX Stress-Test — Anchored Summary

## Goal
UX stress-test the deskops CLI by running real commands and documenting where the experience breaks, confuses, or contradicts the user's mental model.

## Constraints
- Read-only: no files edited, only commands executed and outputs observed.
- Tests anchored in use-case narratives (UC-01–UC-15) in desk/drawer/use-cases/.
- Findings written per-round into desk/drawer/stress-tests/findings/round-*.md.
- Subagents used to parallelize testing across different surfaces.

## Progress
- **6 rounds completed, 28 finding files written**
- Full CLI surface covered: all 14 top-level commands, all 15 add subcommands, all 15 list/show types
- All 15 `--from-yaml` paths tested, all edge cases (empty, malformed, extra fields, type coercion)
- Cross-command workflows (pill lifecycle, board+task, ritual+step, FAQ cycle, inbox, repo+atom, graph rebuild)
- All 6 primitive types (condition, operator, checklist, hook, edge, routine) — creation, list, show, errors
- Python API surface: 23 submodules, 17 Pydantic models, compiler, mermaid, materializers, workspace
- Test suite health: 14 files, 59/59 passing
- Graph resilience: corrupted kg.json rebuilt on `graph build`
- `inbox --list --format json` crash (datetime not serializable)
- 23 residual `*-none.md` test artifacts identified
- `show condition` Subject/Predicate swapped when Subject is empty
- `show routine` edges not displayed (loads full EdgeDocs, filters None)
- `--from-yaml` overrides inline CLI flags (YAML wins)
- Mermaid renderer + materializers: code exists, no CLI surface

---

## CRITICAL BUGS (data integrity / blocking)

| # | Finding | Source |
|---|---|---|
| C1 | **sldb DataExtractor misparses TaskDoc markdown** — AST map indices shift when checklist count differs from template, cross-wiring `routine`, `current_node`, `files`, `checklists`. Makes `advance task` completely non-functional | round-05-advance |
| C2 | **`_resolve_glob` returns wrong artifact** — `show task X` uses `f"{X}*.md"` glob. If `task-X` and `task-X-suffix` both exist, returns alphabetically first (often the suffix). Same bug in `show repository`, `show operator`. No warning. | round-05-list |
| C3 | **`list inbox-notes` shows 2 of 13** — glob pattern `inbox-note-{slug}*` doesn't match date-prefixed filenames (`20260604-*.md`). `inbox --list` (different code path) shows all 13. | round-05-list |
| C4 | **Empty YAML `{}` creates garbage artifacts for 8 types** — pill, ritual, board, atom, repository, inbox-note, faq-doc, step all create `*-none.md` with title `"None"`. No validation. | round-05-from-yaml |
| C5 | **`repo register` overwrites file before store check** — duplicate registration: file written to disk, then store rejects tracking. On-disk state != store index. | round-05-repo |
| C6 | **`init` does not register models in local store** — `deskops init /tmp/test && repo register` fails with "RepositoryDoc model not registered". Models only in global store (`bootstrap`). | round-05-repo |
| C7 | **`_normalize_task_payload` uses `list()` instead of `_coerce_list()`** — scalar string `pills: single-ref` becomes `['s','i','n','g','l','e', ...]` (characters). Affects: references, depends_on, pills, files, validation, history, tags. | round-05-from-yaml |
| C8 | **KG JSON edges serialization bug** — 68 edges exist but all have `role=None target=None`. NetworkX snapshot (.nx.json) has correct data. KG graph cannot be traversed. | round-04-graph |
| C9 | **`advance task` broken** — no `--to` flag exists. Routine field corrupted by checklist cross-wiring (C1). Duplicate error message printed twice. | round-05-advance |
| C10 | **`show condition` swaps Subject/Predicate when Subject empty** — sldb parser bug absorbs next section content into empty field | round-06-primitives |
| C11 | **`show` glob bug confirmed for ALL 15 types** — `show checklist X` returns `X-stress` (different artifact) silently | round-06-primitives |
| C12 | **`inbox --list --format json` crashes** — `datetime` objects not JSON serializable | round-06-remaining |

---

## HIGH-SEVERITY BUGS (constant friction)

| # | Finding | Source |
|---|---|---|
| H1 | **`list tasks` / `list pills` crash entirely on one bad file** — `task-item.md` with `# ` (empty title) causes entire listing to fail with Pydantic traceback. Should skip/warn. | round-05-list |
| H2 | **13/15 `show` types leak absolute filesystem paths** — `show condition nonexistent` shows `Unexpected: No file found for id 'nonexistent' in /home/jp/.../desk/primitives/conditions`. Only `show task` and `show routine` are graceful. | round-05-list |
| H3 | **`show <type> ""` matches all files** — empty ID becomes `*.md` glob, matches everything. `show task ""` crashes on Board.md. `show condition ""` returns first condition silently. | round-05-list |
| H4 | **`show task` / `show repository` silent wrong artifact** — glob prefix match returns suffix file without warning (C2). User asks for one thing, gets another. | round-05-list |
| H5 | **`--from-yaml` has no rollback on failure** — `add task --from-yaml` writes task file + primitives + routine, then fails on `_append_task_to_board`. Orphaned files on disk. | round-04-from-yaml |
| H6 | **`add task` with single string for list fields splits into characters** — `pills: single-ref` becomes `['s','i','n','g','l','e','-','r','e','f']` (C7). | round-05-from-yaml |
| H7 | **Graph: 253 nodes, 0 edges on atom nodes** — all 68 edges are on non-atom nodes (diagram, doc, source_file). Created artifacts show 0 edges post-build. | round-04-graph |
| H8 | **`bootstrap` vs `init` naming confusion** — `bootstrap` only sets up global store (~/.sldb), `init` scaffolds desk/ but doesn't register models. Neither does the full setup. | round-05-repo |
| H9 | **Two completely separate FAQ systems** — `deskops faq` reads `docs/faq.md` (static). `deskops add faq-doc` writes `desk/faq/`. They never interact. | round-05-workflows |
| H10 | **`list inbox-notes` uses incompatible glob** — misses 11 of 13 notes. Date-prefixed filenames don't match `inbox-note-*` pattern. | round-05-list |
| H11 | **Error messages incorrectly go to stdout** — `show task nonexistent 2>/dev/null` still shows message. Should go to stderr. | round-05-edge |
| H12 | **Very long title (10K chars) crashes with OSError** — `[Errno 36] File name too long`. No graceful truncation. | round-05-edge |
| H13 | **`show routine` edges not displayed** — loads full EdgeDoc objects, filters None for non-existent primitives. Data in file, but `show` says empty. | round-06-primitives |
| H14 | **`--from-yaml` silently overrides CLI flags** — `--title "CLI"` + `--from-yaml file.yml` → YAML title wins. No warning. | round-06-remaining |
| H15 | **`list --root /tmp/nonexistent` silently succeeds** — exit 0, no output, no error. User thinks no artifacts exist. | round-06-primitives |

---

## MEDIUM-SEVERITY ISSUES

| # | Finding | Source |
|---|---|---|
| M1 | **`faq --faq-path /nonexistent` silently falls back to default** — no warning that user's path was ignored. | round-05-repo |
| M2 | **`faq` JSON/YAML schema inconsistency** — list wraps in `{"questions":[...]}`, single result has no wrapper. | round-05-repo |
| M3 | **`repo register` doesn't validate path exists** — `/nonexistent/path`, `/etc`, `/tmp/test-file` (file) all accepted silently. | round-05-repo |
| M4 | **`repo register` duplicate slug collision** — `"my repo"` and `"My Repo"` both slug to `my-repo`. Second silently overwrites first. | round-05-repo |
| M5 | **`repo register` empty name → Pydantic traceback** — `""` as name leaks raw validation error. | round-05-repo |
| M6 | **`desk install` doesn't create target directory** — requires `mkdir -p` first. | round-05-repo |
| M7 | **`graph build` does not rebuild `knowledge_graph.nx.json`** — remains stale from first build. | round-05-advance |
| M8 | **`graph neighbors --help` doesn't document `type:id` prefix format** — user must guess `atom:`, `task:`, `issue:` etc. | round-05-advance |
| M9 | **`add task` without args → cryptic Pydantic error** — `Unexpected: 2 validation errors for TaskDoc`. Should show usage. | round-05-advance |
| M10 | **Empty string payload `''` creates `task-none`** — `title` becomes string `"None"`. | round-05-edge |
| M11 | **3 different `list` output formats** — tasks has 3 columns, conditions has 3 (different), pills has 2. | round-05-list |
| M12 | **Ritual files `closeout.md`, `execution.md`, `testing.md` invisible** — filenames don't start with `ritual-`. Same for `Board.md`. | round-05-list |
| M13 | **`show ritual` uses internal `ID:` field, `show pill` uses filename stem** — inconsistent lookup logic. | round-05-list |
| M14 | **`--pythonpath` only on `inbox` and `repo register`** — dead code in main.py for all other commands. | round-04-install |
| M15 | **YAML type coercion: `created_at: 2026-01-01` parsed as `datetime.date`** — Pydantic expects `str`, crashes. Users must quote dates. | round-05-from-yaml |
| M16 | **`--root` accepts any path without validation** — `graph build --root /tmp` creates `.sldb` structure silently. Path traversal `/tmp/../../etc` resolved without warning. | round-04-graph, round-05-edge |
| M17 | **`show board` mislabels tags as rituals** — output shows `rituals: workspace:desk, artifact:board` (actually tags). | round-05-workflows |
| M18 | **`board` writes to `desk/tasks/` (collision), `pill` writes to `desk/contexts/` (misnamed)** — directory names don't match artifact names. | round-05-workflows |
| M19 | **`repo register` vs `add repository` produce different ID formats** — `deskops` (no prefix) vs `repo-deskops-alt` (with prefix). | round-05-workflows |
| M20 | **Whitespace-only inputs accepted** — `--title "  "` creates artifact with 3-space title, generic slug. | round-05-edge |

---

## LOW-SEVERITY / INFO

| # | Finding | Source |
|---|---|---|
| L1 | No `--format json` or `--format yaml` on any `list`/`show` command | round-02-cli |
| L2 | No `--version` flag | round-02-cli |
| L3 | No `--dry-run` support in any command | round-05-edge |
| L4 | `atoms` command group only has `add-namespace` — no list/show/new/validate/split/merge | round-01-nomenclature |
| L5 | `repo` only has `register` — no list/current/switch/unregister | round-02-repo |
| L6 | 6 concepts from atoms have no CLI: drift, materialize, status, closeout, validate, graph reflect | round-01-nomenclature |
| L7 | `list atoms` only returns 4 from `desk/atoms/` root, ignores 60 in subdirectories | round-01-graph |
| L8 | Spec engine (deskops/specs/) has zero CLI surface | round-02-spec |
| L9 | `faq` list output has `answer: null` for all entries — cannot bulk-export answers | round-05-repo |
| L10 | `--pythonpath` accepted by `repo register` but not persisted in markdown | round-05-repo |
| L11 | `bootstrap` minimal/opaque output — hides what it actually does | round-05-repo |
| L12 | `desk install` doesn't create `.sldb` — user still needs `init` | round-05-repo |
| L13 | Multiple `--root` flags silently use the last one (argparse default) | round-05-edge |
| L14 | No progress indicators for any command | round-05-edge |
| L15 | No input sanitization for HTML/special characters in titles | round-05-edge |
| L16 | 6 fields huérfanos en spec/ (category, distinct_from_pills, etc.), task no tiene `doc.model` | round-04-spec |
| L17 | Pydantic tracebacks shown to user on validation errors instead of friendly messages | round-05-advance |
| L18 | `--desk-root` (inbox) vs `--root` (all others) — inconsistent flag naming | round-05-edge |
| L19 | Pre-existing corrupted `*-none.md` artifacts scattered across desk/ (24+ files from prior stress tests) | round-05-workflows |

---

## KEY CODE ISSUES (root causes)

- **main.py:224**: generic `except Exception` wraps all errors in `Unexpected:` — hides internal paths, makes user-facing errors indistinguishable from internals
- **`_resolve_glob` in operations.py**: uses `f"{doc_id}*.md"` pattern → ambiguous for prefix matches (C2)
- **`_normalize_task_payload`**: uses `list()` instead of `_coerce_list()` → characters bug (C7)
- **`extract_model_data` in sldb**: uses positional map indices for field extraction → fragile when checklist count varies (C1)
- **`compile_artifact_spec`**: `.get("title")` returns `None` → `str(None)` → `"None"` → garbage artifact (C4)
- **`__init__.py` in graph/**: only exports 2 of ~10 public symbols from subpackage
- **`models.py`**: 3-tier inheritance (StructuredNLDoc → PrimitiveDoc → OperationalArtifactDoc), 17 model classes

## Relevant Files
- desk/drawer/use-cases/: 15 user-interaction narratives (UC-01 to UC-15)
- desk/drawer/stress-tests/METHODOLOGY.md: methodology document
- desk/drawer/stress-tests/findings/: 24 finding files across 5 rounds
- deskops/cli/main.py: CLI dispatcher, generic exception handler line 224
- deskops/operations.py: task normalization, glob resolution, advance logic
- deskops/graph/: extract_docs.py, extract_edges.py, extract_sources.py, snapshot.py, self_reflection.py, checks.py
- deskops/specs/: loader.py, compiler.py, mermaid.py (full engine, no CLI)
- spec/artifacts/: 9 YAML artifact specs
- spec/fields/: 42 YAML field definitions
- spec/primitives/: 10 YAML primitive definitions
