REFORMULACION
Propósito: implementar en `graph_ui` la vista de evidencia del workspace junto a la TaskDoc. Resultado: mostrar evidencia declarada, encontrada y verificada sin colapsar estados, y abrir su soporte; cambios en `frontends/mindmap/views/workspace/evidence/` y `tests/`, con rutas de lectura del contrato WS11. Repo: `graph_ui`. Límites: sin modelo de comentarios nuevo; no inferir tipo por extensión en el renderer; «verificada» es el resultado del gate de la TaskDoc/tipo, no prueba independiente del artefacto; reporte ausente o fallo de comando es no verificable con error, nunca verificado; solo Markdown dentro del workspace se abre en el lector, el resto muestra ruta y se declara no soportado. Depende de WS13 y WS12; requiere G_UI_READ.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: contratos WS11 y WS12, `task-ws27-2.md`, componentes del lector WS13 y pruebas existentes. Cambios previstos: módulo de evidencia en la ruta de `output_scope`, conexión con la TaskDoc, representación de estados y acción de apertura, más tests. Dependencias: WS13 aporta apertura/lector; WS12 aporta correspondencia por tipo, artefactos soporte y salida pública de `closeout verify`; G_UI_READ se consume por delta al promover. Si falta contrato, dato o reporte, el ejecutor se detiene y registra el hueco con repo dueño, sin crear sustituto. Errores esperados: reporte ausente/fallo de comando → no verificable; artefacto no resoluble → ausente o encontrada según corresponda; no Markdown o fuera del workspace → ruta visible y no soportado. Validación esperada: pruebas de estados distintos, apertura de Markdown, fallback de ruta, ausencia de inferencia por extensión y no colapso de declarada sin artefacto, artefacto no declarado y verificación fallida.

FUTURO
La promoción sigue `not_authorized`: el TaskDoc fijará archivos, textos y pruebas; el receptor P01 emitirá el acta G_UI_READ del delta; WS12 publicará su contrato y WS13 cerrará sus hijos; la aceptación humana del delta y el cierre del agregado WS27 quedan fuera de este nodo.
