# Rewrite plan: generator and tests

The deskops rewrite plan (`../deskops-rewrite-inventory.md`) lives in the desk as deferred
drawer tasks: `desk/drawer/tasks/task-rw-*.md` plus the hand-maintained
`task-doctor-crashes-on-deskless-roots.md`. These scripts write those tasks and test them
before any of them is promoted. Run everything from the deskops repo root.

| Script | What it does |
|---|---|
| `gen.py` | Writes every `task-rw-*` file from its `TASKS` table and rewrites the plan section of `desk/drawer/tasks/Board.md`. Edit the table, not the generated Markdown. |
| `check.py` | Static checks: each task extracts as a TaskDoc with every field filled; no id is a prefix of another (closeout and selectors match by prefix); `depends_on` resolves and is acyclic; no two tasks in the same dependency layer edit the same file; pills, cited files, `path:line` citations and symbols exist (in deskops, tests or `../sldb/src`); validation commands are runnable shapes; every task is on the drawer Board; blocked tasks name their blocker. Prints the layers and what each blocked task holds back. |
| `rehearse.py` | Authors every plan task with the real CLI (`deskops add task --from-yaml ... --from-drawer ...`) in a disposable copy of the repo, checks `next` and `show`, then advances and closes every task in dependency order and asserts that no closure deletes another task's files. |
| `preflight.sh` | Zero-context preflight (execution ritual): gives pi with `deepseek/deepseek-flash` only the TaskDoc and asks for a step-by-step restatement plus every ambiguity. |
| `resolve.sh` | Gives pi/flash read access to the repo and `../sldb` and classifies each ambiguity as `repo_fact` (answered by the code, with evidence), `task_defect` (the task must change), `owner_decision` (already listed as an open decision) or `noise`. |
| `tally.py` | Counts the classes per task for one round and prints every `task_defect`. |

A full pass:

```bash
python runs/planning/rewrite-plan/gen.py
python runs/planning/rewrite-plan/check.py

ls desk/drawer/tasks/task-rw-*.md desk/drawer/tasks/task-doctor-crashes-on-deskless-roots.md > /tmp/plan-files.txt
OUT=runs/subagents/<date>-rw-plan-preflight-rN; mkdir -p $OUT
xargs -P 8 -I{} runs/planning/rewrite-plan/preflight.sh {} $OUT < /tmp/plan-files.txt
xargs -P 8 -I{} runs/planning/rewrite-plan/resolve.sh {} $OUT < /tmp/plan-files.txt
python runs/planning/rewrite-plan/tally.py $OUT

rm -rf /tmp/rw-sandbox && mkdir /tmp/rw-sandbox
rsync -a --exclude .venv --exclude tools --exclude .tmp --exclude .git --exclude __pycache__ \
  --exclude 'runs/subagents/*-rw-plan-preflight-*' ./ /tmp/rw-sandbox/
(cd /tmp/rw-sandbox && git init -q && git add -A && git -c user.email=t@e.x -c user.name=T commit -qm seed)
(cd /tmp/rw-sandbox && python "$OLDPWD/runs/planning/rewrite-plan/rehearse.py" /tmp/rw-sandbox)
```

The sandbox must live outside the repo: deskops' store lookup walks up the parents, so a
sandbox under `.tmp/` would read the repo's registry (inventory finding S7).

Preflight rounds so far are in `runs/subagents/20261016-rw-plan-preflight-r1/`, `-r2/` and
`-r3/`; each task directory holds `preflight.md` (the restatement and ambiguities) and
`resolution.jsonl` (the classification).

## Estado después de F0 (2026-10-18)

Desde la promoción de F0 las tasks del drawer son la fuente: las decisiones del dueño y las tasks
nuevas se escribieron directo en `desk/drawer/tasks/`. No regeneres el drawer con `gen.py`: pisaría
esos cambios y volvería a crear las tasks de F0 ya cerradas.
