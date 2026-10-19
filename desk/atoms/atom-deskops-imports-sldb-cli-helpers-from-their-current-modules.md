---
id: atom-deskops-imports-sldb-cli-helpers-from-their-current-modules
title: Deskops imports sldb CLI helpers from their current modules
five_wh_one_plus: what
tags: []
---

# Deskops imports sldb CLI helpers from their current modules

## Answer

Deskops depends on sldb CLI helper API (get_store_context in sldb.cli.store_context; registered_model/resolve_model_ref in sldb.cli.model_utils); when sldb relocates helpers, deskops must repoint imports rather than pin stale paths. TaskDoc declares its frontmatter fields explicitly and has no frontmatter dict or render_payload override; the sldb renderer invokes render_payload internally.
