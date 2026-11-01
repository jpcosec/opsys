REFORMULACION

- **Propósito**: implementar en graph_ui el alta y baja de relaciones admitidas por el contrato de operaciones, sin definir semántica nueva de relaciones.
- **Resultado**: mutaciones persistentes y confirmables tras recargar; rechazo visible de una relación no permitida o de una revisión obsoleta.
- **Repo**: graph_ui; salida en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.
- **Límites**: depende de WS12; usa API real y la precondición que WS12 fije; no crea semántica de relaciones en el componente. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES

**ninguna**. La frase «relaciones permitidas por contrato» y «la precondición de escritura que fije WS12» delegan whitelist, representación de precondición, operaciones y endpoints a WS12, con productor nombrado; WS45 produce G_PAYLOAD_PRECONDITION, WS16 G_HUMAN_READ y el receptor P01 G_UI_WRITE. Los gates pendientes son intencionales. El detalle de archivos, textos y casos queda para el TaskDoc de promoción.

DRY-RUN

- **Lecturas**: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.2, contrato WS12 y gates.
- **Cambios previstos**: ninguno ahora. En ejecución futura, vistas/componentes de relaciones bajo `views/workspace/relations/`, consumo de endpoints autorizados y pruebas.
- **Dependencias**: contrato WS12; G_PAYLOAD_PRECONDITION (WS45); G_HUMAN_READ (WS16); acta por delta G_UI_WRITE (P01); G_WRITE_CONTRACT por delta. El agregado WS19 cierra cuando cierran WS19.1 y WS19.2.
- **Validaciones futuras**: alta/baja persistente tras recarga; rechazo visible de relación no permitida y revisión obsoleta; store temporal real o corpus WS40; sin commits automáticos.

FUTURO

WS12 fija contrato, whitelist, representación de precondición y endpoints; WS45 verifica la precondición de payload; WS16 emite el acta de lectura; el receptor P01 emite el acta de recepción del delta; el TaskDoc de promoción concreta archivos, escenarios y textos. Nada de esto se ejecuta aquí.
