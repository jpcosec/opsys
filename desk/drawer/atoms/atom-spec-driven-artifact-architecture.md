# Spec-driven artifact architecture

ID: atom-spec-driven-artifact-architecture
Status: stable
Category: architecture

## What

Artifact models are defined in YAML specs under spec/, compiled at runtime into sldb docs. The compiler reads spec YAML, applies field and primitive templates, and produces payloads that are written as structured markdown documents.

## Why

Hardcoded model logic creates coupling between schema and behavior. Specs make the full artifact surface introspectable, derivable, and generatable without changing Python code.

## How

Each artifact spec declares an id_pattern, field composition, operational primitives, and routine templates. The compiler resolves field references, compiles primitives from templates with context variables, and produces a validated payload that sldb persists.

## When

Use this pattern when defining any new workflow artifact type: write the YAML spec first, then the compiler handles the rest.

## Where

spec/artifacts/, deskops/specs/compiler.py, deskops/specs/loader.py

## For Whom

Developers extending the deskops artifact model.

## Related Atoms

- atom:none

## Materializes Into

- deskops/specs/compiler.py, deskops/specs/loader.py, spec/artifacts/

## Stabilized In

- deskops/specs/

## Distinct From

Pills guide one working session. This atom is the durable architecture pattern that pill guidance should reference.

## Tags

- workspace:drawer
- artifact:atom
