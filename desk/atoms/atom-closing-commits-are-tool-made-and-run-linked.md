---
id: atom-closing-commits-are-tool-made-and-run-linked
title: Closing commits are tool-made and run-linked
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:roles
- topic:closeout
- topic:provenance
---

# Closing commits are tool-made and run-linked

## Answer

A task closing commit must never depend on agent discretion. It is created by 'deskops closeout commit', which takes exactly one of two routes. When a subagent ran, use '--task <id> --run-dir <runs/subagents/dir>': it refuses to run without the required evidence files, writes run.yaml (run_id, session, session_sha256) into the commit, embeds Task-Id/Run-Dir/Run-Id/Session-Sha256 git trailers, and appends the resulting commit hash to runs/subagents/index.jsonl. When no subagent ran, use '--task <id> --no-run --reason "<why>"': it embeds Task-Id, 'Closeout-Mode: manual' and 'Closeout-Reason: <why>' trailers (no Run-Dir) and appends an index entry with run_dir null and mode manual. Passing both routes or neither is refused, and --no-run without a non-empty reason is refused. Commit-to-run linkage, or the explicit statement that there was no run, travels in the immutable commit message; run-to-commit linkage lives in the append-only index. Do not handcraft closing commits with plain git commit, do not fabricate a run dir for work no subagent did, and do not treat a green test run as closeout without the tool-made commit.
