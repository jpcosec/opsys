# Corrección de WS12, checkpoint final

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Nada ejecutado en runtime. No es aprobación de nadie. Sin closeout de tarea ni fase. `G_WRITE_CONTRACT` sigue pendiente. Contrato en borrador. Sin push.

- `contratos/operaciones.md` sha256 `754546d60c5ec47b369c8a8b3d47124615659481403939855bb1ff76b4ce9f39`
- `dag.yaml` revisión 10 sha256 `4362aebf4259987b249b4857be6a2d4f4f355d7af1266a74e60a93e8cddb5a64`, `status: final_plan_reviewed`
- Diffs desde `2da226ed`: `patch-desde-congelado-contrato.diff` `9145689bc2c2f148ffeabae9a6c47f8e9ecd7bd8d44a95e6cddb4736424c3786`; `patch-desde-congelado-dag.diff` `18a2fe2bdbcfb7d644fe1106bf86f63b96bbfff003c84642d0d09b91f320e2f3`.

## Checks (`final-validation.log`)

`build --check`, `validate --check`, `status` «all reviews current», 13 pruebas del helper. **Vigencia del plan, no del contrato:** ningún bundle lo contiene.

## Renovación medida

38 nodos: 35 cambiados y WS46, WS47, WS48, sin fallos técnicos, con disposición en cada attempt. Los otros 38 de los 76 no se reejecutaron. Los intentos anteriores se conservan como historia.

## Cambios tras tu última decisión

Aplicadas tus decisiones 1-5 con §4.4 nuevo. Todo declarado en `result-summary.md`.

Añadidos por mí, por lo que salió en las revisiones:

1. §4.4: `show task`, lectura pública, en la comprobación del selector.
2. §4.4: consulta de rastreo con `doc_status`; si falla, recorrido B.
3. WS48: causas del rechazo explícitas, «a las <hora>», y formato de F1 fijado por WS48.
4. WS26.1: título autorable, evidencia pendiente con tu texto.
5. WS47: piso de detección con `_write_doc`, que no se rebaja y solo se amplía si el inventario lo justifica. **Es la frase con más juicio mío: revísala.**

## Evidencia por bytes

| Revisión | Bytes | Resultado |
|---|---|---|
| Tester de decisiones 1-5 | contrato `b96b909d`, dag `3e68ae20` | PASS, `renovacion-6/` |
| Tester, consulta de rastreo | contrato final | PASS, `renovacion-7/` |
| Tester, nodos WS48 y WS26.1 | dag `dd52c84c` | PASS, `renovacion-8/` |
| Tester, F1 y piso | dag `fd09f584` | FAIL, antecedente roto, `renovacion-9/` |
| Tester, frase WS47 | dag roto `a8d39a19` | FAIL, `renovacion-10/` |
| Tester, frase WS47 | dag `47d8c58a` | PASS, `renovacion-11/` |
| Tester, contradicción WS47 | dag `d7089964` | PASS, en este run |

El último cambio de `dag.yaml` tras esos Testers solo registra punteros y `status`. Cobertura incremental: ningún Tester único recorre todo sobre bytes finales y no se certifican las 65 filas. Sin runtime.

**Fallo mío:** un «:» en un escalar rompió `dag.yaml` y lo commiteé (`2fcc22da`). Ninguna revisión lo usó: el helper falló y el Tester lo detectó. Corregido en `5a5c03a5`.

## Disposiciones

Revisiones de contrato: `contrato-review-disposition.md`, las tres rondas finales sobre bytes finales. Helper: `disposition.md` en cada attempt. Leí la sección de ambigüedades de todos y las salidas completas de ocho nodos en una ronda anterior; no de los 38. Sin contradicción sin resolver.

**Límite:** muchas dudas del helper las resuelve `operaciones.md`, que no está en sus bundles. Los futuros preflight deben traerlo enlazado.

## Para root

1. Base `a1b2b22` de WS19.1: las revisiones la cuestionan en cada ronda. Texto previo, no tocado.
2. WS26.1: el recorrido B no usa WS47 ni WS48 pero el nodo depende de ambos. Lo dejé así: es un nodo.
3. WS21 frente a C-15 por `read_only`: sin efecto con P04, no tocado.
4. WS47 y el gap de `update_target` tocan código vecino: si sldb lo repara, van en serie.
