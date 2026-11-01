## REFORMULACION
**Propósito:** versionar en `graph_ui` un generador reproducible del corpus Taller que use el contrato WS11 y los CLI reales de deskops/sldb verificados en WS02/WS03, sin servidor fake.  
**Resultado:** un comando que crea/recrea un entorno aislado con dos repos temporales con desk y sus stores/documentos —Board, FAQ, conocimiento, Markdown no modelado, Code local y referencia rota—, un tercer repo sin desk, enlaces authored entre desks, commits git reales y manifiesto JSON; además, README/instrucciones de arranque y entrada mínima. Acepta opcionalmente plantillas WS17.  
**Repo:** `graph_ui`.  
**Límites:** no toca desk real; no produce índices ricos WS17; WS17 aporta después contenido authored; ubicación `.tmp/workspace-documental-ejemplo/` o `tmp_path`; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería WS11 —identidad, root/store/aliases y recepción por delta—, WS08 —UF01/UF08/UF10—, las auditorías WS02/03 disponibles transitivamente y su TaskDoc. Escribiría el script de seed y las pruebas bajo `tests/fixtures/workspace_documental/` y `tests/`; al ejecutarse, el script elegiría `.tmp/workspace-documental-ejemplo/` o `tmp_path`, inicializaría los repos, crearía stores y documentos con CLIs reales, haría commits y emitiría el manifiesto con roots, stores, commits y documentos clave. Consumiría `G_UI_READ` solo con el recibo per-delta de WS40; sin él no habilitaría lo que el gate bloquee. Ante falta de contrato, CLI, dato o permiso: detenerse, registrar el hueco y su repo dueño, sin crear sustituto. Validaría reejecutando el comando, comprobando aislamiento —desk real intacto—, commits en repos temporales, manifiesto resoluble, entrada mínima abrible, segundo desk y referencia rota. WS17 no es prerrequisito.

## FUTURO
WS16 usará el manifiesto para la validación humana de lectura y arranque; WS30 lo usará como corpus para edición; WS17 escribirá plantillas authored y regenerará el corpus; WS41 leerá el segundo desk; WS43 publicará el desk real. El receptor P01 emitirá el acta `G_UI_READ` por delta. La promoción fijará archivos, escenarios y textos en el TaskDoc.
