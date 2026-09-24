---
id: atom-sldb-template-markers-declare-where-each-field-lives
title: SLDB template markers declare where each field lives
five_wh_one_plus: what
tags:
- system:sldb
- topic:templates
---

# SLDB template markers declare where each field lives

## Answer

A model's __template__ places a marker for every field it renders and extracts: ⸢rev•field⸥ for a required scalar, ⸢optrev•field⸥ for an optional one, ⸢rev,list•field⸥ and ⸢rev,dict•field⸥ for collections, and ⸢render•field⸥ for a composed projection that is written but never extracted. An optional field whose value is None leaves no trace at all in the render, so extraction returns it absent and the model supplies the default.
