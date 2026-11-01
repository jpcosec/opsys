## REFORMULACION

**Propósito:** integrar en graph_ui el enrutamiento explícito de tareas en el Board y una representación de «capa lista» basada en dependencias y solapamiento de archivos. **Resultado:** vista/UI en `frontends/mindmap/views/workspace/routing/` con pruebas; tras enrutar por operación pública, `deskops show board` refleja la tarea y la UI la distingue de una en ejecución; la capa lista se separa de tareas ejecutándose, con dependencias pendientes o archivos solapados. **Repo dueño:** graph_ui. **Límites:** no implementar promoción nueva; invocar solo la operación completa admitida por WS12 o dejar handoff/pendiente; no editar `status` para avanzar; G_HUMAN_READ condiciona uso de mutaciones en UI, no desarrollo/pruebas aisladas de API.

## AMBIGUEDADES

1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista»: no se define quién es «supervisor», por qué canal revisa ni cómo se registra esa revisión. Obligaría a inventar actor, evidencia y efecto bloqueante.

## DRY-RUN

Un ejecutor futuro leería el nodo, `task-ws26-2.md`, el contrato WS12, la vista Board de WS22 y la autoría de WS26.1. Crearía componentes de enrutamiento y tests en el `output_scope`. Consumiría de WS12 la operación pública de enrutado y las reglas de normalización/expansión de `files`; de WS26.1, la tarea autorada con dependencias; de WS22, la representación del Board. Antes de mutar UI comprobaría G_HUMAN_READ; para su delta exigiría recibos G_UI_WRITE y G_WRITE_CONTRACT; G_CLOSEOUT ya está satisfecho. Si falta contrato, operación o API, se detendría, registraría el hueco y mostraría handoff, no promoción terminada. Si la ruta es glob o dudosa, marcaría «no comprobado». Validaría con tests y `deskops show board`, verificando distinción visual y separación de la capa lista.

## FUTURO

WS12 produce el contrato de operaciones y normalización de rutas; WS26.1 produce la tarea autorada; WS22, la representación Board; el receptor P01 emite el acta G_UI_WRITE por delta; WS16 produce G_HUMAN_READ. La promoción del nodo queda a preflight/task-only posterior, no autorizada aquí.
