## REFORMULACION

**Propósito:** implementar en `graph_ui` el alta y baja de relaciones que autorice el contrato WS12, usando API real y before-image, sin definir semántica de relaciones dentro del componente.

**Resultado:** las relaciones persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo:** `graph_ui`. Salidas en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** no crear semántica de relaciones; el uso de mutaciones en UI queda sujeto a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; si falta API/contrato, detenerse y registrar el hueco con repo dueño conforme a las reglas comunes; promoción no autorizada. No commit automático ni cierre desde UI.

## AMBIGUEDADES

Ninguna. Lo que podría parecerlo ya está cubierto: «relaciones permitidas» y «endpoints autorizados por el contrato WS12» nombran productor (WS12) y las reglas comunes resuelven la ausencia de contrato/API; «error visible» es texto de pantalla que fijará el TaskDoc de promoción; los gates pendientes son intencionales y se evalúan por delta concreto; la base reutilizable de workspace está identificada en reconciliacion.md.

## DRY-RUN

**Lecturas previstas:** contrato WS12 (whitelist de relaciones, campos, canal, actor, revisión y errores); base `a1b2b22/f16fcd1/134a665` y archivos de workspace citados; actas del delta para G_UI_WRITE y G_HUMAN_READ.

**Cambios previstos:** componentes y llamadas de alta/baja de relaciones en `views/workspace/relations/`, más pruebas; sin semántica nueva ni commit automático.

**Dependencias:** WS12 y, por transitividad, WS11/WS08 y WS02–WS10; contrato técnico de la operación y API pública existente; gates por delta, no aceptación conjunta.

**Validaciones futuras:** alta y baja persisten tras recarga; relación no permitida rechazada; revisión obsoleta rechazada con error visible; pruebas con store temporal real o corpus WS40.

## FUTURO

- WS12 publica la whitelist y los endpoints/errores aplicables.
- P01 emite el acta G_UI_WRITE del delta concreto; WS16 produce el acta G_HUMAN_READ.
- El TaskDoc de promoción fija archivos exactos, escenarios de prueba y textos de pantalla.
- Si la API de relaciones no existe, un nodo/productor posterior debe cubrirla; entretanto la operación queda no disponible.
