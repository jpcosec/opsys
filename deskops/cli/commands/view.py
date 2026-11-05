from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error


class ViewCLI:
    """Read-only views of a desk for the deskops UI (contract: docs/deskops-ui.md)."""

    def run(self, args: Any) -> int:
        from deskops.services.desk_view import DeskView, DeskViewError, render_text

        fmt = getattr(args, "format", "text")
        try:
            view = DeskView(Path(args.root).resolve(), runs_limit=getattr(args, "runs", 20), herdr=getattr(args, "herdr", "herdr"))
            command = args.view_command
            if command == "board":
                payload = view.board()
            elif command == "task":
                payload = view.task(args.task_id)
            elif command == "drawer":
                payload = view.drawer()
            elif command == "inbox":
                payload = view.inbox()
            elif command == "agents":
                payload = view.agents()
            else:
                return render_error(f"Unknown view: {command}", fmt, type_name="DomainError")
        except (DeskViewError, FileNotFoundError, ValueError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}")
        return render(payload, fmt, render_text)
