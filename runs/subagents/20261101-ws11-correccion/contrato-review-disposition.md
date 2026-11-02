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

# Ronda 2

Evidencia en `renovacion-2/contrato-review/`, sobre sha256 `8c4df02e…`. Tester ronda 2 PASS sobre esos bytes, copia en `renovacion-2/`.

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS13.1 | 1. `repo` de la identidad sin configuración | **Ajustada**, §3.2.1. Marcada por los dos consumidores por separado |
| WS41 | 1. Alias del desk del proceso | **Ajustada**, misma frase |
| WS13.1 | 2. Línea Code frente a C12 | Resuelta por C11a, C12 y §6.1. No cambia |
| WS13.1 | 3. F17 «bloqueado» frente a «soportadas» | El estado de F17 espera a WS11 y WS13.1; §6.1 fija qué se soporta. No cambia |
| WS13.1 | 4. Procedencia de arista en el panel | Resuelta por §6.1, punto 4. No cambia |
| WS41 | 2. Quién implementa volver | H-12: WS41 conserva el alias; historia en WS13.3. WS41 depende de WS13. No cambia |
| WS41 | 3. `output_scope` con `source/` | Ver abajo |

**La frase de §3.2.1 es decisión del Supervisor**, derivada de la resolución root de `local` (`review-source-2.md`). Root la revisa.

**Para root:** el `output_scope` de WS41 nombra `frontends/mindmap/source/`. Ver el estado de esa carpeta en `freeze-final.md`. `dag.yaml` no se edita en este alcance.

Parada: acepto las demás ambigüedades como futuras o ya respondidas. Una revisión fresca sin historial siempre encuentra más; no se itera hasta vaciarla.

# Ronda 3, contrato final

Evidencia en `contrato-review/`, sobre el contrato final. Ninguna cambia el contrato; regla de parada de la ronda 2.

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS13.1 | 1. Dos mecanismos de «mismo origen» | Implementación de WS13.1; el contrato fija lo observable |
| WS13.1 | 2. Recibo frente a aceptación | §12 y H-03: el delta es de WS13.1, el recibo es de P01 |
| WS13.1 | 3. Criterio de reutilización `model=None` | Se verifica al implementar; si falla, hueco de C5b |
| WS13.1 | 4. De dónde sale `local` | Falsa: es reservado, no se configura |
| WS41 | 1. Códigos HTTP de E-MD1 a E-MD4 | §8.5 lo deja a WS41 |
| WS41 | 2. ¿Otro alias para el desk del proceso? | §3.2.1: sí, el de la configuración si el operador lo incluyó |
| WS41 | 3. Qué se compara | §5.4 fija archivos y versión; el medio es del consumidor |
| WS41 | 4. Quién prepara los stores | **Sin dueño nombrado**: §5.4 dice «fuera del request». Queda como límite para root |
