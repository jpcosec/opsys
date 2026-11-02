REFORMULACION

WS19.1 encarga implementar en graph_ui la edición de campos del workspace con conflicto visible, reutilizando editores y API, bajo la precondición de escritura de payload que fija WS12 y verifica WS45, sin asumir hash. El resultado es guardar/recargar dato real, conservar el texto local ante escritura obsoleta y mostrar el conflicto; los campos workflow-protegidos no son editables por este canal. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/fields/`, endpoints del contrato WS12 sin cambios y `tests/`. Límites: delta sobre el workspace a1b2b22, sin cambios de contrato, otros modos read-only, documentos con contenido no declarado no editables hasta WS47, y sin promoción ni aprobación humana implícita.

AMBIGUEDADES

1. «Documentos con contenido no declarado no son editables por este canal hasta que WS47 pruebe la guarda de contenido». Obliga a inventar cómo se determina antes de editar que un documento tiene contenido no declarado y si «no editable» significa deshabilitar la edición o rechazar al guardar; WS47 describe una guarda de `/save`, no una clasificación previa del documento.

DRY-RUN

Un ejecutor futuro leería el contrato WS12 (representación de la precondición, whitelist, errores y endpoints), la guarda producida por WS47, el módulo de admisión WS48, los editores/API existentes del workspace y el ticket `editing` para no duplicar. Verificaría gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT. Cambios previstos: UI de edición de campos bajo `views/workspace/fields/`, consumo de endpoints WS12 sin modificarlos, conservación de buffer ante 409/conflicto, bloqueo de campos protegidos, integración de la admisión WS48 y de la guarda WS47; pruebas en graph_ui. Dependencias: WS12, WS47 y WS48; G_PAYLOAD_PRECONDITION la produce WS45. Si falta contrato, endpoint, guarda o admisión, se detiene y registra el hueco con repo dueño, sin sustituto. Errores esperados: escritura obsoleta rechazada sin perder texto y conflicto visible; campo protegido o contenido no declarado rechazado/deshabilitado. Validación: guardar/recargar dato real, conflicto visible, texto local conservado, campos protegidos no editables, otros modos read-only y pruebas focalizadas. Sin ejecutar nada.

FUTURO

WS12 fija contrato, precondición, whitelist y errores; WS45 verifica G_PAYLOAD_PRECONDITION; WS47 produce la guarda; WS48 produce la admisión; WS16 aporta el acta G_HUMAN_READ; el receptor P01 emite el acta G_UI_WRITE por delta. WS19 cierra cuando cumplen sus hijos. La promoción exige TaskDoc/preflight y no duplicar el ticket `editing`.
