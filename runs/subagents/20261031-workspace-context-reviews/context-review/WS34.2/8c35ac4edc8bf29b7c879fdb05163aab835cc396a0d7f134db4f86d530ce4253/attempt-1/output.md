## REFORMULACION

Propósito: definir el encargo de implementación que expone un adaptador público restringido para reply autorizado, vinculado al intento. Resultado: código en `runtime/`, comando/API en `cli/commands/runtime.py` o la API que fije WS12, y `tests/`, con timeout/errores y autoridad del coordinador. Repo dueño: `deskops`. Límites: no enviar mensajes durante la planificación; no elegir umbral de timeout propio; solo avanzar con la política de WS12 verificada en `G_WRITE_CONTRACT`; requiere `G_EXEC`/`G_SCION`.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Lecturas: `dag.yaml` (nodo y vecinos), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y la guía. Cambios previstos, sin ejecutar: adaptador de reply en `runtime/`, comando/API en `cli/commands/runtime.py` o la API definida por contrato, y pruebas en `tests/`. Dependencias: WS33 (referencias mensaje/intento), WS12 (política y umbral de timeout para este delta), WS34.1 (patrón de dispatch); gates `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`. Validaciones futuras: preflight de promoción; agente real con reply correlacionada al intento correcto; timeout reportado como fallo sin confirmación; ausencia de mensajes en planificación; parada y registro de hueco si falta la política.

## FUTURO

WS12 produce la política/umbral de timeout y la sección contractual del delta; WS44 y el humano resuelven `G_SCION`/`G_EXEC`; el TaskDoc de promoción fija archivos, escenarios y textos; la recepción `per_delta` verifica `G_WRITE_CONTRACT`. Nada de ello es ambigüedad del nodo.
