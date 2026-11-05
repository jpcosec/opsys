FILE:desk/drawer/plans/gates-por-tipo/context-review-guide.md
# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. Ningún nodo tiene ejecución autorizada.
- ROOT y PC son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional, no un defecto. Los gates `G_SLDB_*` los produce otro repo (sldb, plan `grafo-operable`, rev 9); lo que ese plan fija es contrato suministrado, no ambigüedad de este nodo.
- Las decisiones D2, D3, D4, D9 y D10 están tomadas por el dueño; las DC1–DC7 son propuestas de este plan y se leen como dadas. Los pendientes del dueño en decisiones.md no son ambigüedad del nodo salvo que el nodo dependa de uno sin decir qué hace mientras tanto.
- Los bloques `edge` son contratos de vecinos; no los revises.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance (en particular: escribir en sldb, o suplir con Python una regla que sldb debería evaluar).

No cuentan: nombres exactos de archivos, funciones o tests que el TaskDoc fijará al promover; contratos que produce una dependencia nombrada (un nodo GO de sldb o un GC de este plan); trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/gates-por-tipo/brief.md
# Brief: gates por tipo de tarea en deskops

Fecha: 2026-11-04. Repo dueño: deskops. Estado: plan en drawer, ninguna tarea activa, `execution_authorized: false`. Lado consumidor del plan `grafo-operable` de sldb (`sldb/desk/drawer/plans/grafo-operable/`, dag.yaml rev 9); produce su gate externo `G_CONSUMER`.

## Encargo

Que los gates del ciclo de vida de una tarea de deskops sean documentos que sldb evalúa, no hechos calculados en Python y escritos en el payload: los tipos de tarea como modelos con jerarquía que declaran sus gates de activación y su evidencia de cierre; los recibos de revisión como documentos `ReviewDoc` atados al hash de contrato de la tarea; el gate de activación como `RuleDoc`; los efectos de cada transición en la arista; y el cierre de las dos vías que hoy saltan los gates (`advance --to`, `edit task status`). Un comando `deskops review` reemplaza a los dos scripts de revisión en frío que viven en el drawer.

## Por qué ahora

- El dueño decidió el 2026-11-04 (sldb `decisiones.md` D2) que los gates de activación son bloqueo duro sin bandera de salto y que la vía de escape es especializar tipos de tarea (`task.refactor` ≠ `task.debug`), cada tipo con sus gates. Hoy `task_type` es un string libre (`deskops/models/task.py:144-147`) que solo rellena la evidencia de cierre desde un diccionario plano (`deskops/services/closeout_gates.py:30-38`); no hay dónde colgar un gate por tipo.
- El gate de activación `task_activates` tiene condición vacía (`deskops/spec/workflows/task_lifecycle.yaml:26`): toda tarea se activa. El ritual de ejecución exige preflight y cold-bundle antes de despachar (`desk/rituals/execution.md`, pasos 5 a 9), pero nada lo comprueba.
- `advance --to` escribe `status` o `current_node` sin evaluar ninguna condición (`deskops/services/tasks.py:179-192`) y `edit task` acepta cualquier campo salvo `id` (`deskops/operations.py:271-282`). Las dos contradicen D2.
- sldb va a entregar `RuleDoc`, anclas `doc:` con hash de contrato, `edges_holding` con `effects` y `findings`, y `edges_blocked`. Sin un plan consumidor escrito, su gate `G_CONSUMER` no tiene quién lo produzca (sldb `dag.yaml` rev 9, `gates.G_CONSUMER` y `external_references.deskops_consumer_plan: not_written`).
- Las revisiones en frío se corren con scripts copiados de plan en plan (`desk/drawer/plans/workspace-documental/context_review.py`; `sldb/desk/drawer/plans/grafo-operable/context_review.py`). El dueño pidió que el segundo quedara gobernado; el paso siguiente es un comando.

## Resultado esperado del plan completo

