REFORMULACION
Propósito: fijar el encargo de planificación del adaptador público restringido para `reply` de Scion, vinculado al intento, con timeout/errores y autoridad del coordinador. Resultado: implementación en `deskops` (`runtime/`; `cli/commands/runtime.py` o API que fije WS12; `tests/`), con aceptación comprobable: pasan G_SCION/G_EXEC; un agente real demuestra respuesta vinculada al intento correcto y un timeout se reporta como fallo sin confirmación, usando el umbral de WS12. Repo dueño: `deskops`. Límites: no enviar mensajes durante planificación; no ejecutar shell arbitrario ni duplicar transporte; `reply` queda ligado a WS33 y al intento de WS34.1; promoción no autorizada.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, nodo WS34.2 y contratos vecinos WS33/WS12/WS34.1 como dependencias, sin revisarlos. Cambios previstos: adaptador y pruebas en `deskops`; ningún cambio de plan. Dependencias: WS33 aporta referencias mensaje/resultado/decisión; WS12, autoridad, canal/API y umbral; WS34.1, dispatch e identidad de intento; gates G_EXEC, G_SCION y G_WRITE_CONTRACT. Validaciones futuras: prueba con agente real, correlación con intento correcto, timeout como fallo sin confirmación, probe de WS44 y recibo por delta de G_WRITE_CONTRACT. No se ejecuta nada.

FUTURO
WS12 publica contrato, canal/API, autoridad y umbral de timeout; WS33 produce el vínculo de mensajes/decisiones; WS34.1 produce dispatch e id de intento; WS44 produce la evidencia de G_SCION; el humano/designee resuelve G_EXEC; el receptor P01 verifica el delta de G_WRITE_CONTRACT; la promoción fija archivos, pills, átomos y pruebas exactas en TaskDoc.
