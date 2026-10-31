## REFORMULACION
Propósito: implementar en `graph_ui` el enrutamiento explícito de tareas en el Board y una vista de “capa lista” basada en dependencias y solapamiento de `files`. Resultado: tras enrutar, `deskops show board` muestra la tarea y la UI separa capa lista, ejecución, dependencias pendientes y solapamientos. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/routing/` y `tests/`. Límites: no implementar promoción nueva; usar solo una operación completa admitida por WS12 o dejar handoff/pendiente; no editar `status`; no marcar lista con globs dudosos ni heurística optimista.

## AMBIGUEDADES
1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista». No se define quién es el “supervisor”, por qué canal revisa ni qué evidencia deja. Para cerrar la aceptación de esos casos, el ejecutor tendría que inventar el actor, el registro de la revisión y su efecto sobre el estado mostrado.

## DRY-RUN
Lecturas previstas: este nodo, su TaskDoc, el contrato WS12, la representación/lifecycle de Board de WS22, las salidas de autoría de WS26.1 y el ritual de fase vigente. Cambios previstos: componentes de routing y capa lista, llamadas a endpoints autorizados por WS12 y tests; ninguna promoción nueva. Dependencias: WS12, WS22 y WS26.1; gates por delta (`G_UI_WRITE`, `G_WRITE_CONTRACT`) y `G_HUMAN_READ` para uso de mutaciones en UI. Validaciones futuras: `deskops show board` refleja la tarea enrutada; la UI distingue capa lista de ejecución, dependencias pendientes y archivos solapados; igualdad/contención de directorios cuentan como solapamiento; glob dudoso queda “no comprobado”; contrato ausente produce handoff. Sin ejecutar nada.

## FUTURO
WS12 debe producir el contrato de operación pública, campos y normalización de `files`; WS22 aporta la lectura real de Board/lifecycle; WS26.1 aporta la autoría previa. La aceptación por delta y el acta de lectura corresponden al receptor humano (`G_UI_WRITE`, `G_HUMAN_READ`). La designación concreta del supervisor, si se mantiene ese requisito, es una decisión humana posterior.
