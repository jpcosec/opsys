---
id: board
name: board
nodes: []
relations: []
direction: both
notation: ''
layout: {}
params: []
sections:
- key: board
  select:
    path_glob: desk/tasks/Board.md
  fields:
  - tasks
  - pills
  edges:
  - relation: tasks
    direction: out
    as: tasks
  - relation: pills
    direction: out
    as: pills
  group_by: ''
  group_order: []
  rules: []
  transitions: null
- key: tasks
  select:
    model: TaskDoc
    path_glob: desk/tasks/**/*.md
  fields:
  - id
  - title
  - status
  - current_node
  - task_type
  edges:
  - relation: pills
    direction: out
    as: pills
  - relation: atoms
    direction: out
    as: atoms
  - relation: tasks
    direction: in
    as: boards
  group_by: current_node
  group_order:
  - ritual-execution
  - ritual-testing
  - ritual-closeout
  rules: []
  transitions: null
- key: pills
  select:
    model: PillDoc
  fields:
  - id
  - title
  - what
  - when
  - how_not
  edges: []
  group_by: ''
  group_order: []
  rules: []
  transitions: null
- key: atoms
  select:
    model: AtomDoc
  fields:
  - id
  - title
  - five_wh_one_plus
  - answer
  edges: []
  group_by: ''
  group_order: []
  rules: []
  transitions: null
---

# Board del desk

## Description

Tareas del Board por nodo del ciclo de vida (contrato de docs/deskops-ui.md, vista board). deskops view board la proyecta al contrato.
