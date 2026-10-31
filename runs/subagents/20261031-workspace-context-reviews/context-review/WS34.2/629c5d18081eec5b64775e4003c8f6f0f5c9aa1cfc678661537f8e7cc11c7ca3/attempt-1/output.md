REFORMULACION
- Propósito: revisar WS34.2 como encargo de planificación para exponer una respuesta (reply) autorizada y restringida, vinculada al intento.
- Resultado: adaptador público con manejo de timeout/errores y autoridad del coordinador, más pruebas; no se implementa aquí.
- Repo: `deskops`, con `output_scope` en `runtime/; cli/commands/runtime.py o API definida; tests/`.
- Límites: depende de WS33, WS12 y WS34.1; exige G_EXEC, G_SCION y G_WRITE_CONTRACT; prohíbe enviar mensajes en planificación; no autoriza promoción ni ejecución.

AMBIGUEDADES
ninguna.

DRY-RUN
- Lecturas: guía, nodo WS34.2 y contratos vecinos suministrados; sin herramientas ni historial.
- Cambios previstos: ninguno durante esta revisión. La implementación futura tocaría runtime, CLI/API y tests, según el contrato.
- Dependencias: WS33 aporta referencias de mensaje/intento y decisión; WS12 fija canal, autoridad y umbral de timeout; WS34.1 expone dispatch. Gates pendientes: G_EXEC, G_SCION, G_WRITE_CONTRACT.
- Validaciones futuras: comprobar que G_SCION/G_EXEC pasan; un agente real demuestra respuesta vinculada al intento correcto; un timeout se reporta como fallo sin confirmación, usando el umbral de WS12. El TaskDoc de promoción fijará archivos, escenarios y textos dentro de la aceptación.

FUTURO
- WS12 debe producir el contrato de operación, autoridad del coordinador y umbral de timeout.
- WS44 debe producir G_SCION mediante probe real de Scion.
- WS34.1 debe entregar el dispatch con identidad de intento.
- WS33 debe entregar las referencias de mensaje/intento y decisión.
- Un humano debe autorizar G_EXEC y, más adelante, la promoción del nodo.
