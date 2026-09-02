from __future__ import annotations

import argparse
from pathlib import Path

from deskops.materializers.roles import materialize_role_docs


class MaterializeCLI:
    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        out_dir = Path(args.out).expanduser().resolve() if getattr(args, "out", None) else None
        written = materialize_role_docs(root, out_dir)
        if not written:
            print(f"No role docs found under {root / 'desk' / 'roles'}")
            return 1
        for source_path, output_path in written:
            print(f"Materialized {source_path.relative_to(root)} -> {output_path}")
        print(f"Materialized {len(written)} role agent(s).")
        return 0
