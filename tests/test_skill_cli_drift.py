"""Guard test: tracked agent-facing skills must stay in sync with the deskops CLI.

Direct drawer-to-active-task promotion was deliberately removed (commit
d35726a): a drawer item becomes an active task only through
`deskops add task --from-drawer ...`. No agent-facing SKILL.md under the
scanned trees may still document the removed command, and the use-deskops
copies must document the authoring path that replaced it. (.pi/ is
gitignored by design, so this guard reads the on-disk skill surfaces that
agents actually load, tracked or not.)

Scanned surfaces are every SKILL.md under `.pi/skills`, `.agents/skills`, and
`.opencode/skills`. README files are excluded by design because only SKILL.md
files carry CLI instructions for agents.

Per pill-drift-checks-are-review-surfaces-not-mutators, this guard is a
review surface: it only asserts over the documents, it never rewrites them.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_TREES = (".pi/skills", ".agents/skills", ".opencode/skills")

REMOVED_PROMOTION_TOKEN = "drawer-task-to-active-task"
AUTHORING_FLAG = "from-drawer"

USE_DESKOPS_COPIES = (
    ROOT / ".pi" / "skills" / "use-deskops" / "SKILL.md",
    ROOT / ".opencode" / "skills" / "use-deskops" / "SKILL.md",
)


def _collect_skill_files() -> list[Path]:
    """Collect every SKILL.md under the scanned trees; missing dirs are empty."""
    files: list[Path] = []
    for relative_tree in SKILL_TREES:
        tree = ROOT / relative_tree
        if tree.is_dir():
            files.extend(sorted(tree.rglob("SKILL.md")))
    assert files, (
        "no SKILL.md files collected under "
        + ", ".join(SKILL_TREES)
        + "; the drift guard must never pass vacuously"
    )
    return files


def test_no_skill_document_contains_the_removed_promotion_command() -> None:
    offenders = [
        str(skill.relative_to(ROOT))
        for skill in _collect_skill_files()
        if REMOVED_PROMOTION_TOKEN in skill.read_text(encoding="utf-8")
    ]
    assert offenders == [], (
        "agent-facing skills still document the removed direct drawer promotion "
        "command; author active tasks with `deskops add task --from-drawer` "
        "instead: " + ", ".join(offenders)
    )


def test_use_deskops_copies_document_the_from_drawer_authoring_path() -> None:
    for copy in USE_DESKOPS_COPIES:
        assert copy.is_file(), f"missing use-deskops skill copy: {copy}"
        assert AUTHORING_FLAG in copy.read_text(encoding="utf-8"), (
            f"{copy.relative_to(ROOT)} does not document the "
            "`deskops add task --from-drawer` authoring path"
        )