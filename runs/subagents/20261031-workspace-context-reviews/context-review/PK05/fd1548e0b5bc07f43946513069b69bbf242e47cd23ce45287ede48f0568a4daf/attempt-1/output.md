## REFORMULACION

**Propósito:** agrupar la entrega M (autoría y operación manual) como macroencargo de planificación, sin ejecución propia.

**Resultado:** paquete verificable de edición de campos con conflicto, guardado fuente reversible, alternancia fuente/render, captura/triage, autoría de tareas, diff/evidencia, handoff de cierre, operaciones de conocimiento y validación humana UF02–05.

**Repo:** `deskops` (agrupación); hijos en `graph_ui` y `sldb`.

**Límites:** no ejecuta; no crea tareas ni aristas; no sustituye gates; con otro coordinador escritor, UI en read-only/handoff; guardar no hace commit; sin closeout HTTP; mutaciones UI esperan G_HUMAN_READ; desarrollo/pruebas API aisladas pueden avanzar.

## AMBIGUEDADES

1. «WS12→WS19 y sus hijos; … WS12→WS45→G_PAYLOAD_PRECONDITION→WS19 y sus hijos y WS21». WS19 aparece a la vez como dependiente directo de WS12 y como dependiente del gate producido por WS45. Obliga a inventar si WS19 puede iniciarse antes de WS45 o debe esperar G_PAYLOAD_PRECONDITION.
2. «todas las salidas WS17/21/22/23/24/25/26/28/42→WS30». WS17, WS22 y WS23 no son hijos de PK05; llamarlas «salidas» obliga a inventar si el paquete debe producirlas o solo consumirlas como entradas externas.

## DRY-RUN

**Lecturas:** dag.yaml (aristas/gates), brief, alcance, decisiones, contratos WS12 y salidas externas WS17/22/23/24.

**Orden hipotético:** prerrequisitos externos WS12 y WS08/11; WS13 para WS27; WS45 → inventario y pruebas → G_PAYLOAD_PRECONDITION; WS20 → G_SOURCE; WS19.1/19.2 → edición de campos/conflicto; WS21 → fuente/render; WS25 → captura/triage; WS26 tras WS22; WS27 tras WS13; WS42 tras WS19+WS24, no en paralelo con WS19; WS28 tras WS27; WS30 integra todas las salidas.

**Cambios previstos:** código/pruebas en `graph_ui`/`sldb`; contrato en `deskops`; acta humana en `runs/subagents/.../manual/`.

**Dependencias:** WS12, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT, G_CLOSEOUT, G_SLDB_WRITE; entradas externas WS17/WS22/WS23/WS24.

**Validaciones futuras (sin ejecutar):** pruebas WS45 de precondición; roundtrip/conflicto/protegidos WS20; conflicto visible WS19; alternancia con buffer WS21; verificación de cierre WS28; recorrido humano WS30 con acta y evidencia declarada/encontrada/verificada.

## FUTURO

WS12 publica contrato/whitelist; WS45 produce G_PAYLOAD_PRECONDITION; WS20 produce G_SOURCE; WS16 produce el acta G_HUMAN_READ; el receptor P01 emite actas por delta; WS17/22/23/24 aportan salidas; el humano decide la aceptación de WS30. Nada de esto es ambigüedad de PK05.
