# Executor comparison — WS32

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

**Propósito:** unificar la identidad de intento y el cierre de Scion sin crear un segundo pipeline: el intento no es el slug, `dispatch intent` y `dispatch confirmed` son hechos separados, y manifiesto, RunDoc y cierre deben ser consistentes e idempotentes sobre el intento correcto.

**Resultado:** nodo agregado no ejecutable; su resultado son las salidas de WS32.1 (separar identidad de intento y dispatch) y WS32.2 (idempotencia de manifiesto y cierre). Se cumple cuando ambos hijos cumplen su aceptación.

**Repo dueño:** `deskops`. **Límites:** depende de WS05 y WS12; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; promoción no autorizada; prohíbe duplicar pipeline o implementación ya reconciliada.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
