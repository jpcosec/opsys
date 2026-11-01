## REFORMULACION
WS26.1 es un nodo de implementación en `graph_ui`: habilitar autoría explícita de una tarea desde un candidato del drawer, declarando evidencia, dependencias y pills de contexto, y mostrarlas tras recargar. Resultado: UF04 sobre un TaskDoc real con esos vínculos visibles. Repo dueño: `graph_ui`; salida en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`. Límites: no editar `status` para avanzar; si una operación Git carece de contrato o dueño, queda en handoff explícito y no disponible; no exceder los endpoints autorizados; G_UI_WRITE se exige por delta y G_HUMAN_READ antes de habilitar mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar.

## AMBIGUEDADES
Ninguna. Las menciones a pills, archivos exactos y escenarios concretos quedan delegadas al TaskDoc de promoción; las operaciones y canales los produce WS12, y si faltan rigen las reglas comunes de ejecución de `alcance.md`.

## DRY-RUN
Lecturas hipotéticas: nodo WS26.1, `task-ws26-1.md`, contrato WS12 (`contratos/operaciones.md`) para autoría, evidencia, dependencias y pills; salida de WS22 para abrir TaskDoc/pills; un candidato real del drawer y su TaskDoc; evidencia satisfecha de G_CLOSEOUT; acta G_UI_WRITE del delta si se habilita UI; acta G_HUMAN_READ antes de uso de mutaciones UI.

Cambios previstos: en `authoring/`, formulario/acciones de autoría explícita que invoquen solo endpoints autorizados por WS12; vincular evidencia declarada, dependencias y pills; tras recargar, leer estado desde deskops/Board, no desde dag.yaml; tests con store temporal real o corpus WS40 cuando exista.

Dependencias y gates: WS12 debe aportar la operación pública; WS22, la representación que abre TaskDoc y pills. G_CLOSEOUT está satisfecho. G_UI_WRITE y G_HUMAN_READ siguen pendientes y se consumen por delta/uso UI. Si falta contrato, endpoint o dueño Git: registrar hueco, mostrar handoff y declarar no disponible; no inventar operación.

Validación esperada: prueba aislada de API/temporal de que el candidato queda autorado con evidencia, dependencias y pills visibles tras recargar, sin modificar `status`; validación UF04 con corpus WS40 y actas cuando correspondan. Error esperado: fallo de contrato/endpoint se traduce en handoff, no en éxito simulado.

## FUTURO
WS12 produce el contrato de operaciones. WS22 entrega la representación de Board/TaskDoc. El TaskDoc de promoción fija archivos, textos y pruebas. El receptor P01 emite el acta G_UI_WRITE por delta; WS16 produce G_HUMAN_READ. WS26.2 añade enrutamiento y capa lista. WS26 cierra cuando ambos hijos cumplen.
