## REFORMULACION

Propósito: hacer idempotente la finalización de un intento Scion, de modo que manifiesto, RunDoc y registros de closeout queden ligados al mismo id de intento.

Resultado esperado: repetir la finalización sobre un id de intento ya finalizado no crea registros nuevos y conserva identidad y evidencia; manifiesto, RunDoc y closeout coinciden en id de intento, hash de sesión y evidencia.

Repo dueño: `deskops`, con salidas en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.

Límites: no es un segundo pipeline; el manifiesto es el registro canónico por intento según el ticket de `external_references.scion`; integración por delta o ticket existente, sin duplicado paralelo (matriz WS06 llega transitivamente por WS11/WS12). No autoriza implementación hasta promoción.

## AMBIGUEDADES

1. «coinciden en id de intento, hash de sesión y evidencia» — ni el input ni el glosario definen qué es una «sesión» ni de qué se calcula el hash (sesión Scion, RunDoc, proceso local). El ejecutor tendría que inventar la entidad, su fuente y el algoritmo antes de poder hacer comprobable esa coincidencia. WS05 separa slug/agente/intento/dispatch/mensaje/conversación, pero no define «sesión».

No cuento las demás menciones condicionales («identidad de run si la API la expone»), resueltas por el inventario WS05, ni los gates pendientes (G_SCION no verificado, G_WRITE_CONTRACT per_delta), que las Reglas comunes de ejecución y la guía cubren sin inventar.

## DRY-RUN

Lecturas necesarias: ticket `external_references.scion` en `dag.yaml`, inventario `auditoria/scion.md` (WS05), contrato de operaciones WS12, `services/closure.py` y tests de closeout ya citados en G_CLOSEOUT, más los tests de WS32.1.

Cambios previstos: clave de idempotencia por id de intento en el registro; escritura/actualización sin alta duplicada de manifiesto, RunDoc ni registro de closeout; pruebas de doble finalización.

Dependencias: WS05 (identidad/API), WS12 (contrato de operaciones), WS32.1 (ids de intento generados antes del dispatch). G_CLOSEOUT satisfecho; G_SCION y G_WRITE_CONTRACT pendientes por delta.

Validaciones futuras: prueba de finalización repetida, comparación de campos entre los tres registros, ausencia de registros nuevos; ejecución solo al promover.

## FUTURO

- WS44 y el operador designado producen G_SCION mediante probe real; sin él, este nodo se detiene y registra el hueco.
- WS12 emite el recibo técnico por delta para WS32.2 (canal, efectos, errores, pruebas).
- La promoción (TaskDoc, archivos exactos, pills) decide el detalle de implementación.
- El receptor en `deskops` verifica el delta y emite recibo; el humano acepta producto, no implementación.
