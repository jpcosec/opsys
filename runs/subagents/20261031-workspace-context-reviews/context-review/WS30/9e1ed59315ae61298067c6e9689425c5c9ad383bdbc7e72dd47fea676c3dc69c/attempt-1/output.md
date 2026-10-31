## REFORMULACION
Propósito: validar humanamente el recorrido de autoría y revisión manual del workspace documental: UF02, UF03 edición, UF04 y UF05, más UF01 con entradas authored de WS17 materializadas por WS40. Resultado: acta humana bajo protocolo en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, que resuelve `G_HUMAN_MANUAL`; un fallo bloquea el gate y abre tarea en el nodo causal. Repo dueño: `graph_ui`; `output_scope`: `runs/subagents/workspace-documental-acceptance/manual/`. Límites: nodo de validación, no implementación; no llamar ready por tests; una observación solo se registra; `promotion: not_authorized`. No se ejecutó nada.

## AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08»: el `depends_on` de WS30 no incluye WS08 ni se aporta su guion. Obliga a inventar esos escenarios o a asumir que WS08 estará disponible sin dependencia declarada.
2. «abre tarea en el nodo que lo causó»: no hay criterio para atribuir un fallo a un nodo cuando afecta a varios o su causa no es inequívoca. Obliga a inventar la atribución y el destino de la tarea.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, validación humana, user-flows y contratos de WS17/21/22/23/24/25/26/28/42. Cambios previstos por este revisor: ninguno. En una futura ejecución se generaría el acta y, si procede, una tarea de corrección. Dependencias a comprobar: corpus WS40 vía WS17, variante `source_mode` de WS21, capacidades de WS22–WS26/28/42 y protocolo de validación. Validaciones futuras: recorrido humano, evidencia versionada, acta enlazada y resolución del gate.

## FUTURO
WS07/humano debe resolver P04/P08 y designar participantes; WS40 produce el corpus; WS08 debería producir el guion referido; WS17 aporta entradas; WS21–WS26/28/42 producen las capacidades recorridas; la persona participante firma el acta; WS30 resuelve `G_HUMAN_MANUAL`.
