---
kind: suggestion
sender_project: sldb
created_at: 2026-05-26T00:00:00
status: open
---

# Opsys is not yet ready to operate directly over sldb desk tasks

The intended downstream operating layer should work over repo-local `desk/tasks` surfaces instead of relying on ad hoc `issues/` and `inbox/` backlog duplication.

In the current ecosystem state, that direct operation path is not ready yet.

For now, `sldb` is consolidating its repo-local backlog manually into `desk/tasks`, and cross-repo handoff into opsys is also manual.

What opsys still needs:

- a clear way to consume or route repo-local `desk/tasks`
- a stable convention for how downstream opsys instances discover sibling repo desks
- a non-ambiguous repo naming/story, since the local downstream repo is currently named `deskops` while the conceptual layer is still described as `opsys`

Until that is ready, treat manual synchronization as the expected fallback and avoid pushing workflow-specific assumptions back into SLDB infrastructure.
