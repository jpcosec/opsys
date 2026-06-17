from __future__ import annotations

import argparse
from pathlib import Path

from deskops.operations import ARTIFACT_SUBJECTS
from deskops.specs import SpecRegistry


SPEC_ROOT = Path(__file__).resolve().parents[2] / "spec"

WORKFLOW_EPILOG = """
Typical flow:
  deskops bootstrap
  deskops init .
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest"
  deskops list tasks --root .
  deskops show task task-fix-thing --root .
  deskops advance task task-fix-thing --root .

Use docs/quickstart.md for the first full walkthrough.
""".strip()

SELECTOR_HELP = "Selectors accept an exact id, filename, stem, or unique slug fragment where supported."

FIELD_HELP_OVERRIDES = {
    "title": "Human-readable title.",
    "name": "Human-readable name.",
    "path": "Repository or artifact path.",
    "status": "Workflow status, such as active or draft.",
    "description": "Markdown description.",
    "what": "What this context explains.",
    "why": "Why this matters.",
    "when": "When this applies.",
    "where": "Where this applies.",
    "how": "How to apply it.",
    "how_not": "How not to use it; common misuse.",
    "goal": "Outcome this work should achieve.",
    "scope": "Boundary of the work.",
    "validation": "Validation command or assertion.",
    "answer": "Durable answer this atom records.",
    "five_wh_one_plus": "Atom category: who, what, when, where, why, how, or how_much.",
}


def _spec_registry() -> SpecRegistry:
    return SpecRegistry.load(SPEC_ROOT)


def _field_help(field_spec: dict[str, object]) -> str:
    data = field_spec.get("data", {})
    key = str(data.get("key", "value")) if isinstance(data, dict) else "value"
    value_type = str(data.get("value_type", "str")) if isinstance(data, dict) else "str"
    help_text = FIELD_HELP_OVERRIDES.get(key, f"{key.replace('_', ' ').capitalize()} value.")
    if value_type.startswith("list["):
        help_text = f"{help_text} Repeat as needed."
    return help_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deskops",
        description="deskops: Workflow-domain layer for the hum-ecosystem.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=WORKFLOW_EPILOG,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_about_command(subparsers)
    _add_faq_commands(subparsers)
    _add_bootstrap_command(subparsers)
    _add_init_command(subparsers)
    _add_inbox_commands(subparsers)
    _add_promote_commands(subparsers)
    _add_add_commands(subparsers)
    _add_edit_commands(subparsers)
    _add_next_command(subparsers)
    _add_list_commands(subparsers)
    _add_show_commands(subparsers)
    _add_advance_commands(subparsers)
    _add_repo_commands(subparsers)
    _add_desk_commands(subparsers)
    _add_atoms_commands(subparsers)
    _add_graph_commands(subparsers)

    return parser


def _add_atoms_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("atoms", help="Atom model and namespace management.")
    s = p.add_subparsers(dest="atoms_command", required=True)

    add_namespace = s.add_parser(
        "add-namespace",
        help="Add an extensible atom tag namespace to desk/atoms/tag-namespaces.yaml.",
    )
    add_namespace.add_argument("namespace", help="Namespace name, such as pattern.")
    add_namespace.add_argument("--root", default=".", help="Target repository root.")
    add_namespace.add_argument("--meaning", required=True, help="What this namespace means.")
    add_namespace.add_argument("--use-when", required=True, help="When to use this namespace.")
    add_namespace.add_argument(
        "--do-not-use-when",
        required=True,
        help="When an existing namespace should be preferred instead.",
    )
    add_namespace.add_argument(
        "--example",
        action="append",
        default=[],
        help="Example tag using the namespace; repeat as needed.",
    )


