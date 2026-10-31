REFORMULACION  
Propósito: separar identidad de intento de slug/agente y registrar `dispatch intent` y `confirmed` como hechos distintos, sin segundo pipeline. Resultado: implementación en `deskops` que genera ids de intento antes del dispatch, conserva identidades distintas ante dos intentos y un fallo, y deja evidencia en tests. Repo dueño: `deskops`; `output_scope`: `runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`. Límites: nodo candidato, promoción no autorizada; no ejecutar; gates `G_SCION` y `G_WRITE_CONTRACT` pendientes; si falta contrato, detenerse y registrar hueco, sin sustituto.

AMBIGUEDADES  
1. «ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico». No se define qué registro es, dónde vive, su esquema ni si WS32.1 lo crea o ya existe. Como WS32.2 depende de WS32.1, no puede aportarlo antes; el ejecutor tendría que inventar almacenamiento, formato y responsabilidad.  
2. «cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc». No queda claro si “cambios de RunDoc” cubre solo datos runtime o también el código/modelo, aunque `output_scope` incluye `models/run.py`; el ejecutor debe decidir el límite entre cambio permitido y “edición ad hoc”.

DRY-RUN  
Lecturas: nodo y vecinos en `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`; al promover, código real de `deskops` y contratos WS05/WS12. Cambios previstos: generación de ids de intento antes del dispatch; registro separado de intención y confirmación; pruebas de dos intentos y dispatch fallido. Dependencias: WS05, WS12; `G_CLOSEOUT` satisfecho; `G_SCION` sin verificar; `G_WRITE_CONTRACT` pendiente. Validaciones futuras: tests focalizados de identidad y fallo, sin contacto vivo con Scion hasta WS44; preflight de TaskDoc y archivos exactos.

FUTURO  
WS32.2 produce manifiesto canónico e idempotencia; WS44 produce el probe y `G_SCION`; WS12 produce `G_WRITE_CONTRACT`; WS06 integra el delta en ticket receptor. La promoción y el TaskDoc los decide un humano; este nodo no autoriza ejecución.
