REFORMULACION
Propósito: revisar si WS26.1 se entiende como encargo de planificación. Resultado: autorar desde un candidato del drawer una tarea con evidencia declarada, dependencias y pills de contexto vinculadas, visibles tras recargar. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/authoring/`, endpoints que autorice WS12 y `tests/`. Límites: no editar status para avanzar; si una operación Git carece de contrato/dueño, handoff y no disponible. No evalúo producto ni ejecuto; uso los bloques edge solo como contexto.

AMBIGUEDADES
1. «Autoría explícita desde candidato, evidencia declarada...» / «con evidencia declarada». G_CLOSEOUT describe evidencia de closeout; no se aclara si aquí se declara la evidencia esperada al crear la tarea o se escribe el artefacto de cierre. Obligaría a inventar el momento y el contenido de esa evidencia.
2. «Si una operación Git no tiene contrato o dueño...». El alcance de WS26.1 no menciona Git y P05 establece que guardar no hace commit; no se identifica qué operación Git aparecería al autorar. Obligaría a inventar si el nodo debe implementar/handoff de Git o si la cláusula es heredada del agregado.

DRY-RUN
Lecturas: dag.yaml (WS26.1, WS12, WS22, gates), brief.md, alcance.md, decisiones.md, cobertura.md. Cambios previstos: vista de autoría en graph_ui, llamadas a endpoints WS12, pruebas en `tests/`. Dependencias: contrato WS12, vista TaskDoc/pills de WS22, G_CLOSEOUT satisfecho, G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT pendientes. Validaciones futuras: UF04 sobre TaskDoc real, persistencia tras recarga, prohibición de avanzar editando status, comprobación de handoff. Sin ejecutar.

FUTURO
WS12 produce el contrato/whitelist y endpoints; WS22 la vista de TaskDoc/pills; WS16 el acta G_HUMAN_READ; el receptor P01 acepta G_UI_WRITE por delta; WS26.2 enruta en Board y muestra capa lista; la promoción sigue su autorización. Nada de esto es ambigüedad de WS26.1.
