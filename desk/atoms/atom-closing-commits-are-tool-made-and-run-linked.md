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

A task closing commit must never depend on agent discretion. It is created by deskops closeout commit, which takes exactly one of two routes. With a subagent run, use --task <id> --run-dir <runs/subagents/dir>: it refuses to run without board.txt, task.txt, git-status.txt and result-summary.md, updates run.yaml with task_id, run_dir, run_id, session and session_sha256, embeds Task-Id/Run-Dir/Run-Id/Session-Sha256 git trailers, and appends an index entry to runs/subagents/index.jsonl. Without a run, use --task <id> --no-run --reason "<why>": it embeds Task-Id, Closeout-Mode: manual and Closeout-Reason trailers and appends an index entry with run_dir null and mode manual. Passing both routes or neither is refused, and --no-run without a non-empty reason is refused. The index commit field is always null because the entry is amended into the closing commit; resolve the commit with git log -1 --grep "Task-Id: <task-id>". Do not handcraft closing commits with plain git commit, do not fabricate a run dir for work no subagent did, and do not treat a green test run as closeout without the tool-made commit.
