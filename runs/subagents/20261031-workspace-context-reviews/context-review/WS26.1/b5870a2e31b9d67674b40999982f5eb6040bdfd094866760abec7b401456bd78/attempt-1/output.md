## REFORMULACION
**Propósito:** implementar en `graph_ui` la autoría explícita desde un candidato del drawer, con evidencia declarada, dependencias y pills de contexto.  
**Resultado:** un TaskDoc real de UF04 queda autorado, con evidencia, dependencias y pills vinculadas y visibles tras recargar; las operaciones Git sin contrato o dueño quedan en handoff y no disponibles.  
**Repo:** `graph_ui`; alcance en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`.  
**Límites:** no editar `status` para avanzar; no inventar contrato, dueño ni promoción; respetar gates por delta y reglas comunes si falta una dependencia.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas:** nodo WS26.1 y gates; brief, alcance, decisiones, cobertura y guía.  
**Cambios previstos:** módulo de autoría en la UI y pruebas; invocación de endpoints definidos por WS12. Sin ejecución.  
**Dependencias:** contrato de operaciones WS12; representación de Board/TaskDoc WS22; `G_CLOSEOUT` satisfecho; `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` pendientes por delta.  
**Validaciones futuras:** UF04 sobre TaskDoc real; persistencia tras recarga; evidencia, dependencias y pills visibles; `status` sin modificar; handoff explícito ante operación Git sin contrato/dueño; recibos de gates aplicables.

## FUTURO
- WS12 produce el contrato técnico y la whitelist de operaciones.
- WS22 entrega la representación navegable del Board y TaskDoc.
- WS16 produce el acta humana de lectura para `G_HUMAN_READ`.
- El receptor P01 emite el acta por delta para `G_UI_WRITE`.
- La promoción fija archivos, pills, átomos, evidencia y escenarios de prueba.
- WS40 aporta el corpus para validaciones humanas.
