## REFORMULACION

- **Propósito**: crear un generador reproducible del corpus aislado «Taller» para que WS16/WS30 validen lectura, navegación y arranque sin usar un servidor fake.
- **Resultado**: generador versionado y comando único que recrea repos temporales con stores, documentos, Markdown no modelado, Code local, referencia rota, un tercer repo sin desk, enlaces entre desks, instrucciones de arranque y manifiesto JSON.
- **Repo dueño**: `graph_ui`, con salida en `tests/fixtures/workspace_documental/`, script de seed y `tests/`; los repos generados van bajo `.tmp/...` o `tmp_path`.
- **Límites**: no toca el desk real, no usa servidor fake, emplea CLIs reales de deskops/sldb y el contrato WS11; no produce los índices ricos de WS17 ni implementa UI; requiere `G_UI_READ`.

## AMBIGUEDADES

1. **Esquema del manifiesto**: «imprime un manifiesto JSON con roots, stores, commits y documentos clave». No se fijan nombres de campos, tipos, rutas relativas/absolutas ni qué documentos son «clave». El ejecutor tendría que inventar un contrato de facto que WS16/WS30/WS17 consumirán; la aceptación solo enumera categorías, no una estructura verificable de intercambio.

## DRY-RUN

- **Lecturas previstas**: guía de revisión, brief, alcance, decisiones, cobertura, nodo WS40 y aristas WS11/WS08/WS16/WS17/WS41/G_UI_READ. Sin revisar contratos vecinos.
- **Cambios previstos**: añadir generador y seed en `graph_ui`; crear fixtures temporales con dos repos con desk y uno sin desk; incluir documentos, enlaces, referencia rota, instrucciones y manifiesto; añadir pruebas.
- **Dependencias**: contrato WS11, user-flows WS08, gate `G_UI_READ`; CLIs reales verificados en WS02/WS03 por vía transitiva; plantillas WS17 opcionales.
- **Validaciones futuras**: ejecutar el comando, comprobar recreación e aislamiento, commits git reales en repos temporales, manifiesto, enlaces/entrada mínima y ausencia de escritura en desk real; después WS16/WS30 consumen el corpus y WS17 regenera con plantillas.

## FUTURO

WS16 ejecuta la validación humana; WS30 consume el corpus para edición; WS17 aporta contenido authored y solicita regeneración. `G_UI_READ` y la designación del responsable de `graph_ui` corresponden a WS11/WS07 y al solicitante. La promoción fijará archivos, TaskDoc y preflight; WS40 no los decide aquí.
