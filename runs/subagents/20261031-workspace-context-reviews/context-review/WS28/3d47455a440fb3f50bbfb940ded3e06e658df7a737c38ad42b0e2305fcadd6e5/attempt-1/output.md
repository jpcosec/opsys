## REFORMULACION
**Propósito:** integrar en graph_ui la verificación de closeout, el diagnóstico de faltantes y un handoff explícito. **Resultado:** UI que ejecuta/expone `deskops closeout verify` por el canal WS12, muestra faltantes y ofrece salida a `deskops closeout commit` por CLI o al coordinador activo (P03), sin commit/close HTTP. **Repo:** `graph_ui`. **Límites:** sin terminal embebido genérico; mutaciones UI sujetas a `G_HUMAN_READ`; gates por delta; comando o solicitud no equivalen a cierre.

## AMBIGUEDADES
1. «ofrecer handoff explícito con evidencia»: no se define qué evidencia debe acompañar el handoff, dónde se muestra/registra ni cuándo se considera ofrecido. La aceptación solo exige diagnóstico y cierre externo. Obliga a inventar contenido, forma y criterio de éxito del handoff.
2. «se refresca el estado desde deskops»: no indica si el refresco es manual o automático, qué estado observable lo demuestra ni quién lo ejecuta tras el commit externo. Obliga a inventar disparador y comprobación.

## DRY-RUN
**Lecturas previstas:** guía, nodo WS28, vecinos WS27/WS12/WS30, gates, brief, alcance, decisiones y cobertura. **Cambios previstos:** en `frontends/mindmap/views/workspace/review/`, endpoints y `tests/` de graph_ui; verificación, diagnóstico y handoff; sin commit/close HTTP ni terminal. **Dependencias:** WS27 y WS12; `G_CLOSEOUT` satisfecho; `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` pendientes por delta. **Validaciones futuras:** pruebas de UI/API, diagnóstico de faltantes, cierre externo verificable, refresco de estado y aceptación UF05/WS30. No se ejecuta nada.

## FUTURO
WS12 debe producir el contrato/canal por delta y la política de coordinador; WS27 aporta diff/evidencia; WS16 resuelve `G_HUMAN_READ`; P01 emite recibo `G_UI_WRITE`; un actor CLI/coordinador ejecuta el closeout externo; WS30 valida UF05.
