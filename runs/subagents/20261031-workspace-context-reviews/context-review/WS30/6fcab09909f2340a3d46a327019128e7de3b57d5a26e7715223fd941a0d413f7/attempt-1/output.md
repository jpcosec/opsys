## REFORMULACION
**Propósito:** validar con una persona real la autoría y revisión manual del workspace, según el protocolo y los flujos UF01–UF05.
**Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/`, con plantillas/entradas WS17 validadas, paths/hashes y recorridos, trazable por WS43.
**Repo dueño:** `graph_ui`.
**Límites:** no declarar “ready” por tests; un fallo bloquea el gate y abre tarea en el nodo causal; no corregir otros repos ni inventar causalidad; una observación solo se registra.

## AMBIGUEDADES
1. **“los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08”**: WS30 no incluye WS08 en `depends_on` ni se suministra su guion. Obliga a inventar esos escenarios o a decidir si el nodo se bloquea por falta de un artefacto referenciado.
2. **“que supervisor receptor autorice diagnóstico antes de atribuir nodo”**: no se define quién es ese supervisor, cómo se designa ni por qué canal autoriza. Obliga a inventar actor y procedimiento para incidentes no aislados.

## DRY-RUN
**Lecturas previstas:** guía de revisión; nodo WS30 y vecinos WS17/21/22/23/24/25/26/28/42; brief, alcance, decisiones, cobertura, validacion-humana y user-flows.
**Cambios previstos:** ninguno ejecutable. Solo se generaría el acta manual y el recibo de `G_HUMAN_MANUAL`; no se toca código ni otros repos.
**Dependencias:** WS17 aporta plantillas; WS40 las materializa; WS21–26/28/42 aportan edición, navegación y cierre. `G_HUMAN_MANUAL` queda pendiente hasta el acta.
**Validaciones futuras:** recorridos UF01 con entradas WS17, UF02/03 edición/04/05; conflicto en dos ventanas; navegación por teclado; paths/hashes; registro de fallos y bloqueo del gate si el guion falla.

## FUTURO
WS30 produce el acta y satisface `G_HUMAN_MANUAL`; el responsable de `graph_ui` decide y abre tareas de corrección; un supervisor autoriza diagnóstico si la causa no está aislada. WS43 contrasta las entradas WS17 validadas para publicar navegación real; WS31 usa el acta para el manual. La aceptación humana y la atribución de fallos quedan fuera de este revisor.
