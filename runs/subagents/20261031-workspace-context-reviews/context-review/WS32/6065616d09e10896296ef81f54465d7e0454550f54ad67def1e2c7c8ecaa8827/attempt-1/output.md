## REFORMULACION

**Propósito:** unificar identidad de intento y cierre Scion reutilizando el candidato de drawer, sin crear un segundo pipeline.
**Resultado:** agregado cuyas salidas son las de WS32.1 y WS32.2; no ejecutable por sí mismo.
**Repo dueño:** deskops.
**Límites:** no es ticket del Board; no hay dispatch/reply de red ni eventos Hub simulados; identidad/registro/idempotencia se prueban localmente con operaciones reales sobre store temporal; el estado Hub real queda para WS34/WS37 bajo G_EXEC.

## AMBIGUEDADES

Ninguna.

El nodo es agregado y su aceptación queda definida por la aceptación de sus hijos. Los gates pendientes (G_SCION, G_WRITE_CONTRACT) son intencionales y no exigen inventar aprobación. La fuente del candidato está nombrada y existe (`external_references.scion`, sha256 registrado). Las dependencias WS05/WS12 tienen productor explícito para inventario y contrato.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo WS32 y gates), guía de revisión, brief, alcance, decisiones, reconciliación y candidato de drawer referenciado.
**Cambios previstos:** ninguno; WS32 es agregado y su promoción está marcada `not_authorized`.
**Dependencias:** WS05 (inventario Scion, aún no ejecutado), WS12 (contrato de operaciones, G_WRITE_CONTRACT pendiente), WS32.1 y WS32.2 (hijos ejecutables). G_CLOSEOUT está satisfecho.
**Validaciones futuras:** aceptación combinada de WS32.1 (IDs distintos antes de dispatch, sin simular Hub) y WS32.2 (idempotencia y coincidencia manifiesto/RunDoc/closeout); recepción por delta de G_WRITE_CONTRACT para WS32/WS32.1/WS32.2; G_SCION solo mediante WS44. No se ejecuta ninguna prueba en esta revisión.

## FUTURO

- **WS05** debe producir el inventario de identidad/API Scion; sin él, WS32.1 declara hueco, no inventa almacenamiento.
- **WS44** produce G_SCION con probe real; WS32 no lo sustituye.
- **WS12** fija contrato/ubicación del registro por intento y la representación de precondición; WS32.1 la materializa.
- **WS32.1/WS32.2** ejecutan y aportan evidencia local; **WS34/WS37** demuestran dispatch real y correlación bajo G_EXEC.
- **Humano/receptor P01** decide promoción y acta por delta; el plan solo enlaza recibos existentes.
