## REFORMULACION

**Propósito:** implementar en `graph_ui` la verificación de cierre y el handoff de UF05. **Resultado:** una vista de revisión que invoca `deskops closeout verify` por el canal fijado en WS12, muestra los faltantes diagnosticados y prepara un handoff explícito, con evidencia, hacia `deskops closeout commit` por CLI en modo manual o al coordinador activo según P03; después refresca el estado desde deskops. **Repo:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/review/`, endpoints y `tests/`. **Límites:** no hay commit ni cierre por HTTP en baseline, no hay terminal embebido genérico, y comando o solicitud no equivalen a cierre.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS28 y contratos vecinos WS27/WS12, más el bloque de gates. Sin ejecución.

**Cambios previstos:** acciones de UI para lanzar la verificación por el adapter WS12; presentación del diagnóstico de faltantes; preparación de handoff con evidencia y destino CLI/coordinador; refresco de estado mediante deskops; pruebas en `tests/`. No se prevé endpoint de commit/close ni terminal genérico.

**Dependencias:** WS27, agregado no ejecutable que termina con WS27.1/WS27.2; contrato WS12 para canal, actor, efectos y policy de coordinador. Gates: `G_CLOSEOUT` satisfecho; `G_HUMAN_READ` pendiente de WS16 e impide habilitar uso de mutaciones en UI; `G_UI_WRITE` y `G_WRITE_CONTRACT` se evalúan por delta concreto para WS28.

**Validaciones futuras:** pruebas de implementación con store temporal o corpus WS40; verificación de que el diagnóstico refleja `deskops closeout verify`; comprobación de que el handoff no cierra por sí mismo; confirmación externa mediante `deskops show task` y commit de closeout; refresco verificable; validación humana UF05 en WS30.

## FUTURO

WS12 debe publicar el contrato aplicable y la policy de coordinador. WS16 produce el acta de `G_HUMAN_READ`. El receptor P01 emite el recibo por delta de `G_UI_WRITE`. WS27.1/WS27.2 completan diff y evidencia. El cierre externo lo ejecuta CLI o coordinador según P03, no este nodo. WS30 valida UF05 manualmente.
