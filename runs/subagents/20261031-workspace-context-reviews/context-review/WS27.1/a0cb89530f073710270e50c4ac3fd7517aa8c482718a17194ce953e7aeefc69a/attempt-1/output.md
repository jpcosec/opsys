REFORMULACION
Propósito: encargo de planificación para una vista read-only de diff e historial Git junto a la TaskDoc, derivada de `TaskDoc.references`/`TaskDoc.files`. Resultado: vista en graph_ui con secciones por repo alcanzado y fallback a working tree→HEAD si no hay historial referenciado. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`. Límites: no escribir/revertir; no mostrar integridad del store (WS29); no adivinar rutas ni escribir cruzado; la asociación a intento queda para WS35.

AMBIGUEDADES
1. «commits listados en TaskDoc.references» / «una sección por cada repo alcanzado por TaskDoc.files». El input no define cómo se asocia cada commit a un repo cuando `TaskDoc.files` alcanza varios. El ejecutor tendría que inventar si prueba el hash en todos los repos, toma el primero que resuelva o descarta duplicados.
2. «sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD». Solo cubre cero commits; no cubre referencias no vacías pero ninguna resoluble, ni `TaskDoc.files` vacío. El ejecutor debe decidir si eso cuenta como «sin commits», en qué repo ejecutar el fallback y si mostrar cero secciones o un diff de repo completo, con riesgo de exceder alcance.
3. «limitados a TaskDoc.files». No aclara si filtra la lista de commits por rutas tocadas o solo recorta el diff de cada commit. El ejecutor tendría que inventar si un commit referenciado que no toca esas rutas aparece o no.

DRY-RUN
Lecturas previstas: nodo, modelo TaskDoc de deskops, contrato WS11, contrato WS12, registro de vistas de WS13 y repos Git alcanzados. Cambios previstos: vista de diff/historial read-only, resolución de rutas por WS11, tests. Dependencias: WS13, WS12, WS11 transitiva, G_UI_READ por delta. Validaciones futuras: diff/historial reales acotados, ausencia de escritura/revert, sección por repo, rutas no resolubles como no disponibles y acta G_UI_READ del delta.

FUTURO
WS35 añade asociación a intento; WS29 aporta hallazgos de integridad; el receptor P01 emite el acta G_UI_READ por delta; el TaskDoc de promoción fija archivos, pruebas y textos; WS11 publica el contrato de rutas/aliases.
