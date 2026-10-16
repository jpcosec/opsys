RESTATEMENT:
1. Confirm the task is actionable despite `status: deferred`; if not, stop and report.
2. Verify dependencies `task-rw-f1-model-contract-snapshot`, `task-rw-f1-cli-contract-tests`, `task-rw-f1-output-golden-files` are closed/complete before proceeding.
3. Locate the deskops repo root so `runs/planning/sldb-request-unresolved-references.md` resolves; create `runs/planning/` if missing.
4. Read pills `desk/contexts/pill-008-kgdb-sldb-boundary.md` and `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`.
5. Read sldb source `sldb/store/edge_index/declared_references.py` and `resolve_edges` to confirm unresolved declared edges are dropped and no report is produced.
6. Build a reproduction: a TaskDoc (or equivalent fixture) with `depends_on: [task-nope]`, run the sldb edge build/index, and capture evidence that no edge and no unresolved-reference report exist.
7. Choose a desired public sldb API: function name, signature, return shape (per-document list of unresolved declared references), and record the deskops `graph missing` caller that would consume it.
8. Write `runs/planning/sldb-request-unresolved-references.md` containing the reproduction and the proposed API.
9. Run validation: `test -f runs/planning/sldb-request-unresolved-references.md`.
10. Hand the request to the deskops supervisor via the routing mechanism the supervisor expects, and obtain acknowledgement.
11. Confirm the supervisor acknowledged; if yes, mark task complete per `desk/contexts/pill-001-task-closure-commit.md` (own atomic commit).

AMBIGUITIES:
1. Task doc says `status: deferred` yet instructs execution; deferred backlog normally must be promoted first — unclear if promotion is required.
2. No evidence the three `depends_on` F1 tasks are complete; cannot know if prerequisites are satisfied.
3. "sldb coordinator" vs "deskops supervisor" — roles, identity, and handoff channel are undefined.
4. "supervisor has acknowledged it" has no defined acknowledgement artifact or acceptance criteria.
5. Reproduction procedure is unspecified: which repo, which sandbox root, whether mutating `desk/` is allowed (AGENTS.md requires sandbox roots).
6. No specification for the desired function name, signature, or return shape; must be invented.
7. The deskops caller that will use the API is not named or located.
8. Required format of the request file (Markdown, SLDB model/markers, template) is undefined.
9. `runs/planning/...` is not qualified to a repo root; relative-to-deskops vs sldb is ambiguous.
10. Validation only checks file existence; it cannot confirm reproduction validity or API proposal completeness.
11. Referenced pills are not provided; their constraints cannot be checked.
12. Whether the task requires a commit, and whether the drawer-to-active promotion commits apply, is unstated.
13. "Open Ambiguities: None" contradicts items above.
14. No success criteria for the reproduction being technically correct against sldb's actual behavior.