def _add_graph_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("graph", help="Build and inspect deskops KGDB graph runtime outputs.")
    s = p.add_subparsers(dest="graph_command", required=True)

    build = s.add_parser("build", help="Build the KGDB graph snapshot runtime artifact.")
    build.add_argument("--root", default=".", help="Target repository root.")

    neighbors = s.add_parser("neighbors", help="Show incoming and outgoing neighbors for one graph node.")
    neighbors.add_argument("id", help="Graph node id to inspect, formatted as type:id (e.g. atom:atom-name, task:task-name, issue:issue-name).")
    neighbors.add_argument("--root", default=".", help="Target repository root.")
    neighbors.add_argument("--graph", help="Graph snapshot path; defaults to the root runtime snapshot.")

    missing = s.add_parser("missing", help="Report missing graph targets and dangling declared references.")
    missing.add_argument("--root", default=".", help="Target repository root.")
    missing.add_argument("--graph", help="Optional graph snapshot path to check for missing edge targets.")

    reflect = s.add_parser("reflect", help="Write review-only self-reflection findings for a graph snapshot.")
    reflect.add_argument("--root", default=".", help="Target repository root.")
    reflect.add_argument("--graph", help="Graph snapshot path; defaults to the root runtime snapshot.")


def _add_promote_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "promote",
        help="Promote inbox and drawer items through desk workflow surfaces.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Examples:
  deskops promote inbox-to-drawer-task 20260614-unclear --root .
  deskops promote drawer-task-to-active-task task-write-guide --root .

{SELECTOR_HELP}
""".strip(),
    )
    s = p.add_subparsers(dest="promote_command", required=True)

    inbox = s.add_parser(
        "inbox-to-drawer-task",
        help="Promote one inbox note into a deferred drawer task candidate.",
    )
    inbox.add_argument("selector", help="Inbox filename, stem, or unique slug fragment")
    inbox.add_argument("--root", default=".", help="Target repository root")
    inbox.add_argument("--title", help="Override the drawer task title")

    drawer = s.add_parser(
        "drawer-task-to-active-task",
        help="Promote one drawer task candidate into an active task bundle.",
    )
    drawer.add_argument("selector", help="Drawer task filename, stem, or unique slug fragment")
    drawer.add_argument("payload", nargs="?", help="Optional inline JSON payload to override task generation.")
    drawer.add_argument("--from-yaml", help="Load an override payload from a YAML file.")
    drawer.add_argument("--root", default=".", help="Target repository root")
    drawer.add_argument("--title", help="Override the active task title")


def _add_desk_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("desk", help="Desk workspace management.")
    s = p.add_subparsers(dest="desk_command", required=True)

    ins = s.add_parser("install", help="Scaffold a minimal local desk/ surface in a repo.")
    ins.add_argument("path", help="Target repository path")


def _add_about_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparsers.add_parser(
        "about",
        help="Print a short overview of deskops and its first-use commands.",
    )


def _add_bootstrap_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparsers.add_parser(
        "bootstrap",
        help="Install or repair sldb and register deskops models in the global store.",
    )


def _add_init_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "init",
        help="Initialize a local .sldb store and scaffold desk/ if needed.",
    )
    p.add_argument("path", nargs="?", default=".", help="Target repository path")


def _add_repo_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("repo", help="Repository registration and discovery.")
    s = p.add_subparsers(dest="repo_command", required=True)

    reg = s.add_parser(
        "register",
        help="Canonically register a repository in the ecosystem registry and track it in SLDB.",
        description="Canonically register a repository in the ecosystem registry and track it in SLDB.",
    )
    reg.add_argument("name", help="Human-readable name")
    reg.add_argument("path", help="Relative path to repo root")
    reg.add_argument("--id", help="Stable unique ID, defaults to slugified name")
    reg.add_argument("--description", help="Markdown description")
    reg.add_argument("--tags", help="Comma-separated tags")
    reg.add_argument("--store", help="Store path to anchor the registry")
    reg.add_argument("--pythonpath", help="Python path for model resolution")


def _add_inbox_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "inbox",
        help="Log, list, or show messages arriving to a project inbox.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Examples:
  deskops inbox "Need clearer CLI help" --kind unclear --title "CLI help"
  deskops inbox --list --root .
  deskops inbox --show 20260614-cli-help --root .

--show selector: filename, stem, or slug fragment.
""".strip(),
    )
    p.add_argument("message", nargs="?", help="Inbox note body")
    p.add_argument(
        "--kind",
        choices=("unclear", "suggestion"),
        default="unclear",
        help="Type of inbox message to write",
    )
    p.add_argument("--title", help="Short title for the note")
    p.add_argument(
        "--desk-root",
        help="Desk root directory override; defaults to the active project desk",
    )
    p.add_argument(
        "--store",
        help="Store path used to resolve the target project root for the default desk",
    )
    p.add_argument(
        "--repo",
        help="Target a registered repository name in the ecosystem",
    )
    p.add_argument(
        "--pythonpath",
        help="Project path used when auto-tracking inbox notes through a registered InboxNoteDoc model",
    )
    p.add_argument("--list", action="store_true", help="List desk inbox notes")
    p.add_argument("--show", help="Show one inbox note by filename, stem, or slug fragment")
    p.add_argument("--limit", type=int, default=20, help="Limit listed notes")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")


