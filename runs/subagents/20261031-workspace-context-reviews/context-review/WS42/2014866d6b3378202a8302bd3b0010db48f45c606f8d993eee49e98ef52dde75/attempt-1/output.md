REFORMULACION
Propósito: integrar en la UI de conocimiento de Mindmap las operaciones existentes de átomos (dividir/reunir) y tipado de protoátomos, con confirmación humana previa. Resultado: acciones de UF03 con persistencia, referencias y conflictos reales; materializaciones existentes inspeccionadas/validadas sin crear destinos; capacidades no soportadas declaradas no disponibles, sin simulación. Repo dueño: `graph_ui`, con salidas en `frontends/mindmap/views/workspace/knowledge/` y endpoints limitados a la whitelist de WS12. Límites: no generar destinos arbitrarios, no simular capabilities y no exceder el contrato de WS12.

AMBIGUEDADES
1. «con confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar». No se define qué compone “alcance” ni de dónde sale “procedencia”; el ejecutor tendría que inventar campos, fuente y criterio de presentación, y la aceptación quedaría no comprobable.
2. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea». No se identifica dónde está registrado ese modelo ni qué reglas determinan que una materialización sea válida o inválida; obligaría a inventar registro, versión y criterios de validación.

DRY-RUN
Lecturas: nodo WS42, guía, brief, alcance, decisiones, cobertura y contratos vecinos WS19/WS24/WS12/WS30/gates. Cambios previstos: ninguno; esta revisión no modifica archivos ni ejecuta tareas. Dependencias: WS19, WS24 y WS12; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Validaciones futuras: WS30 cubre UF03 mediante registro humano; el TaskDoc de promoción fijará archivos, escenarios y textos dentro de la aceptación.

FUTURO
WS12 produce la whitelist y el contrato de canales; WS24 aporta grafo, fuentes y procedencia; WS19 aporta edición/conflictos; WS16 resuelve G_HUMAN_READ; WS30 valida manualmente; la promoción y el TaskDoc concretan archivos y pruebas. Nada de esto es ambigüedad del encargo.
