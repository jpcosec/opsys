REFORMULACION
Propósito: encargar a `graph_ui` un generador reproducible del corpus “Taller” para validación temprana. Resultado: comando/script que crea un entorno aislado con dos desks temporales y un tercer repo sin desk, stores, documentos, Markdown no modelado, Code local, referencia rota, commits reales, manifiesto JSON, README/instrucciones y entrada mínima con FAQ, conocimiento y enlaces UF08. Repo dueño: `graph_ui`. Límites: no toca desk real; usa contrato WS11 y CLIs reales verificados en WS02/WS03, no servidor fake; plantillas WS17 opcionales; promoción no autorizada.

AMBIGUEDADES
Ninguna. “Documentos clave”, “entrada mínima” y los nombres exactos de archivos/pruebas son detalles que el TaskDoc de promoción concretará dentro de la aceptación. `G_UI_READ` pendiente es un gate intencional, no un defecto.

DRY-RUN
Lecturas: WS40, guía, brief, alcance, decisiones y cobertura; aristas WS11/WS08/WS16/WS17/WS41 solo como contexto, sin revisarlas.
Cambios previstos: generador versionado, script de seed, fixtures y tests en `graph_ui`; creación de tres repos temporales (dos con desk y otro sin desk), stores/documentos, commits, manifiesto, README y entrada mínima.
Dependencias: contrato WS11, user-flows WS08, CLIs verificados WS02/WS03, `G_UI_READ`; WS17 aporta plantillas opcionales.
Validaciones futuras: comando crea/recrea entorno aislado, no toca desk real, hace commits reales, emite manifiesto JSON y deja instrucciones reproducibles; consumo por WS16/WS30. Sin ejecutar nada.

FUTURO
WS11 emitirá el contrato y el acta `G_UI_READ`; WS17 aportará plantillas authored y regenerará el corpus; WS16/WS30 lo consumirán; WS07/P01 designará al responsable de `graph_ui`; P08 podrá fijar ejemplo/umbrales humanos. Nada de eso se decide aquí.
