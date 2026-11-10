# Live unattended acceptance

Passed on the actual Scion Hub/broker and fork Pi, with one initial assignment and zero intermediate parent task prompts. External observer injected one stop/resume while the same executor was active; coordinator recovered without duplicating it. Six distinct Pi sessions prove coordinator, two executors, and three independent testers.

- Greet: executor passed; first independent tester deliberately exited23 after actual assertions passed; coordinator refused closeout and launched fresh tester-a2, which passed with exit0. Failed evidence and marker preserved.
- Tool closeout b168956 included app.py and evidence. Shared phase1 validation passed and phase commit c04ce98 preceded the second task.
- Farewell: coordinator autonomously dispatched executor and independent tester, both passed actual greet+farewell assertions; tool closeout46931ac included app.py. Shared phase2 validation passed and phase commit33a4563 followed.
- Board contains no active tasks; implementation/store are clean; tests and validator match baseline. Independent final pytest validation:2passed.
- Final native coordinator activity was completed; all children stopped. Actual runtime imports were this worktree and sibling sldb/src.

Native label64 rejection was genuinely self-recovered by the coordinator using a63-hex descriptor, while preserving full canonical hash/name. The adapter now implements that observed wire mapping and bounds long/non-ASCII task labels;33focused tests pass. This is not a claim that the original helper succeeded on its first try.

Full immutable evidence, API event timeline, session-header hashes and a verified complete Git bundle are under /home/robocop/setup/runs/subagents/20261110-autonomy-bootstrap/. acceptance-v2.json and autonomy-lab-v2.bundle retain both closeout and phase histories. Prior failed setup attempts are preserved.
