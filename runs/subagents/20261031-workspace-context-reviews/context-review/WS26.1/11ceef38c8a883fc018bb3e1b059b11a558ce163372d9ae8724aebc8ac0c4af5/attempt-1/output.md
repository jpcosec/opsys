REFORMULACION
Propósito: planificar en graph_ui la autoría explícita de un candidato del drawer como TaskDoc, con evidencia declarada, dependencias y pills de contexto vinculadas y persistentes, sin avanzar status. Resultado: superficie de authoring y tests en `frontends/mindmap/views/workspace/authoring/`, usando solo el canal/endpoints que fije WS12. Repo dueño: graph_ui. Límites: no promoción propia, no commit/closeout, no editar status, no inventar API; si falta contrato o dueño Git, handoff y operación no disponible.

AMBIGUEDADES
1. «con evidencia declarada, dependencias y pills de contexto vinculadas y visibles tras recargar»: no se define si un candidato sin evidencia o sin dependencias puede autorarse; la aceptación parece exigir ambos. Obligaría a inventar la fuente de esos valores y su obligatoriedad. El formato de pills no cuenta —queda al TaskDoc—, pero la regla de aceptación de evidencia/dependencias sí.
2. «Si una operación Git no tiene contrato o dueño, la acción queda en handoff explícito»: no se nombra qué operación Git pertenece a este nodo. Obligaría a inventar si «declarar evidencia» incluye preparar commit, solo registrar evidencia o handoff, con riesgo de exceder el límite de no commits/promoción.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo WS26.1 con vecinos WS12/WS22. Cambios previstos: UI de authoring en graph_ui, llamadas al adaptador autorizado por WS12 y tests; sin tocar status ni promoción. Dependencias: contrato WS12 por delta (G_WRITE_CONTRACT), representación WS22, G_CLOSEOUT satisfecho; G_HUMAN_READ y G_UI_WRITE pendientes por delta. Validaciones futuras: UF04 sobre TaskDoc real, recarga, visibilidad de evidencia/dependencias/pills, handoff Git, tests aislados con store temporal o corpus WS40 y acta del receptor.

FUTURO
WS12 debe publicar contrato/adaptador y campos por delta; WS22 aporta Board y representación; el receptor P01 emite el acta G_UI_WRITE; WS16 produce G_HUMAN_READ; el TaskDoc de promoción fija archivos, textos y casos; un humano decide la promoción. Nada se ejecuta aquí.
