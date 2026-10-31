## REFORMULACION

**Propósito:** revisar WS15 como encargo de planificación que agrupa dos entregas de `graph_ui`: errores de lectura/modo degradado (WS15.1) y orientación de proyecto sin desk (WS15.2).

**Resultado:** nodo `aggregate` no ejecutable; se cumple cuando ambos hijos cumplen su aceptación, y sus dependientes siguen apuntando a WS15.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura del workspace; requiere `G_UI_READ`; no autoriza promoción ni implementación; no sustituye validación humana.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** guía, nodo WS15 y aristas vecinas, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`.

**Cambios previstos:** ninguno; `status: candidate` y `promotion: not_authorized`.

**Dependencias:** WS13 como prerrequisito de lectura; WS15.1 y WS15.2 como hijos que definen el cierre; `G_UI_READ` pendiente con resolver WS11, pendiente intencional.

**Validaciones futuras:** aceptación de WS15.1 y WS15.2; `G_UI_READ` producido por WS11; validación humana de lectura en WS16 con corpus WS40. Sin ejecución.

## FUTURO

WS11 debe producir el acta de `G_UI_READ`; WS07 identifica al responsable de `graph_ui`; WS15.1 y WS15.2 ejecutan sus ámbitos; WS16 valida con humano; WS40 aporta el corpus. Nada de esto es ambigüedad del nodo.
