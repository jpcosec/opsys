REFORMULACION

PK02 es una agrupación de revisión, no una tarea ejecutable. Su propósito es reunir los contratos de decisiones, user-flows, vistas, manual, navegación y operaciones (WS07–WS12). El resultado esperado es un paquete planificado verificable: Pxx trazadas, UFs con operaciones/errores/IDs/gates, vistas con soporte/origen y APIs/huecos con productores. Repo dueño: deskops. Límites: no autoriza tareas, no añade aristas, no ejecuta validaciones ni supone editable sin G_SOURCE; su cierre operativo es la revisión vigente de cada hijo.

AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» frente a «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable». No queda definido si el cierre de PK02 exige comprobar la integración sustantiva de las salidas o solo que existan reviews vigentes; tampoco qué constituye la «integración indicada». Sin precisarlo, el revisor tendría que inventar el criterio de completitud y el alcance de esa comprobación.

DRY-RUN

Lecturas: dag.yaml (PK02 y aristas WS07–WS12), decisiones.md, cobertura.md, alcance.md/brief y la guía; después `context_review.py status`.
Cambios previstos: ninguno en el plan ni en deskops; la revisión solo generaría disposition.md en el intento.
Dependencias: salidas de WS07–WS12 y sus reviews vigentes; gates G_PRODUCT/G_WRITE_POLICY; G_SOURCE de WS20 no condiciona L/M; recepción por delta de P01.
Validaciones futuras: ejecutar status, comparar hashes de input/contrato, comprobar disposition.md por hijo y tratar un blocked externo con responsable. Sin ejecutar.

FUTURO

Producen otro nodo: WS07 decisiones, WS08 user-flows, WS09 vistas, WS10 manual, WS11 navegación, WS12 operaciones; WS20 G_SOURCE; P01 recibos por delta. Decide humano/coordinación: bloqueos externos y su responsable, y aceptación de deltas. `context_review.py status` determina la vigencia. Nada de esto es ambigüedad de PK02.
