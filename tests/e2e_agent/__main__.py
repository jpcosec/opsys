"""`python -m tests.e2e_agent [scenario ...] [--reference] [--model provider/id] [--keep]`."""

from __future__ import annotations

import argparse
import json
import sys

from tests.e2e_agent.agent_run import DEFAULT_MODEL, DEFAULT_PROVIDER
from tests.e2e_agent.runner import run_reference, run_scenario
from tests.e2e_agent.scenario import all_scenarios


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m tests.e2e_agent", description="Agent e2e scenarios for deskops.")
    p.add_argument("scenarios", nargs="*", help="Scenario ids (default: all)")
    p.add_argument("--reference", action="store_true", help="Run the reference solutions only (no LLM)")
    p.add_argument("--model", default=f"{DEFAULT_PROVIDER}/{DEFAULT_MODEL}", help="pi provider/model")
    p.add_argument("--keep", action="store_true", help="Keep the sandbox to inspect it")
    args = p.parse_args(argv)
    chosen = [s for s in all_scenarios() if not args.scenarios or s.id in args.scenarios]
    if not chosen:
        p.error(f"no such scenario; known: {', '.join(s.id for s in all_scenarios())}")
    provider, model = args.model.split("/", 1)
    failed = 0
    for s in chosen:
        if args.reference:
            try:
                checks = run_reference(s)
            except RuntimeError as exc:
                checks = [{"name": "setup/reference", "ok": False, "output": str(exc)}]
            ok = all(c["ok"] for c in checks)
            print(f"{'PASS' if ok else 'FAIL'} reference {s.id}" + "".join(f"\n  ✗ {c['name']}: {c['output'][-300:]}" for c in checks if not c["ok"]))
        else:
            r = run_scenario(s, provider, model, args.keep)
            ok = r["verdict"]["pass"]
            print(f"{'PASS' if ok else 'FAIL'} {s.id}: {json.dumps(r['verdict'])} {json.dumps(r['metrics'])}\n  {r['run_dir']}/summary.md")
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
