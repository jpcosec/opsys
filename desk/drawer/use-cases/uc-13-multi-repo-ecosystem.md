# UC-13: Multi-repo ecosystem — "I work across projects"

The hum-ecosystem has multiple repos. The user has deskops installed globally and works across projects.

**Interaction flow:**

1. `deskops repo register ~/projects/hum-ecosystem/tools/deskops` → registers a desk
2. `deskops repo list` → sees all registered desks
3. `deskops repo switch tools/deskops` → active desk context changes
4. Now `deskops atoms list` shows atoms for that project
5. `deskops repo switch tools/another-tool` → context switches

**What this user is trying to do:**
Work across the ecosystem without getting confused about which desk is active. The repo registry is their workspace manager.

**When this breaks:**
- Repo registration requires too many steps
- Switching repos is slow (rebuilds cache unnecessarily)
- Active repo state is ambiguous (which one am I in?)
- Commands run in wrong repo context → surprising results
- Unregistering a repo is destructive (loses local state)
- Symlinks or moved repos break registration silently
