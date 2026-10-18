from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.services.drawer import DrawerService


class PromoteCLI:
    """Promote inbox notes into loose drawer candidates.

    There is deliberately no drawer -> active task promotion. The drawer holds
    disorganized, loosely shaped material; an active task is a fully authored
    TaskDoc routed on the board and walked through the desk's lifecycle graph.
    Converting one into the other mechanically meant filling every required
    field with generic placeholders, producing a task that looked structured
    but was not. A drawer item becomes active work only when someone authors
    the task explicitly with `deskops add task`.
    """

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            result = DrawerService(root).promote_inbox_to_drawer_task(args.selector, args.title)
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1
