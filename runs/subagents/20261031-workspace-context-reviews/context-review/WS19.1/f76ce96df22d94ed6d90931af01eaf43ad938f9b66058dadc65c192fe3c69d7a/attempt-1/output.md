## REFORMULACION
Propósito: planificar un delta de edición de campos en el workspace de `graph_ui`, reutilizando editores y API existentes, con precondición de escritura de payload y conflicto visible. Resultado: una UI que guarda/recarga dato real, rechaza una escritura obsoleta conservando el texto local y muestra el conflicto; los campos workflow-protected no son editables por este canal; la mutación queda restringida a desk en modo manual exclusivo y otros modos son read-only hasta contrato. Repo dueño: `graph_ui`. Límites: cambios en `frontends/mindmap/views/workspace/fields/` y `tests/`; consume endpoints del contrato WS12 sin modificarlo; no inventa API, no edita campos protegidos, no implementa relaciones (WS19.2) ni promueve.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el contrato WS12, la evidencia de WS45/G_PAYLOAD_PRECONDITION, el ticket externo `editing`, el workspace integrado a1b2b22/134a665 y sus pruebas. Crearía componentes en `views/workspace/fields/`, los conectaría a los endpoints WS12, mapearía campos permitidos/protegidos desde la whitelist y añadiría manejo de rechazo/conflicto conservando el buffer local y estados read-only. Gates: WS12 publicado y G_WRITE_CONTRACT aceptado para WS19.1; G_PAYLOAD_PRECONDITION producido por WS45; G_HUMAN_READ antes de habilitar uso; G_UI_WRITE como acta por delta. Validaría guardar/recargar, rechazo de escritura obsoleta sin pérdida de texto, campo protegido no editable y ausencia de cambios de contrato. Si falta contrato, endpoint o precondición: detenerse y registrar el hueco con repo dueño, sin crear sustituto.

## FUTURO
WS12 fija la representación de la precondición, operaciones, escritores y definición operativa del modo manual exclusivo. WS45 verifica o completa G_PAYLOAD_PRECONDITION. WS16 produce G_HUMAN_READ. El receptor P01 emite G_UI_WRITE por delta. La promoción fija TaskDoc, archivos y pruebas. WS19.2 cubre relaciones.
