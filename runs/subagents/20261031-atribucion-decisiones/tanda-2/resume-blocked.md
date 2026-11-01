# Tanda 2 detenida por saldo — 2026-10-31

Sobre `fc5e64a8`, `context_review.py run --stale --jobs 6` dio 47 respuestas completas y 26 fallos técnicos, los 26 con `402 Insufficient Balance` de DeepSeek en sus tres intentos. Una llamada aparte tras la tanda dio el mismo 402. El proceso salió con código 0.

Nada se registró en `dag.yaml`; `status` reporta 73 `input changed`. Las 47 respuestas no se pierden: el helper las reutiliza por hash de entrada. Aún no fueron comparadas.

Tras recargar saldo, sin relanzar `--stale`, que devolvería fallo sin intentar:

    python desk/drawer/plans/workspace-documental/context_review.py run WS27.1 WS27.2 WS28 WS29 WS30 WS31 WS32 WS32.1 WS32.2 WS33 WS33.1 WS33.2 WS34 WS34.1 WS34.2 WS35 WS36 WS37 WS38 WS39 WS40 WS41 WS42 WS43 WS44 WS45 --new-attempt --reason "reintento tras 402 Insufficient Balance de DeepSeek" </dev/null >> runs/subagents/20261031-atribucion-decisiones/review-run-retries.log

Luego: comparar los 73 outputs, disposiciones, registrar, Tester, closeout de la tarea y handoff.

## Actualización 2026-11-01

WS27.1 reprobado: 402, `attempt-4`, request `2128c419-ed51-48dc-a494-d57ecf19e7c5`. No relanzar los 26 sin resolver antes el actor de P07/P09 (ver `comparison-ledger.md`): si root aprueba corregirlo, el input cambia y corresponde `run --stale` de los 73, no este comando. WS13 y WS19 también requieren intento nuevo si la fuente no cambia.

## Sustituido 2026-11-01

Este archivo ya no es ruta de reanudación. Crédito confirmado por el humano; el comando de 26 nodos queda sin efecto. La tanda de 73 se lanza sobre la fuente nueva, tras la comprobación focal de root.