def _add_faq_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("faq", help="Browse the first-use FAQ by question.")
    p.add_argument(
        "question",
        nargs="?",
        help="Question index, slug, or text fragment. Omit to list available questions.",
    )
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    p.add_argument("--faq-path", default="docs/faq.md", help="FAQ markdown path")


def _add_add_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "add",
        help="Create desk workflow artifacts from modeled templates.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest"
  deskops add pill --root . --title "Guardrail: Keep layers clean" --what "..." --why "..."
""".strip(),
    )
    s = p.add_subparsers(dest="subject", required=True)

    task = s.add_parser("task", help="Create an actionable task bundle.")
    task.add_argument("payload", nargs="?", help="Inline JSON payload for the task.")
    task.add_argument("--from-yaml", help="Load the task payload from a YAML file.")
    task.add_argument("--root", default=".", help="Target repository root.")
    task.add_argument("--title", help="Task title")
    task.add_argument("--why", help="Rationale or business driver")
    task.add_argument("--goal", help="Task goal")
    task.add_argument("--scope", help="Task scope")
    task.add_argument("--implementation-path", help="Implementation path")
    task.add_argument("--done-when", help="Task completion rule")
    task.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Validation command or assertion; repeat as needed.",
    )

    condition = s.add_parser("condition", help="Create a condition primitive.")
    condition.add_argument("--root", default=".", help="Target repository root.")
    condition.add_argument("--from-yaml", help="Load the condition payload from a YAML file.")
    condition.add_argument("--title", required=False, help="Condition title")
    condition.add_argument("--summary", help="Condition summary")
    condition.add_argument("--status", default="active", help="Condition status")
    condition.add_argument("--subject", dest="subject_path", required=False, help="Payload path to read")
    condition.add_argument("--predicate", required=False, help="Predicate name")
    condition.add_argument("--expected", help="Expected value")

    operator = s.add_parser("operator", help="Create an operator primitive.")
    operator.add_argument("--root", default=".", help="Target repository root.")
    operator.add_argument("--from-yaml", help="Load the operator payload from a YAML file.")
    operator.add_argument("--title", required=False, help="Operator title")
    operator.add_argument("--summary", help="Operator summary")
    operator.add_argument("--status", default="active", help="Operator status")
    operator.add_argument("--action", required=False, help="Operator action")
    operator.add_argument("--target", required=False, help="Payload path to mutate")
    operator.add_argument("--value", help="Operator value")

    checklist = s.add_parser("checklist", help="Create a checklist primitive.")
    checklist.add_argument("--root", default=".", help="Target repository root.")
    checklist.add_argument("--from-yaml", help="Load the checklist payload from a YAML file.")
    checklist.add_argument("--title", required=False, help="Checklist title")
    checklist.add_argument("--summary", help="Checklist summary")
    checklist.add_argument("--status", default="active", help="Checklist status")
    checklist.add_argument("--item", action="append", default=[], help="Checklist item; repeat as needed.")
    checklist.add_argument(
        "--condition-ref",
        action="append",
        default=[],
        help="Condition id; repeat as needed.",
    )
    checklist.add_argument("--mode", default="all", help="Checklist completion mode")

    hook = s.add_parser("hook", help="Create a hook primitive.")
    hook.add_argument("--root", default=".", help="Target repository root.")
    hook.add_argument("--from-yaml", help="Load the hook payload from a YAML file.")
    hook.add_argument("--title", required=False, help="Hook title")
    hook.add_argument("--summary", help="Hook summary")
    hook.add_argument("--status", default="active", help="Hook status")
    hook.add_argument("--event", required=False, help="Hook event name")
    hook.add_argument("--target-ref", required=False, help="Target primitive id")
    hook.add_argument("--condition-ref", help="Optional guard condition id")

    edge = s.add_parser("edge", help="Create an edge primitive.")
    edge.add_argument("--root", default=".", help="Target repository root.")
    edge.add_argument("--from-yaml", help="Load the edge payload from a YAML file.")
    edge.add_argument("--title", required=False, help="Edge title")
    edge.add_argument("--summary", help="Edge summary")
    edge.add_argument("--status", default="active", help="Edge status")
    edge.add_argument("--source", required=False, help="Source node id")
    edge.add_argument("--target-node", required=False, help="Target node id")
    edge.add_argument("--condition-ref", help="Optional guard condition id")

    routine = s.add_parser("routine", help="Create a routine primitive.")
    routine.add_argument("--root", default=".", help="Target repository root.")
    routine.add_argument("--from-yaml", help="Load the routine payload from a YAML file.")
    routine.add_argument("--title", required=False, help="Routine title")
    routine.add_argument("--summary", help="Routine summary")
    routine.add_argument("--status", default="active", help="Routine status")
    routine.add_argument("--entrypoint", required=False, help="Entrypoint node id")
    routine.add_argument("--decomposition", action="append", default=[], help="Decomposition node id")
    routine.add_argument("--edge", action="append", default=[], help="Edge id")
    routine.add_argument("--terminal-node", action="append", default=[], help="Terminal node id")

    registry = _spec_registry()
    for artifact_id, meta in ARTIFACT_SUBJECTS.items():
        artifact = registry.artifacts[artifact_id]
        subject = meta["subject"]
        help_text = f"Create a {subject} artifact."
        if subject == "repository":
            help_text = (
                "Create a local repository artifact doc; use 'deskops repo register' "
                "for canonical ecosystem registration."
            )
        generated = s.add_parser(
            subject,
            help=help_text,
            description=help_text,
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=f"Example:\n  deskops add {subject} --root . --title \"Example\"",
        )
        generated.add_argument("--root", default=".", help="Target repository root.")
        generated.add_argument("--from-yaml", help=f"Load the {subject} payload from a YAML file.")
        for field_id in artifact["data"].get("fields", []):
            field_spec = registry.fields[field_id]
            key = str(field_spec["data"]["key"])
            value_type = str(field_spec["data"]["value_type"])
            option = f"--{key.replace('_', '-')}"
            required = bool(field_spec["data"].get("required", False)) and key != "title"
            kwargs: dict[str, object] = {"required": False, "help": _field_help(field_spec)}
            if value_type.startswith("list["):
                kwargs["action"] = "append"
                kwargs["default"] = []
            generated.add_argument(option, dest=key, **kwargs)


def _add_edit_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "edit",
        help="Update one field on a modeled desk artifact.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Examples:
  deskops edit task task-fix-thing goal "Updated goal" --root .
  deskops edit pill pill-keep-layers-clean how-not "Do not bypass the guardrail." --root .

Values are parsed with SLDB's field-value parser and the document is re-rendered through its model.
{SELECTOR_HELP}
""".strip(),
    )
    s = p.add_subparsers(dest="subject", required=True)
    subjects = ["task", *[str(meta["subject"]) for meta in ARTIFACT_SUBJECTS.values()]]
    for subject in subjects:
        parser = s.add_parser(subject, help=f"Edit one {subject} field.")
        parser.add_argument("selector", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}")
        parser.add_argument("field", help="Model field name to update; hyphens are accepted for underscores.")
        parser.add_argument("value", help="New field value, parsed like an SLDB field value.")
        parser.add_argument("--root", default=".", help="Target repository root.")


