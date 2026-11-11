---
id: task
name: task
nodes: []
relations: []
direction: both
notation: ''
layout: {}
params:
- name: id
  required: true
  default: null
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
- key: task
  select:
    model: TaskDoc
    path_glob: desk/tasks/**/*.md
    where: id = {id}
  fields:
  - '*'
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
  group_by: ''
  group_order: []
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

# Tarea del desk

## Description

Una tarea por id con sus campos (contrato de docs/deskops-ui.md, vista task).
