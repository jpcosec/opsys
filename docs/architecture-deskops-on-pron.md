# Arquitectura: deskops sobre pron

Fuentes de verdad de esta arquitectura (spec2viz, validados y linteados):

- `docs/diagrams/deskops-pron-component.yml` → `.mmd` — las capas.
- `docs/diagrams/deskops-pron-sequence.yml` → `.mmd` — un movimiento completo.

```bash
cd docs/diagrams
python -m spec2viz.cli diagram validate deskops-pron-component.yml
python -m spec2viz.cli diagram render  deskops-pron-component.yml --renderer mermaid --out .
python -m spec2viz.cli diagram lint    deskops-pron-component.mmd
```

## El giro respecto del plan anterior

El plan previo trataba a pron como una librería de CRUD: `Store.create`,
`Store.update_field`, `Store.track`. Eso desperdicia lo que pron realmente es.

pron admite **dos entradas al mismo nivel** (spec 13): lenguaje natural y
**formas** (s-expressions). La superficie de lenguaje natural convierte una
oración en formas y no hace nada más; un runtime que ya sabe lo que quiere
—como deskops— **escribe las formas directamente**. Las dos entradas terminan
en la misma evaluación.

deskops es exactamente el caso que la spec 13 describe para `graph_ui`: ya
tiene los dos extremos de cada operación (sabe qué task, qué pill, qué campo),
así que no necesita parsear nada. Emite formas.

## Qué gana deskops al entrar por formas y no por CRUD

Escribiendo con `Store.create`/`update_field` deskops obtiene persistencia y
nada más. Entrando por `Session.eval(formas)` obtiene, sin escribir código:

| capacidad | qué significa para deskops |
|---|---|
| prevalidación | el movimiento entero se simula antes de tocar el store; si una parte falla, no se escribe nada. Hoy `operations.py` hace esto a mano con `_rollback` y `_remove_created_file`. |
| movimiento atómico | `(move ...)` agrupa varias partes en una escritura y un refresh. Un `create_task_bundle` (task + checklists + conditions + operators + edges) es **un** movimiento, no N escrituras con rollback casero. |
| ledger | cada movimiento deja un `MoveDoc` con la forma dicha, la forma resuelta, y el `hash_mundo` antes y después. Esto es la traza de auditoría del workflow, gratis. |
| `undo` | deshacer un movimiento es una primitiva de pron, no código de deskops. |
| `why` | "¿por qué este task está así?" se contesta desde el ledger. |
| refresh del grafo | kgdb se reconstruye como parte del movimiento, no como un paso que deskops deba recordar. |
| reproducibilidad | `record["resolved"]` re-evaluado sobre el mismo mundo deja las mismas escrituras. Un test de deskops puede afirmar sobre formas, no sobre archivos. |

Esto convierte a deskops en lo que dice ser en `AGENTS.md` —un harness de
workflow— y deja **toda** la capa de datos en pron.

## Las tres rutas de entrada

```
CLI de deskops ──▶ capa de formas ──▶ eval ──┐
alias de deskops (documentos del mundo) ─────┼──▶ resolver · prevalidar · ejecutar · refrescar · registrar
oracion en lenguaje natural (opcional) ──────┘
```

La tercera ruta sale gratis: una vez que el mundo declara los modelos y los
tipos de relación de deskops, `pron say "which tasks are blocked?"` funciona
sobre el desk sin que deskops escriba una línea. Es un efecto secundario de la
arquitectura, no un objetivo.

## Capas (ver diagrama de componentes)

1. **CLI de deskops** — verbos preservados 1:1. Solo traduce argumentos a una
   intención. Sin lógica de persistencia.
2. **Capa de formas** (nueva, el corazón del refactor) — constructores que
   arman s-expressions por operación de workflow. Es el reemplazo real de
   `operations.py`: donde hoy hay 2.765 líneas de orquestación de escrituras,
   queda la construcción de una forma.
3. **Alias de deskops** — las operaciones compuestas y estables del workflow
   (promote, bind, advance, closeout) se declaran como **alias en documentos
   del mundo** (spec 05), no como código. Un alias nombra una forma compuesta.
   Consecuencia: el vocabulario del workflow deja de ser código y pasa a ser
   dato — coherente con "docs son materializaciones de átomos".
4. **pron `Session.eval`** — resolver, prevalidar, ejecutar, refrescar,
   registrar. Todo lo que deskops hoy hace a mano.
5. **Lecturas** — `World.store` (`find`, `matches`, `payload`) y `World.graph`
   (`children`, `descendants`, `neighbors_via`) para board, `next`, `list`,
   `show`. Las lecturas no necesitan pasar por formas salvo que se quiera
   dejarlas en el ledger.
6. **Modelos** — `deskops/models/` es lo único que se conserva del código
   actual, más mejoras conservadoras.

## Qué sobrevive del deskops actual

| componente | destino |
|---|---|
| `deskops/models/` | **se conserva** (+ mejoras conservadoras) |
| `cli/parser.py` | se conserva la superficie de verbos; los handlers se vacían |
| `operations.py` (2.765 líneas) | **desaparece** — se vuelve constructores de formas + alias |
| `workspace.py`, `identity.py`, `domain_tree.py` | se vuelven lecturas de `World` |
| `bootstrap.py` | `World.ensure_ready` + init de tipos de relación |
| `graph/` extractores | a revisar: si el grafo lo refresca pron, gran parte sobra |
| `materializers/` | render vía el seam; la lógica se conserva |
| tests | contrato de comportamiento; se conservan y se extienden con asserts sobre formas |

## Preguntas abiertas (bloquean el corte en tareas)

1. ¿Las lecturas pasan por formas (quedan en el ledger) o van directo a
   `World.store`? Propuesta: directo, salvo `why`/auditoría.
2. ¿Los tipos de relación del workflow (`binds`, `depends_on`, `blocks`,
   `graduates_to`) se declaran como `RelationTypeDoc`? Propuesta: sí — es lo
   que habilita `pron say` sobre el desk y el refresh automático.
3. ¿`desk/` sigue siendo archivos Markdown trackeados, o pasa a ser
   exclusivamente documentos del store? Impacta cuánto de `graph/` sobrevive.
4. ¿El ledger de pron reemplaza el `runs/` actual de deskops?
