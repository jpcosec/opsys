REFORMULACION
Encargo agregado de planificación: integrar autoría explícita desde candidato, evidencia declarada, dependencias y contexto/pills, y enrutamiento en Board con representación de capa lista; la promoción queda supeditada a contrato autorizado. Resultado: agregado de salidas de WS26.1 y WS26.2; WS26 no se ejecuta y cierra cuando ambos hijos cumplen su aceptación. Repo dueño: `graph_ui`. Límites: no confundir ruta Board con ejecución; no autoriza promoción ni commits; `promotion: not_authorized`; requiere gates y contrato WS12.

AMBIGUEDADES
1. «representación de capa lista por dependencias/no solapamiento». No se define qué es «capa lista» ni el criterio de «no solapamiento». Obligaría a inventar si es frontera de dependencias, conjunto de tareas sin archivos comunes u otra vista, y cómo comprobarlo.
2. «Autoría explícita desde candidato». Las fuentes suministradas no definen «candidato» como entidad, origen ni transición. Obligaría a inventar si es tarea borrador, registro de intake, nodo del DAG u otro soporte, y qué operación de autoría se espera.
3. «El canal de promoción debe respetar commits previos y estado real». No concreta qué commits previos ni cómo se verifica «estado real». WS12 es dependencia, pero el nodo no declara explícitamente que ese criterio queda delegado ni qué hacer si el contrato no lo cubre.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS26, hijos, gates), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`. Cambios previstos: ninguno por WS26; solo agregará salidas de WS26.1/2 cuando existan. Dependencias: WS12 (contrato), WS22 (Board), WS26.1 y WS26.2; gates `G_CLOSEOUT` blocked y `G_HUMAN_READ`/`G_UI_WRITE`/`G_WRITE_CONTRACT` pending. Validaciones futuras: aceptación de ambos hijos, evidencia de gates, preflight task-only, no solapamiento y respeto de commits/estado; WS30 valida manualmente. Sin ejecutar.

FUTURO
Humano/WS07 resuelve P01 y P03–P06 y designa responsables; WS12 produce whitelist/contrato y acepta deltas; WS16 emite `G_HUMAN_READ`; WS22 entrega Board; WS26.1/2 implementan; WS30 registra validación humana; WS43 publica entradas reales. La autorización de promoción y commits corresponde a humano/canal externo, no a WS26.
