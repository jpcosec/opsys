REFORMULACION
Propósito: revisar WS13 como encargo de planificación que integra el lector del workspace con contexto, enlaces, pestañas, historia y foco por documento/nodo. Resultado: nodo `aggregate` no ejecutable; se cumple cuando cumplen WS13.1, WS13.2 y WS13.3, y sus dependientes siguen dependiendo de WS13. Repo dueño: `graph_ui`. Límites: solo lectura; reutilizar workspace a1b2b22 y `shell/registry.js`; no exigir índices nuevos ni crear otro workspace; no inventar mapeo texto→código; no duplicar implementación; promoción no autorizada.

AMBIGUEDADES
ninguna. El gate `G_UI_READ` pendiente es intencional y `per_delta`; no obliga a inventar aceptación ni recepción conjunta.

DRY-RUN
Lecturas previstas: input y fuentes citadas; nodo WS13, dependencias WS11/WS13.1–WS13.3 y gate `G_UI_READ`. Cambios previstos: ninguno; esta revisión no modifica plan, código ni actas. Dependencias: contrato WS11, salidas de los tres hijos y recibo externo por delta. Validaciones futuras: aceptación de cada hijo; lectura de Markdown modelado/no modelado; fuente cruda íntegra; contexto, enlaces y foco compartido; explorador con refresco sin reinicio; pestañas, dos documentos lado a lado e historia; ausencia de índices nuevos y de workspace duplicado. No se ejecuta nada.

FUTURO
WS11 produce el contrato de navegación/identidad. WS13.1–WS13.3 producen implementación y evidencia de aceptación. El solicitante P01 o receptor de `graph_ui` produce el acta `G_UI_READ` del delta concreto. La promoción requiere TaskDoc, preflight y reconciliación WS06; no está autorizada. WS14, WS15, WS22, WS23, WS24, WS27, WS39 y WS41 quedan a la espera de WS13 según el DAG.