def _add_next_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "next",
        help="Show the next valid workflow action for a task without mutating it.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  deskops next task-fix-thing --root .
  deskops next --diagram
""".strip(),
    )
    p.add_argument("task_id", nargs="?", help=f"Task selector. {SELECTOR_HELP}")
    p.add_argument("--root", default=".", help="Target repository root.")
    p.add_argument("--diagram", action="store_true", help="Render the workflow state machine as Mermaid from its source spec.")


def _add_list_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "list",
        help="List desk workflow artifacts.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  deskops list tasks --root .
  deskops list pills --root .
  deskops list atoms --root .
""".strip(),
    )
    s = p.add_subparsers(dest="subject", required=True)

    tasks = s.add_parser("tasks", help="List actionable tasks.")
    tasks.add_argument("--root", default=".", help="Target repository root.")
    tasks.add_argument(
        "--include-repos",
        action="store_true",
        help="Also list tasks routed by registered sibling repositories' desk/tasks/Board.md files.",
    )

    routines = s.add_parser("routines", help="List routines.")
    routines.add_argument("--root", default=".", help="Target repository root.")

    for kind in ("conditions", "operators", "checklists", "hooks", "edges"):
        parser = s.add_parser(kind, help=f"List {kind}.")
        parser.add_argument("--root", default=".", help="Target repository root.")

    for meta in ARTIFACT_SUBJECTS.values():
        kind = meta["list_subject"]
        parser = s.add_parser(kind, help=f"List {kind}.")
        parser.add_argument("--root", default=".", help="Target repository root.")


