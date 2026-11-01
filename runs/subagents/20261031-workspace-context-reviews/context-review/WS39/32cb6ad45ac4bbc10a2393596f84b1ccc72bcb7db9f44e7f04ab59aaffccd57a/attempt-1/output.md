REFORMULACION
El nodo encarga, en `graph_ui`, integrar la inspección y edición de modelos existentes desde el lector: el panel Context de WS13 debe mostrar el Schema/clase origen del documento activo y abrir el editor inventariado por WS04, usando `draft/validate/promote` de sldb sin reimplementar modelos. Resultado: punto de entrada navegable y prueba UF09 de inspección/mutación sobre store temporal real, con acta humana en `runs/.../modelos/acta.md` y `G_HUMAN_MODEL`. Repo dueño `graph_ui`; salidas limitadas a `shell/dialogs.js`, `views/models/`, `tests/` y esa carpeta de actas. Límites: no habilitar promover sin API/autoridad; `G_HUMAN_READ` solo habilita mutaciones UI, no desarrollo/pruebas API aisladas; WS13 aporta lector; ruta/selector exacto queda al TaskDoc; promoción no autorizada. Es implementation, no agregado.

AMBIGUEDADES
1. «acceso desde documento activo muestra Schema/clase origen de ese documento»: no define qué hacer si el documento activo no tiene Schema/clase origen (ocultar entrada, estado vacío o mensaje). Obligaría a inventar comportamiento y criterio de prueba.

DRY-RUN
Ejecutor futuro: leería WS39, contrato WS12, lector/contexto WS13, inventario WS04 y gates. Modificaría `shell/dialogs.js` y `views/models/` para añadir el acceso desde Context y abrir el editor; añadiría pruebas en `tests/` y el acta en `runs/.../modelos/`. Consumiría de WS12 operaciones, efectos, errores y autoridad; de WS13 el punto de integración; de WS04 el editor. Antes de habilitar mutaciones comprobaría `G_HUMAN_READ` y el recibo `G_UI_WRITE` del delta; `G_WRITE_CONTRACT` por efecto. UF09 se probaría con store temporal real. Si falta contrato/API/autoridad, se detendría y registraría hueco, sin promover. Validaría inspección, mutación, entrada desde documento activo, errores declarados y acta humana; luego `G_HUMAN_MODEL`.

FUTURO
WS31 publicará el capítulo 15 del manual solo tras `G_HUMAN_MODEL`; P01/WS12 emitirán recibo y contrato por delta; WS16 resolverá `G_HUMAN_READ`. La promoción y el manual no son de este ejecutor.
