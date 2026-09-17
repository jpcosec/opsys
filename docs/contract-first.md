# Contrato primero: docstring, lint y test como entrada

Diagrama: `docs/diagrams/deskops-pron-contract-first.yml`.

## La inversión

Hoy, en deskops y en casi todo el ecosistema:

```
implementar  →  (a veces) docstring  →  (a veces) test  →  lint al final
```

Resultado medido en deskops: **75 de 624 símbolos con docstring (12%)**.

El flujo correcto:

```
planificar  →  contrato (docstring + lint + test)  →  gate  →  implementar
```

El docstring no es documentación de lo que hiciste. Es **la especificación de
lo que vas a hacer**, escrita cuando todavía es barata.

## El argumento

No hay ninguna razón para no escribir un docstring antes de implementar. Si el
planificador no puede escribir qué hace un símbolo y por qué existe, entonces
no entendió el cambio — y eso es exactamente lo que el gate debe atajar, no la
revisión de código tres horas después.

Lo mismo aplica a lint y test:

- **lint**: las reglas que aplican al símbolo (complejidad, largo de función)
  se conocen antes de escribirlo. Declararlas después es negociar con el
  resultado.
- **test**: `test_plan` describe los casos, no el código de test. Escribir los
  casos antes es diseño; escribirlos después es justificación.

## `SymbolContractDoc`

Contenido dentro de `PlanTargetDoc`. Un contrato por símbolo a tocar:

| campo | qué es |
|---|---|
| `qualname`, `kind` | a qué símbolo |
| `signature` | la firma esperada, antes de existir |
| `docstring` | **obligatorio** — qué hace y por qué existe |
| `purpose`, `architecture` | los campos autorales de `PythonSymbolDoc` |
| `invariants` | qué debe seguir siendo cierto |
| `lint_rules` | reglas que aplican |
| `test_plan` | los casos, antes de escribirlos |
| `test_qualname` | dónde va a vivir el test |

## Las guardas

La inversión no es una buena intención: es una condición de transición.

```yaml
planning → execution
  condition: "{plan_targets_without_contract} == 0"

execution → testing
  condition: "{contracts_implemented} == {contracts_declared}"

testing → closeout
  condition: "{tests_from_contracts_passing} == true"

testing → planning          # ← no vuelve a execution
  condition: ""
```

La última importa: una regresión vuelve a **planning**, no a execution. Si el
código falló, el contrato estaba mal — y se corrige donde se escribió.

## Por qué esto cierra el ciclo con sldb

`sldb selfdoc python-check` ya existe y reporta deriva entre el código y su
documentación trackeada. Con contratos:

1. El contrato declara `docstring`, `purpose`, `architecture`.
2. El ejecutor implementa; el docstring real nace del contrato.
3. `python-check` compara el símbolo real contra su documento trackeado.
4. La deriva es un hallazgo del gate, no una tarea de limpieza futura.

Hoy `sldb` inicializa esos campos en `"Not documented."`. Eso es la deuda
medida y visible; el contrato es el mecanismo para que no crezca.

## Y cierra el ciclo con los tests

`test_plan` y `test_qualname` del contrato, más `TestCoverageDoc` derivado de
los imports declarados, dan el set de tests a correr:

- **del contrato**: los tests que esta task prometió escribir;
- **derivados**: los tests existentes que tocan los símbolos afectados.

Ninguno de los dos requiere ejecutar la suite completa para saber qué correr.

## Flujo completo

```
Supervisor suelta al Planificador
  └─ sldb explore --source docstrings   (qué ya existe)
  └─ PlanTargetDoc                      (qué tocar)
      └─ SymbolContractDoc              (docstring + lint + test, ANTES)
          └─ [gate: sin contrato no hay execution]
              └─ Ejecutor implementa contra el contrato
                  └─ sldb selfdoc python-check  (deriva)
                      └─ verde, o vuelve a planning con PlanIterationDoc
```
