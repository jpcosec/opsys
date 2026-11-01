## REFORMULACION
PK08 es un agregado de planificación no ejecutable del ramal Scion opcional. Su propósito es cerrar un paquete verificable de delegación: intento/manifiesto/RunDoc/cierre consistentes e idempotentes, mensajes con procedencia/dedup, dispatch intent/confirmed separados, permisos explícitos, trazas, intervención humana y publicación del capítulo. El resultado sustantivo es la integración de las salidas de WS32–WS38 y WS44, no una implementación nueva ni la ejecución de esos nodos. Repo dueño: `deskops`. Límites: no duplicar el pipeline Scion; ningún permiso de núcleo se convierte en dispatch; sin acceso real el ramal queda bloqueado; no añade tareas ni aristas; los gates pendientes son intencionales.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Hipotético, sin ejecutar. PK08 no corre: termina cuando terminan sus hijos conforme a `dag.yaml`.

WS05 produce el inventario `auditoria/scion.md`, que alimenta WS44; WS44, con WS07 y `G_PRODUCT`, ejecuta el probe read-only y, con operador/acceso registrados, produce `G_SCION` en `auditoria/scion-probe.md`. WS32 consume WS05, WS12, `G_SCION`, `G_CLOSEOUT` y `G_WRITE_CONTRACT`, y entrega identidad/registro/idempotencia mediante WS32.1/WS32.2. WS33 consume WS32 y WS11, y entrega mensajes/resultados/decisiones con dedup y procedencia. WS34 consume WS33 y WS12 y entrega el adaptador dispatch/reply. WS35 consume WS33 y WS27 y produce la vista de ejecución; puede avanzar tras WS33, sin esperar a WS34. WS36 consume WS34 y WS35 y entrega la UI de delegación/intervención, mostrando ausencia de API o permisos como error probado. WS37 consume WS36 y WS30 y produce el acta UF06 real, sin mocks. WS38 consume WS37 y WS31 y publica manual/átomos.

Validación conjunta: WS37 debe demostrar el recorrido real con actor humano; WS38 debe remitir a esa acta, a operaciones reales y a átomos vinculados. Si falta `G_SCION`, `G_EXEC`, API o acceso, se bloquea y se registra el hueco; no se sustituye ni se declara cerrado.

## FUTURO
El solicitante designa operador/acceso Scion y autoriza `G_EXEC`; WS44 realiza el probe real; WS37 obtiene aceptación humana; WS38 publica tras el manual básico.
