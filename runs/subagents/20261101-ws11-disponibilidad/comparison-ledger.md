# Comparación de disponibilidad de WS11

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Reemplazo aplicado en `b30c24cf`, sha256 `6a4f8518f3d69de6118550b3077921db4bbb46bc9123c26980c6c8fc5f62361e`, idéntico al aprobado por root.

**Tester focal PASS.** No pudo abrir rutas `GU/` ni `DK/` en esta ronda y declara no haberlas verificado; sí leyó `open_store.py`. Rondas anteriores las cubren, sobre bytes anteriores. Sin hash propio: lo toma del log.

**Revisión fresca, `contrato-review/`, sobre estos bytes.**

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS13.1 | 1. Relaciones del panel | §6 y 6.1. Sin cambio |
| WS13.1 | 2. «No depender de conocer un ID» | WS13.2, explorador. Sin cambio |
| WS13.1 | 3. Catálogo WS09 externo | Artefacto del extracto: solo llevaba F17 |
| WS13.1 | 4. Bases `a1b2b22` y `134a665` | La primera es del nodo, la segunda es la observada. Sin cambio |
| WS41 | 1. Quién implementa volver | H-12. Sin cambio |
| WS41 | 2. Rutas fuera de `source/` | El `output_scope` incluye rutas de lectura. Sin cambio |
| WS41 | 3. Códigos HTTP | §8.5 lo deja a WS41 |

Ninguna toca la disponibilidad ni contradice §3.2 y §8.5. Sin contradicción real. Las revisiones anteriores se conservan en sus runs.

**Residuo cosmético, no editado por orden root:** la fila E-MD3 de §8.5 dice «no tiene store» y §3.2 cubre también `root` ausente.
