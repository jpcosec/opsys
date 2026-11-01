REFORMULACION

WS27.2 es un nodo de implementación en `graph_ui` que añade, junto a la TaskDoc, una vista de evidencia: declarada, encontrada y verificada, con apertura de soporte Markdown dentro del workspace y ruta/no soportado fuera de él. Resultado: componentes en `frontends/mindmap/views/workspace/evidence/` y `tests/`. Límites: sin modelo de comentarios, sin inferir tipos por extensión, sin prueba independiente del artefacto y sin prometer apertura fuera de alcance.

AMBIGUEDADES

1. «declarada/encontrada/gates/summary se muestran según reporte real». No se define qué son «gates» y «summary» ni aparecen en `acceptance`; el ejecutor tendría que inventar qué representan y cómo mostrarlos.

2. «una evidencia ausente se ve como ausente». No precisa si es ausencia total de evidencia declarada o artefacto no resoluble; `acceptance` ya separa «declarada sin artefacto» y «artefacto no declarado», así que habría que inventar un cuarto estado o su criterio.

DRY-RUN

Leería `contratos/operaciones.md` de WS12 —correspondencia tipo→artefacto y salida pública de `closeout verify`—, las rutas de lectura de WS11, los componentes de lector/registro de WS13 y `task-ws27-2.md`. Crearía componentes en `evidence/` para listar estados y abrir Markdown, más tests con TaskDoc temporal y salidas simuladas de verify. Consumiría `G_UI_READ` solo con recibo del delta WS27.2. Validaría: declarada sin artefacto, artefacto no declarado, verificación fallida y reporte ausente/fallo de comando como estados distintos; apertura Markdown y ruta/no soportado fuera. Si falta el contrato WS12, se detendría y registraría el hueco, sin sustituirlo. No ejecutaría promoción ni mutaciones.

FUTURO

WS12 publica la correspondencia y salida pública de verify; WS13 entrega lector/foco; el receptor P01 emite el acta `G_UI_READ` de este delta; la promoción fija TaskDoc, archivos y pruebas; WS27 cierra cuando WS27.1 y WS27.2 cumplen.
