## REFORMULACION

Propósito: nodo agregado que agrupa «errores de lectura y modo degradado» (WS15.1) y «orientación sin desk» (WS15.2), sin ejecución propia. Resultado: salidas agregadas de sus hijos; se cumple cuando ambos cumplen su aceptación. Repo dueño: graph_ui. Límites: `node_role: aggregate` no ejecutable, `promotion: not_authorized`, integración `delta_or_existing_ticket` y `never_parallel_duplicate`; depende de WS13 y requiere G_UI_READ, pendiente intencional.

## AMBIGUEDADES

ninguna.

## DRY-RUN

- Lecturas: guía de revisión, brief, alcance, decisiones, cobertura, reconciliación y `dag.yaml` (nodo WS15; los bloques edge de vecinos se usan solo como contexto y no se revisan).
- Cambios previstos: ninguno; el agregado no ejecuta ni produce archivos propios.
- Dependencias: WS13 como lector base; WS15.1 y WS15.2 como hijos; G_UI_READ por delta concreto.
- Validaciones futuras: aceptación de WS15.1 y WS15.2; recibo G_UI_READ por delta; WS16 sobre el corpus WS40.

## FUTURO

WS15.1 y WS15.2 producen implementación y aceptación. El receptor P01 emite las actas G_UI_READ por delta concreto. WS16 ejecuta la validación humana. La promoción exige preflight y no duplicar ticket existente. Los dependientes esperan el ID WS15, no una ejecución propia del agregado.
