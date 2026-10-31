## REFORMULACION
**Propósito:** que la UI muestre, junto a la TaskDoc, la evidencia en tres estados diferenciados: declarada, encontrada y verificada, permitiendo abrir su soporte.

**Resultado:** vistas/componentes en `frontends/mindmap/views/workspace/evidence/`, usando las rutas de lectura definidas por el contrato WS11, más tests.

**Repo dueño:** `graph_ui`.

**Límites:** no introduce modelo de comentarios; solo abre como lector artefactos Markdown dentro del workspace; fuera de ese caso muestra ruta y declara “no soportado”. Depende de WS13 (lector, foco, historia) y WS12 (contrato de operaciones/closeout); requiere `G_UI_READ`.

## AMBIGUEDADES
1. **Estado de verificación no ejecutada.** Cita: «verificada = resultado de `deskops closeout verify`» y «verificación fallida se muestran como estados distintos». Obliga a inventar qué se muestra cuando la verificación no se ha ejecutado: ¿cuarto estado, asimilación a “fallida”, o ausencia de estado? También si el estado es por evidencia individual o por TaskDoc.

2. **Unidad de representación con evidencias mixtas.** Cita: «declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos, sin colapsarlos». No define si una TaskDoc con varias evidencias en estados distintos se representa por lista, por estado agregado o por contadores; obliga a inventar la unidad de estado y su agregación.

## DRY-RUN
**Lecturas previstas:** nodo WS27.2, guía de revisión, brief, alcance, decisiones, cobertura y contratos vecinos WS12/WS13/WS27 (no revisados). No se ejecuta nada.

**Cambios previstos:** componentes de evidencia en `frontends/mindmap/views/workspace/evidence/` y tests; sin cambios en otros repos.

**Dependencias:** WS13 aporta lector y rutas; WS12 aporta contrato/capability de `deskops closeout verify`; `G_UI_READ` aporta acta de aceptación del delta de lectura en graph_ui.

**Validaciones futuras:** tests de estados no colapsados, evidencia ausente visible como ausente, apertura de Markdown dentro del workspace y ruta/no soportado fuera; verificación contra `deskops closeout verify`; prueba con store temporal o corpus WS40; confirmación de no solapamiento en graph_ui.

## FUTURO
WS12 produce el contrato de operaciones y la capability de closeout; WS11 resuelve `G_UI_READ` y las rutas de lectura; WS07 designa al responsable de graph_ui. La promoción fijará archivos, pills, tests y textos exactos. WS27 cierra como agregado cuando también cierre WS27.1. La validación humana y la aceptación final corresponden a otros nodos.
