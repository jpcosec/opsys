## REFORMULACION

**Propósito:** implementar en la UI la captura interna con destino elegido explícitamente entre candidato de drawer y protoátomo, sin exigir tarea.

**Resultado:** una captura persiste tras recargar, conserva un origen tipado —ruta o mensaje— y no crea tarea implícita; los permisos del contrato WS12 se aplican.

**Repo:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** nodo candidato, no ejecutable; no promociona ni modifica otros repos. Depende de WS12 y WS16; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, todos pendientes. La aceptación debe probar cada destino por separado.

## AMBIGUEDADES

1. «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)»: no fija si toda captura debe tener origen ni qué origen corresponde cuando no nace de una ruta o un mensaje. Obliga a inventar obligatoriedad y caso sin origen.

2. «los orígenes ruta y mensaje se registran y se muestran tras recargar»: no aclara si el origen «mensaje» exige la UI de mensaje/ack de WS25.1, que no figura en `depends_on`. Obliga a inventar si falta una dependencia o si puede capturarse sin selección de mensaje.

3. «una captura persiste tras recargar» frente a «cada destino se prueba por separado»: no dice si la aceptación exige cerrar con ambos destinos o basta uno. Obliga a inventar el criterio de cierre.

## DRY-RUN

**Lecturas previstas:** nodo WS25.2, aristas WS12/WS16/WS25, gates, `brief.md`, `alcance.md`, `cobertura.md`, `decisiones.md` y guía.

**Cambios previstos:** código de captura en `graph_ui`, integración de endpoints autorizados por WS12 y pruebas en `tests/`. Sin ejecución.

**Dependencias:** contrato y whitelist de WS12; acta humana de WS16; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes. Si falta una operación, aplica la regla común: detenerse y registrar el hueco.

**Validaciones futuras:** persistencia tras recarga por destino; origen ruta y mensaje registrado y visible; ausencia de tarea implícita; permisos del contrato; pruebas separadas por destino.

## FUTURO

WS12 produce la whitelist/capability y resuelve G_UI_WRITE y G_WRITE_CONTRACT. WS16 produce el acta y resuelve G_HUMAN_READ. La promoción fijará archivos, escenarios y textos en el TaskDoc. El humano resuelve P01/P02/P07/P08/P09 y, si corresponde, WS25.1 aporta la UI de mensaje/ack.
