from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.services.drawer import DrawerService


class DrawerCLI:
    """Drawer entry maintenance."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.drawer_command == "remove":
            result = DrawerService(root).remove_entry(args.selector, force=args.force)
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1
