REFORMULACION  
WS27 es un nodo agregado, no ejecutable, del plan de graph_ui: agrupa la revisión de cambios y evidencia de una TaskDoc en el workspace. Su resultado es la unión de WS27.1 (diff Git e historial read-only por repo y tarea) y WS27.2 (evidencia declarada, encontrada y verificada, con apertura de soporte). No añade implementación propia ni un artefacto combinado distinto. Repo dueño: graph_ui. Límites: solo lectura, sin escribir, revertir ni mostrar integridad del store (WS29); la asociación a intento queda para WS35; depende de WS13 (lector) y WS12 (contrato); requiere G_UI_READ; promoción no autorizada.

AMBIGUEDADES  
ninguna.

DRY-RUN  
No se ejecuta WS27. WS27.1 leería TaskDoc.references/files, resolvería repo/rutas con WS11 y produciría `diff/` e historial read-only; consume WS13 y WS12; validaría diff real acotado, una sección por repo y ruta no resoluble como no disponible. WS27.2 consumiría WS13/WS12 y produciría `evidence/`; mostraría declarada/encontrada/verificada, abriría Markdown del workspace y marcaría el resto no soportado; validaría estados distintos, ausencia visible y fallo de verify como no verificable. Entre WS27.1 y WS27.2 no hay arista ni transferencia: solo comparten dependencias y conviven en el workspace. La integración conjunta es la presencia de ambas superficies sobre la misma TaskDoc; se valida con las aceptaciones de los hijos y el cierre del agregado. G_UI_READ se consume por delta de cada hijo; el recibo del agregado no sustituye el de ellos. Errores: contrato ausente → hueco con dueño, sin sustituto; repo/ruta no resoluble → no disponible.

FUTURO  
WS28 consumirá WS27 para verificación y handoff de cierre; WS35, para trazabilidad e intento. G_UI_READ se recibirá por delta concreto en graph_ui (P01) al promover; no se inventa acta conjunta. La promoción fijará archivos, pruebas y textos en el TaskDoc.
