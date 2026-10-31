# Executor comparison — WS34.1

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION
**Propósito:** definir un adaptador público restringido para dispatch de Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.
**Resultado:** un dispatch aceptado y otro rechazado o vencido por timeout, demostrados con agente real; sin shell arbitrario ni transporte duplicado.
**Repo:** `deskops`; salidas en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`.
**Límites:** depende de WS33 y WS12; exige G_EXEC, G_SCION y G_WRITE_CONTRACT. Es candidato: no hay ejecución autorizada ni promoción autorizada.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
