# result summary: task-goldens-hold-across-sldb-extraction-and-python-versions

Done by the supervisor directly.

- Output goldens re-recorded with `--update-golden` against sldb main (9dcabd9a, d31180e4). The diff only fills fields that used to extract empty: pill what/why/when/where/how/how_not and the ritual `purpose`.
- `tests/test_output_goldens.py`: help goldens are compared after collapsing the usage block and after rewriting the 3.12 spelling `-x METAVAR, --long METAVAR` to `-x, --long METAVAR`. Checked with `/tmp/rw/venv312/bin/python -m pytest tests/test_output_goldens.py -k help_goldens`, which passes on both 3.12.3 and 3.13.
- `tests/test_doc_readability.py`: the hand-written pill has What, Why and Where but no When. sldb anchors headings by position by design, so `where` extracts empty and the detector must report exactly `["where"]`.
- `tests/test_lifecycle_graph.py`: an old ritual cut before `## Step Details` now reads cleanly (d31180e4). The test checks that it ends up readable and tracked, and that it is never archived.
- The store re-extracted RepositoryDoc, FAQDoc and StepDoc with `sldb models update`, because the new extractor reads more text.

Full suite: see validation.log.
