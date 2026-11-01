REFORMULACION
Propósito: hacer idempotentes manifiesto, RunDoc y cierre por id de intento. Resultado: implementación y pruebas en deskops del registro canónico por intento, sin duplicados al repetir la finalización. Repo: deskops. Límites: solo persistencia local con store temporal; sin dispatch/reply, red, Hub simulado ni segundo pipeline; correlación real en WS34/37 bajo G_EXEC; si WS05/WS12 no definen artefacto/hash de sesión, se registra hueco y se bloquea esa coincidencia; no se recrea el candidato drawer.

AMBIGUEDADES
1. «manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia». No fija qué evidencia (declarada, encontrada o verificada), su representación ni criterio de igualdad; el candidato solo la nombra como campo mínimo. Obliga a inventar el cotejo y admite comparación laxa.
2. El alcance exige «evidencia y commit de cierre» como campos mínimos, pero la aceptación solo pide coincidencia en «id de intento, hash de sesión y evidencia». Omite el commit; obliga a decidir si su coincidencia es requisito de aceptación.

DRY-RUN
El ejecutor leería candidato drawer, WS05, WS12, registro WS32.1, `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests. Cambiaría: campos del manifiesto en RunDoc; upsert por id de intento en scion; finalización en closure que reutilice registros y no duplique; pruebas. Consumiría WS05 (artefacto/campo de sesión), WS12 (ubicación, campos, contrato por delta) y WS32.1 (identidad/registro); comprobaría G_CLOSEOUT satisfecho, G_SCION y G_WRITE_CONTRACT; si falta contrato o gate exigido, se detiene y registra hueco, sin sustituto. Errores: sin artefacto/hash de sesión -> hueco WS12/WS05 y bloqueo; sin registro WS32.1 -> parada; segunda finalización crea registro, campos no coinciden o se identifica por agente/slug -> fallo. Validación: store temporal real, dos intentos, finalizar dos veces el mismo id, verificar un manifiesto/RunDoc/registros y coincidencia de id, hash, evidencia y commit; pytest focalizado; sin red/Hub.

FUTURO
WS05 entrega inventario; WS12 contrato y recibo per_delta; WS32.1 registro; WS44 satisface G_SCION; WS34/37 prueban Hub real; WS37 valida; humano acepta y promueve.
