## REFORMULACION

**Propósito:** planificar cómo el workspace muestra errores de lectura y modo degradado.

**Resultado:** nodo agregado no ejecutable; se entiende cumplido cuando WS15.1 (errores de lectura y degradación) y WS15.2 (orientación de proyecto sin desk) cumplen su aceptación.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura; no empaquetado offline; no inicializar desk por GET; sin mutaciones; requiere `G_UI_READ`; promoción no autorizada. El título no menciona orientación, pero el `scope` la incluye explícitamente junto a los errores.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** bloque `WS15` de `dag.yaml`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y `task-ws15.md` (no suministrado).

**Cambios previstos:** ninguno; esta revisión no ejecuta ni modifica archivos.

**Dependencias:** WS13; hijos WS15.1 y WS15.2; `G_UI_READ`, resuelto por WS11; contrato de lectura de WS11; designación del responsable `graph_ui` vía WS07/P01; corpus de WS40 para validación humana.

**Validaciones futuras:** acta de `G_UI_READ` por WS11; preflight de promoción con archivos, pills y evidencia; pruebas de los hijos sobre errores, CDN y refresco; validación humana de WS16 con corpus WS40. Nada se ejecuta en este nodo.

## FUTURO

- WS11 produce el contrato de lectura y el acta de aceptación de `G_UI_READ`.
- WS07/P01 identifica al responsable de `graph_ui`; sin designación, el gate permanece pendiente.
- El TaskDoc de promoción fija archivos exactos, escenarios de prueba y textos de pantalla.
- WS15.1 y WS15.2 implementan; WS16 valida con humano usando WS40.
- WS40 genera el corpus y WS43 publica entradas reales.
- El empaquetado offline y el soporte CDN quedan fuera; el fallo CDN solo debe mostrarse como límite actual.
