REFORMULACION
El nodo WS19.1, «Editar campos con conflicto visible», es un delta de implementación en graph_ui: habilitar la edición de campos de documentos del workspace reutilizando editores y API existentes, con precondición de payload fijada por WS12 (`expected` por valor) y conflicto visible sin pérdida del texto local. Resultado: guardar y recargar confirma el dato real; una escritura obsoleta se rechaza y conserva el buffer. Repo: graph_ui; scope `frontends/mindmap/views/workspace/fields/` y `tests/`. Límites: no edita campos protegidos; no habilita documentos con contenido no declarado hasta WS47; toda mutación exige admisión WS48 y modo manual exclusivo; no crea operaciones de lifecycle ni cambia el contrato; aquí no se ejecuta nada.

AMBIGUEDADES
1. «endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato». No aclara si WS19.1 puede modificar código de endpoints de graph_ui (por ejemplo, el filtro HO-02) o solo consumirlos intactos; obligaría a inventar el alcance de cambios permitidos.
2. «Delta sobre workspace integrado a1b2b22 de edición». No se define `a1b2b22` ni su relación con el workspace; obligaría a inventar la base/commit o asumir cuál es.
3. «una escritura obsoleta no pierde texto local». No precisa si «texto local» es el buffer completo del documento o solo los campos editados; obligaría a inventar la unidad de conservación en conflicto.

DRY-RUN
Lecturas: contrato WS12 (secciones 2, 3, 6, 10), nodos WS19.1/WS45/WS47/WS48, vistas `fields` y rutas `/api/save`. Cambios previstos: editor que envía `update` con `expected`, rechaza campos protegidos antes de invocar, traduce 409 a conflicto y conserva el buffer; consulta la admisión WS48; deshabilita documentos con contenido no declarado hasta WS47. Dependencias/gates: WS12, WS47, WS48; `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Errores esperados: 409, campo protegido, falta de admisión, WS47 pendiente. Validación: guardar/recargar, escritura obsoleta sin pérdida, rechazo de protegidos y no edición de contenido no declarado.

FUTURO
WS47 decide y prueba la guarda de contenido; WS48 entrega la admisión; WS45/`G_PAYLOAD_PRECONDITION` verifica `expected`; P01 registra el acta `G_UI_WRITE`; un humano aporta `G_HUMAN_READ` y autoriza la promoción. Nada de eso lo decide este revisor.
