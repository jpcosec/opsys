## REFORMULACION
**Propósito:** proponer una matriz que corresponda las implementaciones/deltas del plan con el trabajo ya existente en sus repos dueños, clasificando cada caso como ya cubierto, extensión de ticket o nuevo delta.  
**Resultado:** `reconciliacion.md` actualizado con esa matriz y el responsable todavía por designar.  
**Repo:** `deskops` (`owner_repo`).  
**Límites:** no notificar, despachar ni modificar el Board de `graph_ui`; no producir gates ni aprobar deltas no definidos. La designación corresponde a WS07 y la aceptación específica a WS11/12.

## AMBIGUEDADES
1. **Alcance de la matriz frente a Scion.** Cita: «Una matriz por implementación: ya cubierto, extender ticket existente o nuevo delta». `reconciliacion.md` incluye la línea «Scion RunDoc/cierre | WS32/33», pero WS06 solo depende de WS02–WS04. Si la matriz abarca esa línea, el ejecutor tendría que inventar la correspondencia o decidir omitirla sin inventario previo. Falta WS05 como dependencia explícita o una exclusión expresa.
2. **Criterio de «ya cubierto».** Cita: «ya cubierto». No se define si significa cubierto por código existente, por una tarea del Board o por una capacidad ya planificada. El ejecutor tendría que inventar el criterio de clasificación.
3. **Unidad de fila.** Cita: «Una matriz por implementación». No queda fijado si cada fila es un nodo del DAG, una capacidad, un ticket existente o un delta. El ejecutor tendría que inventar la granularidad.

## DRY-RUN
**Lecturas previstas:** `auditoria/deskops.md` (WS02), `auditoria/infraestructura.md` (WS03), `auditoria/ui.md` (WS04), `reconciliacion.md`, `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md` y `cobertura.md`.  
**Cambios previstos:** editar únicamente `reconciliacion.md` para incorporar o ajustar la matriz; no tocar Boards, tareas externas ni código.  
**Dependencias:** WS02–WS04; hueco posible respecto de WS05; designación en WS07; aceptación en WS11/12.  
**Validaciones futuras:** comprobar que cada fila tenga soporte citado, clasificación y responsable «por designar»; confirmar que no se generan gates ni aprobaciones.

## FUTURO
WS07 designa con identidad a los responsables de `graph_ui`, `sldb`, `spec2viz` y Scion, y confirma o corrige P01–P09. WS11/12 obtienen la aceptación específica por repo receptor. El humano dueño del producto decide las propuestas pendientes; WS06 no las aprueba.
