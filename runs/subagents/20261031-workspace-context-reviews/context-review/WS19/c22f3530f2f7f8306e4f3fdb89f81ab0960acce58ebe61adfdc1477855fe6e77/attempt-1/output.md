## REFORMULACION

- **Propósito:** que la UI de graph_ui integre la edición de campos y de relaciones permitidas sobre el ticket draft de edición, mostrando revisión esperada y conflicto, sin crear semántica propia.
- **Resultado:** nodo `aggregate` no ejecutable; su resultado es la suma de WS19.1 (campos con conflicto) y WS19.2 (relaciones por contrato). No produce entregable propio distinto de esas salidas.
- **Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/` y `output_scope` agregado de ambos hijos.
- **Límites:** delta sobre ticket existente, nunca duplicación paralela (`never_parallel_duplicate`); reutiliza editores/API y before-image; campos workflow-protected no editables por este canal; mutaciones sujetas a contrato WS12 y gates. Promoción no autorizada.

## AMBIGUEDADES

Ninguna. Lo que el nodo delega —ticket concreto, archivos, pruebas, textos— queda cubierto por `promotion`/TaskDoc o por WS04/WS06, y el contrato de operaciones lo produce WS12 con regla explícita en alcance.md para su ausencia. No hay resultado indefinido ni aceptación no comprobable en el agregado: “se cumple cuando todos sus hijos cumplen su aceptación”.

## DRY-RUN

- **Lecturas (sin ejecutar):** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19, bloques vecinos y gates ya suministrados. Sin herramientas ni historial.
- **Cambios previstos:** ninguno; WS19 no se ejecuta por ser agregado y su promoción está `not_authorized`.
- **Dependencias:** WS12 (contrato de operaciones), WS16 (validación humana), WS19.1, WS19.2; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, hoy pendientes e intencionales.
- **Validaciones futuras:** aceptación de ambos hijos; resolución de gates por WS12/WS16; preflight de promoción que fije archivos, pills, átomos y evidencia; verificación de no solapamiento contra Board de graph_ui.

## FUTURO

- WS12 cierra whitelist y acepta deltas en graph_ui; WS16 produce `G_HUMAN_READ`.
- WS07 identifica responsables/actores de repo.
- Un humano decide la promoción de WS19 y de sus hijos.
- WS04 revalida Board, archivos y alcance del repo receptor.
- El TaskDoc de promoción fija archivos exactos, escenarios y textos de pantalla.
