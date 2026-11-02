# Comparación del Supervisor — corrección de WS09, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, lista cerrada y límites. Lo que marcan queda fijado aquí.

- «23 bloqueado»: las 23 fichas conservan Estado `bloqueado`, con el texto de su motivo intacto.
- NotationDoc: definición de notación en `s2v/notations/*.yml` = authored (`infraestructura.md:132`). NotationDoc en el store, registrado por `notation sync` (`infraestructura.md:100,132`) = derivado regenerable desde esa definición, solo si esas líneas lo sostienen; si no lo dicen, escribir «no comprobado». Abrir ambas líneas.
- F05: Origen y Campos añaden una frase, sin reordenar el campo.
- «Si el cambio lo exige»: Evidencia se actualiza siempre que se cite una fuente nueva. Clase solo en F18a. Renderer no cambia.
- `dag.yaml:1222-1224` se abre antes de redactar F18b.
- Congelación, Tester, renovación y closeout son del Supervisor. El Executor no los ejecuta ni los invoca.
