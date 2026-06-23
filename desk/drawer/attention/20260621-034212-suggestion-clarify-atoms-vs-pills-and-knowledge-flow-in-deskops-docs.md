---
kind: suggestion
sender_project: paper_IEEE
created_at: 2026-06-21T03:42:12
status: open
---

# Clarify atoms vs pills and knowledge flow in deskops docs

Deskops documentation/help should explicitly explain the knowledge hierarchy and intended flow between atoms, context pills, specs/docs, code, and testing. Current help makes artifact types visible, but it does not make the epistemic model sufficiently clear. Required clarifications: (1) atoms are the baseline stabilized knowledge substrate for project purpose, business rules, domain theory, tooling, code patterns, and testing strategies; (2) context pills are transitionary operational context for subagents and task-phase guidance; (3) avoid duplicating stable knowledge between pills and atoms; (4) tasks should bind enough atoms, files, and pills to enable autonomous execution with minimal hidden chat context; (5) preferred flow is pills -> atoms -> specs/docs -> code -> testing. Suggested surfaces to improve: deskops

Workflow-domain CLI built on top of sldb.

What it manages:
- repo-local desk workspaces
- global and local sldb bootstrap flows
- workflow models such as tasks, boards, pills, rituals, inbox notes, and repository registrations

First-use commands:
- deskops bootstrap
- deskops init .

Useful commands:
- deskops faq
- deskops inbox
- deskops promote
- deskops repo register, quickstart/help docs, and any first-use FAQ material.
