REFORMULACION
WS32.1 es un nodo de implementación en deskops que separa la identidad de un intento de su dispatch: genera IDs de intento y materializa el registro local por intento que fija WS12, con los hechos «intent» y «no confirmado» separados del RunDoc. El resultado son cambios en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`. Límites: sin dispatch/reply de red, sin simular respuesta Hub, sin inventar almacenamiento fuera del contrato WS12, sin Markdown ad hoc y sin afirmar éxito/fallo de Hub; la persistencia se prueba con operaciones reales sobre store temporal. Depende de WS05 y WS12 y requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «WS12 especifica contrato/ubicación del registro por intento (input de WS32.2)... WS32.1 materializa ese registro». El reparto entre lo que materializa WS32.1 y el «manifiesto canónico» de WS32.2 queda indefinido; obliga a inventar el límite y el almacenamiento propio de cada nodo.
2. «dispatch intent ... y confirmed ... ambos se registran» frente a «registro intent/no confirmado ... sin ... invocar red». No se fija si WS32.1 implementa el estado confirmado ni con qué identidad; «la identidad que exponga» y «a comprobar en WS05/WS44» no aportan campo ni criterio, y WS44 no está en `depends_on`. Obliga a inventar el esquema o a decidir que queda fuera.
3. «contrato de integración explícito» aparece en la aceptación sin productor, contenido ni comprobación; obliga a inventar si WS32.1 debe redactarlo y qué debe contener.

DRY-RUN
Un ejecutor leería el candidato de drawer, `auditoria/scion.md` (WS05), `contratos/operaciones.md` (WS12), `dag.yaml`, `runtime/scion.py`, `models/run.py`, `closure.py` y tests. Crearía pruebas con store temporal, añadiría generación de IDs y el registro local según WS12, y editaría RunDoc por API/CLI. Consumiría WS05/WS12; G_CLOSEOUT está satisfecho, G_WRITE_CONTRACT pendiente por delta y G_SCION sin verificar. Si falta el contrato de registro, se detendría y registraría el hueco. Validaría dos IDs distintos, registro intent/no confirmado, ausencia de red/Hub y de etiquetas de éxito/fallo, y que no hay Markdown ad hoc. El agregado WS32 cerraría al cumplir WS32.1 y WS32.2.

FUTURO
WS32.2 fija el manifiesto canónico y la idempotencia; WS34/WS37 prueban dispatch real y correlación bajo G_EXEC; WS44 produce G_SCION; WS05 y WS12 aportan inventario y contrato; la promoción fija archivos, pills y evidencia.
