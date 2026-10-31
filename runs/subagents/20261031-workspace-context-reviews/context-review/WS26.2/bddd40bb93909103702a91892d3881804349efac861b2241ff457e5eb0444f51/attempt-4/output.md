REFORMULACION
Propósito: convertir WS26.2 en un encargo de planificación ejecutable para enrutar tareas en Board y representar la capa lista. Resultado: operación pública que añade la tarea a `tasks` del BoardDoc y UI que muestra tareas listas sin confundirlas con ejecución; la promoción solo procede por canal autorizado que respete commits previos y estado real. Repo dueño: `graph_ui`, con salida en `frontends/mindmap/views/workspace/routing/` y `tests/`. Límites: no sustituir workflow por drag-and-drop; no promocionar sin contrato; gates pendientes y Pxx no aprobadas. No reviso contratos vecinos.

AMBIGUEDADES
1. «sin archivos solapados, como define el ritual de fase»: no se adjunta el ritual ni se fija qué archivos se comparan ni cuándo hay solapamiento. Obligaría a inventar el algoritmo, el conjunto de archivos y la fuente de verdad de la capa lista.

DRY-RUN
Lecturas: input completo —guía, brief, alcance, decisiones, cobertura, nodo WS26.2 y contratos vecinos como contexto—; sin herramientas. Cambios previstos: implementación UI/API para enrutar y calcular/representar capa lista; no se ejecuta promoción ni commits. Dependencias: WS12 (contrato), WS22 (Board), WS26.1 (autoría); gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras: `deskops show board` muestra la tarea; UI la distingue de una en ejecución; canal de promoción respeta commits previos y estado real; pruebas en `tests/` y aceptación del TaskDoc. Nada ejecutado.

FUTURO
WS12 produce contrato/whitelist y efectos; WS22 entrega Board navegable; WS26.1 entrega autoría; WS16 produce el acta de `G_HUMAN_READ`; WS07 y el solicitante resuelven Pxx y responsables; el TaskDoc de promoción fija archivos, escenarios y textos. Los gates se resuelven fuera de este nodo; no son ambigüedades.
