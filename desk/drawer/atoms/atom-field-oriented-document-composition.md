# Field-oriented document composition

ID: atom-field-oriented-document-composition
Status: stable
Category: architecture

## What

Fields are defined as reusable YAML specs under spec/fields/, compiled into FieldInstanceDoc instances stored under desk/fields/. Artifact documents carry field_refs that compose these field instances rather than inlining values.

## Why

Inline fields create duplication when the same concept (goal, scope, status) appears across artifact types. Field specs establish a shared vocabulary and a single source of truth for each semantic dimension.

## How

Each field spec declares a key, value_type, description, and an optional default. The compiler creates one field instance per artifact-field pair, writing it as a standalone sldb doc. Artifact payloads carry a field_refs list pointing back to those instances.

## When

When defining a new artifact field, first check if an existing field spec covers the semantic dimension. If not, write a new field spec in spec/fields/ before adding it to any artifact.

## Where

spec/fields/, desk/models/field.py, deskops/specs/compiler.py, desk/fields/

## For Whom

Developers extending the artifact model or adding new semantic dimensions to existing artifacts.

## Related Atoms

- atom-spec-driven-artifact-architecture

## Materializes Into

- spec/fields/, desk/models/field.py, desk/fields/

## Stabilized In

- spec/fields/, desk/models/field.py

## Distinct From

Pills are temporary context for a working session. Field instances are durable, standardized, and reusable across artifact types.

## Tags

- workspace:drawer
- artifact:atom
