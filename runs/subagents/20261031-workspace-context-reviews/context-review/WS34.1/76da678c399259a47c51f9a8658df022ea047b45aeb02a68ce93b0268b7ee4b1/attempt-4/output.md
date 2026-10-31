REFORMULACION
Propósito: encargar en `deskops` un adaptador público restringido para dispatch de Scion, con confirmación por respuesta de la API, identidad de intento, timeout/errores y autoridad del coordinador según WS12. Resultado: adaptador en `runtime/`, `cli/commands/runtime.py` o API definida, con tests; un agente real demuestra un dispatch aceptado y otro rechazado o vencido por timeout; sin shell arbitrario ni transporte duplicado. Repo dueño: `deskops`. Límites: depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT; no autoriza ejecución ni promoción.

AMBIGUEDADES
1. «output_scope: runtime/; cli/commands/runtime.py o API definida; tests/» no aclara si «API definida» es un canal público ya existente o una API que este nodo deba definir. WS12 establece que el adapter es un canal público existente y que, si falta, se registra hueco y dueño, no se diseña aquí. Obligaría a inventar el canal/contrato de dispatch y podría exceder el alcance.

DRY-RUN
Lecturas: nodo WS34.1, aristas WS33/WS12/WS34/WS34.2, gates y guía/brief/alcance/decisiones/cobertura. Cambios previstos: adaptador de dispatch y tests en `deskops`; nada se ejecuta. Dependencias: WS33 y WS12; gates G_EXEC (autorización humana externa), G_SCION (WS44) y G_WRITE_CONTRACT (WS12). Validaciones futuras: gates pasan; agente real con dispatch aceptado y rechazado/vencido; comprobar ausencia de shell arbitrario y de transporte duplicado; preflight del TaskDoc; promoción no autorizada.

FUTURO
WS07 designa operador Scion; WS44 produce G_SCION; un humano externo produce G_EXEC; WS12 produce G_WRITE_CONTRACT y debe registrar la capability de dispatch para WS34. El TaskDoc fijará archivos, timeout y casos de prueba. Un humano decide la promoción. WS34.2 (reply) corresponde a su propio nodo.
