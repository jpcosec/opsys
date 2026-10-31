## REFORMULACION
**Propósito:** encargo de implementación en `graph_ui` para autoría explícita de una tarea desde un candidato del drawer, con evidencia declarada, dependencias y binding de contexto/pills.

**Resultado:** UF04 sobre TaskDoc real: candidato autorado, evidencia/dependencias/pills vinculadas y visibles tras recargar; nunca editar `status` para avanzar; si una operación Git carece de contrato o dueño, queda handoff explícito y no disponible.

**Repo dueño:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** depende de WS12 y WS22; requiere G_CLOSEOUT (satisfecho), G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; no ejecuta promoción, commits ni closeout por sí mismo.

## AMBIGUEDADES
Ninguna.

Las referencias a contrato de operaciones, TaskDoc, pills, tests y textos de pantalla tienen productor o quedan delegadas al TaskDoc de promoción según la guía. Los gates pendientes son intencionales y `per_delta`; G_HUMAN_READ bloquea mutaciones en UI, no desarrollo/pruebas aisladas de API.

## DRY-RUN
**Lecturas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y el nodo WS26.1 con los contratos vecinos aportados.

**Cambios previstos:** ninguno ahora. En ejecución futura: código de autoría en `graph_ui`, integración de endpoints autorizados por WS12 y pruebas.

**Dependencias:** contrato WS12 por operación/campo/canal; representación Board/TaskDoc de WS22; G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta.

**Validaciones futuras:** UF04 con TaskDoc real; evidencia, dependencias y pills vinculadas y visibles tras recarga; intento de avance no altera `status`; operación Git sin contrato/dueño produce handoff y “no disponible”; pruebas con store temporal real o corpus WS40. No se ejecuta nada.

## FUTURO
WS12 publica el contrato técnico y huecos asignados; WS22 entrega Board y lectura de TaskDoc; WS16 produce el acta de G_HUMAN_READ; el receptor P01 registra actas G_UI_WRITE por delta; WS12 resuelve G_WRITE_CONTRACT. El TaskDoc de promoción fija archivos exactos, escenarios, pills y textos; WS40 aporta corpus si se usa. WS26.2 cubre enrutamiento en Board. `accepted_scope_nodes` sigue vacío.
