## REFORMULACION

**Propósito:** nodo agregado WS33 que reúne los trabajos de vinculación de mensajes/resultados al intento y de registro de decisión humana explícita, con deduplicación y procedencia.

**Resultado:** agregado no ejecutable; se considera cumplido cuando WS33.1 y WS33.2 cumplen su aceptación. No produce por sí mismo un artefacto distinto de las salidas de sus hijos.

**Repo dueño:** `deskops`, con `output_scope` agregado de WS33.1 y WS33.2 (`runtime/`, modelos/reportes y `tests/`).

**Límites:** backend documental, independiente del editor UI. No toca tablas Scion. Solo vincula mensajes/resultados con id de intento existente y registra decisión humana por la operación que fije WS12. Promoción `not_authorized`; no hay ejecución autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas realizadas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS33 y bloques de vecinos usados solo como contrato contextual (WS32, WS11, WS33.1, WS33.2, WS34.x, WS35, gates).

**Cambios previstos:** ninguno. Esta revisión no modifica el DAG, no promueve el nodo y no escribe TaskDoc.

**Dependencias observadas:** WS33 depende de WS32, WS11 y sus hijos WS33.1/WS33.2; requiere `G_SCION`. WS12 llega de forma transitiva por WS32/WS11, conforme a “Una dependencia transitiva cuenta como prerrequisito”. La ausencia de WS12 directo no obliga a inventar porque WS33.2 nombra el contrato WS12 y suple el hueco con dueño.

**Validaciones futuras:** comprobar aceptación de WS33.1 y WS33.2; verificar `G_SCION` producido por WS44 con operador designado en WS07; confirmar contrato WS12 para actor humano y operación de decisión; comprobar en WS05/WS44 el identificador de resultados usado por WS33.1. La aceptación agregada no requiere ejecución propia.

## FUTURO

- WS07 designa al operador Scion y al actor receptor; sin designación, `G_SCION` sigue pendiente.
- WS44 produce el probe público y la evidencia de `G_SCION`; WS05 solo inventaría.
- WS12 fija el contrato de actor humano y la operación de registro de decisión.
- WS05/WS44 exponen el identificador de resultados que WS33.1 debe usar.
- La promoción, el TaskDoc, archivos exactos y preflight quedan a decisión humana; este nodo no los fija.
- WS35 consume las salidas de WS33 para mostrar trazabilidad; no se revisa aquí.
