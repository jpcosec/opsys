## REFORMULACION
**Propósito:** encargo de planificación para que `graph_ui` implemente enrutamiento explícito de tareas en el Board y una representación de «capa lista».  
**Resultado:** UI en `frontends/mindmap/views/workspace/routing/` que añade la tarea a la lista `tasks` del BoardDoc mediante operación pública y muestra la capa lista separada de ejecución, dependencias pendientes y solapamientos.  
**Repo:** `graph_ui`.  
**Límites:** no ejecutar; no editar `status` para avanzar; promoción solo por canal autorizado del contrato WS12; si falta contrato/API/permiso, detenerse y registrar hueco según `alcance.md`; no diseñar el contrato aquí.

## AMBIGUEDADES
1. «sin archivos solapados según los `files` declarados en cada TaskDoc» y «archivos solapados» en acceptance. No se define contra qué conjunto se compara el solapamiento: otras tareas de la capa lista, tareas en ejecución, todo el Board o tareas futuras. Obliga a inventar el criterio de exclusión y, por tanto, el resultado de «capa lista».
2. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real». No queda claro si WS26.2 debe implementar una acción/UI de promoción o solo enrutar y declarar handoff; «estado real» no se define. Obliga a inventar alcance y aceptación observable.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (nodo WS26.2, aristas WS12/WS22/WS26.1, gates), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, guía; `task_file` no suministrado.  
**Cambios previstos:** vista de enrutamiento en `routing/` y `tests/`; cálculo/presentación de capa lista; ninguna escritura real.  
**Dependencias:** contrato/capacidades WS12; representaciones y lector WS22; TaskDoc autorado WS26.1; gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.  
**Validaciones futuras:** `deskops show board` muestra la tarea tras enrutar; distinción UI de tarea en ejecución; capa lista separada; promoción/handoff según contrato; pruebas con store temporal real o corpus WS40; acta `G_HUMAN_READ` en `graph_ui`.

## FUTURO
WS12 produce whitelist/canal/efectos y los gates `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16/actor humano produce `G_HUMAN_READ`; un externo resuelve `G_CLOSEOUT`; WS22 aporta Board/lector; WS26.1 aporta autoría; el TaskDoc de promoción fija archivos, textos y casos; las Pxx de `decisiones.md` no se resuelven aquí.
