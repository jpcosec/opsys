from __future__ import annotations

import argparse
from pathlib import Path

from deskops.materializers.roles import drift_check_role_docs
from deskops.materializers.runtime_profiles import drift_check_runtime_bindings


class DriftCLI:
    def run(self, args: argparse.Namespace) -> int:
        if args.drift_command != "check":
            print(f"Unknown drift command: {args.drift_command}")
            return 2
        root = Path(args.root).resolve()
        out_dir = Path(args.out).expanduser().resolve() if getattr(args, "out", None) else None
        findings = drift_check_role_docs(root, out_dir)
        findings += drift_check_runtime_bindings(root)
        
        from deskops.graph.self_reflection import drift_check_knowledge_surfaces
        findings += drift_check_knowledge_surfaces(root)
        
        if not findings:
            print("No drift found.")
            return 0
        print("Drift findings:")
        for finding in findings:
            print(f"- {finding}")
        return 1
