# Executor comparison — WS33.1

State: accepted_current

## Reformulación examinada

## REFORMULACION

- **Propósito:** vincular mensajes y resultados de Scion a un intento existente, conservando procedencia y evitando duplicados.
- **Resultado:** importación idempotente por Hub/proyecto/conversación/mensaje y por Hub/proyecto/intento/id de fuente; los mensajes sin intento resoluble quedan como hueco de procedencia.
- **Repo dueño:** `deskops`, con salidas en `runtime/`, modelos/reportes y tests.
- **Límites:** no tocar tablas Scion, no depender del editor UI, no vincular sin id de intento existente; `G_SCION` pendiente y promoción no autorizada.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
