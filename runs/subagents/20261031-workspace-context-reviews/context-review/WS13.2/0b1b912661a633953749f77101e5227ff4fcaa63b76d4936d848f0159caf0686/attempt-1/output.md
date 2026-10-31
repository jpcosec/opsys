REFORMULACION

Propósito: encargo de planificación para un explorador que liste y abra documentos modelados del store y Markdown no modelado del desk, obteniendo el árbol de la API del store y del sistema de archivos según el contrato WS11. Resultado: delta de explorador en graph_ui con rutas de lectura fijadas por WS11 y tests, verificable abriendo un documento modelado y otro no modelado sin conocer su ID ni usar índices nuevos, y viendo aparecer un documento añadido al store temporal de prueba sin cambiar código. Repo: graph_ui (`frontends/mindmap/views/workspace/explorer/`). Límites: solo lectura; depende de WS11 y WS13.1; exige G_UI_READ; no crea otro workspace, no usa índices nuevos y no promociona ni ejecuta.

AMBIGUEDADES

Ninguna. Las frases «según contrato WS11» y «store temporal de prueba» remiten a fuentes suministradas; G_UI_READ pendiente es un gate intencional, no un defecto.

DRY-RUN

Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodos WS13.2/WS11/WS13.1/WS13 y gate G_UI_READ. Cambios previstos: explorador en la ruta de `output_scope` y tests; ningún archivo de otros nodos. Dependencias: contrato WS11 (identidad, resolución, rutas de lectura y clasificación de huecos), lector/foco WS13.1 y acta G_UI_READ con responsable graph_ui designado en WS07. Validaciones futuras: abrir modelado/no modelado sin ID ni índices nuevos; alta en store temporal visible sin cambio de código; escenarios del TaskDoc de promoción; evidencia de G_UI_READ. No se ejecuta nada.

FUTURO

WS07 designa responsables; WS11 produce el contrato de navegación y G_UI_READ, o lo deja pendiente; WS06 aporta la matriz; WS40 el corpus; WS17 los índices; WS16 valida. El humano resuelve P01/P02/P07/P08/P09 y P03–P06, incluido `source_mode` de P04, y autoriza promoción/TaskDoc. WS13 cierra cuando cierran sus hijos.
