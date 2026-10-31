## REFORMULACION

WS15.2 es un encargo de implementación —delta o ticket existente— en `graph_ui` para UF10: al abrir un proyecto sin desk, mostrar orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`, sin inicializar por GET; tras un init externo real, refrescar lectura. Resultado: vista en `frontends/mindmap/views/workspace/orientation/`, rutas de lectura según contrato WS11 y `tests/`. Límites: no mutar, no inicializar por GET, `G_UI_READ` pendiente de forma intencional, `promotion: not_authorized`, sin duplicar ticket.

## AMBIGUEDADES

1. «tras ejecutar init fuera de la UI, refrescar muestra el desk real» / «refrescar lectura»: no se define el disparador ni el mecanismo —recarga manual, botón, relectura automática—. Obliga a inventar cuándo y cómo se refresca y qué cuenta como “refrescar”.
2. «la ruta absoluta del proyecto como destino»: “destino” no se define —¿argumento de `init`, ubicación del futuro desk, texto copiable?—. Obliga a inventar su significado y representación.
3. «un proyecto sin desk muestra orientación»: no se nombra criterio ni fuente de detección; WS11 solo se cita para «rutas de lectura definidas por el contrato WS11». Obliga a inventar cómo se determina la ausencia de desk —sistema de archivos, API, qué artefacto lo define—.

## DRY-RUN

Lecturas previstas: `dag.yaml#node:WS15.2`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`. Cambios previstos: crear/ajustar `orientation/` y `tests/` en `graph_ui`; ninguna escritura de dominio ni inicialización. Dependencias: WS13 (lector/historia/foco) de forma transitiva por sus hijos; contrato de rutas de WS11; `G_UI_READ` pendiente, resuelto por WS11. Validaciones futuras: abrir proyecto sin desk y comprobar orientación/destino sin mutación; ejecutar init externo y refrescar; pruebas con store temporal o corpus WS40 cuando exista. Sin ejecución.

## FUTURO

WS11 produce el contrato de lectura y la aceptación de `G_UI_READ`; WS07 designa al responsable de `graph_ui`; el TaskDoc de promoción fija archivos, escenarios, textos y pills; WS16 y la validación humana usan el corpus WS40; WS43 publica entradas reales. Nada de esto es ambigüedad del nodo.
