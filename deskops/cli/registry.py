"""Declarative registry of every deskops CLI command.

The parser in :mod:`deskops.cli.parser` only walks this data; it declares no
command itself. Each command appears exactly once, with its full path, help
text, arguments, handler, and whether it can mutate desk state.

``--help`` output must stay byte-identical to ``tests/fixtures/golden/help``:
argument order, help text, descriptions, epilogs, and formatter choice are all
part of the contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

from sldb.store.layout import project_root

from deskops.cli.model_introspection import DEFAULT_FACTORY
from deskops.cli.model_introspection import REQUIRED
from deskops.cli.model_introspection import artifact_model_fields
from deskops.cli.model_introspection import model_cli_fields
from deskops.errors import UsageError
from deskops.identity import find_context_root
from deskops.identity import find_local_store
from deskops.operations import ARTIFACT_SUBJECTS


ROOT_DESCRIPTION = "deskops: Workflow-domain layer for the hum-ecosystem."
ROOT_EPILOG = """
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


@dataclass(frozen=True, slots=True)
class Arg:
    """One parser argument. Args sharing ``group`` share an exclusive group."""

    flags: tuple[str, ...]
    kwargs: dict[str, Any] = field(default_factory=dict)
    group: str | None = None
    group_required: bool = False


@dataclass(frozen=True, slots=True)
class Command:
    """One command path. ``handler`` is a dotted ``module:attribute`` path."""

    path: tuple[str, ...]
    help: str
    args: tuple[Arg, ...]
    handler: str
    mutates: bool
    epilog: str | None = None
    description: str | None = None
    raw_text: bool = False
    subcommand_dest: str | None = None
    deprecated_for: tuple[str, ...] | None = None


def A(flags: str | tuple[str, ...], **kwargs: Any) -> Arg:
    """Shorthand for an argument declaration."""

    normalized = (flags,) if isinstance(flags, str) else tuple(flags)
    group = kwargs.pop("group", None)
    group_required = kwargs.pop("group_required", False)
    return Arg(
        flags=normalized,
        kwargs=dict(kwargs),
        group=group,
        group_required=group_required,
    )


ROOT_ARG = A("--root", default=".", help="Target repository root.")
ROOT_ARG_NO_PERIOD = A("--root", default=".", help="Target repository root")
ROOT_ARG_MESSAGE = A("--root", default=None, help="Repository root whose desk/ holds the inbox")
ROOT_ARG_INBOX = A(
    "--root",
    help="Repository root whose desk/ holds the inbox; the same --root every other subcommand takes",
)
ROOT_ARG_WHOAMI = A("--root", default=".", help="Repository root to identify")
DESK_ROOT_ARG = A("--desk-root", help="Desk root directory override; defaults to the active project desk")
STORE_ARG = A("--store", help="Store path used to resolve the target project root for the default desk")
REPO_ARG = A("--repo", help="Target a registered repository name in the ecosystem")
PYTHONPATH_ARG = A(
    "--pythonpath",
    help="Project path used when auto-tracking messages through the registered model",
)
PYTHONPATH_INBOX_ARG = A(
    "--pythonpath",
    help="Project path used when auto-tracking inbox notes through a registered InboxNoteDoc model",
)
OUTPUT_FORMAT_ARG = A("--format", choices=("text", "json"), default="text", help="Output format.")
OUTPUT_FORMAT_YAML_ARG = A("--format", choices=("text", "json", "yaml"), default="text")
HERDR_ARG = A("--herdr", default="herdr", help="Herdr executable.")
RUNTIME_ROOT_ARG = A("--root", default=".", help="DeskOps repository root.")


def _add_subject_commands() -> list[Command]:
    """``deskops add <artifact>`` generated from the Pydantic models."""

    commands: list[Command] = []
    models = artifact_model_fields()
    for artifact_id, meta in ARTIFACT_SUBJECTS.items():
        subject = str(meta["subject"])
        help_text = f"Create a {subject} artifact."
        if subject == "repository":
            help_text = (
                "Create a local repository artifact doc; use 'deskops repo register' "
                "for canonical ecosystem registration."
            )
        args = [
            ROOT_ARG,
            A("--from-yaml", help=f"Load the {subject} payload from a YAML file."),
        ]
        model = models.get(artifact_id)
        if model is not None:
            include_special = artifact_id in {"artifact.task"}
            for fmeta in model_cli_fields(model, include_special=include_special):
                # No model field is argparse-required: --from-yaml may supply it,
                # and the model validates what the payload still misses.
                kwargs: dict[str, object] = {"required": False, "help": fmeta.help}
                if fmeta.is_list:
                    kwargs["action"] = "extend"
                    kwargs["nargs"] = "+"
                    kwargs["default"] = []
                if fmeta.choices:
                    kwargs["choices"] = fmeta.choices
                # Carry the default if set (but not sentinel values)
                if fmeta.default is not None and fmeta.default not in (
                    DEFAULT_FACTORY,
                    REQUIRED,
                ):
                    kwargs["default"] = fmeta.default
                args.append(A(fmeta.cli_option, **kwargs))
        commands.append(
            Command(
                path=("add", subject),
                help=help_text,
                args=tuple(args),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=True,
                epilog=f"Example:\n  deskops add {subject} --root . --title \"Example\"",
                description=help_text,
                raw_text=True,
            )
        )
    return commands


