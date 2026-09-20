---
name: blocks
direction: directed
cardinality: many_to_many
axis: ''
source_types:
- TaskDoc
target_types:
- TaskDoc
condition: ''
---

# blocks

## Description

Derived (mode read): a task that cannot advance until this one does.
