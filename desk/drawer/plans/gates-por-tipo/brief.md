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
