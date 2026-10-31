## REFORMULACION
Propósito: implementar en `graph_ui` el alta y baja de relaciones permitidas por el contrato, usando API real y before-image, sin definir semántica de relaciones en el componente. Resultado: relaciones autorizadas se crean/eliminan, persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`. Límites: solo relaciones de la whitelist; no crear semántica propia; promoción no autorizada; depende de WS12 y WS16, con gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. El nodo se entiende como encargo de planificación.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas previstas: nodo WS19.2, aristas WS12/WS16, agregado WS19, gates, guía, alcance y reglas comunes. Cambios previstos: código en `frontends/mindmap/views/workspace/relations/` y pruebas en `tests/`; llamadas a endpoints autorizados por WS12; uso de before-image para alta/baja. Dependencias: contrato/whitelist y capabilities de WS12; validación humana de lectura de WS16; aceptación del delta graph_ui (`G_UI_WRITE`); `G_WRITE_CONTRACT`. Validaciones futuras: alta/baja persisten tras recarga; relación no permitida se rechaza con error visible; revisión obsoleta se rechaza con error visible. Sin ejecución.

## FUTURO
WS12 debe producir el contrato, whitelist y clasificación de APIs, y resolver `G_WRITE_CONTRACT`/`G_UI_WRITE`; WS16 produce `G_HUMAN_READ`; el responsable humano designado acepta el delta de graph_ui. La promoción posterior fijará archivos, pills, átomos, evidencia y preflight. WS19 cerrará cuando cierren sus hijos.
