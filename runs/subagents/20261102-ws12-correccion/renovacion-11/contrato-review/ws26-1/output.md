## REFORMULACION
**Propósito:** preparar un candidato en `desk/drawer/tasks/` desde la UI, separando candidato rastreado (escritura directa con `expected`) y no rastreado (propuesta, handoff a `deskops edit task` y refresco). **Resultado:** candidato con contenido, dependencias, `files`, `references`, `tags`, `pills` y `closeout_evidence` editables, sin crear tarea activa ni Board. **Repo:** `graph_ui`, `output_scope` `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados y `tests/`. **Límites:** no edita `id`, `status`, `current_node`, `history` ni `from_drawer`; no rastrea por reflejo, no amplía S06, no inventa API, no commitea ni promueve.

## AMBIGUEDADES
1. «endpoints autorizados por el contrato WS12»: el contrato describe `POST /save` y el adaptador, pero no enumera una ruta de autoría concreta; obligaría a inventar endpoint o ubicación.
2. «closeout_evidence validada con el vocabulario cerrado existente» frente a «El candidato puede conservar evidencia vacía o incompleta como pendiente»: no fija si un término inválido se rechaza o se guarda pendiente; obligaría a inventar la política de validación.
3. «El handoff se ofrece solo si una comprobación previa confirma que el selector no resuelve a una tarea activa»: no detalla la comprobación ni el comportamiento ante error o ambigüedad; obligaría a inventar el criterio de resolución.
4. «cada referencia se valida (navegación autorizada, existencia, tipo PillDoc)»: no dice dónde ocurre esa validación dentro del alcance `authoring/`; obligaría a inventar backend o duplicar lógica.

## DRY-RUN
Un ejecutor leería WS12 §4.4, §3.3 y §5.9, la ruta existente de actualización, el TaskDoc y tests. Crearía el módulo en `authoring/` y pruebas. Para candidato rastreado: leería `expected`, filtraría solo campos autorables, invocaría `update` existente y esperaría 409 sin pérdida local, rechazo de protegidos, guarda WS47 y admisión WS48. Para no rastreado: mostraría propuesta, comprobaría selector contra `desk/tasks` y `show task`, generaría handoff con `--root` y refrescaría; ninguna escritura HTTP. Dependencias: WS12, WS22, WS47, WS48; gates `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_HUMAN_READ`, `G_WRITE_CONTRACT`. Errores: 409, evidencia inválida, selector coincidente, falta de admisión o lectura fallida. Validación: ambos recorridos, persistencia tras recarga, ausencia de tarea activa/Board y handoff no aplicado.

## FUTURO
WS47 y WS48 producen las guardas; WS26.2 crea y enruta la tarea activa; P01 registra acta y gates humanos; root revisa el contrato.
