"""Measure DeskView(root).board() cold and warm on a desk, read-only.

Usage (from the deskops checkout whose code is measured; put the sldb checkout that
deskops needs first on PYTHONPATH, e.g. the sldb branch wt/closeout-graph-sldb):
    PYTHONPATH=$PWD:../sldb-wt-closeout-graph/src python runs/subagents/20261105-closeout-graph-sldb/measure_board.py \
        [--root ~/proyectos/SLDB_1/deskops] [--runs 3] [--warm 3] [--profile out.txt]

cold = first board() call in a fresh Python process; warm = the same call repeated
in that process. graph_ui frontends/desk/serve.py builds a new DeskView per request,
so "warm" is measured that way (warm_new: new DeskView per call) and also on one kept
DeskView (warm_same). Each run is a new process; the script prints every sample and
the medians.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time


def one_process(root: Path, warm: int, profile: str | None) -> dict:
    t0 = time.perf_counter()
    from deskops.services.desk_view import DeskView

    view = DeskView(root)
    t1 = time.perf_counter()
    if profile:
        import cProfile
        import pstats

        prof = cProfile.Profile()
        prof.enable()
    board = view.board()
    t2 = time.perf_counter()
    if profile:
        prof.disable()
        with open(profile, "w") as fh:
            pstats.Stats(prof, stream=fh).sort_stats("cumulative").print_stats(25)
    expected = json.dumps(board, sort_keys=True, default=str)
    warms = []
    for _ in range(warm):
        s = time.perf_counter()
        again = DeskView(root).board()
        warms.append(time.perf_counter() - s)
        assert json.dumps(again, sort_keys=True, default=str) == expected
    warm_same = []
    for _ in range(warm):
        s = time.perf_counter()
        again = view.board()
        warm_same.append(time.perf_counter() - s)
        assert json.dumps(again, sort_keys=True, default=str) == expected
    cards = sum(len(c.get("cards") or c.get("tasks") or []) for c in board.get("columns", []) if isinstance(c, dict))
    return {"import": t1 - t0, "cold": t2 - t1, "warm": warms, "warm_same": warm_same, "cards": cards, "errors": len(board.get("errors") or [])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path("~/proyectos/SLDB_1/deskops").expanduser()))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--warm", type=int, default=3)
    parser.add_argument("--profile")
    parser.add_argument("--child", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser()
    if args.child:
        print(json.dumps(one_process(root, args.warm, args.profile)))
        return
    samples = []
    for i in range(args.runs):
        cmd = [sys.executable, __file__, "--child", "--root", str(root), "--warm", str(args.warm)]
        if args.profile and i == 0:
            cmd += ["--profile", args.profile]
        out = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        if out.returncode != 0:
            sys.exit(out.stderr)
        sample = json.loads(out.stdout.strip().splitlines()[-1])
        samples.append(sample)
        print(f"run {i + 1}: cold={sample['cold']:.2f}s warm_new={[round(w, 3) for w in sample['warm']]} "
              f"warm_same={[round(w, 3) for w in sample['warm_same']]} "
              f"import={sample['import']:.2f}s cards={sample['cards']} errors={sample['errors']}")
    colds = [s["cold"] for s in samples]
    warms = [w for s in samples for w in s["warm"]]
    same = [w for s in samples for w in s["warm_same"]]
    print(f"median cold={statistics.median(colds):.2f}s median warm_new={statistics.median(warms):.3f}s "
          f"median warm_same={statistics.median(same):.3f}s")


if __name__ == "__main__":
    main()
