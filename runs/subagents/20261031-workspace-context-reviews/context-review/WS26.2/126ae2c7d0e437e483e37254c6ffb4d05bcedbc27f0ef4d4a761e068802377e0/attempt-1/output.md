## REFORMULACION
**Propósito:** revisar WS26.2 como encargo de planificación para enrutar tareas en el Board y representar la capa lista.  
**Resultado:** UI de enrutamiento explícito y vista separada de capa lista; tests en `graph_ui`.  
**Repo:** `graph_ui`, con endpoints autorizados por el contrato WS12.  
**Límites:** no ejecutar; no autoriza promoción, commits ni mutaciones UI sin `G_HUMAN_READ`; depende de WS12, WS22 y WS26.1; aceptación per_delta.

## AMBIGUEDADES
1. «sin archivos solapados según los `files` declarados en cada TaskDoc y el ritual de fase». No se define si “solapado” es igualdad de ruta, contención de directorio, glob o symlink, ni qué parte del ritual de fase fija el criterio. Obligaría a inventar la regla con la que se calcula y valida la capa lista.
2. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real». No queda claro si WS26.2 debe implementar una acción de promoción o solo mostrarla/bloquearla; obligaría a inventar si es salida propia y cuál es su resultado comprobable, aunque WS12 deba producir el contrato.

## DRY-RUN
**Lecturas:** nodo, guía, brief, alcance, decisiones, dag, contrato WS12, salidas de WS22/WS26.1, BoardDoc/TaskDocs y estado deskops.  
**Cambios previstos:** vistas/componentes de enrutamiento y capa lista en `frontends/mindmap/views/workspace/routing/`, más tests; sin ejecución ni escritura.  
**Dependencias:** WS12 para operaciones/whitelist; WS22 para Board; WS26.1 para autoría; gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.  
**Validaciones futuras:** `deskops show board` muestra la tarea enrutada; UI la separa de ejecución, dependencias pendientes y solapamientos; tests de contrato y recibos per_delta.

## FUTURO
WS12 debe publicar contrato/whitelist; WS16 produce el acta de `G_HUMAN_READ`; WS22 y WS26.1 aportan sus salidas. La aceptación humana per_delta y la autorización de promoción quedan fuera de este nodo; el TaskDoc de promoción fijará archivos, escenarios y textos.
