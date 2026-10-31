# Plan final del workspace documental

Este paquete termina la planificación; no entrega producto ni activa ejecución. `dag.yaml` mantiene `execution_authorized=false`; las fichas generadas siguen `candidate`, no son TaskDoc. Reviews baratos prueban comprensión de cada encargo, y el concilio y Tester emiten dictámenes separados. Ningún resultado sustituye promoción, pruebas reales ni aceptación humana del producto.

La base acordada es extender Mindmap con SLDB/pron y Deskops, lectura y operación manual primero, sin migración Kimun. Markdown será editable después de probar API reversible, conflictos, recuperación y campos protegidos; guardar no hace commit. Con otro coordinador escritor, la UI permanece en lectura/handoff hasta canal público coordinado real. El solicitante es responsable de producto/recepción de deltas en graph_ui, SLDB y spec2viz, y participante de Taller con objetivos abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s. Las tres respuestas exactas, fecha, actor y origen están en decisiones.md y owner-decisions.json del run. P07/P09 son defaults técnicos delegados documentados, sin firma humana inventada.

## Qué existe y qué queda

Workspace no es draft: a1b2b22 implementa lector IR/payload, catálogo modelado, contexto, grafo 1–2 hops, Code seguro e historia URL; f16fcd1 registra cierre y 134a665 reconcilia Board. `reconciliacion.md` delimita cada delta WS13/hijos, WS14/15/19/22–24/27–29/32. Faltan comprobaciones ampliadas como Markdown no modelado/fuente, explorador, pestañas documentales/splits, búsqueda backend, editores con conflicto, diff/evidencia y recorridos completos. Editing y Changes siguen drafts con hashes actuales. No volver a implementar base ni asumir que todos esos deltas estén aceptados por existir un commit.

Brief/glosario WS01 ya están documentados en esta tarea y tienen recibo de cobertura en DAG. La parte de decisión de WS07 también está cubierta por respuestas humanas y mapeo Pxx; resta verificar su aplicación contra auditorías/matriz WS06, sin volver a preguntar lo decidido. Cobertura documental no afirma lifecycle de candidatas cerrado. Inventarios amplios WS02–04 y matriz/contratos WS06/08–12 aún deben ejecutarse como tareas propias; esta auditoría acotada no los sustituye.

G_CLOSEOUT depende de evidencia focalizada actual del contrato de evidencia declarada y vínculo exacto task→commit, con recibos históricos verificables; no exige un nuevo sistema de autenticación. Su estado/recibo exacto en DAG es autoridad. Gate satisfecho no convierte verify en ejecutor de tests ni demuestra funcionalidad del workspace. Riesgos de suite histórica se registran sin afirmar suite global verde ni arreglar producto.

## Secuencia por entregas

1. Verificar cobertura documental WS01 al preparar el trabajo; promover auditorías pendientes WS02–04 con archivos, pills/átomos y validación. WS05 inventario Scion es ramal posterior y no bloquea núcleo. Consolidar WS06 y comprobar registro WS07 reutilizando las decisiones dadas; WS08–12 concretan flows/vistas/manual/identidad/operaciones sobre APIs reales.
2. Entrega L: recepción de cada delta lector, base reutilizada y deltas WS13–15, corpus Taller WS40, multidesk read-only WS41 y recorrido humano WS16. Ninguna dependencia de edición, Changes, modelos, Scion o ViewDoc opcional.
3. Entrega M: whitelist y recepción por delta/efecto, campos/conflictos WS19, raw-source WS20/G_SOURCE y WS21, representaciones WS22–24, captura WS25, autoría WS26, diff/evidencia WS27, cierre por handoff WS28, conocimiento WS42. Desarrollo/pruebas aisladas de API pueden avanzar con sus contratos; habilitar mutaciones en UI requiere G_HUMAN_READ. WS17 aporta entradas authored; WS30 acepta el recorrido, WS43 publica entradas reales y WS31 el manual con evidencia.
4. Extensiones independientes: WS18 ViewDoc/spec2viz se recibe por su propio delta y se añade sin bloquear navegación base WS24. WS29 Changes y WS39 modelos tienen pruebas/etiquetas propias. Sus capítulos permanecen propuestos hasta evidencia, sin frenar manual básico.
5. Ramal E posterior: WS05/44 inventario y probe real, operador/acceso designados al abordarlo, G_SCION; WS32–38 intento/trazabilidad/acciones/UI y aceptación con permisos explícitos G_EXEC. Ninguna respuesta de núcleo concede esos permisos ni autoriza mensajes.

## Primera capa preparable y responsables

La verificación semántica distingue dependencias documentadas de tareas cerradas: WS01 está cubierto por el brief actual (hash/recibo), no se reescribe. La primera capa real preparable del núcleo es WS02, WS03 y WS04; WS05 puede prepararse separadamente como inventario posterior sin acceso obligatorio. Revisar no solapamiento, fuentes actuales, recepción y gates antes de authorar TaskDoc en repo dueño; ninguna ficha por sí sola permite ejecutar. La salida de validate_plan.py informa esta preparación, nunca autorización de producto.

El solicitante decide producto y acepta alcance por delta. Supervisor del repo dueño promueve la TaskDoc completa; Executor produce pruebas/código/contratos; el receptor registra acta técnica por IDs/efecto/fecha/commit en su repo. Humano participante acepta recorridos Taller: agentes preparan y miden, no firman como usuario. Supervisor integra/cierra tareas/fases y conserva Tester independiente; Scion requiere operador y permisos futuros expresos.

## Manual, vistas, recorridos y evidencia

`borradores/vision.md`, `user-flows.md`, `vistas.md` y `manual.md` son contratos por contrastar, no manual de un producto disponible. `cobertura.md` traza UF01–10; `validacion-humana.md` fija Taller, dos desks y repo sin desk, mediciones y actas por rebanada. WS09 cataloga vistas, WS11/12 contratos, WS31 publica solo pasos comprobados y WS38 añade delegación demostrada. Actas humanas y recepción viven en repo dueño con commit/blob; este paquete guarda planificación y enlaces. Cualquier capacidad desconocida se clasifica y asigna a productor/repositorio antes de implementar, sin workaround.

Para empezar producto faltan tareas activas completas, auditorías/contratos actuales, recepción y pruebas del delta concreto, gates aplicables, capa sin solapamiento y ejecución/testing/cierre explícitos. `G_PRODUCT` y `G_WRITE_POLICY` solo registran acuerdos. `G_SOURCE`, actas de lectura/manual/modelos/delegación, contratos técnicos y permisos siguen exactamente el estado del DAG. No se anuncia producto disponible por terminar este plan.
