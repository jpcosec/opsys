## REFORMULACION

**Propósito:** integrar en la UI de `graph_ui` las operaciones de conocimiento ya existentes —atoms split/merge y proto typing— y la inspección/validación de materializaciones, con confirmación humana que muestre origen y efecto.

**Resultado:** escenarios UF03 operables con persistencia, referencias y conflictos reales; materializaciones validadas contra `MaterializationContractDoc` mediante API pública SLDB; capacidades no soportadas declaradas no disponibles, sin simulación.

**Repo dueño:** `graph_ui`.

**Límites:** no crear destinos arbitrarios ni renderer propio de validación; endpoints solo según whitelist WS12; no implementar contratos faltantes; no habilitar mutaciones UI sin `G_HUMAN_READ`; el nodo no se ejecuta hasta su promoción.

## AMBIGUEDADES

Ninguna.

Las condiciones de contrato faltante están cubiertas: WS12 registra productor/hueco y la UI queda no disponible; además, `alcance.md` fija la regla común de detenerse y registrar el hueco. La selección del store, archivos, escenarios y textos queda delegada al TaskDoc de promoción, lo que la guía excluye como ambigüedad.

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS42 y contratos vecinos WS19/WS24/WS12/WS30, más gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`.

**Cambios previstos:** implementación en `frontends/mindmap/views/workspace/knowledge/`; endpoints limitados a la whitelist WS12; pruebas en `tests/`. Sin cambios fuera del `output_scope`.

**Dependencias:** WS19 aporta edición/conflictos; WS24, vista de grafo y documento genérica; WS12, whitelist, contrato de operaciones y huecos. Gates pendientes por delta.

**Validaciones futuras:** probar split/merge/typing contra API real; validar materializaciones contra el modelo SLDB en store temporal de TaskDoc o corpus Taller WS40; recorridos UF03; acta humana WS30; recibos `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta.

## FUTURO

- **WS12:** publica whitelist/contrato o registra productor y hueco.
- **TaskDoc de promoción:** fija archivos, store, escenarios y textos.
- **WS40:** aporta corpus/Taller.
- **WS16:** produce acta de `G_HUMAN_READ`.
- **Receptor P01:** emite acta `G_UI_WRITE` del delta concreto.
- **WS30:** ejecuta validación humana y registra resultado.
- **Supervisor receptor:** decide diagnóstico si el fallo no está aislado.
