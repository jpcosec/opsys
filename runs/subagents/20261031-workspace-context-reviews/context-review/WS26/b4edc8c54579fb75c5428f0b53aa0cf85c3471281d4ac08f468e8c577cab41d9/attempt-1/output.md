REFORMULACION
Propósito: WS26 es un nodo agregado que integra autoría explícita desde candidato, evidencia declarada, dependencias, contexto/pills, enrutamiento en Board y capa lista. Resultado: agregado no ejecutable; se considera cumplido cuando WS26.1 y WS26.2 cumplen su aceptación. Repo dueño: `graph_ui`; `output_scope`: salidas agregadas de WS26.1 y WS26.2. Límites: no implementa promoción nueva; debe invocar solo operaciones admitidas por WS12 o dejar handoff; no confunde enrutar en Board con ejecución; no habilita mutaciones UI hasta `G_HUMAN_READ`; los gates pendientes son intencionales.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS26, hijos WS26.1/WS26.2, contratos vecinos WS12/WS22 y definiciones de gates, solo como contexto. Cambios previstos: ninguno; al ser `aggregate` no se ejecuta ni produce artefactos propios. Dependencias: WS12, WS22, WS26.1 y WS26.2; gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras: aceptación de ambos hijos; contrato WS12 por delta; acta humana de lectura de WS16; recibo P01 por delta para `G_UI_WRITE`; verificación `G_WRITE_CONTRACT` por operación/efecto. No se ejecuta nada.

FUTURO
WS12 debe producir el contrato de operaciones/escritura y resolver la precondición aplicable; WS22 aporta la representación navegable del Board; WS26.1 y WS26.2 producen autoría/contexto y enrutamiento/capa lista. WS16 produce el acta de `G_HUMAN_READ`; el receptor P01 registra recibos por delta para `G_UI_WRITE`; WS12 verifica `G_WRITE_CONTRACT`. La promoción sigue `not_authorized` y requiere TaskDoc/preflight en el repo dueño. Nada de esto autoriza implementación ni aprobación de API/uso.
