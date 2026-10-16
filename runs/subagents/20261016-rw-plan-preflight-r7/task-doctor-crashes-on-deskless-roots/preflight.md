RESTATEMENT:
1. Open `deskops/cli/commands/doctor.py`; locate the `if desk_dir.exists():` block and the findings section that reads `unreadable_docs`.
2. Move `unreadable_docs: list[str] = []` to before the `if desk_dir.exists():` block so it is bound on every code path.
3. Remove the dead `tracked_mds` assignment that the later assignment shadows (line numbers cited: 78 dropped, 80 kept).
4. Verify no other reference to `tracked_mds` depends on the removed line (grep in `deskops/cli/commands/doctor.py`).
5. Add one regression test in `tests/test_doctor_unmodeled_surfaces.py` that creates an empty tmp dir and runs `python -m deskops doctor --root <tmpdir>` (subprocess, capture stdout/stderr, check returncode).
6. Assert: returncode == 1; missing-desk-structure finding appears in stdout; `Unexpected:` absent from stderr.
7. Manually reproduce: `python -m deskops doctor --root /tmp/empty` and confirm the finding prints, no `Unexpected:`, exit 1.
8. Run `pytest tests/test_doctor_unmodeled_surfaces.py`, then `pytest tests`.

AMBIGUITIES:
1. Exact missing-desk-structure finding text/code is not given, so the stdout assertion string must be guessed.
2. Contradiction on which `tracked_mds` line to delete: Scope says drop line 78 (shadowed by 80); Implementation Path step 2 says delete "the shadowed" line — ambiguous which is line 78 vs 80 without the file.
3. Cited line numbers ("line 78", "80", "213-215") are not verifiable from the document; may be stale.
4. Test is added to `tests/test_doctor_unmodeled_surfaces.py` (unmodeled-surfaces file) but covers a desk-less-root crash — no statement that the file/location is intentional.
5. No stated style for invoking the CLI in tests (subprocess `python -m deskops` vs in-process runner) beyond the literal command shown.
6. Pills are referenced but not provided; cannot confirm their `when`/`where`/`how_not` binding.
7. No acceptance criterion distinguishing "missing-desk-structure finding" from other findings expected in stdout on a desk-less root (e.g., whether additional findings are allowed).
8. "no `Unexpected:` text in stderr" — whether matching is case-sensitive substring only, or must exclude any traceback, is unspecified.
