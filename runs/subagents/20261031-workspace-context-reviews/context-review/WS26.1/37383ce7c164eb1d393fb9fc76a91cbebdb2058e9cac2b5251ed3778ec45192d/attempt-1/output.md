## REFORMULACION

Encargo: implementar en **graph_ui** la autoría explícita de una tarea desde un candidato del drawer, con evidencia declarada, dependencias y pills de contexto, consumiendo el contrato WS12 y la representación Board/TaskDoc de WS22. Resultado: vista y endpoints autorizados en `frontends/mindmap/views/workspace/authoring/`, más tests; UF04 sobre TaskDoc real, con persistencia visible tras recargar. Límites: no editar `status` para avanzar; si una operación Git o endpoint carece de contrato/dueño, handoff explícito y acción no disponible; G_HUMAN_READ bloquea habilitar mutaciones en UI, no el desarrollo ni pruebas aisladas de API.

## AMBIGUEDADES

Ninguna. Los huecos de contrato tienen productor nombrado (WS12) y regla de parada; gates pendientes y detalles de promoción no cuentan como ambigüedad.

## DRY-RUN

Lecturas: contrato `contratos/operaciones.md` de WS12, TaskDoc de WS26.1, TaskDoc real del corpus WS40 o store temporal, vistas Board/reader de WS22 y tests existentes. Cambios previstos: archivos de authoring, selección de candidato, campos de evidencia/dependencias/pills y llamadas solo a endpoints whitelisted; tests unitarios/API aislados y de recarga. Dependencias: WS12 aporta operación, campos, precondición y errores; WS22, TaskDoc/pills y selección común; G_CLOSEOUT ya satisfecho respalda evidencia declarada. Gates: G_WRITE_CONTRACT y G_UI_WRITE se consumen por delta propio de WS26.1; G_HUMAN_READ se exige antes de habilitar la mutación UI. Errores: contrato, endpoint o Git ausente → detener, registrar hueco con repo dueño y dejar handoff, sin inventar API, campo o lock. Validación esperada: prueba aislada con store real temporal y comprobación de que evidencia, dependencias y pills persisten tras recarga, sin editar `status`.

## FUTURO

WS26.2 enruta en Board y muestra capa lista; WS26 cierra cuando ambos hijos cumplen. WS12 produce el contrato y los recibos G_WRITE_CONTRACT; el receptor P01 emite acta G_UI_WRITE por delta; WS16 produce el acta G_HUMAN_READ. La promoción sigue no autorizada hasta TaskDoc y preflight específicos.
