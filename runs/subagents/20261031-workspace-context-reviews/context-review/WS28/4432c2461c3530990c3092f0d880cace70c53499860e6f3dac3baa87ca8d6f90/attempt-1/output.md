## REFORMULACION

**Propósito:** integrar en `graph_ui` la verificación de cierre y un handoff explícito con evidencia, usando el canal del contrato WS12.

**Resultado:** una vista/flujo que invoca `deskops closeout verify`, muestra los faltantes diagnosticados y prepara el handoff a `deskops closeout commit` por CLI manual o al coordinador activo, con pruebas y endpoints dentro del `output_scope`.

**Repo:** `graph_ui` (`frontends/mindmap/views/workspace/review/`, `endpoints`, `tests/`).

**Límites:** no commit/close desde HTTP; comando o solicitud no equivalen a cierre; sin terminal embebido genérico; G_HUMAN_READ se exige para habilitar mutaciones en UI, no para desarrollo/pruebas aisladas de API; los gates de escritura se evalúan por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** nodo WS28, guía, brief, alcance, decisiones, cobertura; contratos vecinos WS12/WS27/WS30 y gates suministrados; `task-ws28.md` al promover. Sin ejecutar.
- **Cambios previstos:** integrar verificación/diagnóstico de `deskops closeout verify` y handoff con evidencia bajo el `output_scope`; endpoints y tests.
- **Dependencias:** WS27 y WS12; G_CLOSEOUT satisfecho; G_HUMAN_READ pendiente de WS16; G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta con recibo propio.
- **Validaciones futuras:** pruebas aisladas de API con store temporal; acta G_HUMAN_READ antes de mutaciones UI; validación UF05 en WS30; recibo per_delta de WS12.

## FUTURO

WS12 debe fijar el canal público, la política de coordinador activo y el contrato de operaciones. WS16 produce el acta G_HUMAN_READ. El CLI o coordinador externo ejecuta el commit de closeout y la confirmación con `deskops show task`; WS28 no lo sustituye. WS30 valida UF05. El TaskDoc de promoción precisará archivos, textos y evidencia del handoff.
