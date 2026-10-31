## REFORMULACION
WS27 es un nodo agregado, no ejecutable, cuyo propósito es reunir la revisión de cambios y la evidencia junto a la TaskDoc. Resultado: agregado de las salidas de WS27.1 (diff Git) y WS27.2 (evidencia declarada/encontrada/verificada), sin trabajo propio de integración. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: depende de WS13, WS12 y de sus hijos; requiere `G_UI_READ` con evaluación `per_delta`, aún pendiente; promoción no autorizada; no duplica implementación ni infiere cierre por los commits de reconciliación.

## AMBIGUEDADES
Ninguna. No hay frases del nodo que obliguen al ejecutor de WS27 a inventar resultado, repo, actor, aceptación, dependencia o límite. La aceptación remite a la de sus hijos y el nodo declara expresamente que no se ejecuta; `G_UI_READ` pendiente es intencional y su recibo se evalúa por delta.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml#node:WS27`, guía, brief, alcance, decisiones y cobertura. No se revisan los bloques edge de vecinos.
- **Cambios previstos:** ninguno propio; el agregado termina cuando WS27.1 y WS27.2 cumplen su aceptación.
- **Dependencias:** contrato de operaciones de WS12, lector de WS13, salidas de WS27.1/WS27.2 y recibo `G_UI_READ` por delta.
- **Validaciones futuras:** aceptación de ambos hijos, recibo del gate para WS27/WS27.1/WS27.2 y preflight de promoción si se autoriza. Sin ejecución.

## FUTURO
WS27.1 y WS27.2 producen diff y evidencia; WS11 emite el recibo de `G_UI_READ` por delta; el responsable humano acepta ese delta; WS28 y WS35 consumen WS27; la promoción queda sujeta a autorización y preflight, no a este agregado.
