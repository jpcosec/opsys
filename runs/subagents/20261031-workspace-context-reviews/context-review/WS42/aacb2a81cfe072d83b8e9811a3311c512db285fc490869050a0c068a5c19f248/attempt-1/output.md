## REFORMULACION

**Propósito:** integrar en el workspace de graph_ui las operaciones de conocimiento ya existentes —split/merge de atoms y proto typing— y la inspección/validación de materializaciones, con confirmación humana que muestre origen y efecto.

**Resultado:** UI y llamadas reales en `frontends/mindmap/views/workspace/knowledge/`, endpoints ceñidos a la whitelist WS12 y pruebas en `tests/`; aceptación UF03 con persistencia, referencias y conflictos reales.

**Repo:** `graph_ui`.

**Límites:** no generar destinos arbitrarios ni renderer propio para materializaciones; no simular capabilities ausentes (se declaran no disponibles y bloquean solo su escenario UF03); no crear operaciones que falten (WS12 registra productor/hueco); mutaciones UI sujetas a G_HUMAN_READ y a recibos por delta; promoción no autorizada.

## AMBIGUEDADES

1. «validar por API pública SLDB contra ese modelo, no renderer propio». No se nombra qué API pública de SLDB realiza la validación, quién la produce si no existe, ni qué criterio convierte una materialización en inválida (esquema, referencias, versión). El "si faltan, WS12 registra productor/hueco" está escrito solo para split/merge/proto typing. Obligaría al ejecutor a inventar el mecanismo, el criterio o el productor de validación.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo y aristas ya suministradas), brief, alcance, decisiones, cobertura y guía; en ejecución futura, contrato WS12 y corpus/manifiesto WS40.

**Cambios previstos:** componentes de conocimiento en el `output_scope`, invocaciones a endpoints de la whitelist, pruebas en `tests/`. Sin escritura ahora.

**Dependencias:** WS19, WS24, WS12; gates G_HUMAN_READ, G_UI_WRITE (per_delta para WS42), G_WRITE_CONTRACT (per_delta).

**Validaciones futuras:** acta humana de lectura WS16; recibo del receptor P01 para G_UI_WRITE; contrato/efecto WS12; validación manual WS30 sobre corpus WS40.

## FUTURO

- WS12 publica whitelist, contrato de efectos y huecos asignados.
- WS16 produce el acta de lectura que habilita mutaciones UI.
- El receptor P01 emite, al preparar este delta, el acta de G_UI_WRITE.
- WS45 fija/verifica la precondición de escritura de payload.
- WS40 aporta corpus y manifiesto Taller.
- WS30 ejecuta la validación humana y, si falla, atribuye el nodo causante.
- La promoción (archivos, TaskDoc, preflight) queda a decisión humana posterior.
