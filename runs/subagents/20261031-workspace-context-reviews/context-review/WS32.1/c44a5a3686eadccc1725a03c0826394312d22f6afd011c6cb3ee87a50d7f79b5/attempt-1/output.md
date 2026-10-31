REFORMULACION

Propósito: separar identidad de intento de slug y registrar `dispatch intent` y `confirmed` como hechos distintos del RunDoc, materializando el registro por intento según el contrato de WS12, sin red. Resultado: cambios y pruebas en `deskops` que demuestren dos IDs distintos y registro `intent/no confirmado` sobre store temporal real; RunDoc editado por API/CLI SLDB. Repo dueño: `deskops`. Límites: no dispatch/reply de red, no evento Hub simulado, no almacenamiento inventado, no Markdown ad hoc; `G_SCION` y `G_WRITE_CONTRACT` siguen pendientes.

AMBIGUEDADES

ninguna.

DRY-RUN

Lecturas previstas: nodo WS32.1 y aristas WS05/WS12/WS32/WS32.2; guía, brief, alcance, decisiones, cobertura, reconciliación y `external_reference.scion`. Sin ejecutar.

Cambios previstos: materializar registro por intento e identidades según contrato WS12; ajustar `models/run.py` con registro/validación SLDB; tocar `runtime/scion.py` y `services/closure.py` solo en lo que el contrato exija; pruebas en `tests/` con store temporal real. No se modifican nodos vecinos.

Dependencias: WS05 aporta inventario de API/identidades; WS12 aporta contrato/ubicación del registro y `G_WRITE_CONTRACT` por delta; `G_SCION` depende de WS44; `G_CLOSEOUT` está satisfecho; WS32.2 consume el registro; WS34/37 probarán dispatch real y correlación. Si falta contrato, regla común: detenerse y registrar hueco con repo dueño.

Validaciones futuras: dos intentos locales generan IDs distintos; persistencia `intent/no confirmado` sin red ni mock Hub; ningún no confirmado se etiqueta como fallo/éxito Hub; RunDoc trackeado se crea/edita por API/CLI, no ad hoc; modelos se registran/validan en SLDB.

FUTURO

WS44 ejecutará el probe de `G_SCION`; WS12 publicará el contrato de operaciones/registro; WS32.2 convertirá el registro en manifiesto canónico; WS34/37 demostrarán dispatch real fallido/confirmado y correlación exacta. La promoción fijará TaskDoc, archivos y pruebas; el receptor P01 emitirá acta por delta y el humano decidirá la aceptación.
