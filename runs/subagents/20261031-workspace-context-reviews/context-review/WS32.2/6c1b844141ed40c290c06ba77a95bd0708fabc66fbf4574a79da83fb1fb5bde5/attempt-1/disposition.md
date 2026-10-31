# Executor comparison — WS32.2, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
**Propósito:** hacer idempotentes manifiesto, RunDoc y cierre sobre el intento correcto, identificado por id de intento, nunca por agente o slug.  
**Resultado:** registro canónico por intento y cierre consistente en id de intento, hash de sesión y evidencia, sin duplicados.  
**Repo:** `deskops` (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`).  
**Límites:** no inventar sesión/hash; si falta artefacto o contrato, registrar hueco con WS05/WS12 y bloquear; no segundo pipeline; no ejecutar; promoción no autorizada; gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT.

##

## Hallazgos/disposición contra intención

Payload divergente: «conserva identidad y evidencia sin crear registros nuevos» prohíbe sobrescribir evidencia; error/no-op concreto lo define WS12 como contrato, no cambia invariante. Se aclaró identidad/idempotencia local sin evento Hub fingido; integración real WS34/37 G_EXEC. Nueva revisión por contrato cambiado, no por elegir código HTTP aquí.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
