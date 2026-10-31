REFORMULACION
Propósito: definir WS13 como agregado de integración del lector del workspace con documento/fuente de solo lectura, contexto, enlaces, explorador, pestañas/divisiones, historia y foco por documento. Resultado: nodo `aggregate` no ejecutable que termina cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación. Repo dueño: `graph_ui`. Límites: reutilizar el workspace integrado `a1b2b22`, mantener Code local y rutas del host, no requerir índices nuevos ni crear otro workspace independiente; el registro de vistas existente en `shell/registry.js` se reutiliza.

AMBIGUEDADES
Ninguna. La aceptación es comprobable por agregación de hijos; repo, dependencias y límites están declarados. La frase «organización de contenido procede de documentos/consultas» no obliga a inventar en este nodo porque no se ejecuta y el glosario define «consulta»; además, los detalles quedan delegados a la promoción y a los hijos.

DRY-RUN
Lecturas previstas: nodo WS13 en `dag.yaml`; guía de revisión; `brief.md`, `alcance.md`, `decisiones.md`, `reconciliacion.md`; futura acta/contrato de WS11.
Cambios previstos: ninguno; WS13 no se ejecuta.
Dependencias: WS11, WS13.1, WS13.2, WS13.3; gate `G_UI_READ` pendiente y evaluado por delta. La base `a1b2b22/f16fcd1/134a665` está declarada como reutilizable, pero la aceptación ampliada sigue pendiente.
Validaciones futuras: cierre del agregado solo cuando sus tres hijos acrediten su aceptación; verificación del recibo de lectura por delta en repo receptor; comprobación de que no se duplica la implementación existente ni se infiere cierre por commit.

FUTURO
WS11 produce el contrato de navegación y el acta de recepción por delta. WS13.1–WS13.3 ejecutan y aportan evidencia. WS06/promoción decide el TaskDoc, archivos, pills y preflight. El solicitante humano acepta deltas concretos. Nada de esto se ejecuta ni se decide en este nodo.
