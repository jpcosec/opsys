# Taxonomía de documentos de deskops

Extraída de los modelos, no de memoria: 23 clases en `deskops/models/`, sus
campos declarados, sus `__containment__` y sus `__references__`.

Diagrama: `docs/diagrams/deskops-pron-taxonomy.yml`.

Reproducir el inventario:

```bash
python -c "
import importlib, inspect, pkgutil
import deskops.models as M
from sldb import StructuredNLDoc
for _,n,_ in pkgutil.iter_modules(M.__path__):
    mod = importlib.import_module(f'deskops.models.{n}')
    ..."
```

## Jerarquía de clases

Tres raíces, no una:

```
StructuredNLDoc  (sldb)
├── PrimitiveDoc                    title, id, status, summary, tags
│   ├── OperationalArtifactDoc      + routine, current_node, history
│   │   ├── TaskDoc
│   │   ├── BoardDoc
│   │   ├── PillDoc
│   │   └── RitualDoc
│   ├── ChecklistDoc
│   ├── ConditionDoc
│   ├── OperatorDoc
│   ├── EdgeDoc
│   ├── HookDoc
│   ├── RoutineDoc
│   └── RuntimeProfileDoc
└── (directos, sin primitiva)
    ├── AtomDoc, ProtoAtomDoc, CrossroadDoc, MaterializationContractDoc
    ├── StepDoc, RoleDoc, RunDoc, RepositoryDoc
    ├── InboxNoteDoc, FAQDoc
```

`OperationalArtifactDoc` es lo que hace a un documento **movible por el
workflow**: aporta `routine`, `current_node`, `history`. Solo cuatro clases lo
heredan. Ese es el eje real de la taxonomía, y está bien elegido.

## Los cinco grupos

### 1. Conocimiento — lo durable

| doc | campos propios | docs |
|---|---|---|
| `AtomDoc` | `five_wh_one_plus`, `answer`, `provenance` | **95** |
| `ProtoAtomDoc` | `content`, `typed_as`, `provenance` | 0 |
| `CrossroadDoc` | `path`, `content` | 1 |
| `MaterializationContractDoc` | `source_atoms`, `target_kind`, `target_identity`, `intent`, `validation`, `provenance` | — |

Es el grupo con masa real. No tiene `routine`: el conocimiento no se mueve por
gates, se acumula.

### 2. Trabajo — lo que se mueve por el board

| doc | campos propios | docs |
|---|---|---|
| `TaskDoc` | `why`, `goal`, `scope`, `references`, `depends_on`, `pills`, `files`, `checklists`, `implementation_path`, `validation`, `done_when`, `task_type`, `inherits_from`, `atoms`, `from_drawer` | 1 |
| `BoardDoc` | `scope`, `purpose`, `tasks`, `pills`, `rituals`, `notes` | — |
| `PillDoc` | `what`, `why`, `when`, `where`, `how`, `how_not` | — |
| `InboxNoteDoc` | `kind`, `sender_project`, `target_project`, `created_at`, `acknowledged_by`, `body` | — |

`TaskDoc` tiene 20 campos propios. Es el documento más cargado del sistema y el
candidato obvio a revisión.

### 3. Procedimiento — cómo se hace

| doc | campos propios | docs |
|---|---|---|
| `RitualDoc` | `purpose`, `trigger`, `preconditions`, `steps`, `validation`, `failure_modes`, `completion` | — |
| `StepDoc` | `action`, `outcome` | — |
| `RoutineDoc` | `entrypoint`, `decomposition`, `edges`, `terminal_nodes` | 1 |

### 4. Maquinaria — las primitivas que pron absorbe

| doc | campos propios | docs |
|---|---|---|
| `ConditionDoc` | `subject`, `predicate`, `expected` | 5 |
| `OperatorDoc` | `action`, `target`, `value` | 3 |
| `EdgeDoc` | `source`, `target`, `condition_ref` | 6 |
| `HookDoc` | `event`, `target`, `condition_ref` | 0 |
| `ChecklistDoc` | `items`, `condition_refs`, `mode` | 3 |

17 documentos en total sosteniendo una máquina de estados escrita a mano.

### 5. Entorno — quién y dónde ejecuta

| doc | campos propios | docs |
|---|---|---|
| `RoleDoc` | `model`, `tools`, `system_prompt_mode`, `inherit_skills`, `default_context`… | 3 |
| `RuntimeProfileDoc` | `binary`, `model_flag`, `tools_flag`, `session_flag`… | 2 |
| `RunDoc` | `task_id`, `role_id`, `herdr_pane_id`, `session_sha256`, `outcome`, `commit_sha` | 0 |
| `RepositoryDoc` | `name`, `path`, `description` | 14 |

## Cómo se agrupan: contención vs referencia

**Contención** (`__containment__`) — el hijo vive dentro del padre:

```
BoardDoc     ──▶ TaskDoc, PillDoc, RitualDoc
TaskDoc      ──▶ ChecklistDoc, PillDoc, AtomDoc
RitualDoc    ──▶ StepDoc
RoutineDoc   ──▶ ChecklistDoc, ConditionDoc, OperatorDoc, PrimitiveDoc, StepDoc · EdgeDoc
ChecklistDoc ──▶ ConditionDoc
```

**Referencia** (`__references__`) — apunta sin contener:

```
TaskDoc   ──▶ references, depends_on, inherits_from, from_drawer
EdgeDoc   ──▶ source, target, condition_ref
HookDoc   ──▶ target, condition_ref
RoutineDoc──▶ entrypoint, terminal_nodes
RunDoc    ──▶ task_id, role_id
```

## Hallazgos del inventario

1. **Solo 13 de 23 modelos están registrados en el store.** No están:
   `BoardDoc`, `PillDoc`, `RitualDoc`, `StepDoc`, `InboxNoteDoc`, `FAQDoc`,
   `HookDoc`, `MaterializationContractDoc`, `PrimitiveDoc`,
   `OperationalArtifactDoc`. Pills y rituals son centrales al workflow y viven
   como Markdown suelto fuera del store. Eso explica por qué `graph/` tiene
   extractores propios: está supliendo documentos no trackeados.

2. **`RoutineDoc.decomposition` contiene `PrimitiveDoc`**, que es la clase base
   abstracta. Una contención a la raíz de la jerarquía no restringe nada.

3. **`ProtoAtomDoc`, `RunDoc`, `HookDoc` tienen 0 documentos.** Modelos
   declarados sin uso: o se estrenan en la migración, o se borran.

4. **`AtomDoc` no hereda de `PrimitiveDoc`** pese a tener `title`, `id`,
   `status`, `tags`. Duplica la base por fuera de la jerarquía.

5. **`current_node` + `history` en `OperationalArtifactDoc`** es exactamente lo
   que el ledger de pron (`MoveDoc`) mantiene solo. Candidatos a desaparecer.

## Preguntas abiertas

1. ¿Los 10 modelos no registrados entran al store en la migración? Si pills y
   rituals entran, buena parte de `graph/` sobra.
2. ¿`AtomDoc` baja a heredar de `PrimitiveDoc`, o la duplicación es
   deliberada?
3. ¿`ProtoAtomDoc`, `RunDoc`, `HookDoc` se estrenan o se borran?
4. ¿`TaskDoc` con 20 campos se parte, o se queda como está?
