## REFORMULACION

**Propósito:** WS15 agrupa la entrega de errores de lectura y modo degradado, y la orientación de un proyecto sin desk, dentro del lector del workspace documental.

**Resultado:** nodo `aggregate` no ejecutable; se considera cumplido cuando WS15.1 y WS15.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS15, no de los hijos.

**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/`.

**Límites:** alcance agregado limitado a salidas de WS15.1 y WS15.2. WS15.1 cubre errores de referencia, documento, modelo, backend, fuente no editable y fallos CDN visibles, sin empaquetado offline. WS15.2 cubre orientación sin desk, ruta de destino y comando `deskops init <ruta>`, sin inicializar por GET. Integración como delta o ticket existente, sin duplicado paralelo; promoción no autorizada y sin ejecución.

## AMBIGUEDADES

Ninguna. El nodo remite la lectura y el tratamiento de errores al contrato WS11; el gate G_UI_READ está pendiente de forma intencional y es por delta. La ausencia de detalle de archivos, pruebas y textos queda delegada al TaskDoc de promoción y a los hijos, sin obligar a inventar al ejecutor de WS15.

## DRY-RUN

**Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y las entradas `WS15`, `WS13`, `WS15.1`, `WS15.2`, `WS16`, `WS29` y gates de `dag.yaml`.

**Cambios previstos:** ninguno; es revisión de encargo, no implementación.

**Dependencias:** WS13 y, como hijos, WS15.1 y WS15.2; transitivamente WS11 por WS13. El recibo G_UI_READ se exige por delta concreto.

**Validaciones futuras:** comprobar aceptación de ambos hijos; verificar que WS16 consume WS40 y sigue el protocolo humano; confirmar que WS29 depende de WS15 sin exigir su cierre para lector básico. No ejecutado.

## FUTURO

El receptor de `graph_ui` produce el acta G_UI_READ del delta concreto. WS15.1 y WS15.2 materializan sus entregas y pruebas. WS16 realiza la validación humana con el corpus de WS40. WS06 mantiene la matriz de reconciliación al promover. La promoción requiere TaskDoc, archivos, pruebas y preflight, decisión humana fuera de esta revisión.
