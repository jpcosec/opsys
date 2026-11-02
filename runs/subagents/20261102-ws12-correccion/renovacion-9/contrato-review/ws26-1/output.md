REFORMULACION
Propósito: preparar un candidato de tarea bajo `desk/drawer/tasks/` desde la UI (UF04), sin crear tarea activa ni tocar el Board. Resultado: dos recorridos según ruta y store reales —rastreado: escritura directa por `POST /save` update con `expected`, guarda WS47, admisión WS48 y `G_PAYLOAD_PRECONDITION`, solo campos autorables— y no rastreado: propuesta, handoff a `deskops edit task` y refresco, sin escritura HTTP. Repo: graph_ui (`frontends/mindmap/views/workspace/authoring/`, endpoints, tests). Límites: no crea tarea activa ni Board (WS26.2), no rastrea por reflejo, no amplía S06, no inventa API; `status`, `current_node`, `history`, `id` y `from_drawer` protegidos; `closeout_evidence` validada y puede quedar pendiente.

AMBIGUEDADES
1. «endpoints autorizados por el contrato WS12» (nodo) frente a HO-01 «Rutas o adaptadores de UI… Ausente»: no hay ruta, módulo ni nombres fijados; obligaría a inventar la superficie HTTP y su contrato de error.
2. «entrega el comando exacto `deskops edit task <selector> <campo> <valor> --root <raíz>`» (contrato §4.4): para `pills`, `depends_on`, `files`, `references`, `tags` no se fija la forma textual de `<valor>`; obligaría a inventar su serialización.
3. «cada referencia se valida con la navegación autorizada, existencia y tipo PillDoc» (nodo): no se fija el canal de verificación (CLI `show pill`, API sldb o lectura directa); obligaría a elegirlo.
4. `requires: G_PAYLOAD_PRECONDITION` y `depends_on: WS47, WS48` son incondicionales, aunque el contrato dice que el recorrido B no usa `expected`; no queda claro si B puede entregarse antes de WS45/WS47.

DRY-RUN
Ejecución hipotética: leer contrato §3.3, 4.4, 5.9 y 6.3; consumir WS22 (lectura), WS47 (guarda), WS48 (admisión), WS45 (`expected`) y `doc_status` de sldb. Crear en `views/workspace/authoring/` el módulo de preparación, una ruta que filtre campos protegidos y aplique `expected`, y el generador de handoff con la comprobación previa del selector; tests en `tests/` con store temporal. Errores: 409 conserva buffer; rechazo de guarda o admisión bloquea y ofrece handoff; `doc_status` fallido ⇒ tratar como no rastreado. Validación: guardado y recarga, 409, propuesta/handoff sin escritura HTTP, refresco y caso activo/candidato con prefijo.

FUTURO
WS26.2 crea y enruta la tarea activa; WS19.1/WS19.2 comparten HO-02; root decide la aprobación de `G_WRITE_CONTRACT`; P01 registra el acta; la persona autoriza la creación; `promotion` sigue `not_authorized` hasta el preflight de tarea.
