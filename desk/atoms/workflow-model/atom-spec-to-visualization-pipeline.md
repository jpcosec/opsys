---
id: atom-spec-to-visualization-pipeline
title: Spec-to-visualization pipeline
five_wh_one_plus: how
tags:
- system:deskops
- topic:diagrams
- topic:specs
---

# Spec-to-visualization pipeline

## Answer

Deskops renders the lifecycle state machine as Mermaid from its workflow spec (`deskops next --diagram`). Artifact structure diagrams can be rendered from artifact specs through `deskops.specs.mermaid`, but the CLI does not currently expose that projection.
