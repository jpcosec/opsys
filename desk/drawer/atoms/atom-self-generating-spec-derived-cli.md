# Self-generating spec-derived CLI

ID: atom-self-generating-spec-derived-cli
Status: stable
Category: architecture

## What

The deskops CLI add, list, and show commands derive their subcommand surface directly from the artifact registry: each spec artifact produces a subcommand group. Field specs generate --flags for each artifact's add subcommand.

## Why

Manually maintaining argparse for every artifact creates drift between what the CLI advertises and what the code supports. Deriving it from specs guarantees the CLI surface always matches the actual artifact model.

## How

The parser builder iterates ARTIFACT_SUBJECTS to create add/list/show subcommands for each registered artifact. For add subcommands, it reads the artifact's field specs from the registry and generates a --flag per field key. The OperationsCLI dispatches by artifact_id to the generic create_artifact path.

## When

When adding new artifact types: register it in ARTIFACT_SUBJECTS and ARTIFACT_MODELS, and the CLI parser and dispatch should automatically include it.

## Where

desk/cli/parser.py (generated subcommands), desk/cli/commands/operations.py (generic dispatch), deskops/operations.py (ARTIFACT_SUBJECTS registry)

## For Whom

CLI users and developers extending the command surface.

## Related Atoms

- atom-spec-driven-artifact-architecture, atom-field-oriented-document-composition

## Materializes Into

- desk/cli/parser.py, desk/cli/commands/operations.py

## Stabilized In

- desk/cli/, tests/test_cli.py

## Distinct From

Pills explain how to use the CLI for one session. This atom is the pattern by which the CLI constructs itself from specs.

## Tags

- workspace:drawer
- artifact:atom
