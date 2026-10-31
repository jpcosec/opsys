## REFORMULACION

WS16 es un nodo de **validación**, no de implementación. **Propósito**: ejecutar el gate humano temprano de lectura y descubrimiento para UF01, UF03 (lectura), UF07 (diagnóstico), UF08 (lectura entre desks) y UF10 (arranque/ausencia de desk). **Resultado**: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`, con actor, versión, guion, resultado y evidencias, que resuelve `G_HUMAN_READ`. **Repo dueño**: `graph_ui`. **Límites**: consumir el manifiesto de WS40 sin crear corpus propio; solo lectura, sin mutación interdesk ni guardados; el agente prepara y observa, no aprueba; la edición no se valida hasta WS30.

## AMBIGUEDADES

1. «Incluye UF10 arranque/ausencia de desk» junto a «sin crear corpus propio», frente a WS40 («Crear dos repos temporales… sus stores») y validacion-humana («Proyecto Taller… con su propio git y desk/store temporal»; «Segundo desk temporal para UF08»). El corpus descrito no contiene un proyecto sin desk. El ejecutor tendría que inventar/crear ese fixture —corpus propio— o decidir omitir UF10; ninguna de ambas está autorizada.

## DRY-RUN

**Lecturas previstas**: dag.yaml (WS16 y aristas WS14/15/08/40/41, sin revisarlas), guía, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y `task-ws16.md`. **Cambios previstos**: ninguno de código; producir el acta en `lectura/` y, si hay fallo, abrir corrección. **Dependencias**: manifiesto WS40, lectura multidesk WS41, búsqueda WS14, errores/orientación WS15 y criterios WS08. **Validaciones futuras**: recorrido humano, tiempos y pruebas técnicas separadas, decisión explícita; `G_HUMAN_READ` queda pendiente hasta el acta versionada.

## FUTURO

El humano designa participante y confirma P08 (presupuestos); WS40 produce corpus/manifiesto; WS17 enriquece índices; WS30 ejecuta guardados/edición; WS43 publica navegación real. `G_HUMAN_READ` habilita mutaciones posteriores; un fallo abre tarea de corrección, no un cambio de umbral.
