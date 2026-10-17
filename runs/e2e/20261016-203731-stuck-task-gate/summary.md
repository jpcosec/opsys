# e2e: stuck-task-gate (deepseek/deepseek-flash)

- works (harness checks): yes
- docs ok (agent got there from the docs): yes
- cost $0.0065, 49.3s, 20 tool calls, 1 failed, 4 --help, 0 source reads

## Checks

- [x] the task is at the closeout stage
- [x] the task is still open (not completed)
- [x] its validation is pytest
- [x] the local store passes sldb stores check

## Agent

task-ship-notes was blocked by the empty validation field failing the nonempty(validation) gate; I set validation to [pytest] and advanced it to ritual-closeout without completing it.

## Friction

- **major** (missing discovery surface) use-deskops/SKILL.md § Mandatory read route: The mandatory route names AGENTS.md, README.md, and docs/faq.md, but none exist in the repo; docs/quickstart.md referenced by `deskops --help` is also absent. — Read the desk/ artifacts directly and used `deskops faq` for equivalent content.
- **minor** (misleading help) CLI help § deskops edit task --help: Help does not list valid field names or how to express list-valued fields; the value is only described as 'parsed like an SLDB field value'. `validation pytest` failed, requiring bracket syntax `[pytest]`. — Used the type error message to guess `[pytest]`.
- **minor** (naming mismatch) desk/tasks/task-ship-notes.md / state output § Status vs Current node: After advancing, the task reports Status: ready_for_testing while Current node: ritual-closeout, which reads as inconsistent until you see the closeout gate requires that status. — Confirmed intended via the closeout gate condition in `deskops show task`.
- **minor** (hidden state dependency) .sldb/core/models/TaskDoc.yaml § model_hash / roster_hash / model path: Editing one document field rewrote the model hash/roster hash, and model_ref path points to an absolute location outside the repo. — Not resolved; left as runtime bookkeeping.

## Failed commands

- `cd /tmp/deskops-e2e-5k1xq2wn/repo && deskops edit task task-ship-notes validation pytest --root . 2>&1`

## Source reads (docs were not enough)

- none
