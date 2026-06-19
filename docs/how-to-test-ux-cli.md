# How To Test UX CLI

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md`

This is the canonical `deskops` guide for testing CLI user experience, not only CLI correctness.

## Purpose

A CLI can be technically correct and still fail the user if it does not help them discover valid next steps, understand scope, or recover from partial knowledge.

## What UX CLI Testing Is

UX CLI testing checks whether a person can move through a command surface with an understandable mental model.

The primary question is not only "did the command run?" but also:

- could the user infer what to do next
- could the user understand why the command failed
- could the user recover without external help
- did the command names and flags match the user's expectations

## Core Testing Contexts

Always include these contexts when relevant:

- first use
- partial knowledge
- wrong assumption
- uninitialized workspace
- shared or global state
- degraded documentation alignment

## Test Sandbox

Run exploratory or UX CLI mutation against a dedicated sandbox root under `.tmp/`, not the repo's real `desk/`.

Recommended setup:

```bash
export DESKOPS_TEST_ROOT=.tmp/deskops-cli-test
rm -rf "$DESKOPS_TEST_ROOT"
mkdir -p "$DESKOPS_TEST_ROOT"
```

When `DESKOPS_TEST_ROOT` is set, `deskops` commands that default to `--root .` will use that sandbox root instead. This keeps ad hoc `add`, `edit`, `show`, `list`, `advance`, `promote`, `inbox`, `repo`, and `graph` testing from polluting the repository's tracked `desk/` surfaces.

If you want to test the real repo desk intentionally, pass an explicit `--root .` only after unsetting `DESKOPS_TEST_ROOT`.

## Test Method

Run UX CLI testing as a guided walkthrough.

1. define the user intent
2. define the starting knowledge
3. define the starting state
4. walk the natural command path
5. record each expectation break
6. classify the issue

Useful classifications:

- naming mismatch
- missing discovery surface
- scope ambiguity
- hidden state dependency
- misleading help
- recoverability failure
- documentation/runtime divergence

## What To Observe

Look for these signals:

- the user must already know the answer in order to ask the question
- help is reference-heavy but path-light
- flags suggest one scope model but implement another
- the CLI relies on local state without surfacing that dependency clearly
- recovery paths exist in theory but are not discoverable from the current failure

## Pass Heuristics

A CLI path is strong when:

1. the next likely command is visible
2. failure messages expose the relevant missing scope or state
3. discovery commands exist before inspect commands require exact identifiers
4. help text and runtime behavior agree

## Opsys Fit

In `deskops`, UX CLI testing usually begins as a routine.

It becomes a ritual when the team attaches cadence, trigger conditions, ownership, and closure semantics such as:

- before every onboarding-facing release
- after command-surface redesign
- when help text and runtime behavior diverge

It can also drive:

- checklists for release gates
- hooks that trigger on onboarding-surface changes
- reports that capture concrete user-facing breaks
