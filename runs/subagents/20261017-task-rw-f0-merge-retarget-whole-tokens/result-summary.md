# task-rw-f0-merge-retarget-whole-tokens — Result

## Changes

- `deskops/operations.py` — `DeskopsOperations._rewrite_inbound_atom_references`
  - Replaced whole-file `str.replace` with `re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])").sub(...)`, so only whole `atom:<id>` tokens are retargeted.
  - `rewritten` report now lists line numbers whose text actually changed (line-by-line diff of original vs updated text), instead of pre-match candidates. Lines containing only prefix/suffix variants (e.g. `xatom:atom-foo`) are no longer reported or written.
  - Line numbers cited in the task were accurate: rewrite helper at line 1706 (`_rewrite_inbound_atom_references`), caller `merge_atom` at 924, finder at 1685, split call at 823.

- `tests/test_atoms_merge.py` — added `test_atoms_merge_rewrites_only_whole_atom_tokens`
  - Referrer contains `atom:atom-source-guidance` (line 3), `atom:atom-source-guidance-bar` (4), `atom:atom-source-guidance.extended` (5), `xatom:atom-source-guidance` (6).
  - Asserts only line 3 is rewritten/reported, and lines 4-6 are untouched.

## Validation

- `PYTHONPATH=/tmp/rw/wt/merge python -m pytest tests/test_atoms_merge.py tests/test_atoms_split.py -q` → `8 passed in 1.37s`
- `PYTHONPATH=/tmp/rw/wt/merge python -m pytest tests -q` → `345 passed, 3 skipped in 163.58s (0:02:43)`
- No other Validation commands were listed in the task.

## Unfixed-code test result

- Ran the new test before the fix: `1 failed, 4 passed in 1.05s`.
- Failure: `Inbound references rewritten: 2` with `- desk/tasks/task-ref.md:3` and `- desk/tasks/task-ref.md:6` (global replace had also rewritten the `xatom:` prefix variant; the suffix variants were silently rewritten too).

## Notes / discrepancies

- None. The task's cited line numbers and described behavior matched the code. No sldb issues encountered.
- No commits, `git add`, or desk-mutating deskops commands were run.
