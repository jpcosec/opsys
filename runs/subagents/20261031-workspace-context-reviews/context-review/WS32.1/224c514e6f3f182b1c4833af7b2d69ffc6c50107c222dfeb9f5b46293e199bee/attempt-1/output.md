## REFORMULACION
WS32.1 materializa en deskops la identidad de intento y separa el «dispatch intent» local del «confirmed» del Hub, refinando el candidato de `external_references.scion` sin segundo pipeline. Resultado esperado: registro por intento e identidades con pruebas locales sobre store temporal; RunDoc editado por API/CLI SLDB. Repo dueño: deskops. Límites: sin dispatch/reply de red, sin evento Hub fingido, sin Markdown ad hoc, sin inventar almacenamiento ni contrato; solo operaciones locales reales.

## AMBIGUEDADES
1. «requires: - G_SCION» frente a «SIN dispatch/reply de red ni evento Hub fingido» y una aceptación que solo exige registro local. G_SCION lo produce WS44 mediante probe real; el nodo prohíbe la actividad que lo satisface y su aceptación no lo usa. Obliga a inventar si se bloquea por G_SCION o se ejecuta ignorándolo.
2. «dispatch intent (...) y confirmed (...) ambos se registran en el registro por intento» frente a «SIN dispatch/reply de red ni evento Hub fingido». Obliga a inventar cómo registrar `confirmed` —campo vacío, estado ausente o no registrarlo— cuando no puede observarse Hub.

## DRY-RUN
Lecturas: `auditoria/scion.md` (WS05), `contratos/operaciones.md` (WS12), candidato de drawer Scion, `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests existentes. Cambios previstos: identidad de intento, campos separados dispatch intent/confirmed y persistencia del registro por intento en `models/run.py`/`runtime/scion.py`; ajuste de `services/closure.py`; tests con store temporal. Dependencias: WS05, WS12, G_CLOSEOUT, G_WRITE_CONTRACT per_delta y G_SCION. Validación: dos IDs distintos antes de dispatch; registro intent/no confirmado; sin red ni Hub simulado; modelo registrado/validado SLDB; RunDoc editado por API/CLI. Error esperado: si falta contrato WS12 o identidad WS05, detener y registrar hueco con dueño; no fabricar `confirmed`.

## FUTURO
WS12 fija contrato/ubicación del registro e identidades; WS05 inventaría API/identidad Scion; WS44 produce G_SCION; WS32.2 convierte el registro en manifiesto canónico idempotente; WS34/WS37 prueban dispatch real y correlación bajo G_EXEC. La designación del operador Scion y la autorización de ejecución son decisiones humanas posteriores.
