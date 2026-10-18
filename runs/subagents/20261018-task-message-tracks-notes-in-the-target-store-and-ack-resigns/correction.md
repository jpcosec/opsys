# Correction (2026-10-18)

validation.log in this run records `4 failed, 359 passed` for the full suite, and the task was closed anyway: the supervisor's close script did not stop on a red suite (now fixed: it refuses to close when the log reports failures).

Cause, not this task: sldb main moved under the editable install during the run (sldb 0463a9b, 9d6cab2, 9dbf568, inherited models), which changed the contract of sldb's own `RelationDoc`. `tests/test_model_contract_snapshot.py` caught it, and the deskops store held three RelationDoc documents signed under the old contract (`sldb stores check`: contract moved). The other failures of that run did not reproduce: `pytest --lf` passed 4/4.

Fixed in the next commit: `sldb stores update` on the deskops store, the RelationDoc hash in tests/fixtures/model_contract_hashes.json, and a full `pytest tests` run: 363 passed, 3 skipped.
