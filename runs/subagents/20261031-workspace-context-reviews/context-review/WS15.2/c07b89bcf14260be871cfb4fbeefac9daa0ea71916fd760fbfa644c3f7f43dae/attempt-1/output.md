## REFORMULACION

**Propósito:** cubrir UF10 en el punto en que un proyecto no tiene desk: orientar a la persona sin ejecutar acciones de escritura.

**Resultado:** una vista de orientación en graph_ui que muestra el proyecto, su ruta absoluta como destino y el comando `deskops init <ruta>`; abrirla no muta nada y, tras un init externo real, un refresco evidencia el desk real.

**Repo dueño:** graph_ui (`frontends/mindmap/views/workspace/orientation/`, tests).

**Límites:** nunca inicializar por GET; no crear desks desde UI; lectura según contrato WS11; depende de WS13 y del gate G_UI_READ (per_delta); promoción no autorizada.

## AMBIGUEDADES

Ninguna. El resultado y la aceptación son comprobables; repo y dependencias están definidos; el contrato de rutas de lectura se atribuye a WS11 y la ausencia de contrato/API se rige por las reglas comunes de alcance.md. Los textos exactos de pantalla y archivos precisos corresponden al TaskDoc de promoción, no a este nodo.

## DRY-RUN

**Lecturas previstas:** nodo WS15.2, aristas WS13/WS15, gate G_UI_READ, guía, brief, alcance, decisiones, cobertura, reconciliación y referencia externa del workspace. Sin ejecutar.

**Cambios previstos:** implementar o conciliar la vista de orientación en el `output_scope`, con tests; integrarla como delta o ticket receptor existente, sin duplicar la base a1b2b22/f16fcd1/134a665.

**Dependencias:** WS13 (agregado con WS13.1–13.3) y, transitivamente, WS11 para rutas de lectura; G_UI_READ pendiente y evaluado por delta concreto.

**Validaciones futuras:** abrir un proyecto temporal sin desk y comprobar orientación, ruta y comando sin mutación; verificar que GET no inicializa; ejecutar `deskops init` fuera de la UI y refrescar; pruebas de integración y aceptación UF10 (WS16) sobre corpus WS40.

## FUTURO

El receptor humano P01 debe emitir el acta de recepción por delta en graph_ui al preparar/promover. WS11 entrega el contrato de lectura que este nodo consume. El TaskDoc de promoción fija archivos, escenarios y textos. WS06 reconcilia la integración y WS16 valida UF10; nada de ello es ambigüedad del encargo.