1. Tipos de tarea como modelos sldb con herencia (`base_models`): `TaskDoc` es la base y cada tipo es una subclase registrada en el store del desk, de modo que `model <= TaskCodeDoc` nombra a la familia. `task_type` deja de ser libre: es el nombre del tipo y debe existir como modelo registrado. Un desk agrega tipos propios.
2. Cada tipo declara su evidencia de cierre (hoy `TASK_TYPE_EVIDENCE`) y sus gates de activación (RuleDocs `on_transition` por familia).
3. `ReviewDoc`: recibo de una revisión en frío (preflight, cold-bundle) o de otra prueba externa (reproducción, goldens, recibo del dueño), con `subject` anclado al hash de contrato de la tarea (`__doc_anchors__: [subject]`), `verdict` escrito por quien opera el desk, actor, engine y directorio de la corrida.
4. El gate de activación es una `RuleDoc` por tipo que exige recibos intactos y aceptados y dependencias cerradas (`all(depends_on: status = "closed")`); `advance` explica un bloqueo con los `findings` de `edges_blocked`.
5. `sets_status` y `terminal` viven en `RelationDoc.attributes` (sldb GO09); el YAML deja de ser segunda fuente; `advance` usa `edges_holding` y `apply_effects`.
6. `advance --to` desaparece; `edit task` rechaza `status`, `current_node`, `task_type`, `closeout_evidence` e `history`. `blocked` pasa a ser un estado derivado (la regla que no se cumple), no un `status` guardado.
7. `deskops review`: modos `node`, `preflight`, `bundle`, `status`, `dispose`; motor por defecto pi deepseek-flash (sldb D4), después una plantilla de Scion; evidencia en `runs/` como pide el ritual y además un `ReviewDoc` en el desk.
8. Composición real: `parent_id`, `children` y `depends_on` con efecto, tipo `task.aggregate`, promoción nodo a nodo desde un `dag.yaml` del drawer, y `deskops graph` leyendo las aristas de sldb.

## Tipos de tarea (tabla normativa)

Los tipos que deskops trae de fábrica. Un desk puede agregar subtipos (p. ej. `task.code.cli`) heredando de uno de estos; hereda sus gates y puede sumar, nunca quitar. `commit` significa un commit alcanzable desde HEAD; `atom|materialization` es un solo gate con dos alternativas (`closeout_gates.py:21-23`).

| Tipo | Hereda de | Gates de activación (`ReviewDoc` intactos y `accepted` sobre el contrato vigente) | Evidencia de cierre (verificada por deskops al cerrar) |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle`; `depends_on` cerradas | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight`; `depends_on` cerradas | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` (en lugar de `bundle`); `depends_on` cerradas | `tests` + `commit` + `atom\|materialization` (las mismas que `task.code`, sin ser su subtipo: un subtipo solo suma gates) |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` (capturados antes); `depends_on` cerradas | las de `task.code` + `goldens` (los mismos goldens verdes después) |
| `task.decision` | `TaskDoc` | ningún recibo de revisión; `owner` (recibo del dueño); `depends_on` cerradas | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | nunca ejecuta: activa solo cuando todos sus `children` están cerrados | `children` (cada hijo con su commit de closeout) + `commit` |
| `task.external` | `TaskDoc` | `preflight`; `depends_on` cerradas | `external` (URL) |

`task.external` conserva el vocabulario `external` que ya existe (`closeout_gates.py:37`). Los strings de hoy migran así: `code`, `implementation`, `test` → `task.code`; `docs`, `spec`, `design` → `task.docs`; `external` → `task.external`; vacío → `task.code` (es como hoy se gatea una tarea sin tipo, `operations.py:580-588`).

## El límite (lo que este plan no promete)

- **No reimplementa el evaluador.** Toda condición se escribe en el lenguaje de sldb y la evalúa sldb. Si una regla no se puede expresar con lo que rev 9 fija, el nodo registra la hipótesis en su TaskDoc y no escribe Python que la supla (sldb `alcance.md`, regla 6).
- **No autentica.** Un `ReviewDoc` dice qué actor o engine lo produjo; probarlo es cosa de git y de Scion (sldb D7).
- **Los hechos externos siguen siendo de deskops.** Que un commit esté en HEAD, que un test exista o que una URL sea alcanzable lo verifica deskops al cerrar, como hoy (`closeout_gates.py:156-229`); lo que cambia es dónde se declara qué exige cada tipo. Convertir ese resultado en un recibo es un paso posterior, fuera de este plan.
- **No toca sldb.** Lo que falte en sldb se pide con `deskops message send --to sldb` (D3); el canal entre desks es el único escrito permitido en otro repo.
- **No cambia la autoridad de cierre.** `deskops closeout commit` sigue siendo la única puerta que cierra una tarea.

## Vocabulario

