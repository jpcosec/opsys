# Disposición de la revisión fresca del contrato de operaciones

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Revisores pi deepseek-flash sin herramientas, SYSTEM v2 del helper, leído y no modificado. Input: contrato completo, proyección YAML de los nodos, filas de decisiones. No son Testers.

## Ronda 1, `renovacion-6/contrato-review/`, contrato `b96b909d`

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS19.1 | 1. Filtro de protegidos | HO-02 lo asigna a WS19.1. «Sin cambios de contrato» es sobre los endpoints. Sin cambio |
| WS19.1 | 2. Base `a1b2b22` | Es la del nodo; lo excluido es `frontends/workspace/`. Sin cambio |
| WS19.1 | 3. Representación | Resuelta en §6.3 |
| WS25.2 | 1. Forma del origen | §7.2 propuesta; WS46 la prueba. Sin cambio |
| WS25.2 | 2. Endpoints | HO-01: implementación del consumidor. Sin cambio |
| WS25.2 | 3. Semántica de colisión | WS46. Sin cambio |
| WS26.1 | 1. Cómo saber si está rastreado | **Real. Ajustada** en §4.4: `doc_status` |
| WS26.1 | 2. Endpoints | HO-01. Sin cambio |
| WS26.1 | 3. Reglas de navegación | Faltaba en el input: se añade `navegacion.md` §3 a la ronda 2 |

La atribución de implementación coincide con los nodos: `G_WRITE_CONTRACT` a root, recibos a P01, capacidades a WS45-48.

## Ronda 2, `contrato-review/`, contrato final

Con `navegacion.md` §3 en el input de WS26.1. Sin cambio de contrato: parada aquí, ninguna es contradicción.

| Consumidor | Ambigüedad | Disposición |
|---|---|---|
| WS19.1 | 1, 2, 5. Base `a1b2b22` | Texto del nodo; la exclusión es `frontends/workspace/` sin commit. Aparece en dos rondas: anotado para root |
| WS19.1 | 3. Filtro HO-02 | Asignado a WS19.1 |
| WS19.1 | 4. Forma de error | HO-01 |
| WS25.2 | 1. Rutas | HO-01 |
| WS25.2 | 2. Forma del origen | §7.2, WS46 |
| WS25.2 | 3. Colisión | WS46, que el nodo exige |
| WS25.2 | 4. Origen mensaje en drawer | WS46 prueba origen ruta y mensaje sin `promote`, que no está aprobado |
| WS26.1 | 1. Rutas y error | HO-01 |
| WS26.1 | 2. Comprobación fallida | §4.4: sin comando, entrega al responsable |
| WS26.1 | 3. Evidencia vacía | Decisión root: el candidato puede conservarla como pendiente |

Ninguna atribuye implementación a otro nodo. WS19.1 no asume `shell/api.js` ni WS47.
