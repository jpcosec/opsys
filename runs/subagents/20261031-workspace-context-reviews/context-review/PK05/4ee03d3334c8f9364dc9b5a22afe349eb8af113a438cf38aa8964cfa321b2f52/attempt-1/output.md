## REFORMULACION

PK05 es una **agrupación de revisión**, no una tarea ejecutable, del paquete de autoría y operación manual. Propósito: comprobar que el encargo agrupa y ordena hijos verificables. Resultado: revisión vigente de cada hijo directo y disposición guardada. Repo dueño: `deskops` para la coordinación; los hijos pertenecen a `graph_ui`/`sldb`. Límites: no autoriza tareas, no añade aristas ni ejecuta; el dry-run solo describe orden y transferencia entre hijos. La aceptación agregada exige salidas de los hijos y evidencia de integración; no equivale a producto entregado.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y nodo PK05; las aristas vecinas se tratan como contratos de otros nodos y no se revisan.

Cambios previstos: ninguno; solo evaluación de encargo y disposición.

Dependencias: hijos WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30 y WS42; insumos externos WS12 (contrato por delta), WS17 (entradas), WS22/23/24 para WS30 y gates asociados.

Validaciones futuras, sin ejecutar: `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`; coincidencia de hash de input y contrato con los actuales; existencia de `disposition.md` en el intento correspondiente; revisión vigente por hijo; acta WS30 y gates `G_HUMAN_READ`/`G_WRITE_CONTRACT` por delta.

## FUTURO

Otros nodos o humanos producen o deciden: WS12 publica whitelist/contrato por delta; WS20 produce `G_SOURCE`; WS30 genera acta humana; WS16 produce `G_HUMAN_READ`; receptores emiten recibos `G_WRITE_CONTRACT`/`G_UI_WRITE`; el responsable de producto acepta deltas; WS43 publica entradas reales. Nada de esto es ambigüedad de PK05.
