```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "All contracts satisfied; see tester-evidence.md for detailed evidence per contract."
    }
  ],
  "changedFiles": [
    ".pi/skills/use-deskops/SKILL.md",
    ".pi/skills/deskops-task-lifecycle/SKILL.md",
    "tests/test_skill_cli_drift.py"
  ],
  "testsAddedOrUpdated": [
    "tests/test_skill_cli_drift.py"
  ],
  "commandsRun": [
    {
      "command": "deskops show board Board --root .",
      "result": "produced board.txt",
      "summary": "Recovered board state"
    },
    {
      "command": "deskops show task task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task --root .",
      "result": "produced task.txt",
      "summary": "Recovered task state"
    },
    {
      "command": "deskops next task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task --root .",
      "result": "produced next.txt",
      "summary": "Recovered next task"
    },
    {
      "command": "deskops graph missing --root .",
      "result": "produced graph.txt (empty)",
      "summary": "Checked for missing graph edges"
    },
    {
      "command": "git status --short --branch",
      "result": "produced git-status.txt",
      "summary": "Checked git status"
    },
    {
      "command": "grep -rn drawer-task-to-active-task .pi/skills .agents/skills .opencode/skills",
      "result": "no output (exit 1)",
      "summary": "Verified Contract 1: token absence"
    },
    {
      "command": "grep -n \"deskops add task --from-drawer\" .pi/skills/use-deskops/SKILL.md",
      "result": "line 125",
      "summary": "Extracted line for Contract 2"
    },
    {
      "command": "grep -n \"deskops add task --from-drawer\" .opencode/skills/use-deskops/SKILL.md",
      "result": "line 112",
      "summary": "Extracted line for Contract 2"
    },
    {
      "command": "sed -n '125p' .pi/skills/use-deskops/SKILL.md",
      "result": "deskops add task --root . --from-drawer <drawer-selector> --title <title> --goal <goal> --scope <scope> --validation <check>",
      "summary": "Verified full flag form for .pi"
    },
    {
      "command": "sed -n '112p' .opencode/skills/use-deskops/SKILL.md",
      "result": "deskops add task --root . --from-drawer <drawer-selector> --title <title> --goal <goal> --scope <scope> --validation <check>",
      "summary": "Verified full flag form for .opencode and line match"
    },
    {
      "command": "sed -n '46,80p' .pi/skills/deskops-task-lifecycle/SKILL.md",
      "result": "showed Paso 2 section",
      "summary": "Verified Contract 3 elements"
    },
    {
      "command": "grep -q \"Paso 1:\" .pi/skills/deskops-task-lifecycle/SKILL.md && echo found",
      "result": "found",
      "summary": "Verified Contract 4: Pasos headings present"
    },
    {
      "command": "ls -la tests/test_skill_cli_drift.py",
      "result": "-rw-r--r-- 1 ... tests/test_skill_cli_drift.py",
      "summary": "Verified Contract 5: test file exists and non-empty"
    },
    {
      "command": "cat tests/test_skill_cli_drift.py",
      "result": "<test file content>",
      "summary": "Verified Contract 5: test assertions only, no mutation"
    },
    {
      "command": "python -m pytest -q",
      "result": "298 passed",
      "summary": "Verified Contract 6: full suite green"
    },
    {
      "command": "ls -la runs/subagents/20260929-task-sync-pi-skills/validation.log",
      "result": "file exists",
      "summary": "Verified Contract 7b: validation.log exists"
    },
    {
      "command": "grep -i \"sandbox\\|deskops add task --from-drawer\\|exit 0\\|from_drawer\" runs/subagents/20260929-task-sync-pi-skills/validation.log | head -5",
      "result": "<sandbox proof lines>",
      "summary": "Verified Contract 7b: sandbox evidence with exit 0 and real field values"
    }
  ],
  "validationOutput": [
    "See validation.log in runs/subagents/20260929-task-sync-pi-skills/ for full pytest output and sandbox proof."
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "Updated two .pi skill files to use --from-drawer authoring path and added a guard test to prevent drift.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "All validation checks passed; the task is ready for closeout."
}
```