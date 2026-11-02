# Disposición correctiva WS12, attempt-1

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Corrige la `disposition.md` de este intento, que se conserva como historia. Origen: auditoría root, `runs/subagents/20261102-ws12-correccion/review-source-4.md`.

**Rechazado.** La sección FUTURO dice que WS34.1 y WS34.2 fijan el umbral de timeout al prepararse. El input de WS12 dice lo contrario: esa sección del contrato WS12 la fija al preparar esos deltas, «no WS34». Es una transferencia contraria al propio input, no una paráfrasis, y `operaciones.md` §11.1 y §11.2 la confirman.

**Mi fallo.** La disposición anterior respondió solo a AMBIGUEDADES, no leyó FUTURO y contestó la duda con un contrato que ese bundle no contiene.

**Efecto.** Se repite solo WS12 con `--new-attempt`, mismo input y fuentes.
