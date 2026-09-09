from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.config import DeskConfig
from deskops.runtime.herdr import HerdrClient
from deskops.runtime.initializer import ensure_herdr_server, initialize_desk


class RuntimeCLI:
    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        executable = getattr(args, "herdr", "herdr")
        try:
            if args.runtime_command == "init":
                ensure_herdr_server(executable)
                info, handle = initialize_desk(root, agents=args.agents, executable=executable)
                if handle is None:
                    print(f"Herdr Space already exists: {info.identity}")
                else:
                    print(f"DeskOps identity: {info.identity}; tasks discovered: {info.task_count}")
                    print(f"Created Herdr Space: {handle.workspace_id} ({info.identity})")
                    print(f"Panes: {handle.panes}")
                    if handle.agents:
                        print(f"Agents: {handle.agents}")
                return 0

            client = HerdrClient(executable)
            identity = DeskConfig.load(root / "desk").project_identity
            workspaces = client.call("workspace", "list").get("result", {}).get("workspaces", [])
            matches = [item for item in workspaces if isinstance(item, dict) and item.get("label") == identity]
            if args.runtime_command == "status":
                for workspace in matches:
                    print(f"{workspace.get('workspace_id')} | {workspace.get('label')} | panes={workspace.get('pane_count')}")
                if not matches:
                    print(f"No Herdr Space found for {identity}")
                return 0
            if not matches:
                print(f"No Herdr Space found for {identity}")
                return 1
            workspace_id = matches[0]["workspace_id"]
            if args.runtime_command == "attach":
                client.call("workspace", "focus", workspace_id)
                print(f"Focused Herdr Space: {workspace_id} ({identity})")
                return 0
            if args.runtime_command == "stop":
                client.call("workspace", "close", workspace_id)
                print(f"Closed Herdr Space: {workspace_id} ({identity})")
                return 0
        except (ValueError, RuntimeError) as exc:
            print(f"Error: {exc}")
            return 1
        return 1
