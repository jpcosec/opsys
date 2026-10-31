## REFORMULACION
**Propósito:** PK06 es una agrupación de revisión de “Publicación básica”, sin ejecución propia. **Resultado:** verificar que WS31 y WS43 tengan revisión vigente, sin ambigüedad de encargo ni bloqueo externo sin responsable; la completitud sustantiva del paquete depende de las salidas de sus hijos. **Repo dueño:** deskops. **Límites:** no autoriza tareas, no añade aristas ni equivale a producto entregado; Scion/modelos/Changes no demostrados siguen propuestos. La aceptación operativa es `review_completion` mediante hashes y `disposition.md`; la aceptación sustantiva no se ejecuta en esta revisión.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas previstas:** bloque PK06; guía; brief; alcance; decisiones; cobertura; borrador de manual; aristas WS31/WS43 solo para trazar dependencias, sin revisarlas.
- **Cambios previstos:** ninguno; esta revisión no modifica `dag.yaml`, contratos ni repos.
- **Dependencias:** hijas WS31 y WS43; WS31 depende de WS10, WS30 y WS43; WS43 depende de WS17 y WS30; contrato de navegación WS11; gates G_HUMAN_MANUAL, G_PRODUCT y G_WRITE_CONTRACT; script `context_review.py`.
- **Validaciones futuras:** ejecutar `context_review.py status` desde deskops; comprobar coincidencia de hashes de input y contrato y existencia de `disposition.md`; confirmar revisiones vigentes de WS31/WS43. En fases posteriores, WS31/WS43 verifican actas, links, atom→doc, entradas y commit de publicación. Nada se ejecuta aquí.

## FUTURO
La sesión de coordinación ejecuta `context_review.py`, registra `blocked` con responsable cuando corresponda y determina la vigencia de las revisiones. WS31 produce el manual versionado; WS43 publica entradas y mapa reales; WS30 aporta el acta humana y WS17 las entradas authored. La recepción técnica es por delta y no se presume por estas decisiones.
