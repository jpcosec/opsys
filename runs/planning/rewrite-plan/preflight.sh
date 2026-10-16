#!/usr/bin/env bash
# usage (from the repo root): runs/planning/rewrite-plan/preflight.sh <task.md> <outdir>
set -u
task="$1"; out="$2"; id=$(basename "$task" .md)
mkdir -p "$out/$id"
prompt="You are a zero-context executor preflight. You receive ONLY one task document (below). Do not assume anything not written in it.
Produce exactly two sections:

RESTATEMENT:
A numbered, step-by-step restatement of the work you would do to complete this task, concrete enough to execute (files, functions, tests, commands).

AMBIGUITIES:
A numbered list of every point where you would have to guess, choose between interpretations, or lack information to execute or to know you are done. Include contradictions and missing acceptance criteria. If there are none, write exactly NONE.

Lines in italics between underscores (for example _Explain why this task exists..._) are fixed guidance text of the task template, not part of the task. Items under 'Resolved Decisions' are authoritative facts and decisions. Items under 'Open Ambiguities' are known owner decisions; mention them only if the task text contradicts them.

Be terse. No preamble.

----- TASK DOCUMENT -----
$(cat "$task")"
timeout 600 pi -p --no-session --no-tools --no-skills --no-extensions --model deepseek/deepseek-flash "$prompt" > "$out/$id/preflight.md" 2> "$out/$id/preflight.err"
echo "$id exit=$?"
