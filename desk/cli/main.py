from __future__ import annotations

import sys
from typing import Any

from sldb.core.exceptions import SLDBError
from .parser import build_parser


class CLI:
    """Main CLI dispatcher for Opsys."""

    def __init__(self):
        from .commands.inbox import InboxCLI
        from .commands.faq import FAQCLI
        from .commands.repo import RepoCLI
        from .commands.desk import DeskCLI

        self.handlers = {
            "inbox": InboxCLI().run,
            "faq": FAQCLI().run,
            "repo": RepoCLI().run,
            "desk": DeskCLI().run,
        }

    def run(self, argv: Any = None) -> int:
        parser = build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as e:
            if isinstance(e.code, int):
                return e.code
            return 0 if e.code is None else 1

        command = args.command
        handler = self.handlers.get(command)
        if not handler:
            print(f"Unknown command: {command}")
            return 2
        return handler(args)


def main(argv: Any = None) -> int:
    """CLI entry point with error handling."""
    try:
        return CLI().run(argv)
    except SLDBError as e:
        raise SystemExit(str(e))
    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Unexpected: {e}")


if __name__ == "__main__":
    sys.exit(main())