- **Tipo de tarea**: modelo sldb que hereda de `TaskDoc` (directa o transitivamente). Su nombre de tipo es el valor fijo de `task_type` (p. ej. `task.code`); su familia son sus documentos y los de sus subtipos.
- **Gate de activación**: `RuleDoc` con `moment: on_transition`, sujeto `model <= <Tipo>`, `where: current_node = "ritual-execution"`, severidad `error`. Si no se cumple, la arista `task_activates` no está en `edges_holding` y aparece en `edges_blocked` con su explicación.
- **Recibo** (`ReviewDoc`): documento con `kind` (`preflight`, `bundle`, `reproduction`, `goldens`, `owner`), `subject` (ancla `doc:<Modelo>:<id>@sha256:<hash>`), `engine`, `actor`, `run_dir`, `input_sha256`, `verdict` (`pending`, `accepted`, `rejected`, `incomplete`) y `reason`. Lo escribe `deskops review`; el veredicto lo escribe quien opera el desk con `deskops review dispose`.
- **Contrato de la tarea** (`__contract__` de `TaskDoc`): `title`, `goal`, `scope`, `implementation_path`, `files`, `validation`, `done_when`. Cambiar uno de esos campos deja los recibos `changed`; cambiar `references`, `pills`, `status`, `history` o `tags` no.
- **Efecto de una transición**: `attributes.sets` y `attributes.terminal` del `RelationDoc` (sldb GO09).
- **Agregado**: tarea `task.aggregate` con `children`; no se promueve ni ejecuta, cierra cuando cierran sus hijos.

## Fuera de alcance

Cambiar código o documentos de sldb; autenticación de actores; convertir la verificación de cierre (git, archivos) en recibos; coordinación central entre desks (D3: cada desk tiene sus tareas y pide feedback por `deskops message send`); el runtime de Scion más allá de dejar el punto de enganche para una plantilla de revisor; migrar desks ajenos (cada desk corre `deskops desk update --apply` cuando adopte la versión).

FILE:desk/drawer/plans/gates-por-tipo/alcance.md
# Alcance y estado de partida

## Estado de partida de deskops (verificado 2026-11-04, `deskops/`)

- **`task_type` es un string libre.** `TaskDoc.task_type: str = ""` con una descripción que enumera "design, implementation, test, reflection, or closeout" (`deskops/models/task.py:144-147`). Se usa solo al crear, para rellenar `closeout_evidence` desde `TASK_TYPE_EVIDENCE`, un diccionario plano `code|implementation|test → CODE_EVIDENCE; docs|spec|design → DOCUMENT_EVIDENCE; external → EXTERNAL_EVIDENCE` (`deskops/services/closeout_gates.py:30-38`, `deskops/services/tasks.py:85-86`). Un tipo desconocido no falla si trae `--evidence` (`closeout_gates.py:77-96`). No hay jerarquía ni gates por tipo.
- **La evidencia de cierre vive en la tarea.** `closeout_evidence: list[str]` con vocabulario cerrado `tests, commit, atom, materialization, document, external` (`task.py:165-172`, `closeout_gates.py:23`); una tarea sin el campo se gatea como código (`deskops/operations.py:580-588`).
- **Herencia reimplementada en Python.** `inherits_from` e `inherit_acceptance_context` (`task.py:148-154`) los resuelve `_resolve_task_payload` recursivamente, calculando `effective_references`, `effective_pills`, `effective_tags`, `effective_atoms`, `effective_validation`, `effective_done_when` (`operations.py:1028-1071`), aunque `inherits_from` ya es una arista `references` del grafo (`task.py:29-36`). El gate de cierre lee `references` crudo, no `effective_references` (`closeout_gates.py:129`, vía `operations.py:725-731`).
- **`depends_on` no tiene efecto.** Es referencia a `TaskDoc` (`task.py:29-36`, `:120-123`) y ninguna condición del ciclo de vida la lee.
- **Ciclo de vida con dos fuentes.** Estados = `RitualDoc`; transiciones = `RelationDoc` con `condition` evaluada por sldb (`deskops/lifecycle.py:1-13`). Pero `sets_status` y `terminal` salen del YAML (`lifecycle.py:48-49`, `:62-66`, `:137-150`; `deskops/spec/workflows/task_lifecycle.yaml:17-18`, `:27`, `:34`, `:41-42`). El grafo se escribe una vez y no se actualiza (`lifecycle.py:280`, `:328`, `:354`: "Existing documents are left as they are"). `advance` evalúa `condition_holds` transición por transición (`lifecycle.py:176-178`) y no usa `edges_holding`.
- **Gates como hechos inyectados.** `task_activates` tiene `condition: ""` (`task_lifecycle.yaml:26`): toda tarea activa. `task_completes` exige `has(closeout_evidence_verified)` (`:40`), un hecho que `_add_closeout_facts` escribe en el payload antes de evaluar y `advance_task` borra después (`operations.py:441-450`, `tasks.py:196-199`).
- **Dos vías de escape.** `advance --to`: si el destino es `draft|open|in_progress|blocked` escribe `status`, si no escribe `current_node`, sin condición alguna; solo `complete` y `closed` se rechazan (`tasks.py:179-192`). `edit task <campo>`: cualquier campo del modelo salvo `id`, incluidos `status`, `current_node`, `task_type`, `closeout_evidence` e `history` (`operations.py:271-282`; `deskops/cli/registry.py:225-239`).
- **Sin composición.** No existen `parent_id` ni `children` en ningún modelo de `deskops/models/`; la composición vive en scripts del drawer (`desk/drawer/plans/workspace-documental/build_plan.py`, `dag.yaml` por plan).
- **`deskops graph` construye su propio snapshot.** Nodos y aristas salen de extractores propios con regex para tareas, issues, rutas y átomos en prosa (`deskops/graph/extract_edges.py:22-34`, `:631`), además de leer el índice de aristas de sldb (`:245-310`); el snapshot tiene esquema propio (`deskops/graph/snapshot.py:17-21`).
- **Revisiones en frío por script.** `desk/rituals/context-review.md` fija el protocolo (perfil pi deepseek-flash, paso 3; dos roles antes de despachar, paso 8); `desk/rituals/execution.md` exige preflight y cold-bundle (pasos 5 a 9) y guarda la reformulación en `runs/subagents/<run-dir>/preflight.md`. Lo ejecutan dos scripts distintos: `desk/drawer/plans/workspace-documental/context_review.py` (modos `run`, `status`) y `sldb/desk/drawer/plans/grafo-operable/context_review.py` (modos `node`, `preflight`, `bundle`, `status`; tope `--max-attempts 2`; un nodo con input sin cambios no se vuelve a revisar). Ninguno escribe un documento en el desk: la disposición se escribe a mano en `reviews/rN.md`.
- **Modelos que ya sirven de base.** `RunDoc` (`deskops/models/run.py`: `run_dir`, `session_sha256`, `outcome`, `commit_sha`) y `RuntimeProfileDoc` (`deskops/models/runtime_profile.py`: binario, flags de modelo y de system prompt) son el molde de `ReviewDoc` y del perfil del motor. Los modelos se registran por `MODEL_REFS` y se heredan en cada desk desde el store de deskops (`deskops/bootstrap.py:26`, `:118-160`); sldb ya conoce `base_models` y el predicado `model <= X` (`sldb/src/sldb/store/query_engine/where_parse.py:125`).
- **Nota de sldb ya en el inbox**: `desk/inbox/20261104-213901-suggestion-sldb-eval-a-reglas-declaradas-plan-grafo-operable-...md` nombra este plan como lo que queda para deskops.

