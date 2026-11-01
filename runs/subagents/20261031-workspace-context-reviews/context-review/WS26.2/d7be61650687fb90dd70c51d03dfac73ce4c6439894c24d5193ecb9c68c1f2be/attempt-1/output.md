REFORMULACION
Propósito: implementar en graph_ui el enrutamiento explícito de tareas en Board y la representación de capa lista. Resultado: tarea añadida a `tasks` del BoardDoc por operación pública; UI muestra la capa lista separada de ejecución, dependencias pendientes y solapes; promoción solo mediante operación completa admitida por WS12, o handoff. Repo: graph_ui. Límites: no crear promoción ni endpoints, no editar status, no drag-and-drop de workflow, no sustituir contratos ausentes; gates y aceptación del nodo.

AMBIGUEDADES
1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista»: no se define quién es el supervisor ni el canal/registro de esa revisión; obligaría a inventar actor y evidencia.
2. «según los `files` declarados en cada TaskDoc y el ritual de fase»: no fija qué hacer si un TaskDoc no declara `files` o el ritual no cubre el caso; obligaría a inventar si se considera sin solape o no comprobado.

DRY-RUN
Leería el nodo, contrato WS12, salidas de WS22/WS26.1, API/Board/lifecycle de deskops, `files` y ritual. Crearía vista en `frontends/mindmap/views/workspace/routing/`, llamadas a endpoints autorizados y tests. Consumiría G_CLOSEOUT satisfecho; G_HUMAN_READ pendiente habilita solo desarrollo/pruebas aisladas, no uso de mutaciones UI; G_WRITE_CONTRACT per-delta exige contrato WS12 para enrutar/promover; G_UI_WRITE no tiene recibo en `accepted_scope_nodes`, por lo que no habilita la mutación UI de este delta. Si falta operación/endpoint: detener, registrar hueco con dueño y no crear sustituto; si falta promoción: handoff y pendiente; glob dudoso: no marcar lista. Validaría con store temporal/corpus WS40 que `deskops show board` lista la tarea, la UI separa capas y normaliza/contiene rutas; acta humana tras WS16.

FUTURO
WS12 publica operaciones/endpoints y reglas de promoción; WS22 y WS26.1 entregan Board y tarea autorada con `files`/dependencias; WS16 produce acta G_HUMAN_READ; P01 receptor produce acta G_UI_WRITE por delta; el TaskDoc de promoción fija archivos, pruebas y textos; cierre/promoción ocurre por canal externo autorizado.
