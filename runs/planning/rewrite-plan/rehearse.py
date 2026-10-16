"""Rehearse the whole rewrite plan through the real deskops CLI in a sandbox copy.

For every plan task, in dependency order: author it from the drawer entry with
`add task --from-yaml`, check `next` and `show`, then drive it through
`advance` to closed with stand-in evidence, and after each closure assert that
no other task's bundle lost a file.

Usage (the sandbox is a disposable copy of the repo, outside it, e.g. /tmp/rw/sandbox):
  rsync -a --exclude .venv --exclude tools --exclude .tmp --exclude .git --exclude __pycache__ ./ /tmp/rw/sandbox/
  (cd /tmp/rw/sandbox && git init -q && git add -A && git commit -qm seed)
  cd /tmp/rw/sandbox && python <repo>/runs/planning/rewrite-plan/rehearse.py /tmp/rw/sandbox
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml
from sldb.runtime.validation import extract_model_data

from deskops.models import TaskDoc

SB = Path(sys.argv[1]).resolve()
DRAWER = SB / "desk" / "drawer" / "tasks"
PLAN_TAG = "plan:deskops-rewrite"
EXTRA = {"task-doctor-crashes-on-deskless-roots"}

problems: list[str] = []


def run(*argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run([sys.executable, "-m", "deskops", *argv], cwd=SB, capture_output=True, text=True)
    if check and r.returncode != 0:
        problems.append(f"`deskops {' '.join(argv)}` exit {r.returncode}: {(r.stderr or r.stdout).strip()[-400:]}")
    return r


def git(*argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=SB, capture_output=True, text=True, check=True).stdout.strip()


def fm(text: str) -> dict:
    return yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1))


plan: dict[str, dict] = {}
for p in sorted(DRAWER.glob("task-*.md")):
    t = p.read_text(encoding="utf-8")
    meta = fm(t)
    if PLAN_TAG in (meta.get("tags") or []) or p.stem in EXTRA:
        plan[p.stem] = extract_model_data(TaskDoc, t)

order: list[str] = []
done: set[str] = set()
while len(order) < len(plan):
    ready = sorted(t for t in plan if t not in done and all(d in done or d not in plan for d in plan[t].get("depends_on") or []))
    if not ready:
        sys.exit("cycle")
    order += ready
    done |= set(ready)


def bundle_files(task_id: str) -> set[str]:
    out = set()
    for p in (SB / "desk").rglob(f"*{task_id}*.md"):
        if "drawer" in p.parts:
            continue
        # only this task's own files: the id must be followed by '-' + suffix or end the stem
        stem = p.stem
        i = stem.find(task_id)
        rest = stem[i + len(task_id):]
        if rest == "" or not any(stem.find(other) == i and len(other) > len(task_id) for other in plan):
            out.add(str(p.relative_to(SB)))
    return out


# ---- author every task ----
for tid in order:
    d = plan[tid]
    payload = {k: d.get(k) for k in ("title", "why", "goal", "scope", "implementation_path", "done_when")}
    payload["validation"] = d.get("validation") or []
    payload["depends_on"] = d.get("depends_on") or []
    payload["pills"] = d.get("pills") or []
    payload["files"] = d.get("files") or []
    payload["task_type"] = d.get("task_type") or "implementation"
    payload["id"] = tid
    y = SB / ".rehearse" / f"{tid}.yaml"
    y.parent.mkdir(exist_ok=True)
    y.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    r = run("add", "task", "--root", ".", "--from-yaml", str(y), "--from-drawer", tid)
    if r.returncode == 0 and not (SB / "desk" / "tasks" / f"{tid}.md").exists():
        # the CLI derives the id from the title; record it
        problems.append(f"{tid}: add task succeeded but desk/tasks/{tid}.md not created (id derived from title?): {r.stdout.strip()[-200:]}")

active = {p.stem for p in (SB / "desk" / "tasks").glob("task-*.md")}
missing = [t for t in order if t not in active]
print(f"authored {len(order) - len(missing)}/{len(order)}; missing: {missing}")

for tid in order:
    if tid not in active:
        continue
    run("next", tid, "--root", ".")
    s = run("show", "task", tid, "--root", ".")
    if s.returncode == 0 and f"From drawer: desk/drawer/tasks/{tid}.md" not in s.stdout:
        problems.append(f"{tid}: show task lacks From drawer line")

git("add", "-A")
git("commit", "-qm", "rehearsal: author plan tasks")

# ---- drive each task to closed in dependency order ----
atom = SB / "desk" / "atoms" / "atom-rehearsal-evidence.md"
r = run("add", "atom", "--root", ".", "--title", "Rehearsal evidence", "--five-wh-one-plus", "what",
        "--answer", "Stand-in atom for the plan rehearsal.")
atom_rel = next((str(p.relative_to(SB)) for p in (SB / "desk" / "atoms").rglob("atom-rehearsal-evidence.md")), None)
test_rel = "tests/test_rehearsal_smoke.py"
(SB / test_rel).write_text("def test_rehearsal_smoke():\n    assert True\n", encoding="utf-8")
git("add", "-A")
git("commit", "-qm", "rehearsal evidence")

closed: list[str] = []
for tid in order:
    if tid not in active:
        continue
    before = {t: bundle_files(t) for t in order if t in active and t not in closed and t != tid}
    for _ in range(2):
        run("advance", "task", tid, "--root", ".")
    head = git("rev-parse", "HEAD")
    refs = json.dumps([atom_rel, f"{test_rel}::test_rehearsal_smoke", head])
    run("edit", "task", tid, "references", refs, "--root", ".")
    run("edit", "task", tid, "files", json.dumps([atom_rel, test_rel]), "--root", ".")
    r = run("advance", "task", tid, "--root", ".")
    if "Status: closed" not in r.stdout:
        problems.append(f"{tid}: did not close: {r.stdout.strip()[-300:]}")
        continue
    closed.append(tid)
    subj = git("log", "-1", "--format=%s")
    if subj != f"closeout: {tid}":
        problems.append(f"{tid}: HEAD subject is {subj!r}")
    for other, files in before.items():
        lost = {f for f in files if not (SB / f).exists()}
        if lost:
            problems.append(f"closing {tid} deleted {len(lost)} files of {other}: {sorted(lost)[:3]}")

print(f"closed {len(closed)}/{len(active & set(order))}")
print(f"PROBLEMS ({len(problems)}):")
for p in problems:
    print("  " + p)
sys.exit(1 if problems else 0)
