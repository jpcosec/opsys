REFORMULACION
Encargo: implementar en deskops la separación entre identidad de intento y dispatch, materializando el registro por intento que fije WS12 y ajustando la identidad/estado de RunDoc mediante modelo SLDB. Resultado: dos intentos locales con IDs distintos y registro intent/no confirmado en store temporal, sin red. Repo: deskops. Límites: no dispatch/reply ni evento Hub simulado; no inventar almacenamiento; depende de WS05/WS12; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; no es ticket del Board.

AMBIGUEDADES
1. «dispatch intent ... y confirmed ... como hechos separados del RunDoc» frente a «registro por intento que WS32.2 vuelve manifiesto canónico», y el glosario «RunDoc ... su registro canónico». ¿El registro es el RunDoc o un artefacto distinto? Obliga a inventar si se extiende models/run.py o se crea otro registro, y cuál es canónico.
2. «ambos se registran en el registro por intento» frente a «sin simular respuesta Hub ni invocar red» y una aceptación que solo exige «registro intent/no confirmado». Obliga a inventar si WS32.1 debe incluir ya el hecho «confirmed», su forma y origen, siendo inobservable aquí.

DRY-RUN
Un ejecutor leería WS05, el contrato WS12, el candidato drawer y runtime/scion.py, models/run.py, services/closure.py y tests. Cambiaría models/run.py (identidad de intento validada por SLDB), scion.py (registro local de intent) y closure.py (clave por id de intento), y añadiría pruebas con store temporal. Consumiría WS05/WS12; si falta el contrato del registro, se detiene y registra hueco con dueño. G_CLOSEOUT está satisfecho; G_SCION sigue sin verificar y G_WRITE_CONTRACT es por delta: sin recibo, bloqueo. Validaría: IDs distintos, registro no confirmado, ausencia de red/mocks, RunDoc por API/CLI y sin Markdown ad hoc. Errores: id duplicado, modelo inválido, red o evento Hub; resultado esperado: pruebas en verde y hueco registrado si falta contrato.

FUTURO
WS32.2 hará el manifiesto canónico e idempotente; WS34/WS37 probarán dispatch real fallido/confirmado y correlación; WS44 producirá G_SCION; WS12 fijará representación y ubicación del registro; el humano designa operador Scion.
