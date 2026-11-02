## Separación de fuentes

- **Lectura propia:** `fix-diff.txt`, `vistas.md`, `preflight-disposition.md`, `result-summary.md`, `comparison-ledger.md`, `manual.md`, `user-flows.md` y tramos citados de `dag.yaml`.
- **Dato del Supervisor (`tester-v2-facts.log`), no verificado por mí:** HEAD `e4e07f08`, revisiones al día, tabla/diagrama coinciden con `dag.yaml`, 13 tests, hash de `vistas.md`, `dag.yaml` sin líneas fuera de `evidence`/`input_sha256`.
- **No ejecuté nada:** ni tests, ni git, ni validate.

## Hallazgos previos

| Hallazgo previo | Evidencia actual | Resultado |
|---|---|---|
| F11a/F18a/F19a usaban `propuesto` con contratos WS11/WS12 pendientes | `vistas.md:236`, `:372`, `:406`: las tres dicen `bloqueado` | PASS |
| F18a se contradecía sobre contrato | `vistas.md:365` registra contrato de modelo; `:372` aclara «Tiene contrato de modelo, no de UI» | PASS |
| F11b atribuía la conversación a WS44 | `vistas.md:244`: conversación no auditada, vínculo WS33; `:249`: lectura WS35; WS44 queda para acceso | PASS |
| F14 usaba WS11 como productor de la lista de issues | `vistas.md:299`: «sin productor en el DAG, repo dueño graph_ui; contrato de lectura WS11» | PASS |
| F18a usaba WS11 como productor de la vista Specs | `vistas.md:367`: «sin productor en el DAG, repo dueño graph_ui; si entra al lector, contrato WS11» | PASS |

## Comprobación solicitada

| Objeto | Fuente | Evidencia real archivo:línea | Resultado |
|---|---|---|---|
| 23 fichas con Estado coherente | `vistas.md` | 23 líneas `Estado` en `:66,83,100,117,134,151,168,185,202,219,236,253,270,287,304,321,338,355,372,389,406,423,440`; todas `bloqueado` | PASS |
| ¿Queda WS11 como productor de implementación? | `vistas.md` | `:163` F07: «Mostrar la nota como documento… productor WS11»; `:316` F15: «Renderer… productor WS11 (documento por el lector genérico)» | **FAIL** |
| Convención que se incumple | `vistas.md` | `:52`: productor de contrato = WS11/WS12; implementación = nodo del DAG o «sin productor en el DAG» | **FAIL** |
| Contradicción interna tipo F18a | `vistas.md` | F18a resuelta en `:365/:372`; no hallé otra contradicción equivalente | PASS |
| F01 «sin productor» | `dag.yaml`, `vistas.md` | F01 no dice «sin productor»: `vistas.md:61` asigna implementación WS13.1/WS13.2; WS17 produce plantillas (`dag.yaml:1170-1198`) | PASS con corrección: la premisa «F01 sin productor» es falsa |
| F11a sin productor específico | `dag.yaml` | WS24 produce vista genérica para átomos/crossroads/materializaciones/pills (`dag.yaml:1574-1600`), no para roles/runtimes | PASS |
| F12 consulta guardada sin productor | `dag.yaml` | WS14 implementa búsqueda (`dag.yaml:974`); no hay nodo de consulta guardada | PASS |
| F14 lista de issues sin productor | `dag.yaml` | Solo menciones de issues en `dag.yaml:356,619`; no hay nodo de lista de issues | PASS |
| F15 navegación FAQ sin productor | `dag.yaml` | WS40 crea FAQ Markdown (`dag.yaml:2690`); no hay nodo de navegación de preguntas | PASS |
| F18a vista Specs sin productor | `dag.yaml` | WS18 crea ViewDoc/NotationDoc (`dag.yaml:1225`); no produce vista Specs | PASS |
| F19a/F19b frente a capítulo 15 del manual | `vistas.md`, `manual.md` | `manual.md:163`: capítulo 15 `propuesto` hasta WS39; `vistas.md:406`: «esta ficha mide la fila»; `:423`: capítulo propuesto hasta WS39 | PASS: la distinción capítulo/fila se explica |
| Diff solo lo declarado | `fix-diff.txt` | Solo modifica `vistas.md`: convención, F01, F11a, F11b, F14, F18a, F19a | PASS |
| Invención en el diff | `fix-diff.txt` | F01 asigna WS13.1/WS13.2 dentro de su alcance de lector/explorador; no crea nodos, APIs ni mapeos nuevos | PASS |
| Conteo 23/0/0 | `vistas.md`, `result-summary.md` | `vistas.md:52` y las 23 líneas `Estado` dan 23 bloqueado, 0 propuesto, 0 disponible; `result-summary.md:79` fija 23/0/0 | PASS; el resumen conserva conteos obsoletos 19/4 y 20/3, pero los marca como superados |
| Resumen/ledger no exceden lo hecho | `comparison-ledger.md` | `:9` acota que no comprobó el contenido de las 365 citas; `:17` es una afirmación de revisión, no de contenido | PASS con dato no verificable |

## Qué no pude verificar

- No ejecuté tests, git, `status`, `validate` ni build.
- No abrí código de `graph_ui`, `sldb`, `spec2viz`, `pron` ni `scion`.
- No leí `dag.yaml` completo ni las 365 citas; solo tramos y citas citadas.
- No verifiqué las afirmaciones del `tester-v2-facts.log` ni las actas humanas.

RESULTADO: FAIL
