## Separación de fuentes

**LECTURA PROPIA** (abiertos en esta sesión): `runs/subagents/20261102-ws12-correccion/patch-3.diff`; `desk/drawer/plans/workspace-documental/contratos/operaciones.md`; `.../dag.yaml`; ronda previa `renovacion-4/tester-result-summary.md`.

**DATO DEL SUPERVISOR** (`tester-p3-facts.log`): HEAD `2d4bbf20`, sha256 `operaciones.md` `5ea0f7b6…52c02`, `dag.yaml` `e4d8b77…4856f`. No aporta hallazgos. No recalculo hashes: solo leo.

## Tabla

| Objeto | Evidencia real | Resultado |
|---|---|---|
| 1) Alcance del diff: solo los tres FAIL | `patch-3.diff`: 3 hunks; hunk 1 W01, hunk 2 fila PillDoc, hunk 3 `hierarchy`. Sin otros cambios | PASS |
| FAIL 1 resuelto: W01 ya no atribuye la comprobación a WS26.1 | `operaciones.md:95`: «Quien invoque la API (graph_ui, **WS26.2**) debe comprobar… antes de crear» | PASS |
| FAIL 2 resuelto: pills ya no atribuidas a WS26.1 | `operaciones.md:230`: «WS26.1 solo **prepara** pills en el candidato; WS26.2 las vincula sobre la tarea activa» | PASS |
| FAIL 3 resuelto: enumeración del gate incluye WS26.1 | `dag.yaml:3367`: «WS21 y **WS26.1** (la arista WS12 y el gate se suman…)»; WS26.2 hereda por `dag.yaml:3369` (`WS26.1→WS26.2`) y `dag.yaml:1852` | PASS |
| Línea 7 excluida como historia de Rev 9 | `dag.yaml:7` («consumido por WS19, WS19.1, WS19.2 y WS21») no computada, según instrucción | PASS |
| Q3: ¿otra frase donde WS26.1 cree tarea activa/invoque W01? | Ninguna. Las 17 apariciones de «WS26.1» en contrato: `operaciones.md:54,224,230,250,267,270,271,365,392,438,621,622,642,681,682,702,760`; todas lo sitúan en preparación de candidato. En DAG: `dag.yaml:1795-1806` (scope: «No crea la tarea activa… la creación… es de WS26.2»), `dag.yaml:1865-1867` («nunca… efecto oculto de WS26.1»), `dag.yaml:3095` | PASS |
| Q3: ¿otra frase que lo haga vincular con `bind`? | Ninguna con WS26.1. `dag.yaml:1771` («contexto/pill binding») está en `scope` del WS26 **agregado**, no de WS26.1; `operaciones.md:225` asigna `bind` a tarea activa (WS26.2) | PASS |
| Q3: ¿otra enumeración que lo omita como consumidor de `G_PAYLOAD_PRECONDITION`? | `dag.yaml:1807` (`requires`), `dag.yaml:3367` (jerarquía), `operaciones.md:54` («y WS26.1 en la propuesta»), `operaciones.md:270` y `:621` lo incluyen. Única omisión restante: `dag.yaml:7`, excluida por instrucción | PASS |

## Cobertura

Leído el diff completo; `operaciones.md` en §1.5, §2.3 (W01–W05), §3.2–3.3, §5.7–5.9, §6, §9.3, §10.2 y §12; `dag.yaml` en gates, WS26/26.1/26.2, WS48 y `hierarchy`. No se leyeron las 3521 líneas completas ni se ejecutó código; las filas PASS previas sobre otros bytes no se reutilizan.

RESULTADO: PASS
