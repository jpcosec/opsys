## Separación de fuentes

**LECTURA PROPIA** (archivos abiertos en esta sesión): `vistas.md`, `fix-diff.txt`, `review-source.md`, TaskDoc `task-corregir-fichas-de-ws09-tras-revisión-root.md`, `ritual.py`, `testing.md`, `execution.md`, `infraestructura.md`, `deskops.md`, `user-flows.md`, `dag.yaml`, `result-summary.md`, `comparison-ledger.md`.

**DATO DEL SUPERVISOR** (`tester-facts.log`, no verificado por mí): HEAD `50f4729a`; revisiones actuales; tablas/tareas/diagrama coinciden con `dag.yaml`; sin cambio de código de producto; `13 passed in 1.36s`; SHA de `vistas.md` `8fda351d…`; 1 de 73 revisiones renovadas; `dag.yaml` 0 líneas fuera de `evidence` e `input_sha256`.

## 1. Diez ítems del diff

| # | Objeto | Evidencia en `fix-diff.txt` / `vistas.md` | Resultado |
|---|---|---|---|
| 1 | F05 Error, Origen y Campos | `vistas.md:125,128,133`; hunk `@@ -122,19 +122,19 @@` | PASS |
| 2 | F16 Error | `vistas.md:337` | PASS |
| 3 | F18a Clase | `vistas.md:373` | PASS |
| 4 | F18b Destino de escritura | `vistas.md:387` | PASS |
| 5 | F12 Acción/dueño y Destino | `vistas.md:267-268` | PASS |
| 6 | F03 Campos y relaciones | `vistas.md:94` | PASS |
| 7 | F12 `Corpus.rank`/`GET /corpus/rank` | `vistas.md:267` | PASS |
| 8 | F12 consulta guardada / `ProjectionDoc` | `vistas.md:262` | PASS |
| 9 | Nota «Candidaturas sin productor» | `vistas.md:445-447` | PASS |
| 10 | Evidencia; Clase solo F18a; Renderer sin cambio | `vistas.md:137,273,341,392`; sin línea de Renderer modificada | PASS |

**Nada más:** el diff solo toca `vistas.md`. Observación menor: en F18a también se modificó `Origen` (`vistas.md:363`), además de `Clase`; el cambio es coherente con la misma corrección, pero el TaskDoc lo enunciaba como «campo Clase».

## 2. Cotejo directo

| Afirmación nueva | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| `RitualDoc.steps` son prosa ordenada, no referencias documentales | `ritual.py` | `ritual.py:11`; `ritual.py:65-67` | PASS |
| Los rituales tienen pasos inline no vacíos | `testing.md`, `execution.md` | `testing.md:5-16`; `execution.md:9-10` y siguientes | PASS |
| Que no existan instancias StepDoc no implica ausencia de pasos | `deskops.md:200` + `ritual.py` | `deskops.md:200` dice «StepDoc … 0»; `ritual.py:65-67` define `steps` | PASS |
| 0 StepDoc solo niega esas instancias | `deskops.md` | `deskops.md:200` | PASS |
| SpecDoc/SpecNodeDoc se materializan desde spec YAML por `diagram sync` | `infraestructura.md:35` | `infraestructura.md:35` | PASS |
| Las 8 notaciones builtin se definen en `s2v/notations/*.yml` | `infraestructura.md:132` | `infraestructura.md:132` | PASS |
| `notation sync` no dice qué escribe; NotationDoc en store no comprobado | `infraestructura.md:100,132` | `infraestructura.md:100` nombra `notation sync`; `:132` lista notaciones y comandos, sin decir qué escribe | PASS |
| Ruta `sldb/views/` prevista, pendiente de confirmación/registro en WS18 | `dag.yaml:1222-1224` | `dag.yaml:1222` «ruta y registro confirmados según el contrato al promover»; `:1223-1224` prefijo no cambia dueño | PASS |
| Repo owner spec2viz; el prefijo no determina el repo | `dag.yaml` | `dag.yaml:1221` `owner_repo: spec2viz`; `:1222-1224` | PASS |
| `atoms validate` llama `ensure_workspace` y puede crear andamiaje y `tag-namespaces.yaml` | `deskops.md:113,266`; `user-flows.md:179` | `deskops.md:113`; `deskops.md:266`; `user-flows.md:179` | PASS |
| `sldb stores check` puede escribir caché/journal, no corroborado | `deskops.md:265`; `user-flows.md:179` | `deskops.md:265` «no se leyo ni ejecuto»; `user-flows.md:179` | PASS |
| `Corpus.rank` y `GET /corpus/rank` existen sin CLI; 409 si falta índice; `difflib`; embedder no comprobado | `infraestructura.md:115` | `infraestructura.md:115` | PASS |
| Consulta guardada con `where` ausente; `ProjectionDoc` es capacidad vecina distinta | `infraestructura.md:121` | `infraestructura.md:121` | PASS |
| «Ningún comando la calcula» acotado a lo auditado | `user-flows.md:101` | `user-flows.md:101` «`deskops.md` no audita un cálculo…» | PASS |
| La nota no crea productor ni nodo; distingue lectura genérica de vista especializada | TaskDoc, scope 9; `review-source.md` | TaskDoc, ítem 9; `review-source.md`, bloque «Decisión root sobre huecos sin productor» | PASS |

