REFORMULACION
- **Propósito**: implementar en `graph_ui` el enrutamiento explícito de una tarea al Board y la representación de “capa lista”, sin promoción nueva. Enrutar es añadir la tarea a `tasks` del BoardDoc por operación pública; capa lista = sin dependencias pendientes ni `files` solapados según ritual vigente.
- **Resultado**: tras enrutar, `deskops show board` muestra la tarea y la UI la distingue de una tarea en ejecución; la capa lista aparece separada de ejecución, dependencias pendientes y solapamientos; si falta la operación completa de promoción admitida por WS12, se muestra pendiente y handoff.
- **Repo/límites**: `owner_repo: graph_ui`; salida en `frontends/mindmap/views/workspace/routing/`, endpoints autorizados por WS12 y `tests/`. No implementar promoción nueva ni editar status. Glob/no-resolución dudosa no se marca lista.

AMBIGUEDADES
1. “**revisión supervisor antes de marcar lista**”: no se define quién es el supervisor, qué evidencia produce esa revisión ni cómo se refleja en la UI. Obliga a inventar un actor y un procedimiento de aprobación no descritos; podría incluso añadir un gate no previsto. Cita: “glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista, no heurística optimista”.

DRY-RUN
- **Lecturas previstas**: nodo WS26.2, contrato WS12, representación Board WS22, autoría WS26.1, ritual de fase y definiciones de gates.
- **Cambios previstos**: vistas/componentes de enrutamiento y capa lista en el `output_scope`; pruebas en `tests/`. Sin tocar status ni promoción.
- **Dependencias**: WS12 debe publicar canal, normalización/expansión de `files` y operación de promoción; WS22 aporta Board/lifecycle; WS26.1 aporta tarea autorada. G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes; G_CLOSEOUT está satisfecho.
- **Validaciones futuras**: `deskops show board` sobre store temporal o corpus WS40; distinción UI entre enrutada/en ejecución; separación de capa lista; casos de igualdad, contención de directorio y glob; handoff si falta operación.

FUTURO
- WS12 produce el contrato técnico y su recibo por delta.
- WS16 produce el acta de G_HUMAN_READ.
- El receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta concreto.
- La promoción del TaskDoc fija archivos, pills y evidencias; sigue `not_authorized` y requiere decisión humana.
