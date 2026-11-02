REFORMULACION

El nodo WS19.1 es un encargo de implementación en graph_ui para editar campos del workspace sobre la base integrada a1b2b22. El resultado es un editor de campos en `frontends/mindmap/views/workspace/fields/` que guarda y recarga contra la API/endpoints fijados por WS12, aplica la precondición de escritura de payload que WS12 elija y WS45 verifique, y ante escritura obsoleta conserva el texto local y muestra el conflicto. Límites: no cambia el contrato WS12; no edita campos protegidos por workflow; no habilita documentos con contenido no declarado hasta que WS47 pruebe la guarda; la mutación solo se admite en el desk y modo manual exclusivo mediante WS48, y otros modos quedan read-only. G_HUMAN_READ habilita el uso de mutaciones en UI, no el desarrollo ni pruebas aisladas de API. El TaskDoc de promoción fijará archivos, pruebas y textos.

AMBIGUEDADES

ninguna

DRY-RUN

Un ejecutor futuro leería `dag.yaml` (WS19.1, WS12, WS47, WS48), el contrato WS12, las aceptaciones/evidencias de WS47 y WS48, `reconciliacion.md`, el ticket `editing` y el código del workspace en a1b2b22/134a665. Crearía el editor bajo `views/workspace/fields/`, lo conectaría al endpoint de guardado con la precondición de WS12, manejaría 409/conflicto conservando el buffer, ocultaría o deshabilitaría campos protegidos según la whitelist WS12 y consultaría la admisión de WS48 antes de mutar. Consumiría WS47 como guarda de contenido no declarado y añadiría tests con store temporal. Errores: si falta WS12/47/48 o un gate, se detiene y registra el hueco con repo dueño, sin sustituto. Validación: guardar/recargar confirma el dato real; escritura obsoleta no pierde texto local y muestra conflicto; campos protegidos no editables; contenido no declarado bloqueado; otros modos read-only; pruebas aisladas de API pueden correr sin G_HUMAN_READ.

FUTURO

WS12 fija la representación de la precondición y la whitelist; WS45 resuelve G_PAYLOAD_PRECONDITION; WS47 prueba la guarda; WS48 produce la admisión; WS16 y el acta humana resuelven G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; la promoción fija TaskDoc, archivos, pruebas y textos.
