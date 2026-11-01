## REFORMULACION

**Propósito:** implementar en el workspace la edición de relaciones permitidas por contrato: alta y baja, usando API real y before-image, sin introducir semántica de relaciones en el componente.

**Resultado:** altas y bajas persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo:** `graph_ui`.

**Límites:** salida en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`; no se autoriza promoción; no se crea semántica de relaciones en el componente; mutaciones en UI sujetas a G_HUMAN_READ; precondición y contrato sujetos a WS12/WS45.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS19.2, contrato WS12, gates `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, ticket de edición referenciado y matriz WS06/reconciliación.

**Cambios previstos:** componente de relaciones bajo `views/workspace/relations/`, consumo de endpoints autorizados y pruebas en `tests/`. Sin cambios en otros repos ni en semántica de relaciones.

**Dependencias:** WS12 para whitelist, canal, efectos y representación de la precondición; WS45 para G_PAYLOAD_PRECONDITION; WS16 para G_HUMAN_READ; receptor P01 para G_UI_WRITE por delta. El trabajo no puede habilitar mutaciones en UI hasta que G_HUMAN_READ esté satisfecho.

**Validaciones futuras:** pruebas focalizadas con store temporal real, alta/baja persistente tras recarga, rechazo visible de relación no permitida y de revisión obsoleta, y evidencia de gates en el repo dueño. No se ejecuta nada en esta revisión.

## FUTURO

WS12 fijará whitelist por operación/campo, endpoints autorizados, efectos y representación de la precondición. WS45 producirá o verificará G_PAYLOAD_PRECONDITION. WS16 emitirá el acta de G_HUMAN_READ. El receptor P01 producirá el acta G_UI_WRITE del delta concreto al preparar/promover. La promoción fijará archivos exactos, escenarios y textos dentro de la aceptación; WS06/reconciliación determinará si se extiende el ticket de edición o se registra delta, sin duplicar. WS19 cerrará cuando cierren sus hijos.