## Qué consume este plan de sldb (rev 9 de `grafo-operable/dag.yaml`)

| Nodo sldb | Qué entrega | Gate de este plan | Lo usan |
|---|---|---|---|
| GO02 | sintaxis `__contract__` y hash de contrato; firma de `eval` | (documento, sin gate) | GC01 declara `__contract__` |
| GO05 | lenguaje unificado: `and/or/not`, caminos, `any/all/none/count`, `^campo`, `+`, `anchor_state` | `G_SLDB_LANG` | GC05, GC07, GC09 |
| GO06 | `RuleDoc` (subject `model <= X`, `where`, `condition`, `severity`, `moment`), `rules check`, `rules explain` | `G_SLDB_RULES` | GC05 |
| GO07 | anclas `doc:Model:name@sha256:<hash>` en campos `__doc_anchors__`, pinneado al guardar, estados `intact/changed/lost`, `anchors check` | `G_SLDB_ANCHORS` | GC02 (acepta), GC05 |
| GO08 | evaluación `on_write/on_transition/on_check`, `edges_holding` con `findings`, `edges_blocked`, caché en `.sldb_cache` | `G_SLDB_EVAL` | GC05 |
| GO09 | `RelationDoc.attributes.sets/terminal`, `effects` en `edges_holding`, `apply_effects` | `G_SLDB_EFFECTS` | GC04 |

Cada gate `G_SLDB_*` se satisface cuando el nodo de sldb cerró en `main` de sldb y deskops pinnea en `pyproject.toml` una versión de sldb que lo contiene. Hasta entonces los nodos que lo requieren no se promueven; los que ni lo requieren ni dependen de uno que lo requiera (GC01, GC02, GC03, GC06) pueden avanzar.

## Qué produce este plan para sldb

