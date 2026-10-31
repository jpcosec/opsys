## REFORMULACION
- **Propósito:** encargo de planificación para vincular mensajes y resultados a intentos con deduplicación y procedencia, como backend documental independiente del editor UI.
- **Resultado:** adaptador backend, modelos/reportes y tests en `deskops`; importación repetida sin duplicados ni atribución de conversaciones completas a un intento; huecos de procedencia para mensajes no vinculables.
- **Repo:** `deskops` (`output_base: deskops:repository_root/`).
- **Límites:** no tocar tablas Scion; promoción no autorizada; depende de WS32 y `G_SCION`; integración `delta_or_existing_ticket`, sin duplicado paralelo.

## AMBIGUEDADES
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, y se deduplican por Hub + proyecto + intento + id de fuente, conservando procedencia.»  
   No define qué hacer con un resultado que tenga intento pero carezca de id de fuente, o tenga varios. La aceptación solo cubre mensajes no vinculados. Obliga a inventar si se importa, se descarta o se registra como hueco.

2. «matriz WS06 llega de forma transitiva por WS11/WS12» frente a `depends_on: - WS32`.  
   WS32 garantiza WS12, pero no WS11. El ejecutor tendría que decidir si puede avanzar sin la aceptación/matriz de WS11 o inventar el orden; falta la arista o la justificación de que WS11 no aplica.

## DRY-RUN
- **Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS33.1; WS32/WS33 se usan solo como contexto contractual, sin revisarlos.
- **Cambios previstos:** adaptador en `runtime/`, modelos/reportes, tests de deduplicación por claves declaradas y registro de huecos de procedencia; sin tablas Scion.
- **Dependencias:** WS32 para identidad de intento; `G_SCION` vía WS44; WS05/WS44 para identificar fuente; WS12 transitiva. La cobertura de WS11 queda cuestionada.
- **Validaciones futuras:** evidencia de `G_SCION`, prueba de importación repetida, comprobación de no escritura en Scion y preflight/TaskDoc de promoción. Nada ejecutado.

## FUTURO
WS44 produce `G_SCION`; WS05 inventaría la fuente; WS32 fija identidad de intento; WS12 aporta contrato de escritura; WS06/WS11/WS12 acuerdan la matriz. El humano resuelve Pxx, autoriza promoción y el TaskDoc fija archivos, pruebas y textos.
