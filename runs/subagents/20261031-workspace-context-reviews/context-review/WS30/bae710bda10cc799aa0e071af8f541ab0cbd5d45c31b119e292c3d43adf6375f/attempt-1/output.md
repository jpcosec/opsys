## REFORMULACION
**Propósito:** revisar WS30 como encargo de planificación, no como implementación ni juicio de producto. **Resultado:** acta humana de validación de autoría y revisión manual. **Repo dueño:** `graph_ui`. **Límites:** no ejecutar; no promover; no sustituir el guion ni las operaciones reales por mocks; el nodo solo produce registro humano bajo protocolo.

## AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en `depends_on` de WS30. El ejecutor tendría que decidir si espera un guion aún no declarado como prerrequisito, lo reconstruye o inventa los escenarios de teclado, que tampoco aparecen definidos en `validacion-humana.md`.

2. «un fallo de guion bloquea el gate y el responsable del repo dueño abre tarea en el nodo que lo causó». No se define quién determina el nodo causante ni cómo se enruta la corrección cuando el fallo proviene de otro repo o de un nodo agregado. El ejecutor tendría que inventar el criterio de atribución y el destino de la tarea.

3. «Persona recorre UF02/03 edición/04/05». No queda claro si UF03 incluye solo edición o también lectura, búsqueda e inspección; el ejecutor tendría que ampliar o reducir el recorrido sin criterio explícito.

## DRY-RUN
- **Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `validacion-humana.md`, `user-flows.md`, nodo WS30 y bloques de vecinos como contratos.
- **Cambios previstos:** ninguno ejecutado. En promoción futura, acta en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` y registro del gate `G_HUMAN_MANUAL`.
- **Dependencias:** WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42; WS40 por transitividad de WS17. WS08 solo aparece citado, no declarado.
- **Validaciones futuras:** recorrido humano de UF01–UF05 según protocolo; errores, conflicto en dos ventanas y teclado; evidencia de guion, versión y resultado; bloqueo del gate ante fallo.

## FUTURO
La persona participante ejecuta y firma el acta; el responsable del repo dueño decide correcciones y promoción; WS31 y WS43 consumen la validación; la promoción de WS30 sigue no autorizada y requiere preflight de tarea.
