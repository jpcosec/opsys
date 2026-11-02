REFORMULACION
WS26.1 «Autorar tarea, evidencia y contexto»: preparar un candidato en `desk/drawer/tasks/` desde la UI, sin crear tarea activa ni añadir al Board. Resultado: dos recorridos separados por ruta y store reales. Rastreado: `update` con `expected`, solo campos autorables, con WS47, WS48 y `G_PAYLOAD_PRECONDITION`. No rastreado: propuesta, handoff a `deskops edit task` y refresco, sin escritura HTTP. Repo: graph_ui (`frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12, `tests/`). Límites: no editar `id`, `status`, `current_node`, `history` ni `from_drawer`; no rastrear por reflejo, ampliar S06 ni inventar API; pills por reemplazo completo validado; handoff solo si el selector no resuelve a tarea activa; `G_HUMAN_READ` habilita mutaciones de UI, no el desarrollo/prueba aislados.

AMBIGUEDADES
1. «endpoints autorizados por el contrato WS12» (`dag.yaml`, `output_scope`). WS12 describe `POST /save update` y `/api/save` local, pero no fija el endpoint de autoría ni su contrato de error. Obligaría a inventar ruta, forma de error y si hay proxy nuevo o reutilización estricta.
2. «El handoff se ofrece solo si una comprobación previa confirma que el selector no resuelve a una tarea activa» (`scope`) frente a «propuesta y handoff correctos» (`acceptance`). No queda explícito el resultado exigido cuando la comprobación falla. Obligaría a inventar la UI y el texto del caso «no se ofrece comando», aunque WS12 4.4 lo describe.
3. «Evidencia vacía o incompleta queda pendiente» (`acceptance`). No aclara si el candidato puede guardarse con evidencia vacía o solo mostrarse pendiente sin guardado. Obligaría a inventar la regla de guardado del candidato.

DRY-RUN
Lecturas: WS12 3.3, 4.4, 5.9, 6.7; aceptaciones WS47/WS48; `GU/persistence.py`, `sldb_adapter.py`, `deskops_routes.py`, vistas y tests. Cambios previstos: vista de autoría, filtro de campos protegidos, envío `expected`, comprobación previa del selector, generador de handoff y refresco; tests de recorridos A/B. Dependencias: WS22, WS47, WS48; gates citados. Validaciones: 409 sin pérdida local; rechazo de protegidos; cero escrituras HTTP en B; selector coincidente sin comando; evidencia pendiente. Errores esperados: 409, rechazo de WS47, denegación de WS48, selector no comprobable.

FUTURO
WS47 aporta la guarda de contenido; WS48, la admisión; WS22, lectura; WS45, precondición; P01 registra el acta y `G_UI_WRITE`; una persona autoriza y `G_HUMAN_READ` habilita el uso. WS26.2 crea y enruta la tarea activa.
