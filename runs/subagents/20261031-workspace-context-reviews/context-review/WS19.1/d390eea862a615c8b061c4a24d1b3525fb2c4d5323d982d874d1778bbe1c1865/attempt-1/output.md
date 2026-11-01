## REFORMULACION
**Propósito:** encargar en `graph_ui` la edición de campos del documento en el workspace, con precondición de escritura y conflicto visible.  
**Resultado:** guardar/recargar confirma persistencia; una escritura obsoleta conserva el texto local y muestra el conflicto; los campos workflow-protegidos no son editables por este canal; la mutación queda restringida a desk en modo manual exclusivo y otros modos son read-only.  
**Repo:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/fields/` y `tests/`.  
**Límites:** consume endpoints del contrato WS12 sin modificarlo; no define la precondición ni asume hash; no habilita modos distintos ni campos protegidos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS19.1, contrato vecino WS12, gates `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, reconciliación (base `a1b2b22`, ticket de edición) y guía de revisión.  
**Cambios previstos:** UI de edición de campos y conflicto bajo `fields/`, consumo de endpoints WS12 y pruebas.  
**Dependencias:** WS12 fija representación de precondición, operaciones y policy; WS45 verifica `G_PAYLOAD_PRECONDITION`; acta humana de lectura vía WS16; recepción por delta del receptor P01. Solapamiento con `editing` sin duplicar implementación.  
**Validaciones futuras:** guardar/recargar dato real; escritura obsoleta rechazada sin pérdida de texto local y conflicto visible; campos protegidos no editables; read-only fuera del modo exclusivo; pruebas aisladas de API pueden avanzar, las mutaciones de UI requieren `G_HUMAN_READ`. Sin ejecutar.

## FUTURO
WS12 publica whitelist, endpoints y representación de la precondición; WS45 produce la evidencia de `G_PAYLOAD_PRECONDITION`; el receptor P01 emite el acta `G_UI_WRITE` de este delta; WS16 aporta el acta de lectura. La promoción fijará archivos, TaskDoc y casos de prueba. WS19 termina cuando terminan sus hijos.
