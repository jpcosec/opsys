**REFORMULACION**
Propósito: validación humana temprana de lectura y descubrimiento (UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura, UF10 arranque). Resultado: acta de recorrido con guion, versiones, corpus, comandos, tiempos, evidencias y decisión explícita del participante. Repo dueño: `graph_ui`; salida en `runs/subagents/workspace-documental-acceptance/lectura/`. Límites: no crea corpus propio (consume WS40), no implementa correcciones, no muta entre desks, no sustituye la aprobación humana y no habilita mutaciones de UI: `G_HUMAN_READ` es `enable_ui_use_only`.

**AMBIGUEDADES**
1. «supervisor del repo receptor atribuye el fallo por evidencia»: no se identifica quién es, cómo se designa ni dónde registra la atribución; obliga a inventar actor, canal y formato.
2. «revisión explícita del objetivo por humano con razón/evidencia»: no fija qué humano decide ni dónde se asienta esa revisión; obliga a inventar autoridad y registro.

**DRY-RUN**
Leería guía, brief, alcance, decisiones, cobertura, protocolo, user-flows y el nodo. Consumiría el manifiesto de WS40 (roots, stores, commits, documentos clave, segundo desk y repo sin desk), las operaciones de búsqueda de WS14, los errores/degradación de WS15.1, la orientación sin desk de WS15.2 y la lectura multidesk de WS41. Prepararía Taller sin tocar el desk real; ejecutaría con el humano UF01, UF03 lectura, UF07 (link roto/backend ausente), UF08 (dos stores, sin mutación) y UF10 (arranque/ausencia de desk). Mediría ≥20 aperturas y 10 búsquedas, p95 ≤2 s y arranque ≤10 s; no guardaría. Registraría ayudas, fallos, tiempos y pruebas técnicas por separado, y guardaría/commitearía el acta en `graph_ui` enlazando commit y blob. Validaría que el humano completó el recorrido sin instrucciones verbales correctivas y que los estados de error son visibles. Ante fallo: registraría incidente/diagnóstico sin implementar; el gate seguiría pendiente. Errores esperados: manifiesto WS40 incompleto, segundo desk o WS41 ausentes, backend 503, timeout, participante no disponible.

**FUTURO**
El supervisor del repo receptor atribuye fallos y abre corrección; el humano decide si revisa un objetivo P08; WS30 consume la aceptación de lectura; el acta commiteada resuelve `G_HUMAN_READ`.
