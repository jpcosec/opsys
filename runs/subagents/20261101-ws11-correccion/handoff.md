# Corrección de WS11, resultado para revisión root final

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Nada ejecutado en runtime. No es aprobación de nadie. Contrato en estado borrador.

- `contratos/navegacion.md` sha256 `b9db651ec15acbe5df0b6a8a08ce7082ca846ab7f31e1f7036619e1a7b58c789`
- `borradores/vistas.md` sha256 `9772e00ea24602681e9e01fda4e05de61df63574ce0342cb8b822ffca099bc24`, sin cambios desde `b4968374`
- `patch-final.diff` sha256 `a55c4f4070e3e76290995a893bd58a3f23fb06b38cc262f9f2d56f39d54fa51c`, `65f76c46` a `76b77f5d`, dos rutas
- WS09: input `a3adf4d1…`, disposición en su attempt-1. Es la única entrada renovada: `dag.yaml` cambia solo su puntero.

## Lo aplicado desde `b4968374`

Tus dos ajustes y tus cinco resoluciones: §5.2 paso 3 y tabla de ejemplos; §3.2 `local`; §8.5 E-MD1; C5b; H-11. `vistas.md` no se tocó.

Además, por la comparación, cuatro frases mías que no pediste:

1. §5.2: `local:` designa el desk del documento que contiene el enlace, que es el de la petición.
2. §3.2: soporte, formato y carga de la configuración son de WS41, sin valores reales en repo ni corpus.
3. §7.5: E7 es el caso de E4 sobre el propio documento.
4. §3.2.1: sin alias configurado, el desk del proceso usa `local`. **Es decisión mía**, derivada de tu resolución de `local`; revísala. La marcaron WS13.1 y WS41 por separado.

## Evidencia

| Revisión | Bytes | Resultado |
|---|---|---|
| Tester completo A-F, decisiones y puntos | `7d6e234a` | PASS, `renovacion-1/` |
| Tester completo, repetido | `8c4df02e` | PASS, `renovacion-2/` |
| Tester focal de la frase de §3.2.1 | final | Primera corrida: salida vacía con exit 0, descartada, `renovacion-3/`. Segunda: PASS |
| Revisión fresca WS13.1 y WS41 | 3 rondas, la última sobre el final | `contrato-review/`, disposición en `contrato-review-disposition.md` |

**El último Tester completo no cubre la frase final**; esa la cubre solo el focal. El Tester es pi deepseek-flash, sin shell: no vio git ni hashes, y algunos de sus números de línea son aproximados. No reverifiqué cada fila de sus tablas.

`status` da todas vigentes: eso es la revisión del plan. Los bundles no incluyen este contrato y no certifica nada sobre él. Fuera de WS09, las otras 72 no leyeron el contrato. Los consumidores futuros deben traerlo enlazado.

## Límites y puntos para root

1. `output_scope` de WS15.1 no incluye `shell/api.js`, donde §7.3 pone su delta. `dag.yaml` no se editó.
2. §5.4 exige stores preparados fuera del request y no nombra quién los prepara.
3. El `output_scope` de WS41 nombra `frontends/mindmap/source/`: la carpeta existe, así que no hay problema.
4. Ambigüedades restantes de la ronda 3: de implementación, sin cambio. Paré ahí a propósito.
5. La comprobación de cero escritura y el `local:` están solo por lectura.
