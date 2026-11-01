REFORMULACION  
Propósito: implementar en `graph_ui` el enrutado explícito de una tarea al Board y una representación de “capa lista”. Resultado: la tarea añadida al `BoardDoc` por operación pública de WS12 aparece en `deskops show board` y la UI la separa de tareas en ejecución, con dependencias pendientes o archivos solapados. Repo dueño: `graph_ui`. Límites: no crear promoción nueva; usar solo la operación completa admitida por WS12; si falta, handoff y estado pendiente; no editar `status` para avanzar. Dependencias: WS12, WS22, WS26.1 y gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Aceptación: enrutado visible, capa lista calculada con `files`/ritual, solapamiento por igualdad o contención, glob dudoso no listo, y pruebas.

AMBIGUEDADES  
1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista»: no se define “supervisor”, ni quién revisa, ni cómo se registra esa revisión. Obliga a inventar el actor, el canal y la evidencia que permite pasar de “no comprobado” a “lista”.  
2. «sin archivos solapados según los `files` declarados en cada TaskDoc»: no se indica qué ocurre si un TaskDoc no declara `files`, los declara vacíos o son ilegibles; la aceptación solo cubre glob/no-resolución. Obliga a decidir si la ausencia equivale a “sin solapamiento” o a “no comprobado”.

DRY-RUN  
Lecturas previstas: contrato WS12 y endpoints autorizados; implementación/datos de Board de WS22; salidas de WS26.1; TaskDocs y ritual de fase; Board/lifecycle de deskops. Cambios previstos: vistas en `frontends/mindmap/views/workspace/routing/`, estado de capa lista y tests. Dependencias: WS12/WS22/WS26.1 y gates indicados. Validaciones futuras, sin ejecutar: `deskops show board`, distinción visual en UI, handoff si falta promoción, y casos de solapamiento por igualdad, contención, glob/no-resolución.

FUTURO  
WS12 produce contrato, operaciones y endpoints; WS22 aporta Board real; WS26.1 aporta autoría; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; WS12 verifica G_WRITE_CONTRACT por delta. El TaskDoc de promoción fija archivos, escenarios y textos de pantalla.
