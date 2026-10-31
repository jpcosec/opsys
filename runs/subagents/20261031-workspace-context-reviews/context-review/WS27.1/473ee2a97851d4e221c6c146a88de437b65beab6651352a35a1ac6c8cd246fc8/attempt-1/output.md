REFORMULACION
Propósito: encargar una vista que muestre diff Git e historial de solo lectura por repo y tarea, junto a la TaskDoc. Resultado: una sección por repo alcanzado por `TaskDoc.files`, con diff real acotado a los commits de `TaskDoc.references` y a esas rutas; sin commits, working tree contra HEAD limitado a esas rutas. Repo dueño: `graph_ui`, salida en `frontends/mindmap/views/workspace/diff/` y `tests/`. Límites: no escribir ni revertir; no mostrar hallazgos de integridad del store (WS29); asociación a intento en WS35; rutas de lectura según contrato WS11; depende de WS13 y WS12; `G_UI_READ` pendiente; promoción no autorizada.

AMBIGUEDADES
1. «sección por cada repo alcanzado por TaskDoc.files, con el repo declarado». No se especifica qué campo o formato declara el repo de cada ruta ni cómo resolver una ruta sin repo declarado. Obligaría a inventar la asociación ruta→repo.
2. «Diff real e historial read-only acotados al repo y tarea». «Historial» no delimita qué historia se muestra: log de commits referenciados, historial por archivo o rango. Obligaría a inventar el conjunto de eventos y su presentación.
3. «Diff Git e historial read-only junto a la TaskDoc». No se nombra la vista o componente TaskDoc ni un nodo que lo produzca. Obligaría a inventar si se crea el contenedor o se integra en uno existente.

DRY-RUN
Lecturas: nodo WS27.1, guía, brief, alcance, decisiones y cobertura; aristas WS12/WS13 solo como contratos. Cambios previstos: vista de diff en `frontends/mindmap/views/workspace/diff/`, tests y consumo de rutas de lectura definidas por WS11. Dependencias: WS13 (lector) y WS12 (capacidades Git); gate `G_UI_READ` resuelto por WS11. Validaciones futuras: diff/historial real y acotado, secciones por repo, ausencia de escritura o reversión, no mostrar integridad del store; aceptación del gate y preflight task-only antes de promover. Sin ejecutar.

FUTURO
WS12 produce el contrato de operaciones Git; WS11 acepta `G_UI_READ`; WS13 entrega el lector; WS35 añade la asociación a intento; WS29 cubre integridad; el TaskDoc de promoción fija archivos, escenarios y textos; el humano designa responsables y acepta deltas. Si falta contrato, se aplica la regla común: detener y registrar el hueco.
