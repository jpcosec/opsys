REFORMULACION
Propósito: integrar en graph_ui la verificación de cierre de UF05 y un handoff explícito, consumiendo el contrato de operaciones WS12 y la revisión/evidencia de WS27. Resultado: vista de revisión que muestra lo que reporta `deskops closeout verify` por el canal autorizado, diagnostica faltantes y ofrece handoff —con evidencia— a `deskops closeout commit` por CLI en modo manual o al coordinador activo (P03). No hay commit ni close por HTTP. Repo dueño: graph_ui; salidas en `frontends/mindmap/views/workspace/review/`, endpoints y tests. Límites: sin terminal embebido genérico; comando o solicitud no equivalen a cierre; G_CLOSEOUT está satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes por delta; si falta contrato/API, detenerse y registrar el hueco.

AMBIGUEDADES
Ninguna. Las referencias a WS12/P03 cubren el canal, la política de coordinador y la precondición; los gates pendientes son intencionales y los detalles de archivos, textos y pruebas corresponden a la promoción. El refresco posterior es verificable mediante `deskops show task` y el commit externo, sin que el nodo pueda sustituirlos.

DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el contrato WS12, las salidas de WS27 (diff/evidencia), la evidencia de G_CLOSEOUT y la aceptación. Crearía en graph_ui la superficie de revisión, la integración con el adapter/CLI autorizado y pruebas aisladas; no añadiría commit HTTP ni terminal genérico. Consumiría de WS27 la evidencia y de WS12 el canal, campos, errores y política de coordinador. Validaría: diagnóstico con faltantes reales, ausencia de contrato/API con parada registrada, fallo de `verify` mostrado sin declarar cierre, handoff con evidencia y refresco posterior desde deskops. G_HUMAN_READ impediría habilitar mutaciones en UI, no las pruebas aisladas; G_UI_WRITE y G_WRITE_CONTRACT se evaluarían solo para este delta.

FUTURO
El commit de closeout lo ejecuta la CLI en modo manual o el coordinador; la persona P01 receptora acepta el delta de WS28 en graph_ui. WS30 valida UF05 completo. El refresco confirma el cierre externo; WS28 no lo produce.
