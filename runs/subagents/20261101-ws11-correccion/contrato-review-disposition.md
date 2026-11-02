# Comparación de la revisión fresca del contrato, ronda 1

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Evidencia en `renovacion-1/contrato-review/`. Revisores pi deepseek-flash sin herramientas, con el SYSTEM v2 de `context_review.py` (leído, no modificado). Input: contrato, extractos de `dag.yaml` y de F17. Sin historial ni salidas previas.

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS13.1 | 1. borrador frente a «según contrato» | Futuro: root fija el hash. No es del contrato |
| WS13.1 | 2. Recibo antes de implementar o de cerrar | §12: al preparar o promover. No cambia |
| WS13.1 | 3. `output_scope` frente a rutas de servidor | Falsa para WS13.1: el scope incluye «rutas de lectura contrato WS11». Queda el caso de `shell/api.js`, abajo |
| WS13.1 | 4. Qué comparten foco | Resuelta por §6.1 y H-03, H-03b. No cambia |
| WS13.1 | 5. Clave de selección | Resuelta por §2.2 y §5.3. No cambia |
| WS41 | 1. Soporte y formato de la configuración | **Ajustada**: §3.2 lo deja a WS41 con condiciones |
| WS41 | 2. Disyunción en `local:` | **Ajustada**: §5.2 nombra el desk del documento que contiene el enlace |
| WS41 | 3. Migración y remedio | Resuelta por §5.4. No cambia |

Tester ronda 1, PASS, observación E4/E7: **ajustada**, §7.5 declara E7 como caso de E4. Rangos con línea vecina: no se tocan.

**Para root, no resuelto aquí:** el delta de WS15.1 toca `shell/api.js` (§7.3), y el `output_scope` de WS15.1 es `views/workspace/errors/`, rutas de lectura y tests. `dag.yaml` no se edita en este alcance.
