## REFORMULACION
**Propósito:** fijar WS41 como encargo de planificación para implementar lectura segura entre desks. **Resultado:** resolver aliases/roots autorizados por WS11, leer un segundo desk mediante APIs públicas de stores, mostrar identidad/origen, seguir enlaces authored del corpus y volver por la historia, con errores visibles ante alias no autorizado, path escapado o store ausente. **Repo dueño:** `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`. **Límites:** depende de WS13, WS11 y WS40; exige G_UI_READ; no cambia el global `SLDB_STORE`, no hace mutaciones cruzadas, no copia contenido para afirmar federación y no crea corpus propio. Es candidato sin promoción autorizada.

## AMBIGUEDADES
1. **Dependencias contradictorias con cobertura.** El nodo declara `depends_on: WS13, WS11, WS40`, pero cobertura dice: «WS41 lectura multidesk, con WS13/14/15». Obliga a inventar si WS14 y WS15 son prerrequisitos reales —especialmente para búsqueda y errores honestos— o si sus funciones quedan fuera de la aceptación de WS41.
2. **Solapamiento de `tests/`.** WS41 incluye en su alcance «views/workspace/; tests/», mientras WS40 declara «tests/fixtures/workspace_documental/; script de seed; tests/». Obliga a decidir si WS41 puede modificar fixtures o el script de WS40, o solo añadir pruebas propias; es un límite que permite exceder el alcance del corpus ajeno.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS41, contratos vecinos WS11/WS13/WS40/WS16 y gate G_UI_READ. **Cambios previstos:** ninguno; esta revisión no ejecuta ni edita. Si se confirman las ambigüedades, el cambio sería en `dag.yaml`/texto de WS41: aclarar dependencias y delimitar `tests/`. **Dependencias:** WS13 agregado, WS11 contrato y acta G_UI_READ —pendiente—, WS40 corpus; transitivas WS08/WS09. **Validaciones futuras:** acta G_UI_READ emitida por WS11; preflight de promoción y TaskDoc fijando archivos/pruebas; pruebas con stores temporales de WS40; casos de alias/path/store ausente; validación humana UF08 en WS16.

## FUTURO
WS11 produce contrato, rutas y acta de aceptación; WS40 produce el corpus y los enlaces entre desks; WS07 designa responsables; un humano decide las Pxx aplicables; WS16 ejecuta la validación UF08; la promoción fija archivos, pruebas y textos dentro de la aceptación. Nada de esto se resuelve aquí.
