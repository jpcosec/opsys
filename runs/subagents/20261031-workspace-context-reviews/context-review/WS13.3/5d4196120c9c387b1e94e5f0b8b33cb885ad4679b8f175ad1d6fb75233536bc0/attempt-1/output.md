## REFORMULACION

Propósito: revisar WS13.3 como encargo de planificación, no como producto ni ejecución. Resultado esperado: un nodo de implementación en `graph_ui` que añada pestañas documentales, dos documentos en divisiones, foco por documento e historia de navegación local. Repo dueño: `graph_ui`; `output_scope` limita a `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`. Límites: depende de WS11 (contrato de navegación/identidad) y WS13.1 (lectura); requiere G_UI_READ por delta; la disposición es local y no se exige persistir tras recargar; no es documento compartido ni crea workspace paralelo.

## AMBIGUEDADES

1. Relación entre pestañas y divisiones. Cita: «Pestañas, dos documentos lado a lado» y «abrir dos documentos en divisiones, alternar el documento activo». Obliga a inventar si existe una tira de pestañas compartida o una por división, y si abrir un documento en una división crea pestaña, reemplaza la existente o duplica el documento.
2. Efecto de cerrar una pestaña sobre foco e historia. Cita: «cerrar pestañas» y «volver restaura documento, foco y origen». Obliga a inventar si cerrar elimina entradas de historia, si libera el foco guardado y si «volver» puede reabrir un documento cerrado.

## DRY-RUN

Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS13.3 y vecinos WS13/WS13.1/WS11, gates. Sin herramientas ni ejecución. Cambios previstos: ninguno; esta revisión solo emite veredicto. La implementación futura tocaría layout y tests en `graph_ui` dentro del scope. Dependencias: contrato WS11 para identidad, rutas, foco, enlaces e historia; lectura de WS13.1; G_UI_READ per-delta. Validaciones futuras: pruebas de abrir/cambiar/cerrar pestañas, dos divisiones, alternancia y retroceso conservando foco e historia; acta de recepción G_UI_READ con actor P01; validación WS16 sobre corpus WS40.

## FUTURO

WS11 produce el contrato de navegación; si falta, aplica la regla común: detenerse y registrar el hueco sin sustituto. WS13.1 produce la lectura. El humano P01 emite el recibo G_UI_READ del delta. WS06 integra el delta en ticket receptor sin duplicar implementación. El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla. WS16 valida lectura y uso.
