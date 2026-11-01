REFORMULACION
Propósito: separar la identidad de intento de los hechos «dispatch intent» y «confirmed» del RunDoc, y materializar el registro por intento según el contrato de WS12, sin red. Resultado: código y pruebas en deskops que generan dos IDs locales distintos y registran intent/no confirmado con operaciones reales sobre store temporal, sin simular Hub. Repo: deskops. Límites: nada de dispatch/reply de red, evento Hub fingido, etiquetar no confirmado como fallo/aceptado sin evidencia, ni Markdown ad hoc; promoción no autorizada.

AMBIGUEDADES
1. «WS34 (con G_EXEC) y WS37 demostrarán dispatch real fallido/confirmado y correlación exacta al id previo; contrato de integración explícito.» No se dice quién produce ese contrato, dónde vive, qué campos/IDs fija ni si es entregable de WS32.1 o de WS34/37. Obligaría a inventar su contenido, dueño y criterio de aceptación.
2. «dispatch intent ... y confirmed ... ambos se registran en el registro por intento» frente a «registro intent/no confirmado ... sin simular respuesta Hub». No queda definido si `confirmed` debe existir ya en el esquema, con qué representación/valor cuando no hay observación, o si se difiere. Obligaría a inventar el estado y su verificación.

DRY-RUN
Lecturas: nodo WS32.1, candidato de external_references.scion, WS05/WS12, guía/alcance/decisiones y rutas citadas de deskops. Cambios previstos: models/run.py, runtime/scion.py, services/closure.py y tests; registro por intento e IDs locales. Dependencias: WS05, WS12; G_CLOSEOUT satisfecho, G_SCION no verificado, G_WRITE_CONTRACT pendiente per_delta. Validaciones futuras: tests con store temporal, IDs distintos, ausencia de red/Hub simulado, registro/validación SLDB y RunDoc por API/CLI; WS34/37 bajo G_EXEC. Sin ejecutar.

FUTURO
WS05 aporta inventario de identidad/API; WS12, contrato/ubicación del registro; WS44, G_SCION; WS34/WS37, dispatch real y correlación; una persona autoriza promoción y preflight de tarea.
