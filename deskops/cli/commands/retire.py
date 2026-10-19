from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.services.retire import retire_document


class RetireCLI:
    """Retire one obsolete desk document that has no dedicated verb."""

    def run(self, args: Any) -> int:
        result = retire_document(
            Path(args.root),
            args.path,
            args.reason,
            list(args.ref or []),
            force=args.force,
        )
        print(f"Retired {result.path}")
        print(f"Reason: {result.reason}")
        print(f"Refs: {', '.join(result.refs)}")
        for board in result.boards:
            print(f"Unrouted from {board}")
        return 0
