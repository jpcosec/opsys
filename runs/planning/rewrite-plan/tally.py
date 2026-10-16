"""Tally a preflight round: classes per task, and every task_defect with its question.

Usage (from the repo root): python runs/planning/rewrite-plan/tally.py runs/subagents/<round dir>
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

round_dir = Path(sys.argv[1])
total: collections.Counter[str] = collections.Counter()
defects: list[str] = []
unparsed: list[str] = []
for resolution in sorted(round_dir.glob("*/resolution.jsonl")):
    tid = resolution.parent.name
    preflight = (resolution.parent / "preflight.md").read_text(encoding="utf-8")
    questions = dict(re.findall(r"^(\d+)\.\s*(.+)$", preflight.split("AMBIGUITIES")[-1], re.M))
    counts: collections.Counter[str] = collections.Counter()
    for line in resolution.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            unparsed.append(tid)
            continue
        counts[item.get("class", "?")] += 1
        if item.get("class") == "task_defect":
            sev = item.get("severity", "?")
            counts[f"defect:{sev}"] += 1
            defects.append(f"{tid} [{item['n']}] ({sev})\n  Q: {questions.get(str(item['n']), '?')}\n  A: {item.get('answer', '')}")
    total += counts
    print(f"{tid:55s} {dict(counts)}")
print(f"\nTOTAL {dict(total)}; unparsed: {sorted(set(unparsed))}")
print(f"\nTASK DEFECTS ({len(defects)}):")
print("\n".join(defects))
