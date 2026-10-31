## REFORMULACION

**Propósito:** revisar PK03 como encargo de planificación: agrupación de revisión del lector y descubrimiento, no nodo ejecutable.

**Resultado:** veredicto sobre si su alcance y aceptación se entienden sin inventar criterios.

**Repo:** PK03 no declara `owner_repo`; es agrupación, no entrega. Sus hijos declaran graph_ui.

**Límites:** no revisar los bloques edge vecinos; no ejecutar; no evaluar calidad del producto; no dar por aprobadas las Pxx; un gate pendiente no es defecto; las candidatas no están autorizadas.

## AMBIGUEDADES

1. «cada hijo directo tiene revisión vigente» — no se define qué hace vigente una revisión: quién la emite, con qué fecha, dónde se registra ni cuándo caduca. Obligaría a inventar el criterio de aceptación de PK03.

2. «bloqueo explícito con responsable» — no se identifica al responsable ni la autoridad que declara el bloqueo. Obligaría a inventar el actor y el modo de acreditarlo.

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo PK03 y contratos de sus hijos; instrucción.

**Cambios previstos:** ninguno; solo informe de revisión.

**Dependencias:** PK03 agrupa WS13, WS14, WS15, WS16, WS40 y WS41. WS11 y WS08 son prerrequisitos de varios hijos. WS07 debe designar responsables. G_UI_READ y G_HUMAN_READ condicionan lecturas y mutaciones.

**Validaciones futuras:** revisión vigente de cada hijo; ejecución humana de WS16; corpus reproducible de WS40; decisión humana sobre P01/P07/P08/P09; contrato WS11.

## FUTURO

WS07 designa responsables y operador Scion. El humano resuelve las Pxx. WS11 cierra el contrato de navegación. WS40 produce el corpus. WS16 obtiene validación humana real. Los hijos generan sus propias revisiones y salidas. Nada de esto corresponde resolverlo a PK03 ni constituye ambigüedad de su encargo.
