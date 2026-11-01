REFORMULACION

WS34.2 es un encargo de implementación para exponer un adaptador público restringido de reply, vinculado al intento, con timeout/errores y autoridad del coordinador. Resultado previsto: adaptador y pruebas en el repo `deskops`, sujetos a `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT`. Salidas: `runtime/; cli/commands/runtime.py o API definida; tests/`. Límites: no mandar mensajes en planificación, no ejecutar aquí, promoción no autorizada y, si falta contrato/API/dato, detenerse y registrar hueco sin inventar sustituto.

AMBIGUEDADES

ninguna.

El umbral de timeout y la autoridad del coordinador se remiten al contrato WS12; las referencias de mensaje/intento a WS33; la superficie exacta y los archivos al contrato y a la promoción. Son dependencias con productor identificado, no ambigüedades.

DRY-RUN

Lecturas: nodo WS34.2 en `dag.yaml`, guía, brief, alcance, decisiones, cobertura y bloques vecinos aportados. No se ejecuta nada.

Cambios previstos: implementar el adaptador de reply y sus pruebas en `deskops`, por el canal CLI/API que fije WS12, solo tras promoción autorizada.

Dependencias: WS33 aporta referencias de mensaje/intento; WS12 aporta operaciones, autoridad del coordinador y umbral de timeout; WS34.1 es prerrequisito de hermano. Gates: `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`.

Validaciones futuras: agente real demuestra reply vinculado al intento correcto y timeout reportado como fallo sin confirmación, usando el umbral de WS12. La promoción fijará archivos, pills, TaskDoc y preflight.

FUTURO

WS12 produce el contrato de operaciones, la política del coordinador y el umbral de timeout. WS33 produce referencias de mensaje/intento, deduplicación y procedencia. WS44 y el operador designado resuelven `G_SCION`; un humano/designee resuelve `G_EXEC`. La promoción decide archivos exactos y pruebas. Nada de ello se ejecuta en esta revisión.
