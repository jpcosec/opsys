## REFORMULACION
**Propósito:** que WS26.2 defina un encargo ejecutable para enrutar tareas en el Board y representar la capa lista, sin confundir enrutado con ejecución.
**Resultado:** UI de enrutamiento explícito mediante operación pública y vista separada de tareas listas frente a ejecución, dependencias pendientes o archivos solapados.
**Repo dueño:** `graph_ui`, en `frontends/mindmap/views/workspace/routing/`, endpoints del contrato WS12 y `tests/`.
**Límites:** no ejecutar; no sustituir workflow con drag-and-drop; promoción solo con contrato que resuelva commits previos por canal autorizado; gates y contrato pendientes.

## AMBIGUEDADES
1. **Criterio de solapamiento de archivos.** Cita: «sin archivos solapados según los `files` declarados en cada TaskDoc y el ritual de fase». No se define si «solapados» significa coincidencia exacta de ruta, misma carpeta, prefijo o glob. El ejecutor tendría que inventar el algoritmo de comparación, y con él qué tareas aparecen como no listas.
2. **Verificación de la promoción.** Cita: «el canal de promoción respeta commits previos y estado real». No se especifica qué commits previos, qué estado real ni cómo se comprueba en este nodo; la aceptación solo detalla el enrutado y la capa lista. El ejecutor tendría que inventar el comportamiento de promoción y su prueba, o declararlo fuera sin base explícita.

## DRY-RUN
**Lecturas previstas:** guía, `dag.yaml#node:WS26.2`, vecinos WS12/WS22/WS26.1, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.
**Cambios previstos:** componentes de enrutamiento y capa lista en `routing/`; tests de separación por dependencias/archivos; sin tocar nodos vecinos.
**Dependencias:** WS12 debe entregar whitelist/canal; WS22, representación de Board y estados; WS26.1, autoría previa. Gates `G_CLOSEOUT` bloqueado y `G_UI_WRITE`/`G_WRITE_CONTRACT` pendientes.
**Validaciones futuras:** `deskops show board` muestra la tarea enrutada; UI distingue enrutada de ejecución; capa lista separada; tests de dependencias y solapamiento; evidencia de contrato. Nada ejecutado.

## FUTURO
WS12 produce contrato/canal y resuelve la ambigüedad 2 si define promoción; el ritual de fase o WS07 deben fijar el criterio de solapamiento; WS07 designa responsables y `source_mode`; `G_CLOSEOUT` lo resuelve un actor externo; el TaskDoc de promoción fija archivos, textos y casos de prueba; WS16 aporta lectura humana.
