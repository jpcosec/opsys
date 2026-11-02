# Alineación de WS11, resultado para revisión root final

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Nada ejecutado en runtime. No es aprobación de nadie. Contrato en estado borrador. Ejecución: Supervisor, sin Executor; el Tester no fue autor.

- `contratos/navegacion.md` sha256 `d7d3c749e58536a29134f668e68be07b0d27d67f7b5a8cf4875877d641086005`
- `dag.yaml` sha256 `f303e74e48afae025b227a17c57963075f84a523a026053fc3417640221d946d`
- `patch.diff` sha256 `1e17baf286d2200ecd51a0d32741d4254ca5ae2a178669b916ed64a9f2685c98`, desde `1c9bb628`: contrato, DAG y fichas de WS13, WS15 y WS15.1.

## Las cuatro precisiones

1. Serialización: §3.2.1 y §5.1.
2. Alias canónico: §3.2, Validación (WS41).
3. Actores de preparación: §5.4.
4. `output_scope` de WS15.1 y §7.3. Sin cambio de `depends_on`, `requires` ni aceptación.

## Invalidación medida

`context_review.py status` tras el parche: **WS13, WS15, WS15.1**, «input changed». Coincide con tu simulación, medido, no asumido. Renové esas tres, con disposición en cada attempt. Hashes de input nuevos: `85e49703…`, `96daadfd…`, `6e0504be…`. Solo WS15.1 cambia `contract_sha256`. WS09 se conserva: su input no cambió. Las otras 70 no se reejecutaron. `dag.yaml`, aparte del `output_scope`, cambia solo esos punteros (`dag-diff.txt`).

## Evidencia y sus bytes

| Revisión | Bytes del contrato | Resultado |
|---|---|---|
| Tester completo | `8c4df02e` | PASS, `../20261101-ws11-correccion/renovacion-2/` |
| Tester focal de `§3.2.1` | `b9db651e` | PASS, `../20261101-ws11-correccion/` |
| Tester, 4 puntos y no regresión A-F | `03853809` | PASS, `renovacion-1/`, 34 filas |
| Tester focal de la frase de §7.3 | final | PASS |
| Revisión fresca WS13.1 y WS41 | `03853809` y final | `renovacion-1/contrato-review/`, `contrato-review/` |

**Ningún Tester completo cubre los bytes finales.** La no regresión fue por lectura del diff y de las secciones listadas, no fila a fila. El Tester no ve git y sus hashes son dato mío.

**Recibos.** Los manuales de esta ronda capturan PID, en Tester y revisión fresca. Los manuales de `20261101-ws11-correccion` no: límite declarado, sin rellenar. La primera ronda del Tester focal v3 de esa corrida salió vacía y se descartó.

`status` es vigencia del plan. No prueba que las otras 72 leyeran el contrato. Las obligaciones de ausencia de escrituras y readiness quedan en los consumidores; nada de eso se afirma en runtime.

## Ajuste no pedido

§7.3: la frase del punto 4 decía que WS13.1 «consume»; la revisión fresca mostró que podía leerse como espera. Ahora dice que usa el `request()` vigente, sin modificarlo y sin esperar a WS15.1. Queda dentro del punto 4.

## Para root

**Contradicción abierta, fuera de las cuatro precisiones, no editada.** §3.2 hace validar en WS41 que `root` y `store` existen, y §8.5 con la aceptación de WS41 exigen E-MD3 visible para store ausente. Si la carga rechaza esa entrada, E-MD3 no se alcanza. Corrección propuesta, una frase: una entrada cuyo `root` o `store` no existe no se sirve y la petición da E-MD3, en vez de exigir su existencia en la carga. Decide tú si entra antes de cerrar.
