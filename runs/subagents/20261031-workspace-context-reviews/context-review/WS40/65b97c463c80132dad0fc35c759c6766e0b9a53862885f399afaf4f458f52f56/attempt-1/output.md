## REFORMULACION

Propósito: encargar a `graph_ui` un generador versionado y reproducible del corpus Taller. Resultado: un comando que crea/recrea tres repos temporales —dos con desk y uno sin desk— con stores, documentos Markdown no modelado, Code local, referencia rota, commits git reales, README/entrada mínima y manifiesto JSON con roots, stores, commits y documentos clave; más script, fixtures y pruebas. Repo dueño: `graph_ui` (`output_base: repository_root/`). Límites: no toca desk real ni usa servidor fake; usa contrato WS11 y CLIs reales deskops/sldb; plantillas WS17 opcionales; `G_UI_READ` por delta; promoción no autorizada; no implementa UI ni sustituye la aceptación humana.

## AMBIGUEDADES

ninguna.

## DRY-RUN

- **Lecturas:** nodo WS40 y gates; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; al ejecutar, contrato WS11, evidencia CLI WS02/WS03 y ruta opcional de plantillas WS17.
- **Cambios previstos:** script de seed y `tests/fixtures/workspace_documental/` en `graph_ui`; generación de `.tmp/workspace-documental-ejemplo/` o `tmp_path`, repos git, stores, documentos, entrada/README y manifiesto JSON.
- **Dependencias:** WS11 y WS08; gate `G_UI_READ` por delta; CLIs reales de deskops/sldb; WS17 solo si se pasa la ruta de plantillas.
- **Validaciones futuras:** ejecutar dos veces y comprobar aislamiento/idempotencia, commits reales, manifiesto, ausencia de escritura en desk real; consumo por WS16/WS30/WS41 y regeneración por WS17.

No se ejecuta nada.

## FUTURO

WS11 produce el contrato y el recibo `G_UI_READ` por delta; WS02/WS03 dejan evidencia de los CLIs; WS17 aporta plantillas; WS16 valida lectura con humano; WS30 valida edición; el responsable humano acepta el delta y autoriza la promoción. Nada de eso se decide en este nodo.
