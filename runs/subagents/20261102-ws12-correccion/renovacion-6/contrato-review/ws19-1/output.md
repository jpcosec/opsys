REFORMULACION
Propósito: implementar en graph_ui la edición de campos del workspace documental con conflicto visible. Resultado: una UI de campos que guarda mediante los endpoints que fija WS12, conserva el texto local ante un rechazo por estado obsoleto, no permite editar campos workflow-protegidos y no habilita documentos con contenido no declarado hasta que WS47 pruebe su guarda. Repo: graph_ui, en `frontends/mindmap/views/workspace/fields/` y `tests/`. Límites: no cambia el contrato WS12, no implementa WS45/WS47/WS48, no crea operaciones de lifecycle, no muta sin la admisión de WS48, no cierra gates ni actas; `promotion: not_authorized` exige preflight y archivos exactos.

AMBIGUEDADES
1. «endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato» frente a operaciones.md: «HO-02 (filtro de protegidos y whitelist) → graph_ui → WS19.1». Obligaría a inventar si WS19.1 escribe el filtro de campos protegidos o solo lo consume.
2. «Delta sobre workspace integrado a1b2b22 de edición» frente a «No usa `../UIs/graph_ui/frontends/workspace/` (sin commit) como base ni como evidencia». Obligaría a inventar si `a1b2b22` es base autorizada y qué archivos existen en ella.
3. «`expected` por valor, token `version`/`content_hash` o CAS según el contrato»: enumeración que el contrato resuelve en 6.3; obligaría a inventar solo si el ejecutor no lee esa sección. Se deja constancia.

DRY-RUN
Lecturas: operaciones.md §2, §3.2-3.3, §4.4, §6, §10.2; nodos WS45, WS47, WS48; vistas y tests actuales de graph_ui. Cambios previstos: componentes de edición de campos, llamada con `expected`, presentación del 409 conservando el buffer, rechazo de campos protegidos, pruebas de guardar/recargar. Dependencias: contrato WS12 congelado; WS47 para contenido no declarado; WS48 para admisión y F1; WS45 como evidencia de `G_PAYLOAD_PRECONDITION`. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Validaciones futuras: 409 sin pérdida de texto, campo protegido rechazado, sin F1 la mutación se deshabilita, documento con contenido no declarado no editable hasta WS47, persistencia tras recargar. Sin ejecución.

FUTURO
WS47 entrega y prueba la guarda de contenido; WS48, el módulo de admisión y el formato/ubicación de F1; WS45, la evidencia de la precondición; root evalúa G_WRITE_CONTRACT; una persona aporta G_HUMAN_READ y P01 registra el acta.
