from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.config import DeskConfig
from deskops.runtime.herdr import HerdrClient, HerdrProvider
from deskops.runtime.initializer import ensure_herdr_server, initialize_desk
from deskops.runtime.supervise import SuperviseOutcome, run_supervise_loop


class RuntimeCLI:
    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        executable = getattr(args, "herdr", "herdr")
        try:
            if args.runtime_command == "supervise":
                return self._supervise(args, executable)
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

    def _supervise(self, args: Any, executable: str) -> int:
        """Block on one agent, reporting blocked/done settles as they happen.

        Never answers a blocked agent's prompt (only notifies and reports —
        a human decides) and never advances desk state on done (only
        captures and reports). Both are the explicit anti-patterns this
        command exists to avoid; see
        desk/roles/deskops-supervisor.md and
        desk/drawer/features/feature-herdr-supervised-execution-runtime.md.
        """
        provider = HerdrProvider(HerdrClient(executable))
        agent_id = args.agent
        max_iterations = getattr(args, "max_iterations", None)
        read_lines = getattr(args, "read_lines", 200)

        def on_blocked(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[blocked] {outcome.agent_id} is waiting on input. Recent output:\n{excerpt_tail}")
            try:
                provider.notify(
                    f"{outcome.agent_id} blocked",
                    body="Waiting on input; not answering automatically.",
                )
            except Exception as exc:  # noqa: BLE001 - notification failure must not crash supervision
                print(f"(notification failed: {exc})")

        def on_done(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[done] {outcome.agent_id} settled. Recent output:\n{excerpt_tail}")
            print(f"[done] {outcome.agent_id} did not advance any task; review and run `deskops advance` yourself.")

        outcomes = run_supervise_loop(
            provider,
            agent_id,
            max_iterations=max_iterations,
            read_lines=read_lines,
            timeout_ms=getattr(args, "timeout_ms", None),
            on_blocked=on_blocked,
            on_done=on_done,
        )
        if outcomes and outcomes[-1].status in {"timeout", "unknown"}:
            print(f"[{outcomes[-1].status}] stopped supervising {agent_id}.")
            return 1
        return 0
