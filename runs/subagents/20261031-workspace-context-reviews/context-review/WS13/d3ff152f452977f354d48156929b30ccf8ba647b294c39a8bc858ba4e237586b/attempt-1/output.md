## REFORMULACION
Revisar WS13 como encargo de planificación: nodo agregado (`aggregate`) del repo `graph_ui`, cuyo resultado es la integración del lector workspace con explorador, foco, pestañas, divisiones e historia, materializada por WS13.1–WS13.3. Límites: no se evalúa calidad de producto, no se ejecuta nada, no se revisan los bloques de vecinos, no se resuelven Pxx ni se despacha código. G_UI_READ pendiente es intencional.

## AMBIGUEDADES
Ninguna.

WS13 declara propósito, repo dueño, alcance, agregación, dependencias y aceptación comprobable. La aparente dualidad “Implementación o delta conciliado sobre ticket workspace en draft” queda acotada por `integration_mode: delta_or_existing_ticket; never_parallel_duplicate` y por WS13.1, que remite al acta de WS11. La inclusión de sus hijos en `depends_on` es coherente con la guía para agregados, no una dependencia sobrante. Las rutas exactas, TaskDoc y pills se delegan a promoción, y el gate pendiente no es defecto.

## DRY-RUN
- **Lecturas previstas:** nodo WS13 y aristas WS13.1–13.3, WS11 y gate G_UI_READ; guía, brief, alcance, decisiones, cobertura y reconciliación; no lecturas de repositorio ni ejecución.
- **Cambios previstos:** ninguno sobre archivos, DAG, Board o código; solo el informe de revisión.
- **Dependencias:** WS11 debe producir el contrato de navegación e identidad y el acta que resuelve G_UI_READ; WS13.1–13.3 deben cumplir su aceptación para que WS13 cierre como agregado. La recepción en graph_ui exige responsable designado en WS07.
- **Validaciones futuras:** aceptación agregada no ejecutable; aceptación de cada hijo; acta G_UI_READ con `scope_nodes`; preflight de promoción con archivos, pills, átomos y evidencia; conciliación con ticket draft y no duplicación paralela.

## FUTURO
WS11 produce el contrato y el acta de aceptación; un humano designa al responsable de graph_ui en WS07; la promoción fija TaskDoc, archivos y pruebas; los hijos se ejecutan y WS13 termina cuando todos cierran. Ninguna decisión Pxx se aprueba aquí.