`G_CONSUMER` (sldb `dag.yaml` rev 9, `gates.G_CONSUMER`): "en un desk temporal, una tarea sin recibo de revisión no se activa y la explicación nombra la cláusula; con recibo atado al hash de contrato vigente, se activa; con el contrato editado, el recibo queda `changed` y vuelve a bloquear". Lo produce GC05 como test de integración y lo informa a sldb con `deskops message send --to sldb` (D3).

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Mientras GC03 no exista, con el script gobernado de sldb apuntado a este plan; después, con `deskops review`. Una revisión en frío está aceptada cuando quien opera el desk de deskops (D3) escribe su disposición y no queda ninguna ambigüedad abierta según la guía.
2. Tope de rondas: dos a nivel de plan; una preflight y una cold-bundle por promoción, y solo se repite si el input (hash del bundle o hash de contrato del TaskDoc) cambió o con `--force` y razón escrita.
3. La validación corre con `pytest tests` en el host que el dueño indique. Un nodo no cierra con tests rojos ni saltados.
4. Toda capacidad nueva entra con: modelo o documento, comando CLI con envelope, pruebas, entrada en `CHANGELOG.md` y doc en `docs/` (manual de operador o referencia de workflow). Los rituales del desk que nombran el comportamiento cambiado se actualizan en el mismo nodo o en GC08, nunca después.
5. Nada de Python supliendo una regla: si rev 9 no fija lo que un nodo necesita, el nodo registra la hipótesis en su TaskDoc y, si bloquea, manda la nota a sldb.
6. Compatibilidad: los desks existentes migran con `deskops desk update --apply`; cada nodo que cambia un documento del desk (tipos, aristas, reglas) hace que `desk update` lo escriba o reescriba de forma idempotente y lo prueba.
7. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
8. Las cuatro restricciones de D2 no admiten excepción por nodo: ningún nodo agrega una bandera para saltar un gate.

FILE:desk/drawer/plans/gates-por-tipo/decisiones.md
# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. Las decisiones D2, D3 y D4 son del dueño y están registradas en `sldb/desk/drawer/plans/grafo-operable/decisiones.md`; se copian aquí con el mismo id porque este plan las consume. Las DC son propuestas de este plan: quedan como "propuesta" hasta que el dueño autorice el plan; una propuesta aceptada tácitamente se marca como tal.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D2 | Los gates de activación de una tarea son bloqueo duro, sin bandera de salto. La vía de escape es especializar tipos de tarea (`task.refactor` ≠ `task.debug`), cada tipo con sus gates. | Dueño | sldb `decisiones.md` D2 | 2026-11-04 |
| D3 | No hay coordinación central entre desks: cada desk tiene sus tareas y pide feedback al resto (`deskops message send`). Scion coordina ejecución; deskops coordina conocimiento. | Dueño | sldb `decisiones.md` D3 | 2026-11-04 |
| D4 | El revisor barato sigue siendo pi deepseek(-flash), con bundle propio en el fork bajo Scion. | Dueño | sldb `decisiones.md` D4; perfil verificado en `desk/rituals/context-review.md` paso 3 | 2026-11-04 |
| D9 | Las rondas de revisión en frío tienen tope: dos a nivel de plan; una preflight y una cold-bundle por promoción. "8 rondas igual es excesivo". | Dueño | Docstring de `sldb/desk/drawer/plans/grafo-operable/context_review.py` (caps) y encargo de este plan | 2026-11-04 |
| D10 | El driver de revisiones en frío pasa a ser un comando `deskops review`, no otro script en un drawer. | Dueño | Encargo de este plan; nota de sldb en `desk/inbox/20261104-213901-...md` | 2026-11-04 |
| DC1 | Un tipo de tarea es un modelo sldb que hereda de `TaskDoc`; la jerarquía de tipos es `base_models` y la familia de una regla es `model <= <Tipo>`. No se crea un `TaskTypeDoc` aparte: tendría que reimplementar la herencia que sldb ya resuelve (sldb `alcance.md`: "las reglas por familia de modelo se apoyan en esto, no en un mecanismo nuevo"). `task_type` es el nombre fijo del tipo. | Propuesta de este plan | brief.md §Resultado 1 | 2026-11-04 |
| DC2 | Los gates de activación son `RuleDoc` `on_transition` por familia, restringidas a la transición con `where: current_node = "ritual-execution"`; la evidencia de cierre sigue verificada por deskops (hechos de git y archivos) pero se declara en el tipo, no en la tarea. | Propuesta de este plan | brief.md §El límite; sldb brief §El límite ("no produce hechos externos") | 2026-11-04 |
| DC3 | El recibo es un `ReviewDoc` en `desk/reviews/`, tracked, con `subject` en `__doc_anchors__` pinneado por sldb al guardar; el veredicto lo escribe quien opera el desk con `deskops review dispose` y no se edita después: una nueva revisión es un documento nuevo. | Propuesta de este plan | brief.md §Vocabulario | 2026-11-04 |
| DC4 | `advance --to` se retira entero. `status` solo lo escriben los efectos de las transiciones y el cierre; `blocked` deja de ser un `status` guardado: es la regla que no se cumple, visible en `show` y `next` por `edges_blocked`. `edit task` rechaza `status`, `current_node`, `task_type`, `closeout_evidence` e `history`. | Propuesta de este plan | D2; `tasks.py:179-192`; `operations.py:271-282` | 2026-11-04 |
| DC5 | El motor por defecto de `deskops review` es el perfil pi deepseek-flash del ritual, descrito como `RuntimeProfileDoc` del desk; una plantilla de Scion entra después detrás de la misma opción `--engine`. | Propuesta de este plan | D4; `desk/runtimes/runtime-pi.md` | 2026-11-04 |
| DC6 | Composición: `parent_id` en el hijo y `children` en el agregado, los dos como referencias explícitas (`deskops add task --parent` mantiene las dos); `depends_on` se hace efectivo con `all(depends_on: status = "closed")`. Como el cierre borra el archivo de la tarea, una dependencia cerrada no existe en el store y sldb la omite del conjunto (GO02 (c)): la regla se cumple con dependencias borradas y falla con una abierta. Un id mal escrito lo detecta `deskops graph missing`/`doctor`, no el gate. | Propuesta de este plan | sldb `dag.yaml` GO02 (c) y (f); `desk/rituals/closeout.md` | 2026-11-04 |
| DC7 | Un desk agrega tipos propios en `desk/models/*.py` (subclases de un tipo de fábrica) que `deskops desk update --apply` registra en el store del desk; un tipo no registrado no se puede usar en `add task`. | Propuesta de este plan | `bootstrap.py:118-178` | 2026-11-04 |

