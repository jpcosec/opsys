REFORMULACION
- **Propósito:** hacer idempotente la persistencia local del manifiesto, RunDoc y cierre sobre el id de intento correcto, nunca por agente o slug.
- **Resultado:** una finalización repetida del mismo intento conserva identidad y evidencia sin crear registros nuevos; manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia.
- **Repo:** `deskops`.
- **Límites:** sin dispatch/reply de red ni evento Hub simulado; sin hash fabricado ni hash de proceso/slug. La prueba con Hub y correlación real queda en WS34/37 bajo `G_EXEC`. Sujeto a `G_CLOSEOUT`, `G_SCION` y `G_WRITE_CONTRACT`.

AMBIGUEDADES
Ninguna. El nodo define resultado, aceptación y límites. El hash de sesión queda delegado explícitamente: “inventario WS05 y contrato WS12, con campo/algoritmo digest y fuente exactos declarados allí”, y si falta, “registrar hueco con productor WS12/WS05 y bloquear esa coincidencia antes de promoción”. Eso no obliga a inventar: activa la regla común de hueco. La ubicación/forma del registro por intento corresponde a WS12/WS32.1, y la prueba real de Hub a WS34/37, fuera de este nodo.

DRY-RUN
- **Lecturas previstas:** nodo WS32.2, referencia externa `external_references.scion`, guía, brief, alcance, decisiones, reconciliación y código existente de `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests.
- **Cambios previstos:** manifiesto canónico por intento, identidad persistida, deduplicación local y coherencia con RunDoc/closeout en los archivos de `output_scope`.
- **Dependencias:** WS05, WS12 y WS32.1; gates `G_CLOSEOUT`, `G_SCION`, `G_WRITE_CONTRACT`.
- **Validaciones futuras:** repetir finalización con el mismo id de intento; comprobar ausencia de registros nuevos y coincidencia de id, hash de sesión y evidencia; registrar hueco si no existe artefacto/contrato de hash; verificar que no hay red/dispatch/Hub. Nada ejecutado.

FUTURO
- WS05 produce inventario de sesión/API; WS12 fija contrato, ubicación y digest; WS32.1 materializa registro e identidades; WS44 produce `G_SCION`; WS34/37 prueban Hub real bajo `G_EXEC`.
- La promoción, archivos exactos, pills y preflight quedan a TaskDoc/decisión humana; `G_CLOSEOUT` ya está satisfecho y no se reabre.
