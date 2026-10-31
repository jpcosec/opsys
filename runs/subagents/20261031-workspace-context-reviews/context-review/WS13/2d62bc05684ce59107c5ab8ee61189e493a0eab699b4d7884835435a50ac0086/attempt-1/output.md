## REFORMULACION

Propósito: revisar WS13 como encargo de planificación, sin ejecutar ni valorar el producto. Resultado: agregado no ejecutable que integra el lector del workspace con historia y foco; se cumple cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación. Repo dueño: `graph_ui`. Límites: solo lectura, mantener Code local y rutas del host, no requerir índices nuevos, reutilizar la base `a1b2b22` y `shell/registry.js`, y no crear otro workspace independiente. Depende de WS11 y de sus hijos; `G_UI_READ` se evalúa por delta. Promoción no autorizada. No reviso los contratos edge vecinos.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Lecturas, sin ejecutar: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS13 y contratos vecinos aportados como contexto. Cambios previstos: ninguno por este revisor; el agregado no produce cambio propio, cierra con la aceptación de sus hijos. Dependencias: contrato WS11, WS13.1–WS13.3 y recibos `G_UI_READ` por delta. Validaciones futuras: evidencia de aceptación ampliada de cada hijo; no inferir cierre por `f16fcd1` ni por commit; no duplicar implementación; comprobar que no se exigen índices nuevos y que se conserva el workspace integrado. El TaskDoc de promoción fijará archivos, pruebas y textos.

## FUTURO

WS11 define identidad, origen, enlaces y APIs de lectura. WS13.1, WS13.2 y WS13.3 implementan y aportan su evidencia. El solicitante P01 o el receptor de `graph_ui` emite el acta `G_UI_READ` del delta concreto. WS06/promoción integra el agregado en el ticket receptor sin duplicar trabajo. La aceptación humana y la promoción quedan fuera de este nodo.
