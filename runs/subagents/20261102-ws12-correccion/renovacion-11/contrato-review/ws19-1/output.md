REFORMULACION
Propósito: editar campos en graph_ui con precondición de escritura y conflicto visible, conservando el texto local. Resultado: editores en `frontends/mindmap/views/workspace/fields/`, consumo de endpoints del contrato WS12 sin cambiarlo y pruebas. Repo: graph_ui. Límites: depende de WS12, WS47 y WS48; requiere G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT; no edita campos workflow-protegidos; no habilita contenido no declarado hasta WS47; mutación solo con admisión WS48; promoción no autorizada.

AMBIGUEDADES
1. «Delta sobre workspace integrado a1b2b22 de edición» y «base a1b2b22/f16fcd1/134a665 reutilizable»: no define a1b2b22 ni si ese workspace es base. Obligaría a inventar el punto de partida.
2. «endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato»: no identifica ruta (`POST /save` o `/api/save`) ni si incluye HO-02. Obligaría a inventar canal y alcance.
3. «workflow-protected fields no editables por este canal»: no enumera campos ni modelos. Obligaría a inventar la lista; el contrato la da en 3.3.
4. «Documentos con contenido no declarado no son editables por este canal hasta que WS47 pruebe la guarda de contenido»: no fija cómo los detecta la UI antes de WS47. Obligaría a inventar un detector.
5. «desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura»: no delimita qué es «aislado» ni si la ruta queda deshabilitada. Obligaría a inventar el criterio de habilitación.
6. «el conflicto se muestra como tal»: no fija mensaje ni forma de conservar el buffer. Obligaría a inventar el contrato de error/presentación.

DRY-RUN
Lecturas: WS12 (3.3, 5.7, 5.9, 6.3, 6.7), salidas de WS45/47/48, `GU/persistence.py`, `sldb_adapter.py`, `serve.py` y tests. Cambios: editores, `expected` con 409, filtro de protegidos y UI que conserva el buffer; pruebas en `tests/`. Dependencias: WS45 (precondición), WS47 (guarda), WS48 (admisión); gates G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_HUMAN_READ y G_WRITE_CONTRACT. Validación: guardar/recargar, 409 sin pérdida, protegido rechazado, contenido no declarado bloqueado y, sin admisión, lectura/handoff; store temporal.

FUTURO
WS47 declara pérdidas detectadas; WS48 fija F1 y la admisión; WS45 prueba la precondición; P01 registra acta; una persona decide G_HUMAN_READ; root evalúa G_WRITE_CONTRACT; la promoción exige archivos, pills, átomos, evidencia y preflight de tarea.
