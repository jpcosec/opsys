# Spec-to-visualization pipeline

ID: atom-spec-to-visualization-pipeline
Status: stable
Category: architecture

## What

The mermaid.py module generates Mermaid.js diagrams directly from artifact specs, producing structure diagrams (artifact-field relationships) and routine diagrams (operational state machines).

## Why

Visual documentation drifts from code without automatic generation. By deriving diagrams from the same YAML specs that drive compilation, visualization always matches the current model definition.

## How

register_diagram renders one structure diagram per artifact (showing fields) and one routine diagram per operational artifact (showing the state machine). The generate_catalog function produces a combined Mermaid document for all registered artifacts. Each diagram maps spec fields and primitive templates to Mermaid nodes and edges.

## When

Run python -m deskops.specs.mermaid to regenerate the full diagram catalog. Useful before documentation reviews or after spec changes.

## Where

deskops/specs/mermaid.py

## For Whom

Documentation maintainers and developers reviewing artifact model architecture.

## Related Atoms

- atom-spec-driven-artifact-architecture, atom-routine-based-task-execution

## Materializes Into

- deskops/specs/mermaid.py

## Stabilized In

- deskops/specs/mermaid.py, tests/test_specs.py

## Distinct From

Pills advise session workflow. This atom describes the visualization pipeline that generates architecture diagrams from specs.

## Tags

- workspace:drawer
- artifact:atom
