REFORMULACION
Revisar WS13 como encargo de planificación: si su propósito, resultado, repo dueño (`graph_ui`), límites y aceptación son comprensibles. No se evalúa el producto ni se ejecuta nada; los bloques edge vecinos no se revisan.

AMBIGUEDADES
Ninguna. El agregado tiene aceptación comprobable por hijos, repo dueño, alcance acotado y dependencias explícitas. `G_UI_READ` pendiente es intencional y no defecto. La elección entre implementación nueva y delta sobre el ticket en draft queda delegada a WS11 y a su acta, que el propio nodo nombra como contrato; si faltara, aplica la regla común de alcance (detenerse y registrar el hueco), sin obligar a inventar.

DRY-RUN
Lecturas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS13 y gate `G_UI_READ`.
Cambios previstos: ninguno; esta revisión no modifica plan, DAG ni repo.
Dependencias: WS11 y WS13.1–WS13.3; gate `G_UI_READ`; cobertura UF01/UF03/UF04/UF05/UF06/UF08 vía nodos posteriores.
Validaciones futuras: aceptación agregada cuando cierren los tres hijos; acta de WS11 con alcance de lectura y base elegida; evidencia de `G_UI_READ` con responsable designado; preflight de promoción y TaskDoc antes de autorizar ejecución.

FUTURO
WS11 produce el contrato de navegación, identidad y el acta que fija la base (ticket draft o delta) y los `scope_nodes`. WS07 designa al responsable de `graph_ui` y al operador Scion. El humano resuelve P01/P02/P07/P08/P09 y aprueba P03–P06; ninguna propuesta se da por aceptada. La promoción fijará archivos, TaskDoc, pills y evidencias. `G_UI_READ` no se satisface hasta que exista aceptación verificable del receptor; mientras tanto, WS13 no se despacha.
