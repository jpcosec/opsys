# Ajustes canónicos requeridos por la matriz WS06

Estado: propuesta para el Supervisor. Ninguno está aplicado. Cada uno nace de una fila de la sección «Matriz de correspondencia WS06» de `desk/drawer/plans/workspace-documental/reconciliacion.md`. Se listan solo cambios que la matriz vuelve imprescindibles; las ediciones de abajo no las hace WS06.

## 1. Revisión esperada: el CAS por hash no existe y WS19.1 lo da por hecho

- Archivos: `desk/drawer/plans/workspace-documental/dag.yaml` (WS19.1, scope, línea ≈1252-1253 «revisión esperada (hash CAS del documento)»; WS20, scope y acceptance) y `desk/drawer/plans/workspace-documental/brief.md` (línea 40, «Revisión / before-image: hash con que una escritura prueba que partió del estado actual»).
- Cambio propuesto: en brief.md, distinguir lo que existe (comparación pública por valor `expected` en `POST /save` de sldb, que da 409) de lo que se busca (revisión por `version`/`content_hash` en la API pública de escritura). En dag.yaml, o bien ampliar WS20 (sldb) para producir también la revisión esperada de la escritura de payload, o bien cambiar WS19.1 para decir «`expected` por valor (comparación de payload)» hasta que ese productor exista. Hoy WS12 solo admite un requisito de API faltante en el nodo productor WS20, y WS20 ya exige «revisión» y pruebas de conflicto, pero para raw-source (dag.yaml:1331-1339); el vacío es el CAS de guardado de payload por campos, no raw-source.
- Evidencia: matriz C-40 (`expected`, ya cubierto con límites) y C-41 (CAS, nuevo delta sin nodo productor); `auditoria/infraestructura.md` sección 2.1 (`save_plan.py:50,58`; `grep` de `expected_hash`, `If-Match`, `etag` sin resultados) y sección 6, puntos 2 y 3.
- Nodos afectados: WS19, WS19.1, WS19.2, WS20, WS21, WS12 (y WS42, que depende de un canal con autoridad compartida).

## 2. Productor faltante de captura directa a drawer

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (WS25.2, y un nodo productor en deskops).
- Cambio propuesto: WS25.2 (owner graph_ui) exige «candidato de drawer … mediante operaciones permitidas por el contrato WS12», pero deskops solo crea candidatos desde una nota de inbox (`promote inbox-to-drawer-task`, que además borra la nota). Registrar un productor deskops (nodo nuevo o ampliación de uno existente) para la captura directa, o fijar en WS12/WS25.2 que la captura es la composición `message send` al mismo desk más `promote inbox-to-drawer-task`. Es condicional: no hace falta si WS12 elige la composición.
- Evidencia: matriz C-55 (nuevo delta, productor deskops) y C-21; `auditoria/deskops.md`, fila A1 `deskops promote inbox-to-drawer-task`.
- Nodos afectados: WS25.2, WS25, WS12.

## 3. ViewDoc como «contrato existente de spec2viz» y alcance de WS18

- Archivos: `desk/drawer/plans/workspace-documental/brief.md` (línea 24, glosario «Proyección de grafo ViewDoc») y `desk/drawer/plans/workspace-documental/dag.yaml` (WS18, scope y acceptance, líneas ≈1158-1180; también `output_scope: sldb/views/`, ruta de sldb para un nodo con `owner_repo: spec2viz`).
- Cambio propuesto: en brief.md, escribir que el modelo `ViewDoc` existe en spec2viz y que el evaluador, las rutas de evaluación y guardado y el render existen en graph_ui, solo en modo local (501 en remote); ningún código de sldb, pron ni spec2viz evalúa un ViewDoc. En WS18, decir que se reutiliza el evaluador de graph_ui y la notación de spec2viz (`resolve_documents`), que «renderiza sobre un store real» se prueba con ese camino, y corregir o confirmar `output_scope` con el dueño de spec2viz. No se propone evaluador de cero.
- Evidencia: matriz C-37 (evaluador y rutas en graph_ui), C-48 (modelo) y C-50 (ViewDoc portables, nuevo delta); `auditoria/infraestructura.md` sección 5.2 y sección 6, punto 1; `auditoria/ui.md` sección 3.1.
- Nodos afectados: WS18, WS24 (extensión opcional), WS09, WS11.

## 4. Texto «acepta por delta en WS11/12» (WS06) y «aceptación específica» en acceptance de WS06

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (WS06, scope línea ≈485 «el responsable receptor ya designado en P01 acepta por delta en WS11/12»; acceptance «WS11/12 obtienen aceptación específica por repo receptor»). WS18 ya dice «recepción G_SPEC_VIEW para ese delta» y no usa «acepta»; no necesita cambio por esta razón.
- Cambio propuesto: reemplazar por «el receptor P01 produce recibos externos en su repo al preparar cada delta; WS11 y WS12 son fuente de contrato y solo enlazan esos recibos». WS06 no produce aceptación ni permiso interrepo. La TaskDoc de WS06 ya tiene esta lectura; el dag.yaml conserva la anterior, que una lectura literal entiende como que WS11/12 escriben actas.
- Evidencia: aprobación del checkpoint (`runs/subagents/20261031-ws02-04-checkpoint/approval.md`, condición sobre recibos); `decisiones.md` («recepción técnica pendiente por delta»); `alcance.md` («Las actas se guardan y commitean en repo receptor»).
- Nodos afectados: WS06, WS11, WS12.

## 5. Revisiones baratas de 25 nodos invalidadas por editar reconciliacion.md

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (`context_review.input_sha256` y `status` de los nodos que leen reconciliacion.md).
- Cambio propuesto: tras integrar la matriz, correr la revisión de contexto de esos nodos y actualizar `input_sha256` y `evidence`; `validate_plan.py --check` falla hasta entonces. Es el efecto declarado en la TaskDoc de WS06, listado aquí para que el Supervisor lo capture como tarea de ajuste canónico y no dentro de WS06.
- Evidencia: sección «Efecto esperado y declarado» de la TaskDoc de WS06.
- Nodos afectados: PK01, WS04, WS06, WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS19, WS19.1, WS19.2, WS21, WS22, WS23, WS24, WS29, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2.

## Considerados y descartados

- Sin cambio en `decisiones.md` ni `alcance.md`: la matriz no reabre P01-P09.
- Sin cambio en las auditorías: sus residuales de citas no bloquean (approval.md).
- La falta de un canal de escritura con autoridad compartida (P03) ya la registra WS12 como hueco y dueño; no se propone nodo aquí.
