## REFORMULACION
El encargo de WS09 es un nodo de planificación ejecutable —no agregado—: precisar el catálogo de renderizaciones inventariando fuente, contrato, renderer, acción/dueño, error y estado de cada fila. El resultado es actualizar `borradores/vistas.md` con la ficha por fila, incluyendo filas compuestas y clasificación authored/derivado/preferencia local. Repo dueño: `deskops`. Límites: solo planificación; no implementa UI/API ni ejecuta; no inventa actores, APIs ni disponibilidad; no amplía `output_scope`. Depende de WS07, WS10 y WS08; `G_PRODUCT` está satisfecho.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas hipotéticas: `borradores/vistas.md`, contratos de WS07/WS08/WS10 (`decisiones.md`, `user-flows.md`, `manual.md`), auditorías `deskops.md`, `infraestructura.md`, `ui.md`, `reconciliacion.md`, `brief.md` y `alcance.md`.

Cambios previstos: solo `borradores/vistas.md`; recorrer cada fila y ficha F01–F20, completar origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; clasificar authored/derivado/preferencia local; marcar campos sin evidencia como «no definido» con productor WS11/WS12 o implementación futura; separar filas compuestas solo si el delta tiene evidencia/estado independiente.

Dependencias y gates: consumir decisiones de WS07, convención de estado de WS10 y UFs de WS08; no exigir WS11/WS12 como dependencias, solo asignarlos como productores de huecos. `G_PRODUCT` ya satisfecho.

Errores y validación esperada: si falta evidencia, no inventar actor/API; registrar «no definido» y productor. Si falta una salida de dependencia, detenerse y registrar el hueco según reglas comunes. Validar que cada fila/ficha tenga los campos exigidos, estados permitidos, clasificación correcta, contratos/renderers/acciones/errores no inventados y que no se escriba fuera de `borradores/vistas.md`.

## FUTURO
WS11 precisará identidad, navegación y productores de campos no definidos; WS12 precisará contratos de escritura, errores y permisos; WS18 elegirá selecciones concretas de ViewDoc a partir de WS09/WS11; WS22/WS23/WS24 y otras implementaciones consumirán el catálogo. La recepción técnica por delta y las actas humanas corresponden a otros nodos o al solicitante, no a WS09.
