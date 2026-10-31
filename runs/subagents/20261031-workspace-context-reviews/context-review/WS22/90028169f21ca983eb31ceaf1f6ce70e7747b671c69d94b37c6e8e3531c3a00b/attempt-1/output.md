REFORMULACION
Propósito: encargar a graph_ui la representación navegable del Board real como trabajo, sin convertirlo en editor de workflow. Resultado: tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren los mismos TaskDoc y sus pills/átomos referenciados, compartiendo foco y enlaces con el lector; estados y condiciones de lifecycle se leen de deskops (Board, lifecycle), no de dag.yaml. Repo dueño: graph_ui; salida prevista en `frontends/mindmap/views/workspace/board/` y `tests/`. Límites: no reemplazar el workflow con drag-and-drop de status; no duplicar tareas ni presentar un predicado satisfecho como test aprobado; solo lectura (G_UI_READ), sin G_UI_WRITE; integración como delta o ticket existente, nunca duplicado paralelo; promoción no autorizada.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: guía de revisión, brief.md, alcance.md, decisiones.md, cobertura.md, reconciliacion.md, nodo WS22 y bloques de vecinos WS13, WS09, WS26, WS30 y gates.
Cambios previstos: vistas de Board en el output_scope declarado y pruebas, integrando el ticket o delta existente.
Dependencias: WS13 (lector, foco, historia), WS09 (catálogo de renderizaciones), G_UI_READ resuelto por WS11; matriz WS06 de forma transitiva por WS11/WS12; corpus WS40 para validación.
Validaciones futuras: abrir el mismo TaskDoc desde lista, tablero y dependencias; foco y enlaces coherentes con el lector; estados/lifecycle desde deskops; no duplicación de tareas; aceptación humana WS30; evidencia del gate G_UI_READ. Sin ejecución.

FUTURO
WS11 produce la aceptación de lectura; WS06/WS12 aportan matriz e integración; WS09 entrega el catálogo; WS30 valida humanamente; WS40 aporta corpus; la promoción fija archivos, pills, átomos, evidencia y pruebas; WS07/P01 debe designar al responsable de graph_ui. Nada de esto es ambigüedad del nodo.
