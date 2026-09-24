---
id: atom-sldb-extraction-reads-values-relative-to-the-template-s-own-text
title: SLDB extraction reads values relative to the template's own text
five_wh_one_plus: how
tags:
- system:sldb
- topic:templates
---

# SLDB extraction reads values relative to the template's own text

## Answer

TemplateExtractor turns the template into recipes that pair each marker with the text around it, and DataExtractor uses those recipes to read a document. A document that carries a section but not the template's fixed text therefore extracts as empty for that field: the reader is looking for an anchor the file does not have. Reading such a document looks fine and writing it back renders the empty payload, which is how an edit can blank content it was only supposed to touch.