## Pendientes del dueño

- **`--evidence` en `add task`.** Con la evidencia declarada en el tipo, `--evidence` queda como piso: solo puede agregar kinds a los del tipo, nunca quitar (así lo escribe GC01). Confirmar o retirar la opción. La regla "la evidencia se declara al crear la tarea" sigue valiendo: se declara eligiendo el tipo.
- **Tipos propios por desk (DC7).** Exige un módulo Python en cada desk que los quiera. La alternativa (tipos solo de fábrica) no permite la vía de escape de D2 a un desk que no sea deskops. Confirmar DC7.
- **`task.external`.** Se conserva para no perder el vocabulario `external`; si el dueño prefiere, se pliega en `task.docs` con evidencia `external`.
- **Scion.** La plantilla de revisor en Scion no tiene contrato escrito; GC03 deja `--engine` y el perfil como punto de enganche y no la implementa.

FILE:desk/drawer/plans/gates-por-tipo/dag.yaml#node:GC02
id: GC02
title: ReviewDoc como recibo anclado al contrato de la tarea
kind: code
owner_repo: deskops
node_role: delivery
parent_id: PC01
scope: 'Modelo deskops/models/review.py ReviewDoc (StructuredNLDoc, como RunDoc) con
  campos: id (review-<task>-<kind>-<n>), title, kind (preflight | bundle | reproduction
  | goldens | owner; vocabulario cerrado validado), subject (str; valor doc:<Modelo>:<id>
  o vacío para revisiones de nodos de plan), subject_ref (str libre: ruta#node:ID
  cuando subject está vacío), engine (nombre del RuntimeProfileDoc o "human"), actor
  (identidad que corrió o dispuso; deskops/identity.py), run_dir (ruta relativa bajo
  runs/), input_sha256, output_sha256, verdict (pending | accepted | rejected | incomplete),
  reason (str), created_at, disposed_at, disposed_by, tags; cuerpo: sección Summary
  y sección Disposition. __doc_anchors__ = ["subject"] y __references__ = ["subject"]
  (GO07 trata __doc_anchors__ también como references; antes de GO07 el campo es una
  referencia normal que resuelve doc:Model:name sin sufijo, hipótesis: la versión
  actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02
  lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál). Un ReviewDoc
  vive en desk/reviews/<task-id>/<kind>-<n>.md y se trackea; deskops init/desk update
  crean desk/reviews/. Validación al escribir: kind y verdict en su vocabulario; verdict
  accepted o rejected exige reason no vacía y disposed_by; subject con forma doc:<Modelo>:<id>
  o vacío. Un ReviewDoc no se edita con edit review verdict: edit lo rechaza (el veredicto
  se escribe con deskops review dispose, GC03). Registro en MODEL_REFS. Este nodo
  no escribe ReviewDocs desde ningún comando; GC03 lo hace.'
