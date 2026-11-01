REFORMULACION
Propósito: encargar la disposición local de pestañas y divisiones del lector, con foco e historia por documento, sin convertirla en documento compartido. Resultado: comportamiento verificable de abrir, cambiar, cerrar y volver, con dos documentos lado a lado y restauración de documento, foco y origen. Repo dueño: `graph_ui`. Límites: disposición por sesión, sin persistencia tras recargar; solo lectura sujeta a `G_UI_READ`; no se define aquí el contrato de rutas ni la base del lector.

AMBIGUEDADES
1. «Abrir, cambiar y cerrar pestañas» no define qué documento queda activo al cerrar la pestaña activa ni al cerrar la última, ni si el foco/historia de la pestaña cerrada se conserva o se descarta. Obligaría a inventar el fallback, la poda de historia y la restauración.
2. «Volver sigue el orden inverso de navegación» junto con «volver restaura documento, foco y origen» no fija si la historia es global de la sesión o por pestaña/división. Obligaría a inventar el alcance de “volver” y su interacción con cambios de pestaña.

DRY-RUN
Lecturas: `dag.yaml`, contrato WS11, salida de WS13.1, recibo `G_UI_READ` del delta concreto y TaskDoc de promoción. Cambios previstos: extender `frontends/mindmap/views/workspace/layout/` con pestañas, divisiones, estado local de disposición, foco guardado por documento e historial; añadir pruebas. Dependencias: rutas de lectura de WS11; base de lector/foco de WS13.1; acta per-delta; TaskDoc fija archivos, textos y casos. Errores: si falta contrato, recibo o base, detenerse y registrar el hueco con repo dueño. Validación esperada: abrir/cambiar/cerrar pestañas; dos documentos simultáneos; alternancia de activo; volver en orden inverso conservando documento, foco y origen; no persistencia tras recarga.

FUTURO
WS11 produce el contrato de rutas; WS13.1 entrega la base de lectura/foco; el receptor humano P01 emite `G_UI_READ` por delta en `graph_ui`; la promoción fija archivos, pruebas y textos; WS13 cierra cuando aceptan sus hijos. Nada de esto es ambigüedad del nodo.
