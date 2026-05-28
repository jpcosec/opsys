# How Field

ID: field-instance-atom-self-generating-spec-derived-cli-how
Status: active

## Summary

Compiled field instance for how.

## Field Key

how

## Value Type

string

## Owner Artifact

atom-self-generating-spec-derived-cli

## Value

The parser builder iterates ARTIFACT_SUBJECTS to create add/list/show subcommands for each registered artifact. For add subcommands, it reads the artifact's field specs from the registry and generates a --flag per field key. The OperationsCLI dispatches by artifact_id to the generic create_artifact path.

## Tags

- primitive:field
- field:how
- artifact:atom
