## REFORMULACION

**Propósito:** decidir si WS34.2 se entiende como encargo de planificación, sin evaluar el producto ni ejecutar nada.

**Resultado:** nodo de implementación en `deskops` que debe entregar un adaptador público restringido de reply vinculado al intento, con timeout/errores, autoridad del coordinador y pruebas.

**Repo:** `deskops` — `runtime/`; `cli/commands/runtime.py` o API definida; `tests/`.

**Límites:** no ejecutar; no revisar los bloques edge vecinos como contratos propios; no enviar mensajes en planificación; no inventar aprobaciones de ejecución, Scion o escritura; no crear sustituto si falta un contrato.

## AMBIGUEDADES

Ninguna.

El umbral de timeout y el canal/API quedan delegados a WS12, productor nombrado por el propio nodo. G_EXEC, G_SCION y G_WRITE_CONTRACT son gates externos o por delta; su pendiente es intencional y no obliga a inventar resultado, aceptación ni límites.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (WS34.2, WS33, WS12, WS34.1 y gates), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.

**Cambios previstos:** ninguno; esta revisión no modifica el nodo.

**Dependencias:** WS33 (agregado WS33.1/WS33.2), WS12 (contrato por delta), WS34.1 (dispatch); además G_EXEC —humano—, G_SCION —producido por WS44— y G_WRITE_CONTRACT —evaluación per_delta—.

**Validaciones futuras:** al promover, comprobar el contrato WS12; ejecutar prueba con agente real de reply vinculado al intento correcto; verificar que un timeout se reporta como fallo sin confirmación; comprobar que no se enviaron mensajes en planificación; preflight del TaskDoc.

## FUTURO

WS12 debe fijar el umbral y el canal/API. WS44 debe probar Scion. El humano debe resolver G_EXEC y la recepción per_delta de G_WRITE_CONTRACT. El TaskDoc de promoción fijará archivos, escenarios y evidencias. WS33 y WS34.1 deben entregar sus salidas. Nada de esto es ambigüedad del nodo.
