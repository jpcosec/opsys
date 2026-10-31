## REFORMULACION
- **Propósito:** integrar en el workspace la delegación e intervención humanas sobre ejecuciones, sin autoaprobación ni simulación.
- **Resultado:** vista/UI en `graph_ui` que invoca únicamente el adaptador WS34 para dispatch/reply, registra decisiones con WS33.2 y muestra actor humano y evidencia enlazada de WS33.1/WS33.2; la ausencia de API o permisos aparece como error en pantalla.
- **Repo:** `graph_ui`; fuera: `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador autorizada por contrato WS12 y `tests/`.
- **Límites:** solo adaptador WS34; no canales alternativos, no autoaprobación, no simulación. Los gates pendientes son intencionales; no habilitan por sí mismos ejecución ni Scion.

## AMBIGUEDADES
Ninguna. La aceptación es comprobable con los contratos nombrados: WS34 define confirmación/identidad de intento; WS33.1/WS33.2 aportan evidencia y decisiones; WS12 autoriza la ruta y efectos. Los textos exactos, archivos y escenarios quedan para el TaskDoc de promoción.

## DRY-RUN
- **Lecturas previstas:** nodo WS36, guía de revisión, brief, alcance, decisiones, cobertura y contratos vecinos ya citados; no se revisan los bloques edge como nodos.
- **Cambios previstos:** implementar la vista de ejecución, la ruta fina al adaptador WS34, el registro de decisiones vía WS33.2 y pruebas en `tests/`.
- **Dependencias:** WS34, WS35, WS33.1/WS33.2, contrato WS12; gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT por delta.
- **Validaciones futuras:** test de respuesta vinculada al intento y confirmación; test de actor humano y evidencia enlazada; test de error visible ante API/permisos ausentes; comprobación de no autoaprobación ni simulación. Sin ejecutar.

## FUTURO
WS34 entregará el adaptador y su confirmación; WS35, la vista de ejecución/trazabilidad; WS33.1/WS33.2, evidencia y registro de decisiones; WS12, contratos por delta. Los gates los resolverán sus responsables; WS37 validará con agente real. La promoción fijará archivos, textos y pruebas dentro de esta aceptación.
