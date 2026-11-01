## REFORMULACION
**Propósito:** encargar a `graph_ui` el enrutamiento explícito de tareas al Board y una representación de capa lista. **Resultado:** tras enrutar, `deskops show board` muestra la tarea y la UI la separa de ejecución, dependencias pendientes y solapamientos; la promoción solo invoca una operación completa admitida por WS12 o queda en handoff. **Repo:** `graph_ui` (`frontends/mindmap/views/workspace/routing/`, tests). **Límites:** no implementar promoción nueva, no commits/closeout, no mutar fuera de endpoints WS12; gates pendientes son intencionales.

## AMBIGUEDADES
1. «la UI la distingue de una tarea en ejecución»: no define qué estados/campos de lifecycle cuentan como “en ejecución” ni el subconjunto aplicable; obliga a inventar el mapeo para clasificar la capa lista. WS22 indica leer estados de deskops, pero no fija ese subconjunto.
2. «revisión supervisor antes de marcar lista»: no identifica actor, canal ni evidencia del supervisor; obliga a inventar quién revisa, cómo se registra y cuándo se considera cumplida antes de marcar lista.

## DRY-RUN
**Lecturas:** nodo WS26.2 y guía; contratos vecinos solo como dependencias. **Cambios previstos:** `routing/` y tests en `graph_ui`. **Dependencias:** WS12 (operación/endpoints), WS22 (Board), WS26.1 (autoría); `G_WRITE_CONTRACT`, `G_HUMAN_READ` y `G_UI_WRITE` por delta; `G_CLOSEOUT` satisfecho. **Validaciones futuras:** `deskops show board`, distinción UI, pruebas de solapamiento normalizado/glob, handoff si falta operación, revisión supervisor y recibos por delta. Sin ejecutar.

## FUTURO
WS12 produce contrato/operación y registra huecos; WS22 fija estados del Board; WS26.1 aporta autoría; WS16 entrega acta `G_HUMAN_READ`; P01 decide `G_UI_WRITE` por delta; el TaskDoc de promoción fija archivos y pruebas. Si falta contrato/API, se registra hueco y handoff.
