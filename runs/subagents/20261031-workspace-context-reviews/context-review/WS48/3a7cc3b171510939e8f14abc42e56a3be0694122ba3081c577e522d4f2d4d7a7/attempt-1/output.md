REFORMULACION
WS48 es un nodo de implementación en graph_ui: crear un punto único de admisión de escritura de la UI en modo manual exclusivo, previo a toda mutación, que cargue una afirmación vigente desde configuración confiable y consulte evidencia contraria; debe admitir con declaración de ausencia de evidencia contraria o degradar a lectura/handoff con causa. Cubre POST /api/desk/advance y el botón Avanzar, conservando revision, gates y rechazos. Límites: no crea identidad, lock, CAS ni lifecycle nuevo; no habilita uso real; depende de WS12 y de G_UI_WRITE/G_WRITE_CONTRACT por delta.

AMBIGUEDADES
1. «rechazo en el servidor antes de advance_task» frente a output_scope «frontends/mindmap/ (módulo común de admisión de escritura; archivo exacto en el TaskDoc); tests/». Obliga a inventar dónde vive la admisión del servidor o a salir del scope declarado.
2. «una afirmación vigente suministrada fuera de la petición (configuración confiable del responsable del desk, cargada por este nodo y sin valores reales en el repo)». No define formato, campos ni qué hace vigente la afirmación; obliga a inventar el esquema y la validación.

DRY-RUN
Leería dag.yaml, el contrato WS12 (secciones 5 y 5.9), views/workflow/deskops/deskops-view.js y la ruta advance. Crearía el módulo común en frontends/mindmap/, cargaría la configuración, añadiría comprobación antes de advance_task y estado/mensaje del botón, y pruebas con store temporal. Consumiría WS12 y el acta G_UI_WRITE del delta. Validaría rechazo sin afirmación, con evidencia contraria o consulta fallida, y admisión sin exclusividad; si falta contrato o sección, pararía y registraría el hueco.

FUTURO
WS12 fija la representación de la afirmación y las consultas de evidencia; el receptor P01 emite el acta G_UI_WRITE del delta; el TaskDoc fija archivo y configuración exactos; WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39 y WS42 consumen el punto de admisión; G_HUMAN_READ habilita el uso real.
