## REFORMULACION

**Propósito:** inventariar las superficies y operaciones públicas de Deskops en una auditoría verificable. **Resultado:** `auditoria/deskops.md` con una fila por superficie —archivo, comando público o modelo registrado— con ubicación y lista completa de operaciones que la leen o mutan, o «dato pasivo». **Repo dueño:** deskops. **Límites:** solo categorías enumeradas bajo `desk/` de este checkout y el store local `.sldb`; no inventariar binarios ajenos; no inferir modelo por carpeta; dato pasivo se registra con path/hash o listado read-only; lo no comprobado se marca con causa. Es un nodo de planificación con entrega concreta, no un agregado; su promoción no está autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** brief, alcance, decisiones y `dag.yaml`; árbol de `desk/` en las categorías enumeradas; ayuda pública de comandos Deskops; métodos de `DeskopsOperations`; `sldb models list`; store local `.sldb`. **Cambios previstos:** crear `auditoria/deskops.md` con tabla de superficies; no modificar código, store ni archivos fuera de `output_scope`. **Dependencia:** consume WS01 (brief/glosario); verificaría hash/alcance del brief sin reescribirlo. **Gates:** ninguno declarado. **Validación esperada:** cada fila tendría ubicación (`archivo:línea` o símbolo) y operación expuesta; una fila contendría la lista de operaciones, sin duplicar por comando; todo estado comprobado citaría lectura o salida de solo lectura; lo ausente/inaccesible/no encontrado quedaría marcado «no comprobado» con causa; cobertura de todas las categorías enumeradas. **Errores esperados:** store `.sldb` ausente o inaccesible, comando que falla o modelo no localizado; se registrarían como no comprobados, sin sustituirlos por inferencias.

## FUTURO

La promoción a tarea ejecutable —TaskDoc, archivos precisos, pills y evidencia— la decide el coordinador humano y no está autorizada. WS06 usará esta auditoría para la correspondencia de alcance por repo dueño; WS10 la usará para el índice y convención del manual. La recepción o aceptación del delta y cualquier modificación del store quedan fuera de este nodo y corresponden a actores humanos o a nodos posteriores.
