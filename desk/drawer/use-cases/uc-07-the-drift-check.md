# UC-07: "Has reality drifted from the atoms?"

The team has been coding for weeks. The atoms describe how things should work. The user wants to check: do the atoms still match the implementation?

**Interaction flow:**

1. `deskops drift check --root .` → compares atom claims against implementation
2. Reads the findings: each one names the check, the expected claim, and what was found
3. Decides: update the atom or update the code

**What this user is trying to do:**
Keep knowledge and implementation in sync. Drift is inevitable — they want to surface it, not hide it. The report tells them where to focus.

**When this breaks:**
- Everything comes back green because checks are too shallow
- Everything comes back red because checks are too strict
- Can't tell what's a real problem vs a false alarm
- No way to acknowledge or suppress known drift
- Running it takes too long → nobody runs it
