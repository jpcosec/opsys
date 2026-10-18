from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from deskops.services.issues import close_issue
from deskops.services.issues import find_issue
from deskops.services.issues import list_issues


class IssueCLI:
    """Close and list desk issues."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.issue_command == "close":
            path = find_issue(root, args.selector)
            result = close_issue(
                path,
                args.reason,
                args.ref,
                date.today().isoformat(),
                root=root,
                force=args.force,
            )
            print(f"Closed issue {result.issue_id}")
            print(f"Path: {result.path}")
            return 0
        if args.issue_command == "list":
            records = list_issues(root, args.status)
            if not records:
                print("No issues found.")
                return 0
            for record in records:
                print(f"{record.issue_id} | {record.status} | {record.title}")
            return 0
        return 1
