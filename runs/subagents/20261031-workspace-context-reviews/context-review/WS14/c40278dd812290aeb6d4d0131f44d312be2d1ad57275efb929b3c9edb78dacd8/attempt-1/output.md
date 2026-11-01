REFORMULACION
- **Propósito:** integrar en el workspace de graph_ui una búsqueda navegable sobre la API real de sldb, sin parser propio.
- **Resultado:** buscar por texto/campos —semántica solo si la API real la ofrece—, abrir resultados con identidad y ruta de origen, conservar consulta y foco al volver, y distinguir sin resultados, error de backend y búsqueda degradada.
- **Repo dueño:** graph_ui; `output_scope`: `frontends/mindmap/source/`, `views/workspace/`, `tests/`.
- **Límites:** depende de WS13 y de G_UI_READ; consume WS03/WS11 y `sldb find`/`GET /find`; no cargar el grafo completo por tecla; promoción no autorizada; no ejecutar.

AMBIGUEDADES
1. «Con teclado: buscar, abrir un resultado y volver conserva consulta y foco.» No se define si «foco» es el término del glosario —elemento de un documento, compartido entre representaciones— o el resultado/cursor de la búsqueda. Obligaría a inventar qué estado exacto se restaura al volver.

DRY-RUN
- **Lecturas:** nodo WS14, arista WS13, gate G_UI_READ; brief, alcance, decisiones, cobertura y reconciliación; auditoría de infraestructura y contrato WS11 como fuentes nombradas.
- **Cambios previstos:** UI de búsqueda en `views/workspace/`, consumo de `GET /find`/`sldb find`, estados diferenciados y prueba de peticiones; sin parser propio. Archivos exactos quedan para promoción.
- **Dependencias:** WS13 agregado debe cerrar sus hijos; G_UI_READ pendiente por delta con acta externa; contrato WS11 y capacidad C-43. Si falta contrato, detenerse y registrar el hueco.
- **Validaciones futuras:** recorrido con teclado, tres estados, ausencia de carga completa del grafo al teclear; después WS16 con humano y recibo G_UI_READ. Nada ejecutado.

FUTURO
- WS11 produce el contrato de navegación que fija canal, identidad y rutas de resultado.
- WS03 documenta la búsqueda existente; C-43 ya cubre `sldb find`/`GET /find`.
- El receptor P01 emite el acta G_UI_READ por delta concreto.
- La promoción fija TaskDoc, archivos, pills y textos de prueba; hoy no autorizada.
- WS13.1–13.3 entregan el lector y WS16 valida con humano; la semántica/ranking de `Corpus.rank` queda fuera salvo API real.
