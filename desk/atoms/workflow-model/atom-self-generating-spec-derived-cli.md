---
id: atom-self-generating-spec-derived-cli
title: Self-generating model-derived CLI
five_wh_one_plus: how
tags:
- system:deskops
- layer:cli
- topic:models
---

# Self-generating model-derived CLI

## Answer

The deskops CLI derives artifact add/list/show/edit surfaces from the Pydantic artifact models registered in `ARTIFACT_SUBJECTS`, so intentionally exposed workflow artifacts share parser and dispatch behavior instead of duplicating argparse code for every model.
