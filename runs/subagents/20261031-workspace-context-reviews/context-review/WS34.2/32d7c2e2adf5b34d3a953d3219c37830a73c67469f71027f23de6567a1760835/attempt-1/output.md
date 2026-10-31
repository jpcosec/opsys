## REFORMULACION
**Propósito:** planificar un adaptador público restringido para `reply` vinculado al intento, con timeout/errores y autoridad del coordinador.  
**Resultado:** implementación en `deskops`, con salidas en `runtime/`, `cli/commands/runtime.py` o la API definida, y `tests/`. La aceptación exige que un agente real demuestre respuesta vinculada al intento correcto y que un timeout se reporte como fallo sin confirmación, usando el umbral del contrato WS12.  
**Repo:** `deskops`.  
**Límites:** no enviar mensajes durante la tarea de planificación; promoción no autorizada; archivos, escenarios y textos exactos quedan al TaskDoc. Gates: `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas:** nodo WS34.2; vecinos WS33, WS12 y WS34.1; gates; guía, brief, alcance, decisiones y cobertura. Sin herramientas ni ejecución.  
**Cambios previstos:** ninguno ahora. En promoción/implementación: adaptador, API/CLI y pruebas en `deskops`; el TaskDoc fijará archivos, escenarios y evidencia.  
**Dependencias:** WS33 aporta referencias mensaje/intento y procedencia; WS12, umbral de timeout y autoridad del coordinador; WS34.1, dispatch, confirmación e identidad de intento; gates externos. Si falta contrato, aplica “detenerse, registrar el hueco” de `alcance.md`.  
**Validaciones futuras:** `G_SCION` mediante WS44; `G_EXEC` por humano; `G_WRITE_CONTRACT` por WS12; prueba con agente real de reply correcto y timeout sin confirmación; preflight de promoción.

## FUTURO
WS12 produce el contrato técnico, umbral y autoridad; WS33, las referencias y deduplicación; WS34.1, dispatch e identidad; WS44 verifica `G_SCION`; el humano resuelve `G_EXEC` y designa actores en WS07. El TaskDoc de promoción fija archivos, casos y evidencia. Nada de esto es ambigüedad del nodo.
