## REFORMULACION

**Propósito:** validar con una persona humana el recorrido temprano de lectura y descubrimiento del workspace documental.

**Resultado:** acta de aceptación en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`, con recorrido, tiempos, pruebas técnicas y resultado humano.

**Repo dueño:** `graph_ui`, con `output_scope` en `runs/subagents/workspace-documental-acceptance/lectura/`.

**Límites:** no crea corpus propio; consume el manifiesto de WS40. No muta el baseline ni autoriza edición; las representaciones read-only pueden avanzar en paralelo sin aceptación. El agente no sustituye la aprobación humana.

**Dependencias:** WS14 (búsqueda), WS15 (errores/modo degradado y orientación sin desk), WS08 (user-flows), WS40 (corpus y manifiesto), WS41 (lectura multidesk). Produce `G_HUMAN_READ`.

**Aceptación:** recorrido UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque; medir aperturas y búsquedas; guardados no aplican.

## AMBIGUEDADES

1. **Cita:** «Fallos abren correcciones antes de edición».
   **Qué obligaría a inventar:** el input no identifica quién registra la corrección, en qué repo, con qué formato ni si WS16 debe crearla o solo reportarla. El ejecutor tendría que decidir alcance y destino de esas correcciones.

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y definiciones DAG de WS16, vecinos y gate.

**Cambios previstos:** ninguno; esta revisión no ejecuta ni modifica el plan.

**Dependencias:** WS14 aporta búsqueda; WS15 errores y orientación; WS08 flujos observables; WS40 corpus, manifiesto e instrucciones; WS41 segundo desk. `G_HUMAN_READ` queda pendiente hasta el acta.

**Validaciones futuras:** ejecutar el protocolo sobre el corpus WS40; comprobar entrada, enlaces, búsqueda, diagnóstico de link roto/backend ausente, lectura del segundo desk y ausencia de desk; registrar tiempos y pruebas por separado; versionar el acta en el commit atómico del repo dueño.

## FUTURO

- P08 debe fijar participante y presupuestos.
- WS40 debe producir corpus y manifiesto.
- WS41 debe habilitar lectura entre desks.
- WS14/WS15 deben estar implementados y verificables.
- La promoción debe precisar archivos, pills, átomos y TaskDoc.
- Un humano decide la aprobación del gate y, si hay fallos, el destino de las correcciones.
