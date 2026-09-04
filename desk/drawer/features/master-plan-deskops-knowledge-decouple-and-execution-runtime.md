# Master Plan — deskops/knowledge decouple + SLDB execution runtime

## Kind

epic / master-plan

## Status

active — executing directly (god-agent mode) until the launcher exists.

## Decisions (authoritative)

1. **knowledge owns ALL knowledge**: atoms, atom model, tags/namespaces, atom lifecycle, atom materializers, provenance, AND deskops' own documentation atoms. deskops retains zero atoms.
2. **deskops owns execution/workflow**: tasks, board, phases, rituals, pills, routines, closeout, operations, model policy, launcher.
3. **Model policy is execution** → lives in deskops (`ModelPolicyDoc`).
4. **Full SLDB**: operations are typed SLDB documents hooked to CLI entries; agents choose declared operations, never free bash.
5. **KGDB is a live execution graph**: edges/routines/conditions/operations become typed navigable relations; `deskops next` navigates the graph.
6. **Break what must break**, but every phase ends green in BOTH repos.
7. Reference implementation: `~/proyectos/gemini_test/kb_agent/knowledge/compiler.py` (SLDB+KGDB context compiler, per-role structured context, code-enforced non-negotiable floors).

## Boundary (new)

| Concern | Repo |
|---|---|
| AtomDoc model, atom_tags, namespaces | knowledge |
| Atom lifecycle (validate/split/merge/delete/create) | knowledge |
| Atom materializers, provenance | knowledge |
| 132 `desk/atoms/*.md` incl. workflow-model docs | knowledge store |
| Tasks, board, phases, rituals, routines, closeout | deskops |
| Pills (transient workflow context) | deskops |
| OperationDoc (typed ops + CLI entries) | deskops |
| ModelPolicyDoc (cost/fallback/tier/budget) | deskops |
| Context compiler, launcher | deskops |
| KGDB live execution graph | deskops (consumes knowledge atoms) |

## Tasks & Phases

- FASE 1 (desacople): T1 migrate atoms→knowledge, T2 deskops consumes atoms via knowledge boundary.
- FASE 2 (full sldb): T3 OperationDoc typed operations + CLI entries.
- FASE 3 (kgdb vivo): T4 KGDB live execution graph; `deskops next` navigates it.
- FASE 4 (modelos): T5 ModelPolicyDoc — cost, fallback chain, tier, token budget, capabilities.
- FASE 5 (runtime): T6 per-role SLDB context compiler; T7 launcher tmux+codex/agy/pi.
- FASE 6 (doctrina): T8 reconcile pills, migrate RoleDoc structured fields, regenerate spec2viz.

## Execution mode

God-agent: implemented directly by the operator assistant, phase by phase, atomic commits, suite green in both repos per phase. Cross-repo coordination via inbox where needed.
