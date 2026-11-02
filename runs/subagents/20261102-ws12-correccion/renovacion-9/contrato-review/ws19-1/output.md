REFORMULACION

Propósito: implementar en la UI de graph_ui la edición de campos sobre los endpoints que fija WS12, con precondición de escritura y conflicto visible, conservando el texto local ante rechazo. Resultado exigido: guardar/recargar confirma dato real; escritura obsoleta no pierde texto local; mutación solo bajo admisión de WS48; campos workflow-protegidos no editables; documentos con contenido no declarado no editables hasta WS47. Repo: `graph_ui`, `frontends/mindmap/views/workspace/fields/`, endpoints WS12 consumidos sin cambiar contrato, `tests/`. Límites: no define contrato, no duplica WS45/WS47/WS48, no crea operaciones nuevas de lifecycle.

AMBIGUEDADES

1. «token `version`/`content_hash` o CAS según el contrato, sin asumir hash» contradice WS12 §6.3, que elige «before-image por valor (`expected`)». Obligaría a inventar cuál de las tres representaciones implementar.
2. «Delta sobre workspace integrado a1b2b22 de edición»: no identifica archivos ni árbol de partida. Obligaría a inventar la base y el alcance del delta.
3. «workflow-protected fields no editables por este canal»: WS12 §3.3 protege por modelo y operación (p. ej. `status`, `current_node`, `history`, `closeout_evidence`); el nodo no enumera el conjunto aplicable. Obligaría a inventar la lista.
4. «endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato»: no aclara si crear rutas adaptadoras (HO-01) entra en el delta o queda fuera. Obligaría a inventar el límite.

DRY-RUN

Un ejecutor leería WS12 §3.2, §6.3 y §6.7; los TaskDoc de WS45, WS47 y WS48; y en graph_ui `persistence.py`, `sldb_adapter.py` y la vista `views/workspace/fields/`. Cambios previstos: enviar `changes[] update` con `expected`; filtrar en el adaptador los campos protegidos antes de invocar al escritor; mostrar el 409 conservando el buffer; consultar la admisión de WS48 antes de escribir y deshabilitar con causa si falta. Dependencias consumidas: precondición verificada por WS45, guarda de WS47 y admisión de WS48; gates G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_HUMAN_READ y G_WRITE_CONTRACT. Errores esperados: 409 por `expected` obsoleto, rechazo de campo protegido, rechazo de admisión y documento con contenido no declarado no editable si WS47 no probó. Validación futura: guardar/recargar, obsoleto sin pérdida, protegido rechazado, sin F1 deshabilitado.

FUTURO

WS45 entrega la evidencia de G_PAYLOAD_PRECONDITION; WS47, la guarda de contenido; WS48, el punto de admisión. El receptor P01 registra el acta G_UI_WRITE y un humano aporta G_HUMAN_READ. La promoción de WS19.1 (`not_authorized`) y la revisión root de WS12 quedan fuera de este nodo.