acceptance: ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo; un
  kind fuera del vocabulario falla al validar; verdict accepted sin reason falla;
  subject "task-x" (sin prefijo doc:) falla; subject "doc:TaskCodeDoc:task-x" valida;
  en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como
  ReviewDoc:<id> y sldb edges show lo enlaza a la tarea por subject; edit review verdict
  falla con el mensaje que remite a review dispose; tests/fixtures/model_contract_hashes.json
  actualizado; CHANGELOG.
output_scope: deskops/models/review.py, deskops/models/__init__.py, deskops/bootstrap.py
  (MODEL_REFS), deskops/workspace.py (desk/reviews), deskops/operations.py (edit refuses
  verdict), tests/, tests/fixtures/model_contract_hashes.json, CHANGELOG.md
depends_on: []
requires: []

FILE:desk/drawer/plans/gates-por-tipo/dag.yaml#edge:GC03
id: GC03
title: Comando deskops review que reemplaza a los dos scripts de revisión en frío
kind: code
owner_repo: deskops
node_role: delivery
parent_id: PC01
scope: 'Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos
  de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado,
  vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md,
  brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc),
  bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos
  ligados + archivos que files nombra, menores de 60 KB + validación), status [<task>
  | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin
  llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason
  <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc
  ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el
  ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/
  (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo,
  perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json)
  y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de
  la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío
  y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256.
  Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del
  ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md
  con los flags de aislamiento (--offline --no-session --no-context-files --no-skills
  --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del
  script gobernado como texto del perfil; el perfil Scion queda como opción futura
  detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios
  no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan;
  para preflight y bundle una por hash de contrato de la tarea, y una repetición exige
  --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte
  (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con
  technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado
  de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py
  y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py
  es de sldb y no se toca: se le manda nota por deskops message send --to sldb de
  que deskops review lo cubre. Produce G_RECEIPTS.'
acceptance: 'En un desk temporal con un ejecutable pi falso (fixture que devuelve
  una salida con REFORMULACION), deskops review preflight task-x escribe attempt-1
  con los cinco archivos y un ReviewDoc review-task-x-preflight-1 con verdict pending,
  subject doc:TaskCodeDoc:task-x, run_dir e input_sha256 iguales a los del manifest;
  una segunda corrida sin cambios no llama al ejecutable y status lo reporta como
  reviewed; editar goal de la tarea hace que status la reporte stale y la siguiente
  corrida cree attempt bajo otro sha; bundle incluye en input.md los rituales del
  Board, las pills ligadas y los archivos de files, en ese orden, con FILE: por archivo;
  node sobre este mismo plan (gates-por-tipo) escribe un ReviewDoc por nodo con subject
  vacío y subject_ref; review dispose review-task-x-preflight-1 --verdict accepted
  --reason "..." escribe verdict, reason, disposed_at y disposed_by y una segunda
  dispose falla; un tercer intento sobre la misma clave a nivel de plan falla sin
  --force; un pi falso que sale con exit 1 deja technical_ok false y verdict incomplete;
  grep de context_review.py en desk/drawer de deskops no devuelve nada; CHANGELOG;
  docs/operator-manual.md con la sección deskops review.'
output_scope: deskops/cli/registry.py, deskops/cli/commands/review.py, deskops/services/review.py,
  deskops/workspace.py (runtime-pi-deepseek-flash), desk/runtimes/, desk/drawer/plans/workspace-documental/context_review.py
  (borrado), tests/, docs/operator-manual.md, CHANGELOG.md
depends_on:
- GC02
requires: []

FILE:desk/drawer/plans/gates-por-tipo/dag.yaml#edge:GC05
id: GC05
title: Reglas de activación por tipo y explicación por edges_blocked (produce G_CONSUMER)
kind: code
owner_repo: deskops
node_role: delivery
parent_id: PC02
scope: 'Reglas escritas por init y desk update --apply en desk/rules/ (idempotentes,
  reescritas si difieren), todas con severity error, moment on_transition y where
  "current_node = "ritual-execution"" (hipótesis: rev 9 no filtra las reglas on_transition
  por tipo de relación, así que la transición se distingue por el nodo de partida
  en where; si sldb agrega un filtro por relación, se usa ese). Una regla común activation-depends-on.md
  con subject "model <= TaskDoc" y condition all(depends_on: status = "closed") (DC6:
  una dependencia cerrada fue borrada y sldb la omite; una abierta falla nombrándola).
  Una regla por tipo de fábrica que declare __activation_receipts__ no vacío, activation-<tipo>.md,
  con subject "model <= <ModeloDelTipo>", message "activación de <tipo>" y condition
  = conjunción de any(^subject: kind = "<kind>" and anchor_state = "intact" and verdict
  = "accepted") por cada kind de __activation_receipts__ del tipo. Herencia por familia:
  un documento cumple las reglas de su tipo y de todos sus ancestros (sldb evalúa
  cada regla cuyo sujeto lo incluye), así que un subtipo suma gates y nunca quita
  (brief.md §Tipos): task.refactor pasa por la regla de task.code (preflight + bundle)
  y por la suya (goldens); task.debug no hereda de task.code justamente porque reemplaza
  bundle por reproduction. Un tipo propio de un desk sin regla propia queda cubierto
  por las de sus ancestros; si suma kinds, el desk escribe su regla con deskops add
  rule --type <tipo>, que genera el archivo desde __activation_receipts__ del tipo
  menos los kinds que ya exigen sus ancestros. advance: si edges_holding no devuelve
  task_activates, deskops llama a edges_blocked(store, nodo, payload) y muestra cada
  finding (what: message + explicación de GO02 con cláusula, nodo y valor visto) en
  el envelope como la explicación del bloqueo; show y next muestran lo mismo bajo
  gates. El hecho closeout_evidence_verified (operations.py:441-450) se mantiene en
  este nodo: la evidencia de cierre son hechos externos que deskops verifica (DC2);
  se documenta como la única condición que no es regla. Test de integración que es
  la evidencia de G_CONSUMER (sldb dag.yaml gates.G_CONSUMER): en un desk temporal,
  una tarea task.code sin ReviewDoc no se activa y la explicación nombra any(^subject
  ...); con dos ReviewDoc (preflight y bundle) accepted y pinneados se activa; editar
  goal deja los recibos changed y advance vuelve a bloquear nombrando anchor_state;
  editar references no cambia nada. Al cerrar: deskops message send --to sldb --kind
  suggestion con título "G_CONSUMER producido por deskops: gates-por-tipo GC05" y
  cuerpo con el hash del commit y la ruta del test. Produce G_CONSUMER.'
acceptance: desk/rules/ tiene la regla común y una RuleDoc por tipo de fábrica con
  recibos, y sldb rules check sin --subject no reporta errores de parseo; el test
  de integración de G_CONSUMER pasa en sus tres pasos; una tarea task.docs se activa
  con solo preflight y una task.code no; una task.refactor con preflight y bundle
  no se activa hasta tener goldens y una task.debug se activa con preflight y reproduction
  sin bundle; una tarea con depends_on a una tarea abierta no se activa y el finding
  nombra la dependencia; tras cerrar esa dependencia (closeout commit la borra) se
  activa; deskops advance de una tarea bloqueada imprime los findings con cláusula
  y valor visto y deskops show los lista bajo gates; add rule --type task.code.cli
  en un desk con ese tipo genera una RuleDoc válida; desk update --apply sobre un
  desk sin desk/rules/ las escribe y una segunda corrida no cambia nada; la nota a
  sldb existe en sldb/desk/inbox; CHANGELOG; docs/workflow-policy-reference.md con
  la regla de cada tipo.
output_scope: deskops/lifecycle.py, deskops/services/tasks.py, deskops/services/rules.py,
  deskops/workspace.py (desk/rules), deskops/cli/registry.py (add rule), deskops/cli/commands/operations.py
  (show, next), deskops/operations.py, desk/rules/, tests/, docs/workflow-policy-reference.md,
  CHANGELOG.md, sldb/desk/inbox (vía message send)
depends_on:
- GC01
- GC02
- GC04
requires:
- G_SLDB_LANG
- G_SLDB_RULES
- G_SLDB_ANCHORS
- G_SLDB_EVAL

FILE:desk/drawer/plans/gates-por-tipo/dag.yaml#edge:PC01
id: PC01
title: Tipos, recibos y revisor
owner_repo: deskops
node_role: aggregate
children:
- GC01
- GC02
- GC03
scope: 'Lo que deskops puede hacer sin esperar a sldb: tipos de tarea como modelos
  con jerarquía y evidencia de cierre declarada en el tipo (GC01); el modelo ReviewDoc
  como recibo con subject en __doc_anchors__ (GC02); el comando deskops review que
  produce esos recibos y retira los dos scripts (GC03). Antes de G_SLDB_ANCHORS el
  subject se guarda sin hash (sldb lo pinnea cuando GO07 exista; deskops no calcula
  hashes).'
acceptance: G_TYPES y G_RECEIPTS satisfechos; add task --task-type solo acepta tipos
  registrados; deskops review preflight y bundle dejan ReviewDoc y evidencia en runs/;
  ningún script context_review.py queda en los drawers de deskops.

FILE:instruccion
Revisa el nodo GC02 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

