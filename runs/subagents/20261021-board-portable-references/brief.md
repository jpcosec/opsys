Role: executor
Task: task-board-portable-references
Phase MEPU compatibility: this task changes Board context references plus own tests/atom; task-closeout-without-atoms changes closeout code and FAQ plus separate tests/atom. No prerequisite between them and no overlapping implementation files. Coordinator alone manages task routing and closeout.
Board context fields are explicitly in scope; do not mutate Board tasks or close either task. Save stdout.log, stderr.log, result-summary.md, validation.log.