## 3. F05 y F16

- No queda la frase «con 0 StepDoc el procedimiento carece de pasos que mostrar» (`vistas.md:133`).
- F16 ya no dice «con 0 StepDoc no hay pasos que mostrar»; dice que 0 StepDoc solo niega esas instancias (`vistas.md:337`).
- No se inventó progreso: F05 mantiene «Progreso de paso: … ninguno está identificado, por eso no definido» (`vistas.md:128`).
- No se inventó autoavance: sigue «no marca pasos como realizados» y «WS23 es solo lectura» (`vistas.md:130-131`).
- No hay referencias nuevas a StepDoc como pasos: las menciones restantes son al modelo/instancias, no a progreso (`vistas.md:125,127,129,133,329,331,333,337,340`).

## 4. F18a y F18b

- F18a ya separa: spec YAML y definición de notación = authored; SpecDoc/SpecNodeDoc = derivado regenerable, no fuente a editar (`vistas.md:373`).
- NotationDoc en store queda como «derivado regenerable desde su definición no comprobado»; la redacción es ambigua, pero conserva «no comprobado» (`vistas.md:373`).
- F18b ya no dice «confirmada por WS18»; dice «prevista, pendiente de confirmación y registro en WS18 al promover… no está confirmada» (`vistas.md:387`).
- No infiere repo por prefijo: «el prefijo de la ruta no determina el repo»; no afirma que `save_view` de graph_ui escriba en spec2viz (`vistas.md:387`).

## 5. F12

- El diagnóstico queda clasificado por efectos, no por ser «diagnóstico» (`vistas.md:267`).
- No se asume que la UI invoque el comando: «No se asume que la UI invoque el comando» (`vistas.md:267`).
- No se crea endpoint ni mecanismo nuevo; se remite a WS12 (`vistas.md:267-268`).
- No se promete semántica: «WS14 admite capacidad parcial o degradada; no se promete semántica» (`vistas.md:267`).

## 6. Resto de fichas

- **F18a:** corregido; no queda SpecDoc/SpecNodeDoc como authored.
- **F15:** conserva «con 0 documentos no hay orientación que mostrar» (`vistas.md:320`). Es una negación por conteo del mismo tipo, fuera de la lista cerrada y anterior al diff. Contradice parcialmente la nota nueva de que la lectura básica de FAQ reutiliza el lector Markdown (`vistas.md:447`). Observación no bloqueante para los diez ítems.
- **F14:** «sin issues, la lista queda vacía» (`vistas.md:303`) es fáctico: `desk/issues` no existe y `desk/drawer/issues` está vacío.
- **F11a:** «ningún comando de deskops los crea o edita» (`vistas.md:229`) está sostenido por la auditoría: RoleDoc y RuntimeProfileDoc sin comando de creación/edición.
- **Hechos futuros:** F18b corregido. F15 usa presente «WS40 crea…» (`vistas.md:321`), pero dentro de `Estado` como plan de nodo; no lo presenta como hecho actual.
- **Materializados llamados authored:** no encontré otro caso fuera de F18a.

## 7. Candidaturas

- La nota no crea productor, nodo ni compromiso: «No son prerrequisito… no capacidades comprometidas… No crean nodos nuevos» (`vistas.md:447`).
- Distingue lectura genérica de vista especializada: «La lectura básica de FAQ, issues y roles reutiliza el lector Markdown o modelado» frente a navegación de FAQ, lista de issues, renderer de roles y vista Specs embebida (`vistas.md:447`).
- PASS.

## 8. Estados y alcance del resumen/ledger

- Siguen 23 fichas `### F` y las 23 conservan `Estado: bloqueado`; ninguna línea `Estado` aparece en el diff.
- Se mantienen los 14 campos por ficha; la única adición es la sección final de candidaturas.
- `result-summary.md` declara no haber ejecutado commits, closeout, revisiones, build, validate ni suite: coherente con su rol de Executor.
- `comparison-ledger.md` atribuye congelación/status/revisiones al Supervisor; `tester-facts.log` corrobora parcialmente («all reviews current», 1 de 73). No pude reconciliar el hash `ded2e9b6` del ledger con HEAD `50f4729a` del dato del supervisor.

## No pude verificar

- No ejecuté `git diff`, `git status`, build, validate, helper, suite ni revisiones; solo leí archivos.
- No abrí el nodo WS14 del DAG: la frase «WS14 admite capacidad parcial o degradada» la tomo de `review-source.md`.
- No leí el FAQ empaquetado ni `docs/faq.md` (no existe en el repo); por eso F15 queda como observación.
- No verifiqué el bundle, los 73 inputs, los SHA de receipts ni el estado de los 4 archivos sucios ajenos.
- No pude comprobar qué escribe exactamente `notation sync`; las líneas citadas no lo dicen.

RESULTADO: PASS
