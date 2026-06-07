# UC-12: "Oops, I broke the desk"

The user was editing atoms and specs, ran a bad command, and now something is off. Tasks won't load. The graph fails. They need to diagnose and recover.

**Interaction flow:**

1. `deskops status` → health check of the desk workspace
2. Report: "3 issues found — 2 broken atom references, 1 stale graph snapshot"
3. `deskops status --fix` → auto-fixes what it can
4. For things it can't fix: gives clear instructions
5. User follows instructions, re-runs `status`, desk is healthy again

**What this user is trying to do:**
Self-healing. They want the tool to help them recover from mistakes, not just report errors. Good error messages with next steps are more valuable than perfect prevention.

**When this breaks:**
- `status` says "everything fine" when things are obviously broken
- Auto-fix makes things worse without a rollback
- Instructions assume too much context ("fix atom X" — how?)
- Error messages are stack traces instead of human explanations
- No way to undo the last desk-affecting command
- Broken desk blocks all operations (can't do *anything* until it's fixed)
