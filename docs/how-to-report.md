# How To Report

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-reports-capture-evidence-and-next-decision-surface.md`
- `desk/atoms/workflow-model/atom-reports-carry-minimal-reproduction-evidence.md`
- `desk/atoms/workflow-model/atom-inbox-is-coordination-intake.md`

This is the canonical `deskops` guide for writing reports that are operationally useful across tools and repos.

## Purpose

A good report does not only say that something feels wrong. It captures the user intent, the context, the break in expectation, the evidence, and the next decision surface.

## What A Report Is

A report is a durable account of an observed problem, ambiguity, friction point, or operational mismatch.

It should help another person answer:

- what happened
- to whom it happened
- under which conditions it happened
- why it matters
- what should change
- what should not be changed by accident while fixing it

## When To Report

Write a report when:

- a user cannot complete an intended path
- the product behaves correctly but opaquely
- two valid interpretations of the system compete with each other
- documentation and runtime behavior diverge
- a repeated confusion signal appears across sessions
- the team needs a durable artifact instead of chat memory

## Reporting Structure

Use this structure:

- `what`
- `why`
- `when`
- `where`
- `how_fix`
- `how_not_fix`
- `who`
- `whom`
- `which`
- `with`

## Minimal Evidence Set

Attach or summarize:

- reproduction steps
- command transcript or screenshots
- expected behavior
- actual behavior
- relevant references
- open questions if certainty is incomplete

## Severity Cues

Increase urgency when the issue:

- blocks first use
- produces the wrong mental model
- causes destructive actions
- creates invisible state mismatches
- scales across many repos or users

## Opsys Fit

In `deskops`, a report should be reusable across tools and repos and should later fit stateful operational handling such as tasks, routines, checklists, and conditional hooks.

That means the structure should survive beyond one command surface and should remain useful when promoted into a richer workflow object.

## Related Workflow Primitives

- a routine can consume the report as an input
- a ritual can trigger from repeated reports on the same surface
- a checklist can verify the evidence set before closure
- a hook can fire when a report matches a known class of regression
