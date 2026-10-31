# Executor comparison — WS40

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

Propósito: encargar a `graph_ui` un generador versionado y reproducible del corpus Taller. Resultado: un comando que crea/recrea tres repos temporales —dos con desk y uno sin desk— con stores, documentos Markdown no modelado, Code local, referencia rota, commits git reales, README/entrada mínima y manifiesto JSON con roots, stores, commits y documentos clave; más script, fixtures y pruebas. Repo dueño: `graph_ui` (`output_base: repository_root/`). Límites: no toca desk real ni usa servidor fake; usa contrato WS11 y CLIs reales deskops/sldb; plantillas WS17 opcionales; `G_UI_READ` por delta; promoción no autorizada; no implementa UI ni sustituye la aceptación humana.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
