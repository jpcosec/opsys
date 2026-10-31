## REFORMULACION

**Propósito:** agrupar la producción del paquete de decisiones y contratos que permite preparar cada delta del workspace documental.

**Resultado sustantivo:** un conjunto coherente —`decisiones.md`/`owner-decisions.json`, `user-flows.md`, `vistas.md`, `manual.md`, `navegacion.md` y `operaciones.md`— con P01–P09 trazadas, cada UF01–UF10 con operaciones/errores/IDs/gates, cada vista con soporte/origen/contrato/renderer, y APIs/huecos con productor; recepción técnica por delta y editable solo con G_SOURCE.

**Repo dueño:** deskops.

**Límites:** PK02 no ejecuta ni autoriza tareas, no añade aristas, no sustituye contratos ausentes, no crea actas interrepo; los extras no bloquean el núcleo; la revisión de comprensión no acredita producto entregado.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». No se indica qué artefacto o evidencia constituye esa integración ni quién la valida; obligaría a inventar un entregable integrador y su criterio de comprobación.

## DRY-RUN

Orden hipotético: **WS07 → WS08 y WS10 en paralelo → WS09 → WS11 → WS12**.

- **WS07** consume WS06 y el registro humano; entrega decisiones, `source_mode` y restricciones a todos.
- **WS08** entrega `user-flows.md` a WS09/WS11/WS12.
- **WS10** entrega convención y etiquetas del manual a WS09.
- **WS09** entrega catálogo de vistas a WS11.
- **WS11** entrega identidad/navegación, clasificación de huecos y mapa de recepción a WS12.
- **WS12** entrega whitelist de operaciones.

Validación futura, sin ejecutar: trazar Pxx; comprobar UF→operación/error/nodo/gate; vista→origen/contrato/renderer/estado; coherencia navegación↔vistas↔UFs; whitelist cubre mutaciones referidas y huecos con productor; G_SOURCE pendiente impide editable; recepción por delta solo mapeada, nunca supuesta.

## FUTURO

Salidas de los hijos, actas de P01 por delta, G_SOURCE de WS20, corpus WS40, gates WS16/30/37/39, G_SPEC_VIEW de WS18 y aceptación en repos receptores.
