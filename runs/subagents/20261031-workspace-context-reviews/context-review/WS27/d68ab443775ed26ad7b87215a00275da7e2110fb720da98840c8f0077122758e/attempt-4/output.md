REFORMULACION
Propósito: integrar en el workspace la revisión de cambios y la evidencia asociada a una TaskDoc. Resultado: un nodo agregado cuyas salidas son las de WS27.1 (diff Git por repo y tarea) y WS27.2 (evidencia declarada, encontrada y verificada). Repo dueño: `graph_ui`, con `output_base: graph_ui:repository_root/`. Límites: es `aggregate`, no ejecutable; no produce implementación propia ni se promociona sin autorización (`promotion: not_authorized`). Depende de WS13, WS12, WS27.1 y WS27.2; requiere `G_UI_READ`, pendiente e intencional. Su aceptación es comprobable por agregación: se cumple cuando todos sus hijos cumplen la suya.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: `dag.yaml#node:WS27`, guía de revisión, brief, alcance, decisiones, cobertura y contratos de vecinos aportados como contexto; no se revisan estos últimos. Cambios previstos: ninguno; WS27 no se ejecuta ni edita archivos. Dependencias: WS13 y WS12 como prerrequisitos directos, WS27.1 y WS27.2 como hijos que deben cerrar; `G_UI_READ` debe resolverlo WS11. Validaciones futuras: aceptación de WS27.1 y WS27.2, verificación de que sus salidas agregadas cubren diff y evidencia, y confirmación de que WS28 y WS35 siguen dependiendo de WS27. No se ejecuta nada.

FUTURO
WS11 debe producir la aceptación de deltas de lectura en `graph_ui` y resolver `G_UI_READ`. WS27.1 y WS27.2 deben entregar sus respectivas implementaciones y aceptaciones. WS12 aporta el contrato de operaciones y lectura Git. La promoción de WS27 requiere autorización humana y TaskDoc de promoción con archivos, pruebas y evidencia; este revisor no la concede. WS28 y WS35 consumen el agregado cuando esté cerrado.
