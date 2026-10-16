"""Static test battery over the deskops rewrite plan written as drawer tasks.

Run from the deskops repo root:  python runs/planning/rewrite-plan/check.py
Exit 1 if any FAIL.
"""
from __future__ import annotations

import fnmatch
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from sldb.runtime.validation import extract_model_data

from deskops.models import TaskDoc

ROOT = Path.cwd()
DRAWER = ROOT / "desk" / "drawer" / "tasks"
ACTIVE = ROOT / "desk" / "tasks"
PLAN_TAG = "plan:deskops-rewrite"
EXTRA_IN_PLAN = {"task-doctor-crashes-on-deskless-roots"}

fails: list[str] = []
warns: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def section(text: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


# ---- load ----
all_ids: set[str] = set()
for d in (DRAWER, ACTIVE):
    for p in d.glob("task-*.md"):
        all_ids.add(p.stem)

plan: dict[str, dict] = {}
texts: dict[str, str] = {}
for p in sorted(DRAWER.glob("task-*.md")):
    text = p.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if PLAN_TAG in (fm.get("tags") or []) or p.stem in EXTRA_IN_PLAN:
        plan[p.stem] = fm
        texts[p.stem] = text

print(f"plan tasks: {len(plan)}")

# ---- T1 parse as TaskDoc ----
REQUIRED = ["title", "why", "goal", "scope", "implementation_path", "done_when"]
for tid, text in texts.items():
    try:
        data = extract_model_data(TaskDoc, text)
    except Exception as exc:  # noqa: BLE001
        fail(f"T1 {tid}: TaskDoc extraction failed: {exc}")
        continue
    if data.get("id") != tid:
        fail(f"T1 {tid}: id field {data.get('id')!r} != filename")
    for f in REQUIRED:
        v = str(data.get(f) or "").strip()
        if not v or v.startswith("_") or v == "Not provided.":
            fail(f"T1 {tid}: field {f} empty after extraction")
    if not data.get("validation"):
        fail(f"T1 {tid}: validation list empty after extraction")
    try:
        TaskDoc(**data)
    except Exception as exc:  # noqa: BLE001
        fail(f"T1 {tid}: TaskDoc validation failed: {exc}")

# ---- T2 prefix collisions (closeout glob `*-{id}*` and _resolve_glob `{id}*`) ----
for a in plan:
    for b in all_ids:
        if a != b and b.startswith(a):
            fail(f"T2 {a} is a prefix of existing task {b} (D1/D5 collision)")
        if a != b and a.startswith(b):
            fail(f"T2 existing task {b} is a prefix of {a} (D1/D5 collision)")

# ---- T3 dependencies resolve and form a DAG ----
deps = {tid: list(fm.get("depends_on") or []) for tid, fm in plan.items()}
for tid, ds in deps.items():
    for d in ds:
        if d not in all_ids:
            fail(f"T3 {tid}: depends_on {d} does not exist")
        elif d not in plan:
            warn(f"T3 {tid}: depends_on {d} is outside the plan")

layers: list[list[str]] = []
done: set[str] = set()
remaining = set(plan)
while remaining:
    ready = sorted(t for t in remaining if all(d in done or d not in plan for d in deps[t]))
    if not ready:
        fail(f"T3 cycle among: {sorted(remaining)}")
        break
    layers.append(ready)
    done |= set(ready)
    remaining -= set(ready)

# ---- T4 no file overlap inside a layer ----
def files_of(tid: str) -> list[str]:
    return [str(f).rstrip("/") for f in (plan[tid].get("files") or [])]


for i, layer in enumerate(layers):
    owners: dict[str, list[str]] = defaultdict(list)
    for t in layer:
        for f in files_of(t):
            owners[f].append(t)
    for f, ts in owners.items():
        if len(ts) > 1:
            fail(f"T4 layer {i}: {f} edited by {ts} in parallel")

# ---- T5 pills / references exist; files exist or are created by the task or an ancestor ----
def ancestors(tid: str) -> set[str]:
    seen: set[str] = set()
    stack = list(deps.get(tid, []))
    while stack:
        d = stack.pop()
        if d in seen or d not in plan:
            continue
        seen.add(d)
        stack.extend(deps.get(d, []))
    return seen


for tid, fm in plan.items():
    for p in fm.get("pills") or []:
        if not (ROOT / p).exists():
            fail(f"T5 {tid}: pill {p} missing")
    for r in fm.get("references") or []:
        if "/" in r and not (ROOT / r).exists():
            fail(f"T5 {tid}: reference {r} missing")
    for f in files_of(tid):
        if not (ROOT / f).exists():
            creators = [t for t in {tid} | ancestors(tid) if f in files_of(t)]
            if creators == [tid] or creators:
                warn(f"T5 {tid}: {f} is new (created here or by {sorted(set(creators) - {tid}) or 'this task'})")
            else:
                fail(f"T5 {tid}: {f} does not exist and no ancestor creates it")

# ---- T6 validation commands are runnable shapes ----
help_cache: dict[tuple, str] = {}


def deskops_help(argv: list[str]) -> tuple[int, str]:
    key = tuple(argv)
    if key not in help_cache:
        r = subprocess.run([sys.executable, "-m", "deskops", *argv, "--help"], capture_output=True, text=True, cwd=ROOT)
        help_cache[key] = (r.returncode, r.stdout + r.stderr)
    return help_cache[key]


for tid, text in texts.items():
    cmds = [l[2:].strip() for l in section(text, "Validation").splitlines() if l.startswith("- ")]
    created = set()
    for t in {tid} | ancestors(tid):
        created |= set(files_of(t))
    for cmd in cmds:
        argv = shlex.split(cmd.split(" | ")[0])
        tool = argv[0]
        if tool in {"pytest", "python", "deskops", "sldb", "grep", "test"}:
            pass
        else:
            fail(f"T6 {tid}: unknown tool in {cmd!r}")
            continue
        if tool == "pytest":
            for a in argv[1:]:
                if a.startswith("-"):
                    continue
                path = a.split("::")[0]
                if not (ROOT / path).exists() and path not in created:
                    fail(f"T6 {tid}: pytest target {path} missing and not created by the task chain")
        dargv = None
        if tool == "deskops":
            dargv = argv[1:]
        elif tool == "python" and argv[1:3] == ["-m", "deskops"]:
            dargv = argv[3:]
        elif tool == "python" and argv[1].endswith(".py"):
            if argv[1] not in created and not (ROOT / argv[1]).exists():
                fail(f"T6 {tid}: script {argv[1]} not created by the task chain")
        if dargv is not None:
            # global options before the subcommand
            globals_ = [a for a in dargv if a.startswith("--") and dargv.index(a) == 0]
            words = [a for a in dargv if not a.startswith("-")]
            # find the longest subcommand path that --help accepts
            path: list[str] = []
            for w in words:
                code, _ = deskops_help(path + [w])
                if code == 0 and w in deskops_help(path)[1]:
                    path.append(w)
                else:
                    break
            code, out = deskops_help(path)
            flags = [a.split("=")[0] for a in dargv if a.startswith("--")]
            for fl in flags:
                if fl not in out and fl not in globals_:
                    # flags introduced by the plan itself are allowed only if the task says so
                    if fl in text:
                        warn(f"T6 {tid}: `{cmd}` uses {fl}, not present today (introduced by the plan?)")
                    else:
                        fail(f"T6 {tid}: `{cmd}` uses unknown flag {fl}")
                elif fl in globals_ and fl not in deskops_help([])[1]:
                    warn(f"T6 {tid}: `{cmd}` uses global {fl}, not present today (introduced by the plan?)")

# ---- T7 code citations point at real lines/symbols ----
CITE = re.compile(r"((?:\.\./sldb/src/|(?<![\w/.]))(?:deskops|tests|sldb)/[\w/]+\.py):(\d+)(?:-(\d+))?")
for tid, text in texts.items():
    for m in CITE.finditer(text):
        path, start, end = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        fp = ROOT / path
        if not fp.exists():
            fail(f"T7 {tid}: cited {path} missing")
            continue
        n = len(fp.read_text(encoding="utf-8").splitlines())
        if end > n:
            fail(f"T7 {tid}: cited {path}:{start}-{end} beyond EOF ({n})")
    for sym in set(re.findall(r"`(_[a-z_]+)`", text)):
        r = subprocess.run(["grep", "-rqn", f"def {sym}\\|{sym} =", "deskops", "../sldb/src"], cwd=ROOT)
        if r.returncode != 0:
            r2 = subprocess.run(["grep", "-rqn", sym, "deskops", "tests"], cwd=ROOT)
            if r2.returncode != 0:
                r3 = subprocess.run(["grep", "-rqn", sym, "../sldb/src"], cwd=ROOT)
                if r3.returncode != 0:
                    fail(f"T7 {tid}: symbol {sym} not found in deskops/ or ../sldb/src")

# ---- T8 drawer Board routes every plan task ----
board = (DRAWER / "Board.md").read_text(encoding="utf-8")
for tid in plan:
    if f"`{tid}`" not in board:
        fail(f"T8 {tid}: not listed on desk/drawer/tasks/Board.md")

# ---- T9 blocked tasks carry an ambiguity; deferred tasks carry none ----
for tid, fm in plan.items():
    amb = section(texts[tid], "Open Ambiguities").strip()
    st = fm.get("status")
    has_amb = bool(amb) and amb != "None."
    if st == "blocked" and not has_amb:
        fail(f"T9 {tid}: blocked without an open ambiguity naming the blocker")
    if has_amb and st != "blocked":
        warn(f"T9 {tid}: has open ambiguities but status {st}")

# ---- T10 what each blocked task holds back ----
blocked = {t for t, m in plan.items() if m.get("status") == "blocked"}
children = defaultdict(set)
for t, ds in deps.items():
    for d in ds:
        children[d].add(t)
held: dict[str, set[str]] = {}
for b in sorted(blocked):
    seen: set[str] = set()
    stack = list(children[b])
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(children[x])
    held[b] = seen
    unblocked_down = sorted(x for x in seen if x not in blocked)
    print(f"T10 blocked {b}: holds back {len(seen)} ({len(unblocked_down)} not blocked themselves: {unblocked_down})")
runnable = [t for t in plan if t not in blocked and not any(t in h for h in held.values())]
print(f"T10 runnable without any owner decision: {len(runnable)}/{len(plan)}")

# ---- report ----
print("\nPhases (dependency layers):")
for i, layer in enumerate(layers):
    print(f"  L{i}: {', '.join(layer)}")
print(f"\nWARN ({len(warns)}):")
for w in warns:
    print("  " + w)
print(f"\nFAIL ({len(fails)}):")
for f in fails:
    print("  " + f)
sys.exit(1 if fails else 0)
