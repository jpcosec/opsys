## REFORMULACION
Revisar WS24 como encargo de planificación: integrar conocimiento y grafo local reutilizando el grafo actual y una vista de documento genérica. Resultado esperado: propósito, alcance y aceptación comprobables. Repo dueño: `graph_ui`; salida acotada a `frontends/mindmap/views/workspace/graph/; Context; tests/`. Límites: no ejecutar, no evaluar el producto, no revisar los bloques `edge` de vecinos, no dar por aprobados gates ni propuestas Pxx.

## AMBIGUEDADES
1. «Vecindad = hasta 2 hops» y «la vecindad de hasta 2 hops». No indica dirección ni tipos de relación: ¿entrantes, salientes o ambas? Obliga a inventar el criterio de recorrido y qué validar.
2. «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» frente a «La vista muestra la clasificación (tipo y tags)» y «un soporte no modelado (Markdown sin modelo)». No queda definido qué clasificación mostrar sin modelo, ni si los tags provienen del modelo o del documento. Obliga a inventar representación y fuente.
3. «preservar Code local del ticket workspace en draft que identifique el acta WS11» figura en `scope`, pero no en `acceptance`. El ejecutor tendría que inventar cómo preservarlo, cómo verificarlo y qué significa identificar el acta.

## DRY-RUN
Lecturas previstas: input completo —guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS24—; los bloques de vecinos solo como contratos. Cambios previstos: ninguno; esta revisión no modifica archivos. Dependencias declaradas: WS13 y WS18; gate `G_UI_READ` pendiente; artefacto de WS03 `auditoria/infraestructura.md`; modelo `deskops/models/materialization.py` como referencia. Validaciones futuras: WS30 (recorrido manual UF03), consumo por WS29/WS42 y TaskDoc de promoción fijando archivos y pruebas.

## FUTURO
WS11 produce el acta de `G_UI_READ`; WS03 la auditoría de grafo; WS18 los ViewDoc; WS07 designa responsables; el humano resuelve Pxx y autoriza promoción. WS30 valida manualmente. Nada de esto se ejecuta ni se aprueba aquí.
