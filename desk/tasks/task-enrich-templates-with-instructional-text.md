---
id: task-enrich-templates-with-instructional-text
status: draft
references:
- desk/contexts/pill-sldb-template-markers.md
- desk/contexts/pill-template-instructional-text.md
tags:
- system:deskops
- topic:templates
- topic:documentation
---

# Enrich all deskops model templates with instructional fixed text

## Goal

Que cada `__template__` en los modelos de deskops contenga texto fijo instructivo que:
- Guíe a quien escribe el documento sobre qué poner en cada campo
- Sirva de anclaje para SLDB al extraer datos (más robusto que texto vacío)
- Haga que un documento nuevo renderizado sea útil como punto de partida

## Scope

### In scope

- Todos los modelos en `deskops/models/*.py`
- Solo texto instructivo **fijo** (el que aparece igual en todos los documentos del tipo)
- No incluye implementación de `⸢rev,table•⸥` (es issue separado en SLDB)

### Out of scope

- Cambios al motor de templates SLDB
- Agregar/quitar campos de los modelos
- `⸢rev,table•⸥` marker

## Current state

Los templates actuales son esqueletos mínimos. Por ejemplo `TaskDoc.__template__`:

```python
__template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
---

# ⸢rev•title⸥

## Goal

⸢rev•goal⸥
"""
```

No hay texto que explique qué va en cada campo al crear un documento nuevo.

## Target state

Cada template debe incluir texto instructivo corto al lado de los marcadores. Ejemplo:

```python
__template__ = """---
id: ⸢rev•id⸥            # task-xxx, único por tarea
status: ⸢rev•status⸥      # draft | active | blocked | closed
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Goal

_Resultado concreto que debe producir esta tarea._

⸢rev•goal⸥

## Scope

_Qué está dentro y fuera del alcance._

⸢rev•scope⸥

## Validation

_Criterios que debe cumplir antes de cerrarse._

- ⸢rev,list•validation⸥
"""
```

## Models to update

- `deskops/models/atom.py` — AtomDoc
- `deskops/models/task.py` — TaskDoc
- `deskops/models/board.py` — BoardDoc
- `deskops/models/pill.py` — PillDoc
- `deskops/models/ritual.py` — RitualDoc
- `deskops/models/step.py` — StepDoc
- `deskops/models/routine.py` — RoutineDoc
- `deskops/models/repository.py` — RepositoryDoc
- `deskops/models/operator.py` — OperatorDoc
- `deskops/models/hook.py` — HookDoc
- `deskops/models/condition.py` — ConditionDoc
- `deskops/models/checklist.py` — ChecklistDoc
- `deskops/models/edge.py` — EdgeDoc
- `deskops/models/inbox.py` — InboxNoteDoc
- `deskops/models/faq.py` — FAQDoc

## Validation

- `⸢rev•⸥` markers siguen presentes y funcionales
- Tests de roundtrip pasan (extract → render → extract)
- Un documento nuevo renderizado se entiende sin contexto externo
- El texto instructivo no interfiere con la extracción (SLDB lo ignora al parsear)

## Pills

- `pill-sldb-template-markers.md` — cómo funcionan los marcadores
- `pill-template-instructional-text.md` — cómo escribir buen texto instructivo
