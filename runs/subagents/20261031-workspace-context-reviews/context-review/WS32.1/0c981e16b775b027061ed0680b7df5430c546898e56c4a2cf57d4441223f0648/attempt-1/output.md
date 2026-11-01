REFORMULACION
WS32.1 es un nodo delivery de implementación en deskops, no agregado. Encargo: refinar el candidato de drawer externo y separar identidad de intento, dispatch intent local y confirmed (solo respuesta Hub), materializando el registro por intento que WS32.2 hará manifiesto canónico, con contrato/ubicación de WS12 e identidad de WS05. Resultado: cambios en deskops/runtime/scion.py, models/run.py, services/closure.py y tests; dos intentos locales con IDs distintos y registro intent/no confirmado con store temporal real; modelo registrado/validado SLDB. Límites: sin red, dispatch/reply ni Hub simulado; sin Markdown ad hoc; gates G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT.

AMBIGUEDADES
1. «dispatch intent ... y confirmed ... ambos se registran» frente a «SIN dispatch/reply de red ni evento Hub fingido»: obliga a decidir si WS32.1 persiste ya `confirmed` y cómo, sin poder observarlo; riesgo de placeholder o estado inventado.
2. «Dos intentos locales generan IDs distintos antes de dispatch y registro intent/no confirmado» no comprueba «intento no es slug» ni que dispatch intent y confirmed sean hechos separados. Obliga a inventar representación y prueba de la separación central.
3. «Refinar el candidato de drawer de external_references.scion» no aclara si se edita el candidato o solo se lee; output_scope no lo incluye. Obliga a decidir si se modifica un artefacto con hash externo.

DRY-RUN
Leería candidato, auditoria/scion.md (WS05), contratos/operaciones.md (WS12) y gates; inspeccionaría runtime/scion.py, models/run.py, services/closure.py y tests. Cambios: generar id de intento, modelar dispatch intent/no confirmado y registro por intento según WS12, sin red; registrar/validar modelo y probar con store temporal. Dependencias: WS05 separa identidades; WS12 fija ubicación/contrato; WS32.2 consumirá el registro; WS34/37 probarán Hub. Gates: G_CLOSEOUT satisfecho; G_WRITE_CONTRACT per-delta pendiente de recibo; G_SCION unverified bloquearía. Si falta contrato o identidad, detener y registrar hueco. Validación: dos IDs distintos, ningún no confirmado etiquetado como aceptado/fallido Hub, modelo validado, RunDoc por API/CLI.

FUTURO
WS32.2 hará manifiesto canónico e idempotencia; WS34/37, dispatch real y correlación bajo G_EXEC; WS44/G_SCION, probe; WS12, contrato por delta; un humano designará operador Scion y emitirá recibos.
