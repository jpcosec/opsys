REFORMULACION
Propósito: implementar en graph_ui la lectura segura entre desks, resolviendo aliases/roots autorizados por el contrato WS11 mediante APIs públicas, sin cambiar el global SLDB_STORE ni producir mutaciones cruzadas. Resultado: sobre los dos stores de WS40, mostrar identidad/origen, seguir enlaces authored entre desks y volver por la historia; alias no autorizado, path escapado, root arbitrario y store ausente deben dar error visible; no se afirma federación. Repo dueño: graph_ui (frontends/mindmap/source/, views/workspace/, tests/). Límites: solo lectura; depende de WS11, WS13 y WS40; requiere G_UI_READ; promoción no autorizada.

AMBIGUEDADES
Ninguna. El contrato de aliases/roots se atribuye a WS11 y alcance.md fija la conducta si falta; los textos exactos de pantalla y casos de prueba quedan al TaskDoc de promoción. El gate pendiente es intencional y per_delta.

DRY-RUN
Lecturas: dag.yaml (WS41 y vecinos), guía, brief, alcance, decisiones y cobertura. Cambios previstos: código de resolución de aliases/roots y lectura de segundo desk en graph_ui, más tests; no se toca desk real. Dependencias: contrato WS11; lector/historia/foco WS13; corpus y manifiesto WS40; G_UI_READ por delta. Validaciones futuras: UF08 sobre dos stores, identidad/origen, enlaces y vuelta por historia, errores de alias/path/root/store, ausencia de federación; pruebas en tests/ y validación humana WS16.

FUTURO
WS11 produce contrato y recibo G_UI_READ; WS40 produce corpus; WS13 entrega lector; WS16 ejecuta validación humana de UF08; P01 acepta el delta. La promoción de WS41 sigue no autorizada.
