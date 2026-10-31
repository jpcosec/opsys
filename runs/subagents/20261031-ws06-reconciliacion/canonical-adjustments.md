# Ajustes canónicos tras la matriz WS06 (versión corregida)

Estado: aplicados en el plan (revisión 9 de `dag.yaml`) por la tarea `task-consolidar-ajuste-canónico-del-plan-workspace-tras-ws06`, según `runs/subagents/20261031-ajuste-canonico-ws06/review-source.md` (puntos A-F), que prevalece sobre la versión anterior de este archivo. La versión anterior era parcialmente errónea; su historia está en Git. Todo es planificación: nada está implementado ni aceptado, `execution_authorized` sigue en false y los reviews baratos de los nodos afectados quedan a cargo del Supervisor.

## 1. Precondición de escritura de payload (antes «CAS por hash»)

- Corrección: la versión anterior decía que «el CAS por hash no existe». Existe una capacidad optimista real: `expected` por valor en `POST /save` de sldb (HTTP 409, C-40) y `version`/`content_hash` publicado al leer (C-38). Lo que no está probado es una comparación o escritura pública con precondición compartida entre API, CLI y UI. No se infiere frescura por CLI.
- `brief.md`: el glosario distingue esas tres cosas.
- `dag.yaml`: WS12 define representación, precondición, operaciones y escritores alcanzados (sin forzar CAS en toda CLI ni un algoritmo; P03 no cambia). Nuevo nodo productor planificado WS45 (sldb, `depends_on` WS12, `requires` G_SLDB_WRITE y G_WRITE_CONTRACT), independiente de `source_mode`: primero reutilizar, pruebas reales focalizadas, código solo si al ejecutarlo falta capacidad. WS20 conserva raw-source. Gate técnico nuevo G_PAYLOAD_PRECONDITION (pending, `produced_by` WS45), exigido por los consumidores que guardan payload por campos: WS19, WS19.1, WS19.2 y WS21. Ningún lector se conecta.
- `reconciliacion.md`: C-41 reescrita; WS45 en la tabla de cobertura; WS20 queda solo con C-42.

## 2. Captura directa a drawer

- Corrección: la ausencia de un comando Deskops especializado no equivale a ausencia de primitiva pública. Existen `sldb.api.documents.create_document` y `DrawerService` (candidato TaskDoc, `deskops/services/drawer.py:261`).
- `dag.yaml` (WS12, WS25.2) y C-55: canal permitido de captura con origen preservado, sin tarea activa y colisiones controladas, pendiente del contrato WS12, que compara API SLDB existente, composición y eventual wrapper Deskops. No se crea API ni modelo por reflejo. `message send` más `promote` no queda aprobado (la promoción borra la nota, `why` apunta a una ruta borrada, hay fallo parcial por probar, y mete trabajo local en inbox). Productor Deskops explícito solo si falta conducta de workflow, antes de WS25.2; si la composición cumple, se documenta prueba y contrato.

## 3. ViewDoc y alcance de WS18

- Corrección: no falta una capacidad de portabilidad genérica. ViewDoc es datos sin ruta de store y `evaluate_view(store, view)` recibe el store por petición (graph_ui).
- `brief.md` y WS18: el modelo está en spec2viz; evaluador, rutas y render en graph_ui (solo local). C-50 pasa a delta de autoría de ViewDoc y NotationDoc concretos (WS09/WS11) y su comprobación sobre stores reales reutilizando C-37 y C-49; sin servicio, CLI ni runtime fuera de graph_ui, ni extracción del evaluador. `output_scope` `sldb/views/` con `output_base` spec2viz puede ser legítimo (`spec2viz/sldb/views/`): se confirma ruta y registro según contrato, sin cambiar dueño por el prefijo.

## 4. Texto «acepta por delta» de WS06 y Scion

- `dag.yaml` (WS06) y C-64: WS06 puede clasificar y conservar la descomposición sin ejecutar WS05; WS32 y WS33 conservan sus dependencias y gates canónicos. El acta es del receptor P01; WS11 y WS12 son fuente de contrato que solo enlaza. Sin firmas, gates ni recepción ficticia. «No designado en P01» para deskops es un dato de esa tabla, no un permiso que frene trabajo local.

## 5. Revisiones baratas invalidadas

Editar `brief.md`, `reconciliacion.md` y contratos invalida los `input_sha256` y `contract_sha256` de muchos nodos, más los nuevos o pendientes (WS45). El Supervisor congela y corre `context_review.py run --stale`; el Executor no lo ejecuta ni edita bloques `context_review` existentes. `validate_plan.py --check` falla hasta entonces solo por reviews vencidos.

## Considerados y descartados

- Sin cambio en `decisiones.md`, P01-P09 ni auditorías.
