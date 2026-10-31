## REFORMULACION
WS32 es un nodo agregado, no ejecutable, del plan del workspace documental. Su propósito es refinar el ticket de Scion para unificar identidad de intento y cierre, sin crear un segundo pipeline: intento distinto de slug, dispatch `intent`/`confirmed` separado y manifiesto/RunDoc/cierre consistentes e idempotentes. El resultado es el agregado de las salidas de WS32.1 y WS32.2; el repo dueño es `deskops`. Límites: no hay ejecución autorizada, la promoción está `not_authorized`, se prohíbe duplicar pipeline y la integración es delta sobre ticket existente (`delta_or_existing_ticket`, `never_parallel_duplicate`).

## AMBIGUEDADES
Ninguna. La aceptación del agregado queda definida por la aceptación de sus hijos; las identidades, el manifiesto y la idempotencia están acotados en WS32.1/WS32.2. Los gates pendientes tienen productor nombrado y no obligan a inventar sustituto.

## DRY-RUN
- Lecturas previstas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS32, sus hijos y definiciones de gates.
- Cambios previstos: ninguno en WS32 por ser agregado; solo se consolidan las salidas de WS32.1/WS32.2, que tocan `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y tests.
- Dependencias: WS05, WS12, WS32.1, WS32.2; gates `G_CLOSEOUT`, `G_SCION`, `G_WRITE_CONTRACT`.
- Validaciones futuras: aceptación de ambos hijos; prueba de identidades de intento, dispatch fallido y finalización repetida; ausencia de duplicados en manifiesto, RunDoc e índice de cierre.

## FUTURO
WS44 debe producir `G_SCION` mediante probe real; WS12 produce `G_WRITE_CONTRACT`; `G_CLOSEOUT` queda a cargo del resolver externo indicado. La autorización de promoción y cualquier cambio de alcance corresponden a un humano. WS33 y otros dependientes no se revisan aquí.
