## REFORMULACION

**Propósito:** encargar en `graph_ui` el alta/baja de relaciones permitidas por el contrato de WS12, usando API real y before-image, sin crear semántica de relaciones en el componente.

**Resultado:** mutaciones de relaciones que persisten y se confirman tras recargar; rechazo visible de una relación no permitida o de una revisión obsoleta.

**Repo:** `graph_ui`. **Salida:** `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** depende de WS12; requiere `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; no duplicar implementación ni inferir cierre por commit; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

El contrato que fija relaciones permitidas, endpoints y revisión esperada tiene productor nombrado —WS12— y las reglas comunes de ejecución cubren su ausencia. Los gates pendientes son intencionales y se evalúan por delta.

## DRY-RUN

**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.2, agregado WS19 y contrato vecino WS12.

**Cambios previstos:** implementar UI de alta/baja en la ruta declarada y pruebas; consumir endpoints y before-image definidos por WS12; reutilizar el workspace integrado y el ticket receptor sin duplicar.

**Dependencias:** contrato WS12; gates por delta `G_WRITE_CONTRACT`, `G_UI_WRITE` y `G_HUMAN_READ`; reconciliación WS06 vía WS11/WS12.

**Validaciones futuras:** persistencia tras recarga; error visible ante relación no permitida y revisión obsoleta; pruebas aisladas de API permitidas antes del acta humana de lectura. No se ejecuta nada.

## FUTURO

WS12 produce el contrato, endpoints/whitelist y `G_WRITE_CONTRACT` por delta. El receptor P01 emite el acta `G_UI_WRITE` con alcance y commit verificable. WS16/humano satisface `G_HUMAN_READ`. WS19 cierra cuando cumplen sus hijos. El TaskDoc de promoción fija archivos exactos y casos de prueba.
