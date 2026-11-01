## REFORMULACION

- **Propósito:** agrupar la revisión de cambios y evidencia del workspace: diff Git por repo/tarea y evidencia declarada, encontrada y verificada junto a la TaskDoc.
- **Resultado:** nodo `aggregate` no ejecutable; se satisface cuando WS27.1 y WS27.2 cumplen su aceptación. Sus dependientes siguen apuntando a WS27.
- **Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).
- **Límites:** solo lectura; no escribe, no revierte, no verifica por cuenta propia. Los hallazgos de integridad del store son de WS29. Asociación a intento se añade en WS35. No hay aprobación de promoción (`promotion: not_authorized`).

## AMBIGUEDADES

ninguna.

El nodo es agregado y la guía resuelve que termina cuando terminan sus hijos; `scope` y `output_scope` remiten explícitamente a WS27.1/WS27.2, sin exigir una integración adicional no definida. `G_UI_READ` pendiente es intencional y `evaluation: per_delta`.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS27, WS27.1, WS27.2, gate G_UI_READ), `task-ws27.md` al promover; contratos vecinos WS13/WS12 solo como dependencias.
- **Cambios previstos:** ninguno propio; el agregado no produce artefactos. WS27.1 implementaría diff/historial read-only; WS27.2, estados de evidencia.
- **Dependencias:** WS13 (lector, foco, historia y rutas), WS12 (contrato de operaciones y correspondencia de evidencia), hijos WS27.1/WS27.2.
- **Validaciones futuras:** aceptación de ambos hijos; diff acotado a `TaskDoc.references`/`TaskDoc.files` por repo declarado; evidencia declarada/encontrada/verificada sin colapsar estados; apertura de soporte Markdown o ruta declarada no soportada; sin escritura ni cierre.

## FUTURO

- WS27.1 y WS27.2 producen la implementación y su aceptación; WS28 consume WS27 para verificación/handoff.
- El receptor P01 en `graph_ui` emite el acta de `G_UI_READ` por delta concreto al preparar/promover.
- WS12 fija la correspondencia por tipo de evidencia y el canal público; WS13 aporta rutas y lector.
- La promoción fijará archivos, pruebas y textos exactos dentro de la aceptación ya descrita.
