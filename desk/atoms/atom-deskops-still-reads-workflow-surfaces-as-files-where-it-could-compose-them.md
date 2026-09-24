---
id: atom-deskops-still-reads-workflow-surfaces-as-files-where-it-could-compose-them
title: Deskops still reads workflow surfaces as files where it could compose them
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:composition
---

# Deskops still reads workflow surfaces as files where it could compose them

## Answer

Too many structured workflow surfaces are still read as Markdown to be parsed by hand instead of as modeled documents to be queried and composed through sldb. The consequence shows up as documentation that grows to compensate for weak semantic access: prose where a query would do, and frontmatter that becomes reading noise because nothing queries it. The write path now goes through sldb (tracked documents are rewritten through it and the store stays consistent), but the read path in the graph extractors and several CLI surfaces still walks files.
