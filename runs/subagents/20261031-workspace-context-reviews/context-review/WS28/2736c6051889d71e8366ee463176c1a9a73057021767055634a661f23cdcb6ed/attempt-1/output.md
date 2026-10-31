REFORMULACION
Propósito: integrar en graph_ui la verificación de cierre (`deskops closeout verify`) mediante el canal del contrato WS12, mostrar faltantes y ofrecer handoff explícito con evidencia al CLI manual o al coordinador (P03). Resultado: superficie de revisión en `frontends/mindmap/views/workspace/review/` que diagnostica y prepara el cierre externo, sin ejecutarlo. Repo dueño: graph_ui. Límites: no commit/close por HTTP; sin terminal embebido genérico; G_HUMAN_READ se exige antes de habilitar mutaciones UI, no para desarrollo/pruebas aisladas de API; depende de WS27 y WS12.

AMBIGUEDADES
1. «output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/» frente a «No commit/close desde HTTP en baseline.» No se define qué endpoints ni con qué efecto; el ejecutor tendría que inventar si son de lectura, verificación o cierre, pudiendo contradecir el límite.
2. «G_HUMAN_READ aplica porque es una acción de escritura del baseline.» No se identifica la escritura UI: el handoff parece preparar un comando externo y el cierre está prohibido por HTTP. Habría que inventar qué mutación existe y dónde aplica el gate.
3. «o al coordinador si está activo (P03).» Falta una condición observable de “activo” y el mecanismo de entrega del handoff (copiar comando, mensaje, registro). P03 fija la política, no la detección ni el canal.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS28 y aristas WS27/WS12/WS30, gates.
Cambios previstos: ninguno; esta revisión no modifica el plan.
Dependencias: WS27 (agregado de diff/evidencia) y WS12 (contrato de operaciones por delta); G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes y evaluados por delta.
Validaciones futuras: confirmar que el contrato WS12 nombra canal y efectos para verify/handoff; comprobar que no se crea endpoint de cierre HTTP; verificar que la aceptación se observa con `deskops show task`, commit externo y refresco; revisar que el handoff incluye evidencia y no un terminal genérico.

FUTURO
WS12 produce el contrato técnico y mapea el delta; el receptor P01 emite el acta G_UI_WRITE; WS16 produce el acta G_HUMAN_READ; WS30 valida UF05; la promoción fija archivos, pruebas y textos dentro de la aceptación.
