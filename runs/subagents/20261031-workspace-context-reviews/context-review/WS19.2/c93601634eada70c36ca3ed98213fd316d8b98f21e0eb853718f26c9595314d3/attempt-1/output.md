## REFORMULACION

**Propósito:** implementar en `graph_ui` el alta y baja de relaciones permitidas por el contrato de escritura.
**Resultado:** vistas/componentes en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados y tests.
**Repo dueño:** `graph_ui`.
**Límites:** usar API real y before-image; no crear semántica de relaciones en el componente; promoción no autorizada y sujeta a preflight.

## AMBIGUEDADES

1. «usando API real y before-image»  
   No se define qué es la before-image, quién la produce, su formato, persistencia ni qué ocurre si no está disponible. WS12 cubre contrato de operaciones, CAS/locks y fallos parciales, pero el nodo no declara explícitamente que la before-image forme parte de ese contrato. El ejecutor tendría que inventar su modelo y ciclo de vida.

2. «endpoints autorizados por el contrato WS12»  
   El nodo nombra a WS12 como productor, pero no indica qué hacer si el contrato no incluye endpoints de alta/baja de relaciones. Sin un fallback explícito en el encargo (detener, handoff o registrar hueco), el ejecutor debe decidir por su cuenta.

## DRY-RUN

**Lecturas previstas:** nodo WS19.2, contrato producido por WS12, evidencias de gates, task file y referencias de `graph_ui`.
**Cambios previstos:** componentes de relaciones en workspace, integración con endpoints autorizados y tests.
**Dependencias:** WS12 y WS16; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.
**Validaciones futuras:** alta y baja persisten tras recargar; relación no permitida rechazada con error visible; revisión obsoleta rechazada; aceptación del delta en `graph_ui`; contrato verificado; preflight de promoción. Sin ejecutar.

## FUTURO

WS12 debe producir whitelist, endpoints, revisión/CAS y, si corresponde, before-image. WS07 debe designar actores humanos. El responsable de `graph_ui` debe aceptar el delta (`G_UI_WRITE`). La persona usuaria resuelve los gates. WS06/integración decide ticket receptor y no duplicación. La promoción requiere autorización posterior.
