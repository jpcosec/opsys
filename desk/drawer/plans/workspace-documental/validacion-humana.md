# Protocolo de uso y evidencia

Propuesta pendiente de P08. Participante: solicitante humano de esta sesión o persona explícitamente designada. Agente de pruebas prepara entorno y observa; no firma como usuario humano ni convierte screenshots en aprobación.

## Ejemplo reproducible

Proyecto Taller bajo graph_ui:.tmp/workspace-documental-ejemplo/, con su propio git y desk/store temporal creado por CLI real. Incluir Board, task, pill, ritual/step, átomo/protoátomo/crossroad, FAQ, issue Markdown no modelado y una referencia intencionalmente rota. Segundo desk temporal para UF08. Todo dato de prueba debe generarse por contratos reales cuando aplique, no mocks que sustituyan la API; sin secretos/corpus ajeno. No probar mutaciones sobre este desk de desarrollo. WS40 es el productor único del generador versionado y de los dos desks temporales. WS17 aporta solo plantillas de navegación authored bajo ejemplo/nav/; WS40 las materializa si se suministran.

## Gates por rebanada

- WS16: UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque. Encontrar un concepto desde entrada/búsqueda, abrir soporte, volver y cambiar representación con identidad; diagnosticar link roto y backend ausente. Necesita corpus WS40 y lectura multidesk WS41; no necesita edición, índices nuevos, Scion ni Changes global.
- WS30: UF02, UF03 edición, UF04, UF05. Capturar sin tarea obligatoria, preparar autoría/contexto y evidencia, provocar conflicto en dos ventanas, comparar diff real y cerrar por handoff autorizado externo. WS17 integra entradas/index authored en esta prueba; WS42 cubre operaciones de conocimiento. WS30 usa variante source_mode de P04, con fuente editable o explícitamente read-only según decisión.
- WS37: UF06 con Scion real e intervención humana; requiere G_EXEC. No se ejecuta solo porque el DAG está revisado.
- WS39: UF09 modelos; validar su prueba específica antes de etiquetar capítulo de personalización como disponible.
- WS29: UF07 impacto avanzado; prueba propia de mutaciones y soporte. Su ausencia no bloquea manual básico, que debe decirlo.

Las mutaciones de baseline requieren G_HUMAN_READ; las representaciones solo lectura pueden construirse en paralelo sin que eso implique aceptación humana.

## Evidencia y aceptación

Guardar guion, versiones/commits, corpus, comandos públicos, timestamps y resultados técnicos; grabación o capturas del recorrido; observaciones, fallos y decisión explícita del participante. La persona debe poder completar el guion sin rutas memorizadas ni instrucciones verbales correctivas del agente. Registrar ayudas solicitadas. Un fallo de recorrido bloquea el gate correspondiente y abre tarea de corrección, no solo un cambio de umbral.

Presupuestos propuestos (P08 debe confirmarlos): lectura/navegación local caliente p95 <=2 s, guardado local <=3 s; primer arranque <=10 s en corpus de ejemplo. Si una operación excede 1 s, estado de progreso visible sin afirmar éxito; registrar error/timeout. Medir al menos 20 aperturas, 10 búsquedas y 10 guardados sobre corpus y tamaño documentados; no extrapolar producción. Carga grande se reporta aparte.

## Qué significa disponible

Disponible y comprobado: versión/commit implementado, pruebas relevantes verdes, recorrido correspondiente aceptado y pasos del manual verificados en esa versión. Propuesto: intención/diseño sin esa evidencia. Bloqueado: dependencia o decisión identificada impide completarlo. Una tarea cerrada o un archivo existente no prueban por sí solos la etiqueta.

## Ubicación de evidencias

Las actas de WS16/30/37/39 viven en graph_ui:runs/subagents/workspace-documental-acceptance/{lectura,manual,delegacion,modelos}/acta.md (cada caso en su subdirectorio), no en el repo de planificación. WS43 guarda publicación real en deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md. Se pueden enlazar desde este plan; no copiarlas como segundo registro. output_base y output_scope de dag.yaml son autoridad de ubicación. El corpus tiene entrada mínima generada e instrucciones en WS40; WS16 no se reduce a buscar. WS30 prueba UF01 con las entradas enriquecidas de WS17.

La ubicación versionable no acredita que el acta esté versionada: incluirla explícitamente en el commit atómico de la tarea de validación del repo dueño. El recibo del gate debe enlazar ese commit y el blob de acta verificables; un archivo solo local o una captura no bastan.
