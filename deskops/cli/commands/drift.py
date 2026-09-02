from __future__ import annotations

import argparse
from pathlib import Path

from deskops.materializers.roles import drift_check_role_docs


class DriftCLI:
    def run(self, args: argparse.Namespace) -> int:
        if args.drift_command != "check":
            print(f"Unknown drift command: {args.drift_command}")
            return 2
        root = Path(args.root).resolve()
        out_dir = Path(args.out).expanduser().resolve() if getattr(args, "out", None) else None
        findings = drift_check_role_docs(root, out_dir)
        if not findings:
            print("No role-agent drift found.")
            return 0
        print("Role-agent drift findings:")
        for finding in findings:
            print(f"- {finding}")
        return 1
