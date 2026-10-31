## REFORMULACION

**Propósito:** revisar WS34.2 como encargo de planificación: adaptador público restringido para `reply` vinculado al intento, con timeout/errores y autoridad del coordinador.

**Resultado:** dictamen de inteligibilidad del nodo; no se implementa ni se ejecuta nada.

**Repo dueño:** `deskops`. Salidas previstas: `runtime/`; `cli/commands/runtime.py` o API definida; `tests/`.

**Límites:** no revisar los bloques edge de los vecinos; no resolver Pxx ni dar por aprobadas propuestas; los gates pendientes son intencionales; WS34.2 es candidata y no tiene ejecución autorizada; la promoción exige preflight y evidencia específica.

## AMBIGUEDADES

Ninguna.

La identidad del intento remite a WS33; la autoridad del coordinador y la whitelist, a WS12/G_WRITE_CONTRACT; la API pública, a G_SCION/WS44; y la aceptación es comprobable mediante agente real. El timeout y los errores quedan como detalle de implementación, no como resultado indefinido.

## DRY-RUN

**Lecturas:** input completo —guía, brief, alcance, decisiones, cobertura, nodo WS34.2, bloques de WS33/WS12/WS34.1/WS34 y gates—.

**Cambios previstos:** ninguno; solo revisión.

**Dependencias:** WS33 aporta referencias de mensaje/intento; WS12 aporta contrato de operaciones y policy del coordinador; WS34.1 aporta dispatch. Gates: G_EXEC, G_SCION y G_WRITE_CONTRACT.

**Validaciones futuras:** G_SCION mediante probe de WS44; G_EXEC mediante autorización humana externa; G_WRITE_CONTRACT mediante WS12. La aceptación requerirá que un agente real demuestre una respuesta vinculada al intento correcto, sin mensajes durante planificación.

## FUTURO

- WS44 produce el probe público de Scion y G_SCION.
- WS12 produce la whitelist y la política concreta del coordinador.
- WS07 registra designaciones y resoluciones humanas de Pxx.
- Un humano autoriza G_EXEC y, más adelante, la promoción del nodo.
- WS34, como agregado, cierra cuando WS34.1 y WS34.2 cumplan su aceptación.
