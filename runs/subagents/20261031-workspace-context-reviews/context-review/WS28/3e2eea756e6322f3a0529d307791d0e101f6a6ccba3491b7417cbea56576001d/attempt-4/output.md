## REFORMULACION

**Propósito:** WS28 es un encargo de implementación para integrar en `graph_ui` la verificación de closeout y el handoff externo con evidencia, sin cerrar tareas desde HTTP.

**Resultado:** piezas en `frontends/mindmap/views/workspace/review/`, endpoints y tests que: ejecutan o solicitan `deskops closeout verify` por el canal definido en WS12, diagnostican faltantes y ofrecen handoff explícito a `deskops closeout commit` por CLI en modo manual, o al coordinador si está activo (P03).

**Repo dueño:** `graph_ui`.

**Límites:** no commit/close desde HTTP en baseline; sin terminal embebido genérico. Depende de WS27 y WS12; requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS28, WS27, WS12 y gates), futuro `contratos/operaciones.md` de WS12, salidas de WS27, reglas de alcance y decisión P03.
- **Cambios previstos:** vista/flujo de revisión de closeout, endpoints de verificación/handoff y tests en `graph_ui`; los archivos exactos y TaskDoc los fija la promoción.
- **Dependencias:** WS27 aporta diff/evidencia; WS12 define capability, canal y efectos; G_CLOSEOUT aporta contrato de evidencia; G_HUMAN_READ y G_UI_WRITE/G_WRITE_CONTRACT condicionan la escritura. Si falta el contrato, se detiene y se registra el hueco con repo dueño, sin sustituto.
- **Validaciones futuras:** `deskops closeout verify` por canal autorizado; diagnóstico de faltantes; handoff visible; confirmación externa mediante `deskops show task` y commit de closeout; refresco de estado; comprobación de que comando o solicitud no equivalen a cierre; ausencia de terminal genérico.

## FUTURO

- **WS30** valida UF05 manualmente bajo protocolo humano.
- **WS12** produce el contrato de operaciones y los gates G_UI_WRITE/G_WRITE_CONTRACT.
- **WS07/humano** designa responsables y resuelve P03; G_CLOSEOUT tiene resolver externo.
- **Promoción** requiere autorización explícita y TaskDoc con archivos, escenarios y evidencia.
