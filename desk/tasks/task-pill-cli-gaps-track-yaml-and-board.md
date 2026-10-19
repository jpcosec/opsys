---
id: task-pill-cli-gaps-track-yaml-and-board
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/cli/registry.py
- deskops/operations.py
- deskops/services/retire.py
- tests/test_retire_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Pill CLI gaps: add pill tracks what it creates, --from-yaml needs no flags, retire unroutes the pill from the Board

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by sldb-04 on 2026-10-18 (inbox note 20261018-221234) while retiring 15 pills in sldb. (1) `deskops add pill` writes desk/contexts/<pill>.md but does not track it; doctor reports it as untracked until `sldb docs track --model PillDoc`, and `doctor --repair` says "Manual repair required". deskops' own test tests/test_retire_cli.py needed `desk update --apply` for the same reason. (2) `deskops add pill --from-yaml` still makes argparse demand --what/--why/--when/--where/--how/--how-not. (3) `deskops retire` on a pill leaves it in the Board's `pills` list, which then dangles, and the Board had to be fixed by hand with `deskops edit board`.

## Goal

_Describe the concrete result this task must produce._

`add pill` tracks the created PillDoc in the store. `add pill --from-yaml` accepts a payload without the per-field flags, as `add task --from-yaml` already does. `retire` on a pill removes it from every Board's `pills` list in the same transaction and reports that it did.

## Scope

_State what is in scope and what is out of scope._

In scope: the add command wiring for pill (deskops/cli/registry.py and the add handler), the pill tracking path in deskops/operations.py or the artifact creation service, deskops/services/retire.py (Board unrouting for pills), and tests. Out of scope: the italic template hints, which are sldb template rendering.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Find how `add task` tracks its document and how its --from-yaml makes the flags optional, and apply the same to pill (and to the other artifact subjects if they share the code path). 2. In retire, when the path is under desk/contexts/ and a Board lists it in pills, rewrite the Board through the BoardDoc write path before deleting, and count that Board reference as handled for the inbound-reference check. 3. Tests: add pill leads to doctor reporting no untracked document; add pill --from-yaml with all fields in YAML succeeds with no flags; retire of a Board-routed pill leaves no dangling pill and stores check stays PASS.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_retire_cli.py tests/test_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The three cases pass in tests and `pytest tests` is green.
