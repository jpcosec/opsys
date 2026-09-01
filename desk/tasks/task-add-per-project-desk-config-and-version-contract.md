---
id: task-add-per-project-desk-config-and-version-contract
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-add-per-project-desk-config-and-version-contract
current_node: checklist-task-add-per-project-desk-config-and-version-contract-closeout-ready
history:
- operator-task-add-per-project-desk-config-and-version-contract-activate
- operator-task-add-per-project-desk-config-and-version-contract-ready-for-testing
references:
- 53a57e7
- tests/test_config.py
- atom:atom-desk-test-root-precedence-is-explicit
depends_on: []
pills:
- desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md
- desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
files: []
checklists:
- checklist-task-add-per-project-desk-config-and-version-contract-execution-ready
- checklist-task-add-per-project-desk-config-and-version-contract-testing-ready
- checklist-task-add-per-project-desk-config-and-version-contract-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-desk-test-root-precedence-is-explicit
closeout_evidence_verified: true
pill_graduation_verified: true
---

# Add per-project desk config and version contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Give each project desk one explicit local configuration contract that declares desk identity, desk/version expectations, and per-project testing defaults such as sandbox behavior.

## Scope

_State what is in scope and what is out of scope._

- tracked project config for shared desk behavior
- optional local override file for machine-specific settings
- explicit desk format or migration version
- explicit model/workflow expectation version fields
- per-project testing sandbox policy instead of shell-global heuristics
- interaction with environment overrides and explicit CLI flags

## Implementation Path

_Outline the expected implementation route or affected surface._

- Format: JSON. The tracked config file plus an optional gitignored local-override file. Confirmed.
- Harden `DeskConfig.load` into one deterministic deep-merge (config.json then config.local.json), including nested `versions`. Keep tolerant of missing files, but do not swallow malformed JSON silently — surface via a load warning/flag.
- Precedence (authoritative, document it): explicit CLI flag > `DESKOPS_TEST_ROOT` env > `config.local.json` > `config.json` > defaults.
- Single source of truth for current `desk_format` constant (dedupe the two hardcoded `"1.0.0"` in config.py and workspace.py).
- OUT: consuming `project_identity` for routing (owned by horizontal-discovery). OUT: legacy detection/migration (owned by legacy-migrate). `model_version` stays a declared field; no consumer added here.
- Capture the precedence rule as an atom under desk/atoms/ then reflect in README/docs.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
