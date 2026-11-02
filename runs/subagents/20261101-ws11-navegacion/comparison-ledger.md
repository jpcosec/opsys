# Comparación WS11

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. El Tester es pi deepseek-flash, sin shell: no ejecutó nada ni vio git. Esto no es aprobación humana ni root.

| Ronda | Resultado | Hallazgo | Disposición |
|---|---|---|---|
| Executor | entregó | contrato de 13 secciones, sin commit | Leído completo. Congelado en `820b4d57` |
| Mi revisión | sin hallazgos | No vi las dos lecturas falsas | Fallo de revisión mía, registrado |
| Tester v1 | FAIL | §2.2 y §4, negaciones falsas | Reales. Corregidas en `76155db9` |
| Tester v2 | FAIL | §4 enumeración incompleta; 13 negaciones y 6 citas sin otra falla | Real. Corregida en `4d710c02` |
| Tester v3 | PASS | Solo sobre la enumeración de §4 | Vigente |

Cobertura: v1 cotejó identidad, rutas, C1-C4, dependientes, G_UI_READ, productores. v2, negaciones y §7-§10. No se muestreó todo el contrato: las filas C5-C14 y H-01 a H-25 se cotejaron solo por existencia de productores y por las citas abiertas. No cubierto: conducta en runtime, commits (el Tester no ve git).

Contrato final: sha256 `ca537c71d585a86032a1bf3817705f00af4904139e50534f0f5b70416b3597df`.
