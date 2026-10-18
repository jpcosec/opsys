# result summary: task-rw-f6-apply-store-migration

Run by the supervisor; the owner authorized it on 2026-10-18 ("Hazlo ... Te doy total y absoluto permiso").

## What ran

- Backed up desk/, knowledge/ and .sldb/ of all 40 repos to /tmp/rw/mig/backup/.
- Ran a fresh dry-run, then surveyed each repo: dirty paths and the `desk update` report. spec2viz had data_mutation changes, and its agent confirmed them before the apply.
- Pass 1, 39 stores: 23 PASS. 13 failed on lifecycle rituals RitualDoc could not carry, and on hum-core, whose store lacked RitualDoc. That led to task-desk-update-archives-rituals-the-model-cannot-carry (fb86e33).
- Pass 2, the 15 failures: 12 PASS. Pass 3, spec2viz: PASS.
- sldb: committed desk/ and .sldb/ only (sldb 6fbb47b6), after untracking the duplicate `desk-board` record that caused the 26 `edges check` errors. sldb-04 has the hash.
- spec2viz-49 committed its repo (30f0a22). mepu-ocs-dev-29 committed shared/llm-gateway on a branch (PR 12, merge blocked by GitHub Actions billing). chatbot-95 was told about the four chatbot repos. The other repos have no live agent; their changes stay in their working trees for their owners.

## Final state

See runs/planning/store-migration-20261018.md: 34 stores pass `stores check`, and every store passes `edges check` except one archive with 3 stale shards. Six stores still fail on their own data (paper_IEEE, tutor_apoe, the kimun archive, mepu_ocs_dev, TraderBot, hum-scrapper). Four got an inbox note through `deskops message send`. paper_IEEE and TraderBot could not get one through the CLI (no project_identity; sender not in their registry), so they go into the coordinator report.

## Validation

`pytest tests`: see validation.log. The suite ran on the deskops code used for passes 2 and 3.
