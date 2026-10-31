REFORMULACION
Propósito: hacer idempotentes manifiesto, RunDoc y cierre sobre el id de intento citado por el cierre, nunca por agente o slug. Resultado: registro canónico por intento con campos mínimos y finalización repetida sin duplicados ni pérdida de identidad/evidencia. Repo dueño: deskops. Límites: `output_scope` acotado a `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`; `promotion: not_authorized`; no ejecutar ni revisar nodos vecinos; los gates pendientes son intencionales.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, bloque WS32.2 y gates.
Cambios previstos: los cuatro paths del `output_scope`; sin ejecución.
Dependencias: WS05, WS12 y WS32.1, más G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.
Validaciones futuras: repetir la finalización con el mismo id de intento; comprobar que no se crean registros nuevos y que manifiesto/RunDoc/closeout coinciden en id de intento, hash de sesión y evidencia; cubrir dos intentos del mismo agente/slug; preflight de TaskDoc antes de promover.

FUTURO
WS32.1 aporta la separación identidad de intento/dispatch; WS05 el inventario; WS12 el contrato de operaciones; WS44 el probe y G_SCION; WS07 designa al operador Scion. El resolver externo de G_CLOSEOUT y la promoción/TaskDoc fijan archivos, pruebas y textos. Nada de eso es ambigüedad de este nodo.
