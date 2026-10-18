# result summary: task-second-migration-pass-deskfaqdoc-and-ritual-prose

Run by the supervisor. Full detail is in runs/planning/store-migration-20261018-pass2.md.

- 40 stores backed up to /tmp/rw/mig2/backup, then migrated. 35 pass stores check, and every store passes edges check (the kimun archive shows only stale shards).
- Seven failures came from data_mutation caused by sldb extraction fixes, not by deskops. Following sldb's safe-to-run advice, only the affected models were re-extracted.
- sldb: 86f9be0b, desk/ and .sldb/ only. sldb-04 verified and pushed it.
- Agents told: sldb-04, spec2viz-49 (no changes), chatbot-95 (committed its four PRs), mepu-ocs-dev-29 (committed in PR 12). graph_ui had no changes.
- The 5 stores whose own data still fails are the same as in pass 1; their notes are already in each inbox.

Validation: pytest tests on the deskops checkout (see validation.log).
