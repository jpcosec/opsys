# Round 03 — Model layer and sldb state

**Source:** ST-models

## Model hierarchy

```
StructuredNLDoc (sldb)
├── AtomDoc, FAQDoc, InboxNoteDoc, RepositoryDoc, StepDoc
└── PrimitiveDoc (desk.models.base)
    ├── ChecklistDoc, ConditionDoc, EdgeDoc, HookDoc, OperatorDoc, RoutineDoc
    └── OperationalArtifactDoc
        ├── BoardDoc, PillDoc, RitualDoc, TaskDoc
```

17 clases de modelo, 3 niveles de herencia, todos con Pydantic v2. **Estructuralmente sano.**

## sldb store state

- **core/store_index.yaml**: Solo `AtomDoc` registrado como modelo
- **models/AtomDoc.yaml**: Descriptor completo del modelo
- **documents/AtomDoc.yaml**: 15+ AtomDoc entries indexados
- **runtime/**: knowledge_graph.kg.json (216KB) + knowledge_graph.nx.json (351KB)
- **.config/**: Ausente (no es problema)
- **Solo AtomDoc está persistido** — ningún otro modelo tiene documentos en store todavía

## Spec-driven CLI generation

El parser en `desk.cli.parser.build_parser()` genera dinámicamente los 15 subcomandos de `add`/`list`/`show` desde el spec registry. Cada `add` expone flags derivados de spec (`--title`, `--goal`, `--what`, `--why`, etc.). **El mecanismo funciona.**

## Runtime classes

9 clases runtime que reflejan el model layer: `Task`, `Routine`, `Condition`, `Checklist`, `Edge`, `Hook`, `Operator`, `TransitionResult`, `Primitive`. Mismo patrón de 3 niveles.

## Issues encontrados

1. `DeskopsOperations.__init__` frágil con tipos — espera `Path` pero `root.resolve()` falla si recibe `str`
2. `__fields__` usado en vez de `model_fields` — deprecated en Pydantic v2, rompe en v3
3. Solo `AtomDoc` persiste en store — los demás modelos existen como clases pero no están registrados