def _list_subject_commands() -> list[Command]:
    commands: list[Command] = []
    for meta in ARTIFACT_SUBJECTS.values():
        kind = str(meta["list_subject"])
        args = [ROOT_ARG]
        if kind == "atoms":
            args.append(
                A(
                    "--axis-value",
                    help="Filter atoms by the configured atom_folder_axis namespace value (e.g. licitaciones).",
                )
            )
        args.append(OUTPUT_FORMAT_ARG)
        commands.append(
            Command(
                path=("list", kind),
                help=f"List {kind}.",
                args=tuple(args),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=False,
            )
        )
    return commands


def _edit_subject_commands() -> list[Command]:
    subjects = ["task", *[str(meta["subject"]) for meta in ARTIFACT_SUBJECTS.values()]]
    return [
        Command(
            path=("edit", subject),
            help=f"Edit one {subject} field.",
            args=(
                A("selector", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}"),
                A("field", help="Model field name to update; hyphens are accepted for underscores."),
                A("value", help="New field value, parsed like an SLDB field value."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
        )
        for subject in subjects
    ]


def _show_subject_commands() -> list[Command]:
    commands: list[Command] = [
        Command(
            path=("show", "task"),
            help="Show one actionable task by selector.",
            args=(
                A("task_id", help=f"Task selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog=f"Example:\n  deskops show task task-fix-thing --root .\n\n{SELECTOR_HELP}",
            raw_text=True,
        )
    ]
    for meta in ARTIFACT_SUBJECTS.values():
        subject = str(meta["subject"])
        commands.append(
            Command(
                path=("show", subject),
                help=f"Show one {subject} by selector.",
                args=(
                    A("doc_id", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}"),
                    ROOT_ARG,
                    OUTPUT_FORMAT_ARG,
                ),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=False,
            )
        )
    return commands


def _operation_shared_commands() -> list[Command]:
    """The ``add/edit/bind/next/list/show/advance`` command group."""

    commands: list[Command] = [
        Command(
            path=("add",),
            help="Create desk workflow artifacts from modeled templates.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog="""
Examples:
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest"
  deskops add pill --root . --title "Guardrail: Keep layers clean" --what "..." --why "..."
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("add", "task"),
            help="Create an actionable task bundle.",
            args=(
                A("payload", nargs="?", help="Inline JSON payload for the task."),
                A("--from-yaml", help="Load the task payload from a YAML file."),
                ROOT_ARG,
                A("--title", help="Task title"),
                A("--why", help="Rationale or business driver"),
                A("--goal", help="Task goal"),
                A("--scope", help="Task scope"),
                A("--implementation-path", help="Implementation path"),
                A("--done-when", help="Task completion rule"),
                A(
                    "--from-drawer",
                    help="Drawer file this task is authored from (path, stem, or slug fragment). "
                    "Recorded in the task's from_drawer field; the drawer file is kept for manual cleanup.",
                ),
                A(
                    "--validation",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Validation command or assertion; repeat or space-separate as needed.",
                ),
                A(
                    "--depends-on",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Task identifiers that must complete first; repeat or space-separate as needed.",
                ),
                A("--task-type", help="Workflow task type such as design, implementation, test, reflection, or closeout."),
                A(
                    "--inherits-from",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Task identifiers that provide inherited workflow context; repeat or space-separate as needed.",
                ),
                A(
                    "--atom",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Workflow or knowledge atom refs bound to the task; repeat or space-separate as needed.",
                ),
                A(
                    "--inherit-acceptance-context",
                    action="store_true",
                    help="Inherit validation and done-when context from tasks listed in --inherits-from.",
                ),
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
        ),
        *_add_subject_commands(),
        Command(
            path=("edit",),
            help="Update one field on a modeled desk artifact.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops edit task task-fix-thing goal "Updated goal" --root .
  deskops edit pill pill-keep-layers-clean how-not "Do not bypass the guardrail." --root .

Values are parsed with SLDB's field-value parser and the document is re-rendered through its model.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        *_edit_subject_commands(),
        Command(
            path=("bind",),
            help="Bind workflow context artifacts to tasks.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops bind pill task-fix-thing pill-phase-gate --root .

This updates the task's modeled `pills` list through the deskops artifact layer.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("bind", "pill"),
            help="Bind one pill to one task.",
            args=(
                A("task", help=f"Task selector. {SELECTOR_HELP}"),
                A("pill", help=f"Pill selector. {SELECTOR_HELP}"),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops bind pill task-fix-thing pill-phase-gate --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("next",),
            help="Show the next valid workflow action for a task without mutating it.",
            args=(
                A("task_id", nargs="?", help=f"Task selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                A(
                    "--diagram",
                    action="store_true",
                    help="Render the workflow state machine as Mermaid from its source spec.",
                ),
                A(
                    "--why",
                    action="store_true",
                    help="Explain why this task and these actions were selected.",
                ),
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog="""
Examples:
  deskops next task-fix-thing --root .
  deskops next --diagram
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("list",),
            help="List desk workflow artifacts.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog="""
Examples:
  deskops list tasks --root .
  deskops list pills --root .
  deskops list atoms --root .
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("list", "tasks"),
            help="List actionable tasks.",
            args=(
                ROOT_ARG,
                A(
                    "--include-repos",
                    action="store_true",
                    help="Also list tasks routed by registered sibling repositories' desk/tasks/Board.md files.",
                ),
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
        ),
        *_list_subject_commands(),
        Command(
            path=("show",),
            help="Show one desk workflow artifact by selector.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog=f"""
Examples:
  deskops show task task-fix-thing --root .
  deskops show pill pill-keep-layers-clean --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        *_show_subject_commands(),
        Command(
            path=("advance",),
            help="Advance an operational artifact through the desk's lifecycle graph.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement fires the first lifecycle transition (an sldb RelationDoc between rituals) whose condition holds for the task.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("advance", "task"),
            help="Advance one actionable task through the desk's lifecycle graph.",
            args=(
                A("task_id", help=f"Task selector. {SELECTOR_HELP}"),
                A("--to", help="Optional target node or status for a manual override."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement fires the first lifecycle transition (an sldb RelationDoc between rituals) whose condition holds for the task.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
        ),
    ]
    return commands


def _message_target_args(*, root_arg: Arg, repo: bool = True) -> list[Arg]:
    args = [
        root_arg,
        DESK_ROOT_ARG,
        STORE_ARG,
    ]
    if repo:
        args.append(REPO_ARG)
    args.extend([PYTHONPATH_ARG, OUTPUT_FORMAT_YAML_ARG])
    return args


def _commands() -> list[Command]:
    commands: list[Command] = [
        Command(
            path=("about",),
            help="Print a short overview of deskops and its first-use commands.",
            args=(),
            handler="deskops.cli.commands.core:AboutCLI",
            mutates=False,
        ),
        Command(
            path=("doctor",),
            help="Detect and repair common broken desk states safely.",
            args=(
                ROOT_ARG,
                A("--repair", action="store_true", help="Attempt non-destructive repairs."),
            ),
            handler="deskops.cli.commands.doctor:DoctorCLI",
            mutates=True,
        ),
        Command(
            path=("status",),
            help="Deprecated alias for `deskops doctor`; show current workspace and workflow status.",
            args=(ROOT_ARG,),
            handler="deskops.cli.commands.doctor:DoctorCLI",
            mutates=False,
            deprecated_for=("doctor",),
        ),
        Command(
            path=("faq",),
            help="Browse the first-use FAQ by question.",
            args=(
                A(
                    "question",
                    nargs="?",
                    help="Question index, slug, or text fragment. Omit to list available questions.",
                ),
                OUTPUT_FORMAT_YAML_ARG,
                A("--faq-path", default="docs/faq.md", help="FAQ markdown path"),
            ),
            handler="deskops.cli.commands.faq:FAQCLI",
            mutates=False,
        ),
        Command(
            path=("bootstrap",),
            help="Install or repair sldb and register deskops models in the global store.",
            args=(),
            handler="deskops.cli.commands.core:BootstrapCLI",
            mutates=True,
        ),
        Command(
            path=("init",),
            help="Initialize a local .sldb store and scaffold desk/ if needed.",
            args=(A("path", nargs="?", default=".", help="Target repository path"),),
            handler="deskops.cli.commands.core:InitCLI",
            mutates=True,
        ),
        Command(
            path=("inbox",),
            help="Deprecated alias for `deskops message`; use message send/list/read/ack.",
            args=(
                A("message", nargs="?", help="Inbox note body"),
                A(
                    "--kind",
                    choices=("unclear", "suggestion"),
                    default="unclear",
                    help="Type of inbox message to write",
                ),
                A("--title", help="Short title for the note"),
                ROOT_ARG_INBOX,
                DESK_ROOT_ARG,
                STORE_ARG,
                REPO_ARG,
                A("--sender", help="Override the resolved sender identity with a registered project id"),
                PYTHONPATH_INBOX_ARG,
                A("--list", action="store_true", help="List desk inbox notes"),
                A("--show", help="Show one inbox note by filename, stem, or slug fragment"),
                A("--ack", help="Acknowledge one inbox note by filename, stem, or slug fragment"),
                A("--limit", type=int, default=20, help="Limit listed notes"),
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
            deprecated_for=("message",),
            epilog="""
Deprecated: use `deskops message send|list|read|ack`.

Examples:
  deskops inbox "Need clearer CLI help" --kind unclear --title "CLI help"
  deskops inbox --repo sibling-repo --sender current-repo "Need follow-up"
  deskops inbox --list --root .
  deskops inbox --show 20260614-cli-help --root .
  deskops inbox --ack 20260614-cli-help --root .

--show/--ack selector: filename, stem, or slug fragment.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("message",),
            help="Send, list, read, or acknowledge cross-desk messages.",
            args=(),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
            epilog="""
Examples:
  deskops message send "Need follow-up" --to sibling-repo --title "Follow-up"
  deskops message list --root .
  deskops message read 20260614-cli-help --root .
  deskops message ack 20260614-cli-help --root .

read/ack selector: filename, stem, or unique slug fragment.
""".strip(),
            raw_text=True,
            subcommand_dest="message_command",
        ),
        Command(
            path=("message", "send"),
            help="Send a message to a project desk.",
            args=(
                A("body", help="Message body"),
                A("--title", help="Short title for the message"),
                A(
                    "--kind",
                    choices=("unclear", "suggestion"),
                    default="suggestion",
                    help="Type of message to send",
                ),
                A("--to", dest="repo", help="Target a registered repository name in the ecosystem"),
                A(
                    "--from",
                    dest="sender",
                    help="Override the resolved sender identity with a registered project id",
                ),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE, repo=False),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
        ),
        Command(
            path=("message", "list"),
            help="List received messages.",
            args=(
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
                A("--limit", type=int, default=20, help="Limit listed messages"),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=False,
        ),
        Command(
            path=("message", "read"),
            help="Read one received message.",
            args=(
                A("selector", help="Message filename, stem, or unique slug fragment"),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=False,
        ),
        Command(
            path=("message", "ack"),
            help="Acknowledge one received message.",
            args=(
                A("selector", help="Message filename, stem, or unique slug fragment"),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
        ),
        Command(
            path=("promote",),
            help="Promote inbox notes into loose drawer candidates. Drawer items become tasks only by authoring them with `deskops add task`.",
            args=(),
            handler="deskops.cli.commands.promote:PromoteCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops promote inbox-to-drawer-task 20260614-unclear --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="promote_command",
        ),
        Command(
            path=("promote", "inbox-to-drawer-task"),
            help="Promote one inbox note into a deferred drawer task candidate.",
            args=(
                A("selector", help="Inbox filename, stem, or unique slug fragment"),
                ROOT_ARG_NO_PERIOD,
                A("--title", help="Override the drawer task title"),
            ),
            handler="deskops.cli.commands.promote:PromoteCLI",
            mutates=True,
        ),
        Command(
            path=("drawer",),
            help="Manage deferred drawer entries.",
            args=(),
            handler="deskops.cli.commands.drawer:DrawerCLI",
            mutates=True,
            subcommand_dest="drawer_command",
        ),
        Command(
            path=("drawer", "remove"),
            help="Remove one drawer entry, its tracking, and its bullets on the drawer board.",
            args=(
                A("selector", help=f"Drawer file selector. {SELECTOR_HELP}"),
                ROOT_ARG_NO_PERIOD,
                A(
                    "--force",
                    action="store_true",
                    help="Remove even when a task in desk/tasks/ records the entry in from_drawer.",
                ),
            ),
            handler="deskops.cli.commands.drawer:DrawerCLI",
            mutates=True,
        ),
        Command(
            path=("retire",),
            help="Retire one obsolete desk document that has no dedicated verb, with its reason and refs.",
            args=(
                A("path", help="Path of the file under desk/ to retire (pills, inbox notes, steps, roles, runtimes, faq, logbook, materializations, leftovers)."),
                ROOT_ARG_NO_PERIOD,
                A("--reason", required=True, help="Why the document is obsolete."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Commit (HEAD or an ancestor) or existing path that replaces or resolves it. Repeatable.",
                ),
                A(
                    "--force",
                    action="store_true",
                    help="Retire even when other desk or docs files still reference it.",
                ),
            ),
            handler="deskops.cli.commands.retire:RetireCLI",
            mutates=True,
            raw_text=True,
            epilog=(
                "Example:\n"
                "  deskops retire desk/contexts/pill-old.md --root . \\\n"
                "    --reason \"Describes the retired routine primitives\" --ref a0e00e3\n\n"
                "Tasks, drawer entries, atoms and registry entries keep their own verbs:\n"
                "closeout, drawer remove, atoms delete, repo remove."
            ),
        ),
        Command(
            path=("issue",),
            help="Close and list desk issues.",
            args=(),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=True,
            subcommand_dest="issue_command",
            epilog="""
Examples:
  deskops issue close issue-empty-selector --root . --reason "Fixed by the CLI" --ref abc1234
  deskops issue list --root . --status open

Issues live under desk/issues/ or desk/drawer/issues/. Closing keeps the file and appends a ## Resolution section.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("issue", "close"),
            help="Close one issue with its reason, keeping the file as the trace.",
            args=(
                A("selector", help=f"Issue selector. {SELECTOR_HELP}"),
                A("--reason", required=True, help="Why the issue is closing."),
                A(
                    "--ref",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Commit or path supporting the close; repeat or space-separate as needed.",
                ),
                ROOT_ARG,
                A("--force", action="store_true", help="Close again even when already closed."),
            ),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=True,
            epilog="""
Example:
  deskops issue close issue-empty-selector --root . --reason "Fixed by the CLI" --ref abc1234 --ref deskops/cli

Selector: issue id, filename, stem, or unique slug fragment under desk/issues/ or desk/drawer/issues/.
The issue status is set to closed and a ## Resolution section records Closed, Reason and Refs.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("issue", "list"),
            help="List desk issues with id, status and title.",
            args=(
                ROOT_ARG,
                A(
                    "--status",
                    choices=("open", "closed", "all"),
                    default="all",
                    help="Filter issues by status group.",
                ),
            ),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=False,
        ),
        *_operation_shared_commands(),
        Command(
            path=("repo",),
            help="Repository registration and discovery.",
            args=(),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            subcommand_dest="repo_command",
        ),
        Command(
            path=("repo", "register"),
            help="Canonically register a repository in the ecosystem registry and track it in SLDB.",
            args=(
                A("name", help="Human-readable name"),
                A("path", nargs="?", help="Repository root path (relative to ecosystem root or absolute)"),
                A(
                    "--path",
                    dest="path_option",
                    help="Repository root path (relative to ecosystem root or absolute)",
                ),
                A("--id", help="Stable unique ID, defaults to slugified name"),
                A("--description", help="Markdown description"),
                A("--tags", help="Comma-separated tags"),
                A("--store", help="Store path to anchor the registry"),
                A("--pythonpath", help="Python path for model resolution"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            description="Canonically register a repository in the ecosystem registry and track it in SLDB.",
        ),
        Command(
            path=("repo", "whoami"),
            help="Print the canonical project identity for the current repository.",
            args=(
                ROOT_ARG_WHOAMI,
                A("--store", help="Store path to anchor the registry lookup"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=False,
            description="Print the canonical project identity for the current repository.",
        ),
        Command(
            path=("repo", "remove"),
            help="Remove a repository from the ecosystem registry so it can be registered again.",
            args=(
                A("selector", help=f"Repository id, file stem, or repo-<id>. {SELECTOR_HELP}"),
                ROOT_ARG,
                A("--store", help="Store path to anchor the registry lookup"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            description="Remove a repository from the ecosystem registry so it can be registered again.",
        ),
        Command(
            path=("desk",),
            help="Desk workspace management.",
            args=(),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
            subcommand_dest="desk_command",
        ),
        Command(
            path=("desk", "install"),
            help="Scaffold a minimal local desk/ surface in a repo.",
            args=(A("path", help="Target repository path"),),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "migrate"),
            help="Adopt a legacy or partial desk into the current non-destructive workspace contract.",
            args=(ROOT_ARG,),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "replace"),
            help="Replace an exact substring in one desk file that has no modeled edit verb.",
            args=(
                A(
                    "path",
                    help="Path of the file under desk/ (desk/... or relative to the desk root).",
                ),
                ROOT_ARG,
                A("--old", required=True, help="Exact text to replace; must occur --count times."),
                A("--new", required=True, help="Replacement text."),
                A(
                    "--count",
                    type=int,
                    default=1,
                    help="Exact number of occurrences of --old to require (default: 1).",
                ),
            ),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "update"),
            help="Report and repair divergence between the current desk, its models, and its store.",
            args=(
                ROOT_ARG,
                A("--apply", action="store_true", help="Apply repairs (dry run by default)."),
            ),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("atoms",),
            help="Atom model and namespace management.",
            args=(),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
            subcommand_dest="atoms_command",
        ),
        Command(
            path=("atoms", "add-namespace"),
            help="Add an extensible atom tag namespace to desk/atoms/tag-namespaces.yaml.",
            args=(
                A("namespace", help="Namespace name, such as pattern."),
                ROOT_ARG,
                A("--meaning", required=True, help="What this namespace means."),
                A("--use-when", required=True, help="When to use this namespace."),
                A(
                    "--do-not-use-when",
                    required=True,
                    help="When an existing namespace should be preferred instead.",
                ),
                A(
                    "--example",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Example tag using the namespace; repeat or space-separate as needed.",
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "list"),
            help="Deprecated alias for `deskops list atoms`; list all atoms.",
            args=(
                ROOT_ARG,
                A(
                    "--axis-value",
                    help="Filter atoms by the configured atom_folder_axis namespace value (e.g. licitaciones).",
                ),
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
            deprecated_for=("list", "atoms"),
        ),
        Command(
            path=("atoms", "reorganize"),
            help="Move atoms into folders derived from the configured atom_folder_axis tag namespace. Idempotent.",
            args=(
                ROOT_ARG,
                A("--dry-run", action="store_true", help="Report planned moves without changing files."),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "show"),
            help="Deprecated alias for `deskops show atom`; show an atom.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
            deprecated_for=("show", "atom"),
        ),
        Command(
            path=("atoms", "validate"),
            help="Validate one atom or all atoms for lifecycle safety checks.",
            args=(
                A("doc_id", nargs="?", help=f"Atom selector. {SELECTOR_HELP}", group="target", group_required=True),
                A(
                    "--all",
                    action="store_true",
                    help="Validate all atoms under desk/atoms/.",
                    group="target",
                    group_required=True,
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
        ),
        Command(
            path=("atoms", "create"),
            help="Create one atom from a pill, graph finding, or diagram source while preserving exact provenance.",
            args=(
                A("doc_id", help="New atom id to create, conventionally atom-<slug>."),
                A(
                    "--five-wh-one-plus",
                    required=True,
                    choices=("what", "why", "how", "how_not", "when", "where", "for_whom"),
                    help="The single 5WH1+ question this atom answers.",
                ),
                A("--title", help="Optional title override for the created atom."),
                A(
                    "--tag",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Atom tag to add; repeat or space-separate as needed.",
                ),
                A(
                    "--from-pill",
                    metavar="PILL_ID",
                    help="Create the atom from one pill field chosen by --five-wh-one-plus.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--from-graph",
                    metavar="SOURCE_ID->TARGET_ID",
                    help="Create the atom from one missing graph finding resolved by source and target ids.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--from-diagram",
                    metavar="SPEC_PATH",
                    help="Create the atom from one diagram source file such as docs/diagrams/example/source.mmd.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--graph",
                    help="Optional graph snapshot path consulted in addition to declared-edge findings when resolving --from-graph.",
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "delete"),
            help="Delete one atom after checking inbound references.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help="Delete even when inbound atom:<id> references are present.",
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "split"),
            help="Split one atom into new atoms while keeping the original as a redirect stub.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                A(
                    "--into",
                    nargs="+",
                    required=True,
                    metavar="NEW_ATOM_ID",
                    help="New atom ids to create from the source atom. Provide at least two.",
                ),
                A(
                    "--section",
                    action="append",
                    default=[],
                    metavar="NEW_ATOM_ID:SECTION_HEADING",
                    help=(
                        "Assign a created atom id to a specific markdown heading inside the source atom answer. "
                        "Repeat once per target. When omitted, sections are assigned to --into ids in order."
                    ),
                ),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help=(
                        "Proceed even when inbound atom:<id> references exist. The original atom is kept as a redirect stub; "
                        "referrers are not rewritten automatically."
                    ),
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "merge"),
            help="Merge one source atom into an existing target atom while rewriting inbound references.",
            args=(
                A("doc_id", help=f"Source atom selector. {SELECTOR_HELP}"),
                A(
                    "--into",
                    required=True,
                    metavar="TARGET_ATOM_ID",
                    help="Existing target atom selector that absorbs the source atom.",
                ),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help=(
                        "Proceed when merge semantics are ambiguous, such as conflicting five_wh_one_plus values. "
                        "Inbound atom:<source> references are rewritten to atom:<target>, and the source atom is kept as a redirect stub for traceability."
                    ),
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "crossroad"),
            help="Write the crossroad of a domain path: the mandatory parent that describes what hangs below it.",
            args=(
                A(
                    "path",
                    help="Domain path such as pizzeria.carta; its parent path needs a crossroad first.",
                ),
                A("--title", required=True, help="Short title of the domain area."),
                A("--content", required=True, help="Written description of what hangs below this path."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "proto"),
            help="Create a protoatom: a free atom with a title, content and tags.",
            args=(
                A("doc_id", help="New protoatom id, conventionally proto-<slug>."),
                A("--title", required=True, help="Short title of the free knowledge unit."),
                A("--content", default="", help="Free markdown content."),
                A(
                    "--tag",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Atom tag; a single domain:<path> tag places the protoatom in the domain tree.",
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "type"),
            help="Type a protoatom into another sldb model, keeping the protoatom as a redirect stub.",
            args=(
                A("doc_id", help="Protoatom selector: id or filename."),
                A("--model", required=True, help="Target sldb model name, such as AtomDoc or TaskDoc."),
                A("--id", dest="new_id", help="Id of the typed document; defaults to <model>-<slug>."),
                A(
                    "--content-field",
                    help="Target field that receives the protoatom content; defaults to 'content' when the model has it.",
                ),
                A("--data", help="Inline JSON with the remaining fields the target model requires."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "tree"),
            help="Show the domain tree: crossroads and the documents hanging from them.",
            args=(ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
        ),
        Command(
            path=("graph",),
            help="Build and inspect deskops KGDB graph runtime outputs.",
            args=(),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
            subcommand_dest="graph_command",
        ),
        Command(
            path=("graph", "build"),
            help="Build the KGDB graph snapshot runtime artifact.",
            args=(
                ROOT_ARG,
                A(
                    "--output",
                    help="GraphSnapshot destination; relative paths are resolved from --root.",
                ),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
        ),
        Command(
            path=("graph", "neighbors"),
            help="Show incoming and outgoing neighbors for one graph node.",
            args=(
                A(
                    "id",
                    help="Graph node id to inspect, formatted as type:id (e.g. atom:atom-name, task:task-name, issue:issue-name).",
                ),
                ROOT_ARG,
                A("--graph", help="Graph snapshot path; defaults to the root runtime snapshot."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=False,
        ),
        Command(
            path=("graph", "missing"),
            help="Report missing graph targets and dangling declared references.",
            args=(
                ROOT_ARG,
                A("--graph", help="Optional graph snapshot path to check for missing edge targets."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=False,
        ),
        Command(
            path=("graph", "reflect"),
            help="Write review-only self-reflection findings for a graph snapshot.",
            args=(
                ROOT_ARG,
                A("--graph", help="Graph snapshot path; defaults to the root runtime snapshot."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
        ),
        Command(
            path=("materialize",),
            help="Render tracked desk role prompts into installed pi-agent files.",
            args=(
                ROOT_ARG,
                A("--out", help="Output directory override; defaults to ~/.pi/agent/agents."),
            ),
            handler="deskops.cli.commands.materialize:MaterializeCLI",
            mutates=True,
        ),
        Command(
            path=("drift",),
            help="Check for role-agent drift between tracked role docs and installed agent files.",
            args=(),
            handler="deskops.cli.commands.drift:DriftCLI",
            mutates=False,
            subcommand_dest="drift_command",
        ),
        Command(
            path=("drift", "check"),
            help="Compare rendered role-agent output to installed files.",
            args=(
                ROOT_ARG,
                A("--out", help="Agent directory override; defaults to ~/.pi/agent/agents."),
            ),
            handler="deskops.cli.commands.drift:DriftCLI",
            mutates=False,
        ),
        Command(
            path=("closeout",),
            help="Workflow closeout operations.",
            args=(),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            subcommand_dest="closeout_command",
        ),
        Command(
            path=("closeout", "commit"),
            help="Create the tool-made closing commit, linked to a run evidence directory or marked manual.",
            args=(
                ROOT_ARG,
                A("--run-dir", help="Run evidence dir under runs/subagents/.", group="closing_route"),
                A(
                    "--no-run",
                    action="store_true",
                    help="Close without a subagent run; requires --reason. Use instead of --run-dir.",
                    group="closing_route",
                ),
                A("--reason", help="Why the task closes without a run; required with --no-run."),
                A("--task", required=True, help="Task id being closed."),
                A(("-m", "--message"), help="Commit message subject."),
                A(
                    "--paths",
                    nargs="*",
                    default=None,
                    help="Paths to stage; defaults to run.yaml touched paths, else staged index.",
                ),
                A("--run-id", help="Subagent run id to record in run.yaml (--run-dir only)."),
                A("--session", help="Child session.jsonl path to hash into run.yaml (--run-dir only)."),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout commit --root . --task task-fix-thing \\
    --run-dir runs/subagents/20260729-120000-task-fix-thing \\
    --run-id 6046eaef --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \\
    --paths deskops/foo.py tests/test_foo.py

Without a subagent run, close the task manually and say why:
  deskops closeout commit --root . --task task-fix-thing \\
    --no-run --reason "Fixed by the supervisor directly; no subagent was dispatched" \\
    --paths deskops/foo.py tests/test_foo.py

With --run-dir the commit message carries Task-Id/Run-Dir/Run-Id/Session-Sha256
trailers; with --no-run it carries Task-Id/Closeout-Mode: manual/Closeout-Reason.
Either way an index entry is recorded back into runs/subagents/index.jsonl
and committed with the closing commit; it names the task and run, and the
commit hash is resolved from the commit's Task-Id trailer. The commit is made
by this command, not by agent discretion.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "supersede"),
            help="Close a task whose subject no longer exists, naming a reason and a resolvable ref.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being closed."),
                A("--reason", required=True, help="Why the task's subject no longer exists."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Ancestor commit id or existing path; repeat for more refs.",
                ),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout supersede --root . --task task-fix-thing \\
    --reason "The owner deleted the target feature in 9f64f0f; there is nothing left to do" \\
    --ref 9f64f0f

Supersede skips the evidence gates, because no run, test, or atom describes
work that was never done. It still makes exactly one closing commit: status and
history record `superseded`, the commit carries Closeout-Mode: superseded with
Closeout-Reason and one Closeout-Ref per ref, the task leaves the Board, and
the run index entry is marked superseded.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "retire"),
            help="Remove a task that was already resolved before the ritual lifecycle.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being retired."),
                A("--reason", required=True, help="Why the task is already resolved."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Ancestor commit id that resolved the task; repeat for more refs.",
                ),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout retire --root . --task task-fix-thing \\
    --reason "Resolved before the ritual lifecycle existed" \\
    --ref 3900ad4

Retire removes a task whose status is already resolved, closed, done or
complete, as pre-lifecycle tasks are. The ref must be a commit that is HEAD or
an ancestor. The status is not rewritten and the evidence gates do not run. It
makes exactly one closing commit: the task leaves the Board, the commit carries
Closeout-Mode: legacy-resolved with Closeout-Reason and one Closeout-Ref per
ref, and the run index entry is marked legacy-resolved.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "verify"),
            help="Strictly verify closeout evidence gates for one task and print a structured report.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being verified."),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=False,
        ),
        Command(
            path=("runtime",),
            help="Manage the live Herdr runtime for this DeskOps desk.",
            args=(),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
            subcommand_dest="runtime_command",
        ),
        Command(
            path=("runtime", "init"),
            help="Initialize or reuse this desk's Herdr Space.",
            args=(
                RUNTIME_ROOT_ARG,
                A("--agents", action="store_true", help="Start executor and tester Pi agents."),
                HERDR_ARG,
            ),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
        ),
        Command(
            path=("runtime", "status"),
            help="Show this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "attach"),
            help="Focus this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "stop"),
            help="Close this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
        ),
        Command(
            path=("runtime", "workers"),
            help="List live Herdr agents across all workspaces on this machine.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "supervise"),
            help="Block on one agent's Herdr lifecycle and report blocked/done settles without advancing the desk.",
            args=(
                A("agent", help="Herdr agent name or pane id to supervise, e.g. deskops-executor."),
                RUNTIME_ROOT_ARG,
                HERDR_ARG,
                A(
                    "--max-iterations",
                    type=int,
                    default=None,
                    help="Stop after this many settle events instead of running forever (mainly for testing).",
                ),
                A(
                    "--read-lines",
                    type=int,
                    default=200,
                    help="Terminal lines to capture from the agent on a blocked or done settle.",
                ),
                A(
                    "--timeout-ms",
                    type=int,
                    default=None,
                    help="Give up waiting after this many milliseconds per settle attempt (default: wait indefinitely).",
                ),
            ),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
    ]
    return commands


def command_registry() -> tuple[Command, ...]:
    """Return every command in declaration order (parents before children)."""

    return tuple(_commands())


def command_for_path(path: tuple[str, ...]) -> Command:
    """Look up one command by its full path."""

    for command in command_registry():
        if command.path == path:
            return command
    raise KeyError(path)


def resolve_context(args: Any) -> tuple[Path, Path | None]:
    """Resolve one ``(desk_root, store)`` pair for every command.

    ``--root`` sets the desk root and ``--store`` sets the store. When both are
    given they must agree (the store must be ``<root>/.sldb``). With neither,
    the upward walk stops at the nearest ancestor containing ``desk/`` or
    ``.git``; the store is that boundary's ``.sldb`` only, never an ancestor's.
    """
    root_arg = getattr(args, "root", None)
    store_arg = getattr(args, "store", None)
    root_given = bool(
        getattr(args, "_deskops_root_explicit", False)
        or getattr(args, "_deskops_root_override", False)
        or root_arg not in (None, "", ".")
    )
    store_path = Path(store_arg).expanduser().resolve() if store_arg else None

    if root_given:
        root = Path(root_arg).expanduser().resolve() if root_arg else Path.cwd().resolve()
        if store_path is not None:
            expected = (root / ".sldb").resolve()
            if store_path != expected:
                raise UsageError(
                    f"--root '{root}' and --store '{store_path}' disagree; "
                    f"when both are given the store must be '{expected}'."
                )
        else:
            store_path = find_local_store(root)
        return root, store_path

    if store_path is not None:
        return project_root(store_path), store_path

    root = find_context_root()
    return root, find_local_store(root)
