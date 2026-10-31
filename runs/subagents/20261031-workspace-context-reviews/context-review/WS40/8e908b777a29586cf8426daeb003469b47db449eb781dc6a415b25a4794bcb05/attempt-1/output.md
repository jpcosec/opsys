## REFORMULACION
**Propósito:** planificar un generador reproducible del corpus Taller para validaciones humanas y pruebas de lectura. **Resultado:** un comando en `graph_ui` que crea/recrea un entorno aislado con repos temporales (dos con desk, uno sin desk), stores, documentos Markdown modelados y no modelados, Code local, referencia rota, enlaces entre desks, commits git reales, manifiesto JSON e instrucciones de arranque. **Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`). **Límites:** no toca desk real, no usa servidor fake, no produce el corpus de otros nodos, no es productor de las plantillas WS17 (solo acepta su ruta opcional) y no ejecuta mutaciones UI; depende de `G_UI_READ`, pendiente e intencional.

## AMBIGUEDADES
1. **«los CLI reales de deskops/sldb verificados en WS02/WS03»**: el nodo solo declara `depends_on: WS11, WS08`; si WS02/WS03 no son ancestros, falta dependencia y el ejecutor tendría que inventar que esos CLI ya están verificados.
2. **«hace commits git reales en los repos temporales»**: no fija autor, email ni configuración git; obligaría a inventar identidad de commit o asumir una configuración global no declarada.
3. **«dos repos temporales bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)»** frente a **«Incluir un tercer repo temporal sin desk»**: no dice si el tercero vive bajo el mismo root ni cómo se limpian; obligaría a inventar ubicación y política de recreación.
4. **«bajo graph_ui:.tmp/...»**: no define exclusión git ni efecto sobre el worktree de `graph_ui`; obligaría a inventar si añadir `.gitignore` o asumir que los repos anidados no contaminan el repo real.

## DRY-RUN
**Lecturas:** input, guía, `dag.yaml` (nodo y vecinos), brief, alcance, decisiones, cobertura. Sin ejecución.
**Cambios previstos:** script de seed, fixtures bajo `tests/fixtures/workspace_documental/`, tests, manifiesto JSON, README/instrucciones y árboles temporales de tres repos.
**Dependencias:** contrato WS11, user-flows WS08, `G_UI_READ` (pending), CLI verificados WS02/WS03 (a confirmar por aristas), plantillas WS17 opcionales.
**Validaciones futuras:** comando reproducible, `git log` en temporales, manifiesto con roots/stores/commits/documentos clave, ausencia de escritura en desk real, consumo por WS16 y regeneración posterior por WS17.

## FUTURO
WS11 produce el acta y `G_UI_READ`; WS02/WS03 confirman CLI; WS17 aporta plantillas; WS16 ejecuta la validación humana; WS07/P01 designa responsables y WS43 publica entradas reales. Ninguna de esas piezas se decide aquí.
