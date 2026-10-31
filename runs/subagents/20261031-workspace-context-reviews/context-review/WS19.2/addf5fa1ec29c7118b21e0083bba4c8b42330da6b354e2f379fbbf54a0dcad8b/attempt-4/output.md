## REFORMULACION

**Propósito:** implementar en `graph_ui` el alta y baja de relaciones que el contrato WS12 declare permitidas, sin definir semántica de relaciones en el componente.

**Resultado:** acciones de mutación de relaciones que usan la API real y la revisión/before-image, persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo dueño:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** no crear semántica de relaciones en el componente; solo operaciones incluidas en la whitelist contractual. Depende de WS12 y WS16 y requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

El nodo nombra el contrato que define las relaciones permitidas («permitidas por contrato»), la API («usando API real») y la revisión («before-image»); WS12 produce la whitelist y las capabilities, y `alcance.md` resuelve qué hacer si faltan. La aceptación es comprobable: persistencia tras recarga y rechazo visible de relación no permitida o revisión obsoleta. Los textos exactos de pantalla y archivos quedan delegados al TaskDoc de promoción.

## DRY-RUN

**Lecturas previstas:** nodo WS19.2 y vecinos en `dag.yaml`; `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`; contrato `contratos/operaciones.md` de WS12; acta de WS16; TaskDoc `task-ws19-2.md` al promoverse.

**Cambios previstos:** componentes de alta/baja de relaciones en `frontends/mindmap/views/workspace/relations/`, llamadas a endpoints autorizados, manejo visible de rechazo, pruebas en `tests/`.

**Dependencias:** WS12 (whitelist/capabilities y gates G_UI_WRITE/G_WRITE_CONTRACT); WS16 (G_HUMAN_READ); matriz WS06 de forma transitiva; WS19.1 como hermano del agregado.

**Validaciones futuras:** alta y baja persisten y se confirman tras recarga; relación no permitida rechazada con error visible; revisión obsoleta rechazada con error visible; pruebas con store temporal o corpus WS40.

## FUTURO

- WS12 debe entregar la whitelist por campo/operación y registrar canal, efectos y revisión; también resuelve G_UI_WRITE y G_WRITE_CONTRACT.
- WS16 debe producir el acta humana de lectura (G_HUMAN_READ).
- El humano debe resolver P01/P03–P05 y designar responsables receptores en WS07.
- La promoción debe fijar archivos exactos, escenarios y textos de pantalla dentro de la aceptación.
