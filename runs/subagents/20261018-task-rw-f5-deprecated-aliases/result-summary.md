# task-rw-f5-deprecated-aliases — result

## What changed

Owner decision applied: `inbox`, `status`, `atoms list`, `atoms show` all stay as warned aliases; none removed.

- `deskops/cli/registry.py`
  - `Command` gained `deprecated_for: tuple[str, ...] | None = None`.
  - Set `deprecated_for` on:
    - `status` -> `("doctor",)`
    - `inbox` -> `("message",)`
    - `atoms list` -> `("list", "atoms")`
    - `atoms show` -> `("show", "atom")`
  - Added deprecation wording to the `help=` text of `status`, `atoms list`, `atoms show` (inbox already had it).
- `deskops/cli/render.py`
  - Added `render_deprecation(replacement)`; prints ``Deprecated: use `deskops <replacement>` `` to stderr only.
- `deskops/cli/main.py`
  - `CLI.run` calls `render_deprecation(command.deprecated_for)` immediately after resolving the command and before any handler work.
- `tests/test_cli.py`
  - Added `_capture_main` plus three tests: `status` vs `doctor`, `atoms list` vs `list atoms`, `atoms show` vs `show atom`. Each asserts identical exit code/stdout, exact stderr warning, and empty canonical stderr.
- `tests/test_message_cli.py`
  - Added `test_inbox_alias_warns_and_matches_message_list`, same contract for `inbox --list` vs `message list`.
- Help goldens re-recorded (only the alias help text changed):
  - `tests/fixtures/golden/help/deskops.txt`
  - `tests/fixtures/golden/help/deskops_atoms.txt`
- `docs/faq.md`, `README.md`, `desk/atoms/`, `desk/contexts/`: no edit needed; surviving hits are deprecation notes.
- `.pi/skills/deskops-health-and-drift/SKILL.md` (gitignored, not committed): replaced `deskops status` recommendations with `deskops doctor`.
- `.opencode/skills/deskops-health-and-drift/SKILL.md`: new tracked mirror of the edited `.pi` skill (currently untracked; supervisor must add it).
- No removal paths implemented.

## Validation

1. `PYTHONPATH=/tmp/rw/wt/aliases python -m pytest tests -q`
   - `424 passed, 3 skipped in 471.08s (0:07:51)`
2. `PYTHONPATH=/tmp/rw/wt/aliases python -m deskops faq`
   - exit `0`, printed the FAQ question list.
3. `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`
   - exit `0`; all remaining hits are `deskops inbox` deprecation notes/mentions in `docs/faq.md`, `README.md`, `.pi/skills/deskops-inbox-coordination/SKILL.md`, `desk/atoms/workflow-model/atom-message-is-the-cross-desk-transport-verb.md`, and `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`. No `deskops status`, `deskops atoms list`, or `deskops atoms show` hits remain.
4. Targeted new tests:
   - `5 passed in 1.48s` (4 behavior tests plus the pre-existing inbox help-note test).
5. Goldens:
   - `PYTHONPATH=/tmp/rw/wt/aliases python -m pytest tests/test_output_goldens.py::test_help_goldens -q --update-golden`
   - `1 passed in 98.34s`.

## Test against unfixed code

Stashed `deskops/cli/registry.py`, `deskops/cli/main.py`, `deskops/cli/render.py`, ran the four new behavior tests, then restored with `git stash pop`:

- Result: `4 failed in 1.37s`.
- Failure cause in every case: expected stderr warning was absent (`assert '' == 'Deprecated: use ...'`).

## Task issues / ambiguities

- Task line numbers are stale: the commands are declared in `deskops/cli/registry.py` (around lines 508, 544, 809, 833), not in `parser.py:500-505`; `parser.py` only walks registry data. Used the registry as the source of truth.
- Task says main.py prints the warning; implemented the printing helper in `render.py` and called it from `main.py`, matching the "registry declares, render prints" boundary in the dispatch instruction.
- "today's behavior" deprecation notes existed only for `inbox`; added equivalent notes to `status`, `atoms list`, and `atoms show`, which is why two help goldens changed.
- `.pi/skills/deskops-health-and-drift` had no pre-existing `.opencode/skills` counterpart, so the mirror was created as a new file.
- No sldb bug found.
