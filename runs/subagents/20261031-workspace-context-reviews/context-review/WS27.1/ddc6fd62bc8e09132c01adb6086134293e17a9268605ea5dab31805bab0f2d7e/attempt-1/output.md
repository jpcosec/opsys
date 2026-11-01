REFORMULACION
WS27.1 es un nodo de implementación de graph_ui cuyo propósito es mostrar, junto a la TaskDoc, diff Git e historial read-only por repo y tarea. El resultado esperado es una vista que agrupa por cada repo alcanzado por TaskDoc.files, declara el root del repo y usa commits de TaskDoc.references limitados a TaskDoc.files; sin commits, diff working tree→HEAD. Debe resolver repo/rutas por contrato WS11; una ruta sin repo resoluble queda no disponible. Límites: solo lectura, sin escribir ni revertir; no muestra integridad del store (WS29); no añade asociación a intento (WS35). Depende de WS13 y WS12 y requiere G_UI_READ, pendiente intencional y per_delta.

AMBIGUEDADES
1. «Base: commits listados en TaskDoc.references ...; sin commits, working tree contra HEAD limitado a esas rutas». No define qué diff mostrar cuando sí hay commits: ¿cada commit contra su padre, el commit referenciado contra HEAD/working tree, o un rango? Obliga a inventar la pareja de revisión y el alcance del diff; «Diff real» no lo fija.
2. «working tree contra HEAD» no aclara si incluye staged y untracked. Obliga a inventar si el diff debe incluir cambios indexados y archivos no rastreados o solo tracked no staged.

DRY-RUN
Un ejecutor futuro leería WS11, el modelo TaskDoc, la integración WS13 y registry/aliases; inspeccionaría el repo en modo read-only. Tomaría WS13 como cumplido solo cuando sus hijos lo estén. Crearía archivos bajo frontends/mindmap/views/workspace/diff/ y tests/, integraría la vista y agruparía TaskDoc.files por repo. Por repo resolvería root y ejecutaría consultas Git de solo lectura; con TaskDoc.references usaría commits resolubles y el filtro por TaskDoc.files que el nodo pide; sin commits usaría `git diff HEAD -- <rutas>`. Ruta sin repo: no disponible; commit no resoluble: excluido/declarado, sin adivinar. Errores Git se mostrarían como límite, no como éxito. Validaría con repos temporales: diff real, historial acotado, sección por repo, root explícito, ausencia de escrituras/reverts y de hallazgos WS29. Consumiría el recibo G_UI_READ del delta al preparar/promover.

FUTURO
El acta G_UI_READ la produce el solicitante P01 en graph_ui al preparar/promover este delta. WS11 fija rutas/aliases; WS12, el contrato de operaciones; WS35 añade asociación a intento; WS29, integridad. El TaskDoc de promoción fija archivos exactos, pruebas, textos y pills.
