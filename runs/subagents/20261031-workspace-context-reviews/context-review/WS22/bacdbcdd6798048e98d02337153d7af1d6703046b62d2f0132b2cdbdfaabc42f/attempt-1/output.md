REFORMULACION
Propósito: representar el Board real como trabajo navegable dentro del lector. Resultado: tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc y sus pills/átomos referenciados, con selección y links comunes al lector. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/board/` y `tests/`. Límites: no reemplazar el workflow con drag-and-drop de status; estados y condiciones de lifecycle se leen de deskops (Board, lifecycle), no de `dag.yaml`; no duplicar tareas ni presentar predicado satisfecho como test aprobado. Depende de WS13 y WS09; requiere G_UI_READ (per_delta, pendiente intencional).

AMBIGUEDADES
Ninguna. Los términos que podrían parecer abiertos quedan cubiertos: pills/átomos y archivos exactos los fija el TaskDoc de promoción; la fuente de estados/lifecycle está nombrada (deskops); el lector y la selección común vienen de WS13; el catálogo, de WS09. Si faltara contrato, API o dato, aplica «Reglas comunes de ejecución»: detenerse y registrar el hueco, no inventar sustituto.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS22, contratos de WS13/WS09 y gate G_UI_READ. Cambios previstos: implementación solo en `board/` y `tests/` de graph_ui; reutilizar lector y APIs reales de deskops; sin tomar `dag.yaml` como fuente de estados ni implementar arrastre de status. Dependencias: WS13 (lector, foco/historia), WS09 (catálogo de renderizaciones), G_UI_READ (recibo por delta) y transitivas WS11/WS12. Validaciones futuras: que las tres vistas abran el mismo TaskDoc; selección/links comunes; estados/lifecycle desde deskops; ausencia de duplicados; no confundir predicado con test; acta G_UI_READ; promoción y validación humana. No se ejecuta nada.

FUTURO
WS13 entrega lector/selección; WS09, catálogo; WS11/WS12, contratos de navegación/operaciones; el receptor humano P01 emite el acta G_UI_READ del delta; WS06 resuelve integración/no duplicación; el TaskDoc de promoción fija archivos, pills, átomos, textos y pruebas; WS30 registra la validación humana. Nada de eso es ambigüedad de WS22.
