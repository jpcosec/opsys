## REFORMULACION

**Propósito:** agrupar la producción de contratos de producto, user-flows, manual, vistas, navegación y operaciones que permiten preparar cada delta del workspace documental.

**Resultado:** paquete integrado en `deskops` con `decisiones.md`/`owner-decisions.json`, `borradores/user-flows.md`, `borradores/manual.md`, `borradores/vistas.md`, `contratos/navegacion.md` y `contratos/operaciones.md`, trazando P01–P09, todas las UF, soporte/origen de vistas y APIs/huecos con productor.

**Repo dueño:** `deskops`.

**Límites:** agrupación sin ejecución propia ni autorización de tareas; no añade aristas; no acredita producto, recepción de deltas ni permisos Scion; termina cuando terminan sus hijos.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». No se define qué evidencia demuestra esa integración —coherencia cruzada, acta humana o ejecución del resultado—, lo que obligaría a inventar el criterio de cierre del agregado.

## DRY-RUN

Lecturas hipotéticas: `dag.yaml`, `decisiones.md`, `owner-decisions.json`, auditorías WS02–04, `reconciliacion.md` de WS06 y salidas previas de hijos.

Orden por aristas:

1. WS07, tras WS06, consolida Pxx y entrega base a WS08/WS10.
2. WS08 produce `user-flows.md` y lo pasa a WS09/WS11/WS12.
3. WS10 produce `manual.md` y lo pasa a WS09.
4. WS09 produce `vistas.md` y lo pasa a WS11.
5. WS11 produce `navegacion.md` y lo pasa a WS12.
6. WS12 produce `operaciones.md`.

Cambios previstos: solo documentos de planificación en `deskops`.

Dependencias: WS02/WS06 previos; `G_PRODUCT` en WS08–WS11 y `G_WRITE_POLICY` en WS12.

Validación futura: comprobar que cada UF tiene operación/error/ID/gate y aparece cubierta por navegación y operaciones; que cada fila de vistas declara soporte, contrato o «sin contrato», renderer, dueño y error; que cada API/hueco nombra productor; y revisar coherencia Pxx. No se ejecuta.

## FUTURO

WS40 genera el corpus Taller; WS20/`G_SOURCE` habilita raw-source; WS45/`G_PAYLOAD_PRECONDITION` cubre la precondición de payload; P01 y repos receptores emiten actas por delta; `G_WRITE_POLICY` se resuelve; pruebas humanas WS16/30/37/39. Nada de esto se inventa aquí.
