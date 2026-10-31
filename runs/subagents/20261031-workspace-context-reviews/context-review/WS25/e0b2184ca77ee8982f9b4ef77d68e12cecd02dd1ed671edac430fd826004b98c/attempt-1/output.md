## REFORMULACION

**Propósito:** nodo agregado de implementación que integra en la UI de `graph_ui` la lectura/ack/respuesta local de mensajes y la captura interna en drawer/protoátomo, usando solo operaciones permitidas por contrato; el ack no equivale a aprobación.

**Resultado:** agregado de las salidas de WS25.1 (`views/workspace/inbox/`) y WS25.2 (`views/workspace/capture/`), con endpoints autorizados por WS12 y tests.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).

**Límites:** agregado no ejecutable; termina cuando sus hijos cumplen aceptación; no confundir ack con aprobación; sin tarea implícita ni envío interdesk; mutaciones sujetas a contrato y gates.

## AMBIGUEDADES

1. «captura interna de drawer/protoátomo» — “protoátomo” no aparece definido en brief, glosario, alcance ni decisiones, y no se nombra fuente que fije su esquema, campos o ciclo de vida. Obligaría al ejecutor a inventar qué es un protoátomo, cómo se distingue de un drawer y qué datos mínimos debe persistir.

## DRY-RUN

- **Lecturas:** `dag.yaml` (WS25 y vecinos), guía, brief, alcance, decisiones, cobertura; bloques de hijos para entender el agregado.
- **Cambios previstos:** ninguno directo en WS25; al cerrar hijos se agregan UI de inbox, UI de captura y tests.
- **Dependencias:** WS12 (contrato), WS16 (lectura humana), WS25.1/WS25.2; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT` (pendientes).
- **Validaciones futuras:** aceptación de hijos; WS30 valida UF02/03 manualmente; promoción exige archivos exactos, pills, evidencia y preflight de tarea; hoy `not_authorized`.

## FUTURO

WS12 produce la whitelist/contrato y acepta el delta de `graph_ui` (`G_UI_WRITE`, `G_WRITE_CONTRACT`); WS16 produce `G_HUMAN_READ`; el humano confirma P01/P03/P04/P08 y decide la promoción; WS30 valida el recorrido manual.
