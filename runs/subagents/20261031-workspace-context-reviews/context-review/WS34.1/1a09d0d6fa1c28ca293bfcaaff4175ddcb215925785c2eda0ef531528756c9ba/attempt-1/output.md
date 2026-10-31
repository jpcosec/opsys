## REFORMULACION
**Propósito:** definir un adaptador público restringido para dispatch de Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.
**Resultado:** un dispatch aceptado y otro rechazado o vencido por timeout, demostrados con agente real; sin shell arbitrario ni transporte duplicado.
**Repo:** `deskops`; salidas en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`.
**Límites:** depende de WS33 y WS12; exige G_EXEC, G_SCION y G_WRITE_CONTRACT. Es candidato: no hay ejecución autorizada ni promoción autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas:** nodo WS34.1, aristas WS33/WS12/WS34/WS34.2 y gates; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y guía. Sin herramientas ni ejecución.
**Cambios previstos:** ninguno en esta revisión. Si se promoviera, el TaskDoc fijaría archivos, cápsulas y evidencia dentro de `runtime/`, `cli/commands/runtime.py` o API WS12, y `tests/`.
**Dependencias:** WS33 aporta referencias de intento; WS12, autoridad del coordinador y contrato de operaciones; WS34.2 cubre reply; G_EXEC/G_SCION/G_WRITE_CONTRACT condicionan la prueba.
**Validaciones futuras:** gates aprobados; agente real con dispatch aceptado y rechazado/timeout; ausencia de shell arbitrario y transporte duplicado; recibo G_WRITE_CONTRACT por delta; preflight de promoción.

## FUTURO
WS44 debe producir el probe y contrato público de Scion para G_SCION. Un humano/designee debe resolver G_EXEC y autorizar agente, proyecto, acciones, alcance y sesión. WS12 debe publicar el contrato de operaciones y autoridad del coordinador. WS33 debe entregar identidad de intento. WS34.2 implementa reply. El TaskDoc de promoción concretará archivos, escenarios y umbrales de prueba; la recepción G_WRITE_CONTRACT se verifica por delta, no por aceptación conjunta.
