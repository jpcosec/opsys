## REFORMULACION

WS26.1 es un nodo `implementation` de `graph_ui` cuyo propósito es autorar una tarea desde un candidato real del drawer, con evidencia declarada, dependencias y pills de contexto vinculadas, persistentes y visibles tras recargar. Depende del contrato WS12 y de la representación de WS22; G_CLOSEOUT está satisfecho, mientras G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes por delta. Límites: no editar `status` para avanzar, no implementar promoción/enrutamiento —eso corresponde a WS26.2— ni commits; una operación Git sin contrato o dueño queda en handoff explícito y no disponible. Promoción no autorizada.

## AMBIGUEDADES

ninguna

## DRY-RUN

Lecturas: nodo y `task_file`; contrato WS12 (`contratos/operaciones.md`); salida de WS22; modelos TaskDoc/lifecycle y API deskops; recibos de gates y reglas de alcance. Cambios previstos: componentes en `frontends/mindmap/views/workspace/authoring/` y tests; la UI invoca la operación autorizada por WS12 para crear tarea desde archivo del drawer, declarar evidencia, dependencias y pills; recarga y muestra el resultado.

Dependencias consumidas: WS12 debe aportar operación, campos, actor, revisión y errores; WS22 el render de TaskDoc y dependencias; G_CLOSEOUT ya satisfecho; G_HUMAN_READ antes de habilitar uso de mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT por delta para WS26.1. Si falta contrato, dato o permiso: detener, registrar hueco con repo dueño y dejar la operación no disponible; Git sin contrato/dueño → handoff.

Validación esperada: prueba con store temporal real o corpus WS40 sobre TaskDoc real; comprobar autoría, evidencia, dependencias y pills visibles tras recargar; verificar que no se editó `status` ni se promovió; tests en graph_ui; acta G_UI_WRITE en repo receptor y WS26.1 en `accepted_scope_nodes` de WS12. Un gate pendiente bloquea el uso que lo exige, no las pruebas aisladas de API.

## FUTURO

WS12 fija la operación y campos exactos; WS16 produce el acta de lectura; el receptor P01 emite el acta G_UI_WRITE por delta en graph_ui; WS26.2 enruta en Board y gestiona promoción/handoff; WS22 aporta la representación; WS40 el corpus. El TaskDoc de promoción fija archivos, escenarios y textos. La aceptación de gates corresponde a humanos.
