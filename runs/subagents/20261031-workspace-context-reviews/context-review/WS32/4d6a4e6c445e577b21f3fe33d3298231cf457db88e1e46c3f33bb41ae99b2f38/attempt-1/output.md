REFORMULACION
Propósito: unificar identidad de intento y cierre Scion, sin segundo pipeline: separar intento/slug y dispatch intent/confirmed, y hacer manifiesto, RunDoc y cierre consistentes e idempotentes. Resultado: agregado no ejecutable; cierra cuando WS32.1 y WS32.2 cumplen su aceptación, y sus dependientes siguen dependiendo de WS32. Repo dueño: deskops. Límites: candidato sin promoción autorizada (`promotion: not_authorized`), integración como delta o ticket existente sin duplicado paralelo, solapamiento declarado con scion, gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT y matriz WS06 transitiva por WS11/WS12.

AMBIGUEDADES
1. «Refinar el ticket de external_references.scion, sin segundo pipeline» frente a «Agregado: salidas de WS32.1, WS32.2». No se identifica ruta, ID ni ubicación del ticket, ni se aclara si el entregable aceptado es ese ticket refinado o el código agregado de los hijos. Obliga a inventar el artefacto concreto y su ubicación. La aceptación remite a los hijos, pero no acredita el ticket citado.
No se detectan otras ambigüedades en el bloque WS32: repo, propósito, dependencias, límites y aceptación agregada están expresados.

DRY-RUN
Lecturas previstas: bloque WS32 de dag.yaml, guía de revisión, brief, alcance, decisiones, cobertura y reconciliación; lectura estática, sin herramientas ni ejecución. Cambios previstos: ninguno; nodo agregado no ejecutable y sin promoción. Dependencias: WS05, WS12, WS32.1 y WS32.2; gates G_CLOSEOUT (blocked, externo), G_SCION (unverified, WS44) y G_WRITE_CONTRACT (pending, WS12). Validaciones futuras: aceptación de ambos hijos, evidencia de gates, no duplicar pipeline y confirmar integración sin paralelismo.

FUTURO
WS44 produce el probe de G_SCION; WS12 produce whitelist y G_WRITE_CONTRACT; el resolver externo aporta evidencia de G_CLOSEOUT; WS07 designa actores y decisiones humanas; responsables de graph_ui/sldb aceptan deltas. La promoción y cualquier cambio de alcance los decide un humano o el nodo receptor, no este revisor.
