#!/usr/bin/env bash
# usage (from the repo root): runs/planning/rewrite-plan/resolve.sh <task.md> <preflight dir>
set -u
task="$1"; out="$2"; id=$(basename "$task" .md)
amb=$(sed -n '/AMBIGUITIES/,$p' "$out/$id/preflight.md")
prompt="You are resolving ambiguities a zero-context reader found in a task document for the deskops repo (your cwd). You may read the repo (read/grep/find/ls) and the sibling ../sldb repo (its code is under ../sldb/src/sldb). Do not edit anything.

For EACH numbered ambiguity below, output one line of JSON (JSON Lines, nothing else), with keys:
  n: the ambiguity number
  class: one of
    \"repo_fact\"   - the answer is a fact you verified in the code/files; put it in 'answer' with file:line evidence
    \"task_defect\" - the task text is wrong, contradictory, or omits a decision that only the author/owner can make; explain in 'answer' and propose a concrete fix
    \"owner_decision\" - the point is exactly an owner decision already listed under the task's Open Ambiguities
    \"noise\"       - not a real execution risk (generic process, style, or already stated in the task)
  severity: only for task_defect, one of
    \"blocking\" - a factual error in the task (wrong file, line, symbol, command or claim), an internal contradiction,
                   a validation or Done When that cannot pass or passes trivially, or a gap that would likely make the
                   executor build the wrong thing
    \"minor\"    - a detail a competent executor can decide within the task's stated intent and note in the closeout
  answer: short text (max 300 chars)

Be strict: only call something repo_fact if you actually opened the file and saw it. Verify claims in the task text too: if the task cites a line number or symbol that is wrong, report it as task_defect.

----- TASK DOCUMENT -----
$(cat "$task")

----- AMBIGUITIES -----
$amb"
for attempt in 1 2; do
  timeout 900 pi -p --no-session --no-skills --no-extensions --tools read,grep,find,ls --model deepseek/deepseek-flash "$prompt" > "$out/$id/resolution.jsonl" 2> "$out/$id/resolution.err"
  rc=$?
  grep -q '^{' "$out/$id/resolution.jsonl" && break
done
echo "$id exit=$rc attempts=$attempt"
