## REFORMULACION
**Propósito:** implementar en `graph_ui` la autoría explícita de un candidato del drawer como TaskDoc, con evidencia declarada, dependencias y contexto/pills vinculados, sin avanzar estado.
**Resultado:** el candidato queda autorado y visible tras recargar, con sus vínculos.
**Repo dueño:** `graph_ui`.
**Límites:** solo `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`; no editar `status` para avanzar; si una operación Git carece de contrato o dueño, handoff explícito y no disponible. Requiere WS12, WS22 y los gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. **“el candidato queda autorado con evidencia declarada”**: no se define qué constituye evidencia, quién la declara ni cómo se comprueba su validez. Obliga al ejecutor a inventar campos, formato y criterio de aceptación de la evidencia. G_CLOSEOUT habla de evidencia de closeout, no necesariamente de la evidencia de autoría.
2. **“dependencias y binding de contexto/pills”**: no se aclara si “dependencias” son las `depends_on` del TaskDoc, contra qué fuente se validan ni qué “contexto” debe vincularse. Obliga a inventar el modelo de relación y su validación. (Los “pills” quedan fuera por la guía; el “contexto” no está definido en el glosario.)
3. **“visibles tras recargar”**: no se especifica si la recarga es de la vista, del desk o del TaskDoc, ni qué debe persistir exactamente. Obliga a inventar el alcance de la comprobación de persistencia.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS26.1, WS12, WS22, WS26, WS26.2, gates), `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; sin ejecutar comandos.
**Cambios previstos:** UI de autoría en `authoring/` y tests; no se tocan otros scopes ni se implementa promoción no autorizada.
**Dependencias:** WS12 debe producir whitelist/capabilities y aceptar G_UI_WRITE/G_WRITE_CONTRACT; WS22 aporta Board; G_CLOSEOUT y G_HUMAN_READ deben estar satisfechos antes de ejecutar.
**Validaciones futuras:** UF04 sobre TaskDoc real; recarga conserva evidencia, dependencias y pills; no se edita `status`; Git sin contrato queda como handoff; pruebas en `tests/` con corpus WS40 cuando exista.

## FUTURO
WS12 define operaciones, actor y efectos; WS22 entrega la representación del Board; WS16 produce la aprobación humana de lectura; el solicitante resuelve P01/P03–P06/P08 y designa responsables; la promoción fija TaskDoc, archivos, pills y escenarios; WS26.2 enruta en Board; WS27/28 cubren cierre. Nada de ello se decide aquí.
