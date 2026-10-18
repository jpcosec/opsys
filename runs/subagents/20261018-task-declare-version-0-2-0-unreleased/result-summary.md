# result summary: task-declare-version-0-2-0-unreleased

Done by the supervisor directly.

- pyproject.toml: version 0.1.0 -> 0.2.0. Reinstalling the editable package gives importlib.metadata.version("deskops") == "0.2.0".
- CHANGELOG.md: the entries move under `## [0.2.0] - Unreleased` (no date), with an empty `## [Unreleased]` above it.
- The release drawer task now lists only the remaining steps: sldb v0.1.13 tagged or published, the release date, the suites on 3.12 and 3.13, and the tag and push. It was updated with `deskops edit task`.
- No tag was created.

Full suite (against sldb main 52553cde): see validation.log.
