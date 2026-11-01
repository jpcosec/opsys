REFORMULACION
Propósito: implementar en deskops un adaptador público restringido para reply vinculado al intento, con timeout/errores y autoridad del coordinador. Resultado: capacidad de respuesta autorizada, probada con agente real. Repo dueño: deskops; salidas en runtime/, cli/commands/runtime.py o la API que fije WS12, y tests/. Límites: no enviar mensajes durante planificación; no elegir umbral de timeout; no duplicar transporte ni shell arbitrario; solo avanzar si WS12 produjo la política de timeout de este delta y G_WRITE_CONTRACT la verificó; si falta, detenerse y registrar el hueco. Es implementación, no agregado, pero depende de gates pendientes.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: nodo y aristas en dag.yaml; sección de WS12 sobre política, umbral y clasificación de timeout para WS34.2; adaptador y correlación de WS34.1; registros/vinculación de WS33.2; IDs de intento de WS32.1; evidencia de G_SCION (WS44); autorización G_EXEC; task_file. Cambios: añadir la operación reply en el canal público definido, validar autoridad del coordinador, vincularla al intento, tratar timeout como fallo local sin confirmación y manejar errores; añadir pruebas. Dependencias: WS34.1 debe existir; WS33.2 debe aportar referencia de intento/decisión; WS12 debe aportar umbral y clasificación; los gates deben estar satisfechos para este delta. Errores esperados: contrato/umbral ausente, intento no correlacionable, timeout o rechazo. Validación futura: agente real responde y queda vinculado al intento correcto; timeout se reporta como fallo sin confirmación; G_SCION/G_EXEC y G_WRITE_CONTRACT por delta pasan. Sin ejecutar.

FUTURO
WS12 fija el umbral y la clasificación; WS34.1 entrega dispatch; WS33.2 entrega vinculación/decisión; WS44 produce el probe de G_SCION; un humano autoriza G_EXEC; la promoción/TaskDoc fija archivos, pruebas y textos. Nada de esto es ambigüedad.
