REFORMULACION
Propósito: mostrar junto a la TaskDoc la evidencia declarada, encontrada y verificada, distinguiendo estados y abriendo su soporte. Resultado: componentes de evidencia en graph_ui que consumen la TaskDoc y el resultado de `deskops closeout verify`, con tests. Repo: graph_ui. Límites: no crear modelo de comentarios; no probar el artefacto de forma independiente; abrir solo Markdown dentro del workspace y, fuera de ese caso, mostrar ruta y “no soportado”; ceñirse a `output_scope` y a los contratos WS11/WS12; no ejecutar closeout.

AMBIGUEDADES
Ninguna.

DRY-RUN
Un ejecutor futuro, tras promoción, leería el contrato WS11 (rutas de lectura), el WS12 (correspondencia por tipo de evidencia, artefactos soporte y salida pública de `closeout verify`), los componentes del lector WS13 y los campos `closeout_evidence`, `references`/`files` de la TaskDoc. Crearía la vista/panel en `frontends/mindmap/views/workspace/evidence/`, la integraría junto a la TaskDoc y añadiría tests. Mostraría declarada, encontrada y verificada sin colapsar declarada-sin-artefacto, artefacto-no-declarado y verificación fallida; para soporte, abriría Markdown interno con el lector y para el resto mostraría ruta/no soportado. Reporte ausente o fallo de comando producirían estado “no verificable” con error, nunca “verificado”. Consumiría WS13 y WS12; si falta contrato/dato, se detendría y registraría el hueco con repo dueño, sin sustituto. G_UI_READ sigue pendiente y se consume por delta; sin recibo no hay aceptación/promoción de este nodo. Validaría con tests los estados, ausencias, error y apertura permitida, y con el corpus WS40 cuando aplique validación humana.

FUTURO
WS12 debe publicar la correspondencia, artefactos y salida de verify; WS11 las rutas de lectura; el receptor P01 emite el acta G_UI_READ de este delta; otro nodo/humano autoriza promoción y fija TaskDoc/preflight; reconciliacion.md registra la aceptación del delta.
