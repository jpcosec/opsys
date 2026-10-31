# REFORMULACION

- **Propósito:** nodo agregado que agrupa la exposición de un adaptador público restringido para dispatch y reply de Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.
- **Resultado:** agregado no ejecutable; se cierra cuando WS34.1 y WS34.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS34.
- **Repo dueño:** `deskops`, con `output_base: deskops:repository_root/` y salidas agregadas de sus hijos.
- **Límites:** adaptador público restringido; no shell arbitrario ni duplicación de transporte; autoridad del coordinador según contrato WS12; gates G_EXEC, G_SCION y G_WRITE_CONTRACT.

# AMBIGUEDADES

Ninguna.

El nodo es agregado y su aceptación declara explícitamente que no es ejecutable, en línea con la guía. El repo, los hijos, las dependencias y los gates están identificados. La autoridad del coordinador remite a WS12, que la produce, y el comportamiento ante contrato ausente lo cubre alcance.md ("detenerse, registrar el hueco... no crear sustituto"). Las decisiones Pxx pendientes no se interpretan como aprobadas.

# DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS34, WS34.1, WS34.2), guía de revisión, brief, alcance, decisiones y cobertura.
- **Cambios previstos:** ninguno propio por ser agregado; no se ejecuta. Los hijos apuntan a `runtime/`, `cli/commands/runtime.py` o API definida, y `tests/`.
- **Dependencias:** WS33 (mensajes/resultados/decisiones), WS12 (contrato y G_WRITE_CONTRACT), WS34.1 y WS34.2; transitivas WS32, WS11, WS08 y WS44/G_SCION.
- **Validaciones futuras:** aceptación de cada hijo, paso de G_SCION/G_EXEC/G_WRITE_CONTRACT, prueba con agente real para dispatch aceptado y rechazado/timeout, y preflight de promoción.

# FUTURO

- **WS12** produce G_WRITE_CONTRACT y la autoridad del coordinador.
- **WS44**, con operador Scion designado en WS07, produce G_SCION.
- **Humano/solicitante** resuelve G_EXEC en `autorizaciones/scion.md`.
- **TaskDoc de promoción** fija archivos, pills, átomos y evidencia.
- **WS34.1/WS34.2** implementan; **WS36** consume el adaptador.
