REFORMULACION
Propósito: encargo de implementación para mostrar diff e historial Git de solo lectura junto a la TaskDoc. Resultado: vista en `frontends/mindmap/views/workspace/diff/`, con una sección por repo alcanzado por `TaskDoc.files`, acotada a commits de `TaskDoc.references` y rutas de `TaskDoc.files`. Repo dueño: `graph_ui`. Límites: no escribir ni revertir; no mostrar integridad del store (WS29); no asociar a intento (WS35); resolver repo/rutas por contrato WS11 y declarar no disponible lo no resoluble; promoción no autorizada.

AMBIGUEDADES
1. Cita: «Base: commits listados en TaskDoc.references y rutas en TaskDoc.files …; sin commits, working tree contra HEAD limitado a esas rutas». No se define qué diff se muestra cuando sí hay commits: ¿working tree contra el último commit referenciado, diff de cada commit contra su padre, o un rango? La aceptación exige «Diff real» sin fijar la comparación, así que el ejecutor tendría que inventar el resultado y el criterio comprobable.
2. Cita: «sin commits, working tree contra HEAD limitado a esas rutas». No se indica cómo tratar rutas de `TaskDoc.files` nuevas/no trackeadas, que `git diff HEAD` no muestra, ni un repo sin HEAD. Obliga a inventar si se omiten, se muestran como diff sintético o se declaran no disponibles.

DRY-RUN
Lecturas: dag.yaml (nodo y vecinos), guía, brief, alcance, decisiones y cobertura; aristas no revisadas. Cambios previstos: ninguno; esta revisión no modifica el nodo. Dependencias: contrato WS11 (rutas/registry/aliases) a través de WS12/WS13, modelo TaskDoc de deskops y gate G_UI_READ. Validaciones futuras: acta de recepción por delta de G_UI_READ, pruebas de diff/historial read-only con TaskDoc con y sin commits, repo declarado y rutas no resolubles.

FUTURO
El TaskDoc de promoción fijará archivos, escenarios y textos; WS11 produce la resolución de rutas; WS35 añade la asociación a intento; WS29 cubre integridad del store; el solicitante P01 emite el acta G_UI_READ en graph_ui. La promoción sigue no autorizada.