def _add_show_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "show",
        help="Show one desk workflow artifact by selector.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Examples:
  deskops show task task-fix-thing --root .
  deskops show pill pill-keep-layers-clean --root .

{SELECTOR_HELP}
""".strip(),
    )
    s = p.add_subparsers(dest="subject", required=True)

    task = s.add_parser(
        "task",
        help="Show one actionable task by selector.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Example:
  deskops show task task-fix-thing --root .

{SELECTOR_HELP}
""".strip(),
    )
    task.add_argument("task_id", help=f"Task selector. {SELECTOR_HELP}")
    task.add_argument("--root", default=".", help="Target repository root.")

    routine = s.add_parser("routine", help="Show one routine by selector.")
    routine.add_argument("routine_id", help=f"Routine selector. {SELECTOR_HELP}")
    routine.add_argument("--root", default=".", help="Target repository root.")

    condition = s.add_parser("condition", help="Show one condition.")
    condition.add_argument("primitive_id", help="Condition identifier.")
    condition.add_argument("--root", default=".", help="Target repository root.")

    operator = s.add_parser("operator", help="Show one operator.")
    operator.add_argument("primitive_id", help="Operator identifier.")
    operator.add_argument("--root", default=".", help="Target repository root.")

    checklist = s.add_parser("checklist", help="Show one checklist.")
    checklist.add_argument("primitive_id", help="Checklist identifier.")
    checklist.add_argument("--root", default=".", help="Target repository root.")

    hook = s.add_parser("hook", help="Show one hook.")
    hook.add_argument("primitive_id", help="Hook identifier.")
    hook.add_argument("--root", default=".", help="Target repository root.")

    edge = s.add_parser("edge", help="Show one edge.")
    edge.add_argument("primitive_id", help="Edge identifier.")
    edge.add_argument("--root", default=".", help="Target repository root.")

    for meta in ARTIFACT_SUBJECTS.values():
        subject = meta["subject"]
        parser = s.add_parser(subject, help=f"Show one {subject} by selector.")
        parser.add_argument("doc_id", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}")
        parser.add_argument("--root", default=".", help="Target repository root.")


def _add_advance_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "advance",
        help="Advance an operational artifact through its routine gates.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement walks a task through execution, testing, and closeout gates when its checklist conditions pass.
{SELECTOR_HELP}
""".strip(),
    )
    s = p.add_subparsers(dest="subject", required=True)

    task = s.add_parser(
        "task",
        help="Advance one actionable task through its routine gates.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement walks a task through execution, testing, and closeout gates when its checklist conditions pass.
{SELECTOR_HELP}
""".strip(),
    )
    task.add_argument("task_id", help=f"Task selector. {SELECTOR_HELP}")
    task.add_argument("--root", default=".", help="Target repository root.")
