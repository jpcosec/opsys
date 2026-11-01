## REFORMULACION
Encargo de planificación: nodo de implementación **WS27.2** en `graph_ui`, que debe mostrar junto a la TaskDoc la evidencia **declarada / encontrada / verificada**, abrir su soporte cuando sea Markdown dentro del workspace y distinguir estados de ausencia, artefacto no declarado y verificación fallida. Resultado acotado a `frontends/mindmap/views/workspace/evidence/`, rutas de lectura del contrato WS11 y `tests/`. Sin modelo de comentarios nuevo y sin mutaciones. Depende de WS13 y WS12; requiere G_UI_READ por delta.

## AMBIGUEDADES
1. «declarada/encontrada/gates/summary se muestran según reporte real»: no se define qué son `gates` ni `summary`, ni cuál es el “reporte real” o su esquema. El ejecutor tendría que inventar su contenido, fuente y si forman parte de la aceptación, o decidir omitirlos pese a estar en `scope`.

2. «encontrada = artefactos resolubles en las references/files de la TaskDoc»: no se fija la base de resolución —TaskDoc, raíz del workspace u otra—, ni reglas de contención, symlinks o rutas relativas. El ejecutor inventaría cómo resolver y cuándo un artefacto “resuelve”.

3. «una evidencia ausente se ve como ausente» frente a «declarada sin artefacto»: no queda claro si “ausente” es el mismo estado o uno adicional. Detectarlo obligaría a inventar un conjunto de evidencia esperada —posiblemente desde `gates`, también indefinido—.

## DRY-RUN
- Lecturas previstas: nodo WS27.2, guía, brief, alcance, decisiones, cobertura y bloques de dependencias; sin código ni ejecución.
- Cambios previstos: módulo de evidencia bajo `frontends/mindmap/views/workspace/evidence/` y pruebas; punto de integración con la vista de TaskDoc no nombrado.
- Dependencias: WS13 aporta lector/historia; WS12, contrato de correspondencia y salida de `deskops closeout verify`; G_UI_READ se recibe por delta.
- Validaciones futuras: fixtures con evidencia declarada, encontrada, verificada, ausente, no declarada y fallo de verificación; abrir Markdown dentro del workspace y, fuera de ese caso, mostrar ruta y “no soportado”; reporte ausente o fallo de comando debe verse como no verificable con error.

## FUTURO
WS12 debe publicar la correspondencia por tipo de evidencia y la salida pública de `closeout verify`; WS13, la apertura en el lector; el receptor P01, el acta G_UI_READ del delta. La promoción fijará archivos, textos y pruebas concretas, y una persona aceptará el delta.
