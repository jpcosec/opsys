## REFORMULACION
Propósito: registrar una decisión humana explícita —aprobar o pedir corrección, con texto en este último caso— asociada a un intento Scion y, por él, a su tarea. Resultado: un registro con actor humano, referencia al intento y a la tarea, y resultado explícito; `completed` del agente nunca se registra como aprobado. Repo dueño: deskops (`output_base: deskops:repository_root/`), con salidas en runtime/modelos-reportes/tests según contrato. Límites: solo escribe la decisión mediante la operación que fije WS12; no escribe estados de testing/closeout ni validado/cerrado, no despacha ni responde a Scion, no toca tablas Scion y no duplica en paralelo el candidato Scion. Si falta contrato u operación, se detiene y registra hueco con dueño. Gates: G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12 aplicable al delta (operación, actor, campos, revisión y errores) y las salidas de WS32 (identidad de intento/RunDoc/manifiesto) y WS33.1 (vínculo de mensajes/resultados). Comprobaría G_SCION y G_WRITE_CONTRACT antes de escribir. Cambios previstos: añadir la operación de registro de decisión en deskops —servicio/CLI o adaptador que fije el contrato—, su modelo/reporte y tests; sin tocar tablas Scion ni estados de tarea. Validación esperada: aprobación y petición de corrección quedan con actor, intento y tarea; la corrección sin texto falla; un `completed` de agente no se acepta como aprobación; referencia inexistente se rechaza. Errores: contrato ausente → parar y registrar hueco con repo dueño; gate no satisfecho → no ejecutar; fallo de escritura → no crear sustituto.

## FUTURO
WS12 fija la operación y el formato de actor; WS44 produce el probe de G_SCION; WS32 y WS33.1 aportan identidad de intento y vínculos. La promoción a TaskDoc sigue no autorizada y exige preflight específico. WS34/WS36 y WS35/WS37 consumen o validan después; el receptor P01 emite el acta por delta. La aceptación del delta es una decisión humana futura.
