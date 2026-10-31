REFORMULACION
- **Propósito:** agrupar la unificación de identidad de intento y cierre Scion, refinando el ticket existente de `external_references.scion` sin abrir un segundo pipeline.
- **Resultado:** nodo agregado no ejecutable; su salida es la de WS32.1 y WS32.2.
- **Repo dueño:** `deskops` (`output_base: deskops:repository_root/`).
- **Límites:** no se ejecuta ni autoriza promoción; `overlap_with: scion`; `integration_mode: delta_or_existing_ticket` y `never_parallel_duplicate`; depende de WS05, WS12 y sus hijos; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
Ninguna. La referencia a “external_references.scion” no obliga a inventar: el resultado y la aceptación quedan definidos por WS32.1/WS32.2, y el nodo es agregado. Los gates pendientes son intencionales.

DRY-RUN
- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación y fragmentos de `dag.yaml`.
- **Cambios previstos:** ninguno propio de WS32; solo agregación. WS32.1/WS32.2 tocan `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`.
- **Dependencias:** inventario WS05, contrato WS12, hijos WS32.1/WS32.2; gates G_CLOSEOUT (externo), G_SCION (WS44) y G_WRITE_CONTRACT (WS12).
- **Validaciones futuras:** aceptación de cada hijo, evidencia de gates y no duplicación del pipeline Scion.

FUTURO
- WS44 produce el probe de G_SCION; WS12 produce G_WRITE_CONTRACT; el closeout externo produce G_CLOSEOUT; WS07 designa al operador Scion.
- Un humano debe autorizar la promoción; WS33 y dependientes esperan el cierre de WS32.
