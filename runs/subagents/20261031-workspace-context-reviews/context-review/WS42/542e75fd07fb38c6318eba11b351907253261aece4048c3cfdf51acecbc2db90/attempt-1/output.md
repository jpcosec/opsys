REFORMULACION
Propósito: integrar en graph_ui las operaciones de conocimiento ya inventariadas —split/merge de atoms y proto typing— mediante contratos públicos, con confirmación humana que muestre origen y efecto, y validar materializaciones existentes contra `MaterializationContractDoc`. Resultado: operaciones en `knowledge/` que persisten, muestran referencias y conflictos, marcan materializaciones inválidas y declaran no disponible lo no soportado. Repo: graph_ui; salidas en `frontends/mindmap/views/workspace/knowledge/` y `tests/`, endpoints solo de la whitelist WS12. Límites: no crear destinos arbitrarios, no renderer propio de validación, no simular; si faltan contratos/API, WS12 registra productor/hueco y la UI no queda disponible. G_HUMAN_READ habilita el uso de mutaciones, no el desarrollo ni pruebas aisladas. Nodo de entrega, no agregado.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: contrato/whitelist WS12, salidas de WS19 (edición/conflicto), WS24 (vista de grafo/registry), módulo de admisión WS48, inventarios WS02/WS03 vía WS12, `MaterializationContractDoc` y store temporal/WS40. Cambios: en `knowledge/`, invocar split/merge/proto typing por el canal público; mostrar origen/efecto y pedir confirmación; consultar WS48 antes de mutar; inspeccionar materializaciones existentes y validarlas por API pública SLDB; marcar inválidas/no disponibles; pruebas en `tests/`. Dependencias/gates: consumir WS12, WS19, WS24 y WS48; G_HUMAN_READ antes de habilitar uso; G_UI_WRITE y G_WRITE_CONTRACT por delta, con recibo del nodo/efecto concreto. Errores: si falta contrato/API, detenerse y registrar hueco con dueño, sin sustituto; conflicto visible; materialización inválida no operable. Validación: tests con store real temporal; WS30 recorre UF03 y registra acta; G_HUMAN_READ (WS16) y actas P01 por delta.

FUTURO
WS12 publica whitelist/contrato; WS19/24/48 entregan sus integraciones; WS16 produce G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; WS30 ejecuta la validación humana; el TaskDoc de promoción fija archivos, textos y pruebas.
