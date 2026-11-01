## REFORMULACION

Encargo: nodo agregado `WS26` «Integrar autoría y contexto de tareas» en `graph_ui`; no se ejecuta, se cumple cuando `WS26.1` y `WS26.2` cumplen su aceptación. Resultado esperado: autoría explícita desde candidato con evidencia, dependencias y pills de contexto, más enrutamiento en Board y vista de capa lista, sin confundir Board con ejecución ni crear una promoción nueva. Límites: mutaciones UI solo con gates; promoción únicamente por operación completa admitida por WS12 o handoff; no editar status para avanzar; agregado sin archivos propios.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Nodo agregado no ejecutable: no cambia archivos por sí mismo. Un ejecutor futuro cumpliría mediante sus hijos:

- `WS26.1` modificaría `frontends/mindmap/views/workspace/authoring/` y `tests/`, usando endpoints autorizados por WS12 y la lectura/selección de WS22. Consumiría G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Validaría que el candidato queda autorado con evidencia, dependencias y pills visibles tras recargar, sin editar status. Si falta contrato/operación Git, dejaría handoff y declararía no disponible.
- `WS26.2` modificaría `frontends/mindmap/views/workspace/routing/` y `tests/`, invocando solo operación pública admitida por WS12. Validaría que `deskops show board` muestra la tarea enrutada y que la UI separa capa lista, ejecución y bloqueos por dependencias/solapamiento. Glob o resolución dudosa quedaría «no comprobado» con revisión de supervisor; no habría promoción nueva ni heurística optimista.
- Errores: contrato ausente → detenerse, registrar hueco y handoff; G_HUMAN_READ pendiente bloquea uso de mutaciones UI, no pruebas aisladas de API; G_UI_WRITE se exige por delta concreto.

Validación agregada esperada: ambas aceptaciones hijas registradas; WS30 podrá comprobar UF04 sobre TaskDoc real.

## FUTURO

WS12 produce el contrato de operaciones; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite recibos G_UI_WRITE por delta; WS30 valida manualmente; WS28 y el canal externo gestionan cierre/promoción. Esas dependencias no son ambigüedades de este nodo.
