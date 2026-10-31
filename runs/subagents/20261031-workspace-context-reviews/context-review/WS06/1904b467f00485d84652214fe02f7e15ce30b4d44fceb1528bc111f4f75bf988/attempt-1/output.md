## REFORMULACION
WS06 es un nodo de planificación, `owner_repo: deskops`, cuyo propósito es proponer en `reconciliacion.md` una matriz por implementación —ya cubierto, extender ticket existente o nuevo delta— agrupada por repo dueño, con correspondencia ticket/delta y responsable «por designar». No produce gates, no aprueba deltas indefinidos y no notifica, despacha ni modifica el Board de graph_ui. Depende de WS02, WS03 y WS04.

## AMBIGUEDADES
1. «ya cubierto (capacidad observable en código o en el Board, con referencia), extender ticket existente o nuevo delta»: no fija criterio para elegir entre las tres categorías. Obliga a inventar el umbral que separa «ya cubierto» de «extender» y de «nuevo delta».
2. «capacidad observable en código o en el Board»: no establece qué prevalece si código y Board discrepan. Obliga a inventar la autoridad de observación.
3. «Matriz con una fila por delta o capacidad propuesta»: no define granularidad de «delta» ni de «capacidad». Obliga a inventar la unidad de descomposición de las filas.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodos WS06/WS02–WS04/WS07 del DAG y `task-ws06.md`; insumos `auditoria/deskops.md`, `auditoria/infraestructura.md` y `auditoria/ui.md`. Cambios previstos: solo redactar la matriz y la atomización propuesta en `reconciliacion.md`, conservando la fila Scion RunDoc/cierre con WS32/33 sin WS05. Sin cambios en Board, gates ni tareas externas. Dependencias: WS02–WS04 como fuente de inventario; WS07 para designación. Validaciones futuras: filas agrupadas por repo, correspondencia ticket/delta y responsable marcado «por designar»; promoción exige preflight y archivos/pills/átomos/evidencia, pero está `not_authorized`.

## FUTURO
WS07 designa con identidad a responsables de graph_ui/sldb/spec2viz y operador Scion, y resuelve P01–P09 y `source_mode`. WS11/12 obtienen aceptación específica por repo receptor. El humano dueño del producto confirma decisiones; otro nodo fija el TaskDoc de promoción. WS06 solo propone correspondencias y no aprueba deltas.
