# Workflow de deskops sobre pron

Complementa `architecture-deskops-on-pron.md`, que definió las capas. Esto es
el workflow, que es lo que realmente se migra.

Diagramas (validados y linteados):

- `docs/diagrams/deskops-pron-workflow-state.yml` — ciclo de vida de una task.
- `docs/diagrams/deskops-pron-primitives.yml` — las primitivas como documentos.

## Corrección al documento anterior

El diagrama de secuencia anterior usaba `bind pill → task` como ejemplo. Fue
una mala elección: `bind` es una arista suelta, no el workflow. El workflow de
deskops es una **máquina de estados declarativa** que ya existe en
`desk/primitives/`, y ese es el objeto de la migración.

## Lo que deskops ya tiene y yo no había mirado

`desk/primitives/` no es decoración: es un intérprete de workflow guardado
como documentos.

| primitiva | campos | qué es |
|---|---|---|
| `ConditionDoc` | `subject`, `predicate`, `expected` | predicado evaluable sobre un campo del doc |
| `ChecklistDoc` | `condition_refs`, `mode` (all/any) | conjunción o disyunción de condiciones |
| `OperatorDoc` | `action`, `target`, `value` | efecto (`set_field status active`) |
| `EdgeDoc` | `source`, `target`, `condition_ref` | transición con guarda |
| `HookDoc` | `event`, `target`, `condition_ref` | efecto disparado por evento (`on_complete`) |
| `RoutineDoc` | agrupa lo anterior | la máquina de un tipo de task |
| `RitualDoc` | `steps[]` | el procedimiento humano (execution, testing, closeout, phase) |

Esto mapea **uno a uno** contra lo que pron ya evalúa: `sexpr/resolving/`
tiene `condition_check.py`, `state_machine.py`, `relation_checks.py`,
`edge_assertion.py`. deskops reimplementó en Python lo que pron evalúa como
formas.

## La decisión: specyaml, no graph_ui

Miré `graph_ui` (`tools/graph_ui`): es un editor visual de cualquier store
pron/sldb, con vista de Schema (clases, contenciones, referencias) y edición
de contratos de clase.

- **Para declarar los modelos**: specyaml. La declaración tiene que ser
  revisable en diff, versionable y ejecutable en CI. Un editor visual no deja
  rastro de por qué cambió un contrato.
- **graph_ui entra después**, como superficie de inspección y edición del desk
  ya migrado. Es el argumento fuerte de la arquitectura: una vez que el desk es
  un mundo pron, graph_ui funciona sobre él **sin escribir una línea** —
  igual que `pron say`. Tres superficies sobre las mismas formas (spec 13).

## Qué falta en mi plan — inventario honesto

Automatizaciones de deskops que no había considerado:

| automatización | qué hace | destino en pron |
|---|---|---|
| `deskops next` | próxima acción desde el estado actual del task, contra `spec/workflows/task_lifecycle.yaml` | lectura de estado + `RitualDoc.steps`; el ledger da el estado real |
| `deskops next --diagram` | renderiza la máquina de estados como Mermaid desde su spec | se conserva; ahora la fuente es el mundo, no un YAML aparte |
| `deskops advance task` | avanza gates corriendo checklists/conditions/operators | **esto es `eval` de formas**: transiciones con guarda, ya en pron |
| `deskops drift check` | detecta deriva entre RoleDoc y agentes materializados | se conserva; compara payloads vía `World.store` |
| `deskops graph missing` | referencias colgantes en el grafo | `World.graph` + `graph missing` |
| `deskops graph self-reflection` | hallazgos sobre el propio repo, con decisiones persistidas | se conserva; la fuente pasa a ser el grafo refrescado por pron |
| `deskops materialize` | genera roles/runtime profiles desde docs | se conserva; render vía el seam |
| `deskops closeout` | verifica evidencia, untrack, quita del board, commit atómico | alias compuesto + hooks `on_complete` |
| `deskops doctor` | salud del store y del desk | `World` + checks semánticos |
| `deskops repo` | registro de repos para rutas cross-repo | stores enlazados de pron (`World` ya los soporta) |
| auto-commit de cierre | commit atómico como gate final | hook `on_complete`; el ledger da la evidencia |
| board pills / routing | qué pills aplican a qué task | aristas tipadas + `neighbors_via` |

## Lo que el ledger reemplaza

`runs/` y la evidencia de closeout hoy se arman a mano
(`_has_verified_task_closeout_evidence`, `_closeout_reference_evidence`). El
`MoveDoc` de pron ya guarda qué se leyó, qué se escribió y el hash del mundo
antes y después de cada movimiento. La verificación de closeout pasa de
heurística sobre archivos a consulta sobre el ledger.

## Preguntas que siguen abiertas

1. ¿Las conditions de deskops (`subject`/`predicate`/`expected`) se traducen a
   predicados `where` de sldb, o se declaran como condiciones de arista de
   kgdb? Determina si `ConditionDoc` sobrevive como modelo.
2. ¿`RoutineDoc` se vuelve un conjunto de `RelationTypeDoc` con transiciones, o
   sigue siendo un documento que deskops interpreta?
3. ¿`spec/workflows/task_lifecycle.yaml` se declara en el mundo, o sigue siendo
   un YAML fuera del store? Si entra al mundo, `next` sale gratis.
4. ¿Los hooks (`on_complete`) los dispara pron o deskops?
