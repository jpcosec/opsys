---
# pill-xxx
id: pill-sldb-template-markers
# e.g., language:python, library:pydantic
tags:
- workspace:desk
---

# SLDB template markers

## What

_Define the context or guardrail this pill carries._

SLDB usa marcadores dentro del `__template__` de un modelo para definir dónde va cada campo en el markdown. Hay tres tipos:
### `⸢rev•fieldname⸥`
Valor **scalar**. Se reemplaza por el valor del campo al renderizar, y se extrae del mismo lugar al leer. Usado en frontmatter y body:
```yaml
id: ⸢rev•id⸥
status: ⸢rev•status⸥
```
```markdown

## Why

_Explain why this context matters for safe execution._



## When

_Describe when an agent should apply this pill._



## Where

_Name the files, surfaces, or scope this pill applies to._

Los templates se definen en `__template__` como strings multilínea en cada modelo Pydantic bajo `deskops/models/*.py`.

## How

_Describe the correct way to apply this guidance._

`TemplateExtractor` parsea el template y registra recipes (marcador → posición/contexto). `DataExtractor` usa esos recipes para leer el documento real. `SLDBRenderer` usa los mismos recipes para escribir.

## How Not

_Describe the shortcut or failure mode to avoid._