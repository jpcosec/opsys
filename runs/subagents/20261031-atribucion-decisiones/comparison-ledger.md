# Ledger de comparación, tanda 3 sobre b2720ae2

Fecha: 2026-11-01. Rol: Supervisor. Actor: Claude Opus 5.5, pane `w3Y:p1`. Revisores: `pi`, deepseek-flash, por `context_review.py`, instrucción `v2-ejecucion-hipotetica`. Vigente. Sustituye como evidencia a las tandas 1 (`tanda-1/`, `47b9e38b`) y 2 (`tanda-2/`, 47 respuestas y 26 sin respuesta), que quedan como historia.

Fuente aprobada de forma focal por root, por bytes: `root-focal-approval-20261101.md`. Esa aprobación no cubre el plan ni estos outputs.

## Qué se corrió

- `run --stale --jobs 6`: 73 `ok`, `review-run.log`.
- Reintentos con `--new-attempt --reason`: PK02, PK07, WS16, WS19, WS33.2, WS37, `review-run-retries.log`.
- Vigentes: 67 `attempt-1` y 6 `attempt-2`, los 73 con recibo completo, sin fallo técnico, manifest v2 e `input_sha256` igual al bundle. Lista: `final-attempts.json`.

## Qué leí exactamente

`output.md` completo de los 73 y de los seis reintentos. Los contratos completos (scope, acceptance, output_scope y los demás campos) los leí en la tanda 1, en esta sesión; `git diff 47b9e38b b2720ae2 -- dag.yaml` es vacío, así que son los mismos. En esta tanda volví a ver id, rol, kind, repo, depends_on, requires y children. No releí scope ni acceptance nodo por nodo salvo donde cito. No leí bundles completos, `reconciliation`, `promotion` ni TaskDocs generados. No hubo agente preparatorio.

Por programa: cuatro secciones en cada output; una clase por ambigüedad numerada; alcanzabilidad WS37→WS08, WS30→WS08 y WS12→WS09. El script solo cuenta y recorre aristas: las clases son juicio mío.

## Regla de rechazo

Intento nuevo solo si el output afirma algo contrario al contrato sobre arista, gate, productor o actor. Una vez por nodo. No por redacción.

| Nodo | Defecto del attempt-1 |
|---|---|
| PK02 | G_PRODUCT y G_WRITE_POLICY como pendientes; están satisfechos |
| PK07 | WS39 produce el capítulo 15; lo publica WS31 |
| WS16 | G_UI_READ requerido; `requires` vacío |
| WS19 | Precondición solo para WS19.1; WS19.2 también la requiere |
| WS33.2 | Acta de receptor P01 en delta de deskops |
| WS37 | WS44 designa operador; lo designa el solicitante |

Residuos aceptados con nota, sin tercer intento: WS33.2 repite «el receptor humano emite acta» en FUTURO; PK02 dice que WS09 entrega a WS12, sin arista directa pero con camino por WS11.

## Resultado

| Dato | Valor |
|---|---|
| Comparadas | 73 |
| Aceptadas como comprensión | 73 |
| Ambigüedades en intentos vigentes | 41 |
| `detalle de promoción` | 24 |
| `no es ambigüedad` | 10 |
| `futuro asignado` | 7 |
| Ambigüedades reales | 0 |

Efecto de la corrección: WS07 sin ambigüedad de actor; WS19.1 sin ambigüedad y asignando a WS12 la definición operativa; WS13, WS15, WS19, WS25, WS27, PK04 y PK07 declaran hermanos sin arista. Esto sugiere que la instrucción v2 era causa de las transferencias falsas; no lo prueba, porque es una sola tanda.

## Límites

- **WS12:** su reformulación ambigüedad 1 dice que la aceptación no enumera la definición de «modo manual exclusivo». Tiene razón. Queda resuelto por T-P03.1 y la decisión root, sin cambio de contrato. Si WS12 se promueve sin leer esa nota, podría cerrar sin ella: conviene que su TaskDoc la cite.
- Las clases son juicio del Supervisor; 24 quedan para promoción y ninguna se resolvió aquí.
- Citas por línea a `dag.yaml` en `decisiones.md`: correctas tras registrar, comprobadas por muestra; cualquier edición futura del DAG las mueve.
- `decisiones.md` no tiene ambigüedad en revisores, pero tres revisores previos y dos Tester no vieron la pérdida de actor. Una revisión en verde no prueba ausencia de defecto.

## Para la promoción

- WS12: citar T-P03.1 en su TaskDoc.
- WS36: `output_scope` solo nombra la ruta a WS34; el scope pide también WS33.2.
- WS24: `output_scope` no nombra ruta backend si la API de grafo la requiere.
- WS22: clave de agrupación y campo de dependencias.
- WS13.3: conducta al cerrar pestañas y frontera con `workspace.mjs`.
- WS35: tratamiento de mensajes-hueco, con productor TaskDoc.
- WS45: sin la frase de WS20 sobre convertirse en la tarea propia en sldb.

## Adenda 2026-11-01, tras Tester v4 FAIL

Hallazgos aceptados:

- Cuatro disposiciones (WS02, WS03, WS04, WS06) decían «aprobado por root» sin cita, y eso excedía lo que declaraban haber leído. Corregidas: WS02–WS04 citan `runs/subagents/20261031-ws02-04-checkpoint/approval.md`, que abrí; WS06 cita su cierre `ff28c68c` y declara que no localicé aprobación root propia.
- La cobertura no daba la ruta completa de `owner-decisions.json`. Corregida.

Hallazgos que no acepto, con motivo:

- WS26 «sus aristas WS12/WS22/WS30» no es defecto: WS30 depende de WS26, así que la arista existe, saliente.
- «`owner-decisions.json` no existe»: existe y está versionado. El Tester no lo halló porque la cobertura no daba la ruta.
- El Tester dice que hubo cambio de fuente: es la corrección autorizada, no un hallazgo nuevo.

## Adenda 2026-11-01, tras Tester v5 FAIL

El Tester v5 pasó todos los puntos salvo uno: «distinto de la autoría inicial» podía leerse como que son personas distintas, sin fuente que lo sostenga. Corregí esa frase en la cobertura y en la adenda 3 del mapa: ahora dice que el actor registrado no prueba la autoría inicial. Sin Tester posterior: es un cambio de redacción sobre dos archivos fuera de los bundles, y lo comprobé con `grep`.
