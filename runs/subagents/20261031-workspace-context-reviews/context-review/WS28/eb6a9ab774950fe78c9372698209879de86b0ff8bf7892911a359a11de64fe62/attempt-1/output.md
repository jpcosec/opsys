## REFORMULACION
Propósito: integrar en la UI de revisión la verificación de cierre (`deskops closeout verify`), el diagnóstico de faltantes y un handoff explícito con evidencia hacia `deskops closeout commit` por CLI o al coordinador activo (P03).
Resultado: una vista/handoff que muestra el estado de cierre y faltantes, sin declarar cierre por comando o solicitud, sin commit/close por HTTP y sin terminal embebido genérico.
Repo dueño: `graph_ui`. Alcance de salida: `frontends/mindmap/views/workspace/review/`, endpoints y `tests/`.
Límites: baseline; handoff, no ejecución de cierre; gates pendientes.

## AMBIGUEDADES
1. «se refresca el estado desde deskops» — no se nombra operación/canal de refresco, momento ni criterio observable de “estado refrescado”. Obligaría a inventar el mecanismo y cómo probarlo dentro de la aceptación.
2. «ofrecer handoff explícito con evidencia» — no se define qué evidencia compone el handoff ni qué hace válido el handoff al coordinador. La aceptación solo exige mostrar faltantes y que comando/solicitud no equivalgan a cierre; obligaría a inventar el contenido mínimo y su comprobación.

## DRY-RUN
Lecturas previstas: nodo WS28, vecinos WS27/WS12, gates, guía, brief, alcance, decisiones, cobertura.
Cambios previstos: vista de revisión, endpoints de verificación/handoff y pruebas en `graph_ui`.
Dependencias: WS27 y WS12; G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta/efecto.
Validaciones futuras: pruebas con store temporal real o corpus WS40; recibos por delta; ausencia de commit/close HTTP y de terminal genérico.

## FUTURO
WS16 produce el acta de lectura humana; WS12 produce contrato y recibo técnico por delta; el receptor P01 en `graph_ui` acepta el delta WS28; un actor externo (CLI/coordinador) ejecuta el cierre; WS30 valida UF05.
