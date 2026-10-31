## REFORMULACION

Propósito: integrar en el workspace documental de `graph_ui` la verificación de closeout y el handoff de cierre, sin cerrar desde HTTP. Resultado: una vista de revisión que invoca `deskops closeout verify` por el canal que fije WS12, muestra los faltantes y ofrece handoff con evidencia a `deskops closeout commit` por CLI o al coordinador. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/review/`, endpoints, tests). Límites: no commit/close por HTTP; sin terminal embebido genérico; toda operación sin contrato queda no disponible; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/» — no se especifica qué endpoints ni con qué efectos. Obliga a inventar si WS28 expone un endpoint de verificación, de handoff o incluso de cierre, lo que podría contradecir «No commit/close desde HTTP en baseline».

2. «G_HUMAN_READ aplica porque es una acción de escritura del baseline» — el `scope` describe verificación, diagnóstico y handoff, no una escritura ejecutada por el nodo. Obliga a inventar si WS28 debe implementar un control de escritura o solo preparar la acción externa; de ello depende qué se prueba y qué gate aplica realmente.

## DRY-RUN

Lecturas previstas: `dag.yaml` (WS28 y vecinos), guía, brief, alcance, decisiones, cobertura, contrato WS12 y salidas de WS27. Cambios previstos: vista de revisión, endpoint acotado y tests en `graph_ui`; ningún commit/close desde HTTP. Dependencias: WS27 (agregado diff/evidencia), WS12; gates indicados; G_HUMAN_READ es producido por WS16. Validaciones futuras: tests con store temporal real, recorrido UF05 en WS30 y acta humana; sin ejecutar nada aquí.

## FUTURO

WS12 fija whitelist, canal y efectos, y produce G_WRITE_CONTRACT/G_UI_WRITE. WS07 y el solicitante humano resuelven P03, P05, P06, P01 y P02. WS16 produce el acta de G_HUMAN_READ. El resolver externo de G_CLOSEOUT estabiliza la evidencia y el commit de cierre. WS30 valida UF05; WS43 publica entradas reales.
