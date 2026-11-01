REFORMULACION
El nodo WS02 encarga una auditoría de planificación en el repo deskops: inventariar en `auditoria/deskops.md` cada superficie concreta de Deskops —archivo, comando público o modelo registrado de las categorías enumeradas— y todas sus operaciones públicas, con ubicación y estado comprobado. Depende de WS01 (brief/glosario). Límites: solo `desk/` de este checkout, comandos Deskops y modelos que sirven esas superficies, store local `.sldb`; sin binarios ajenos, sin inferir modelo por carpeta y sin elegir una sola operación por fila. La aceptación exige evidencia citada o marcar «no comprobado» con causa.

AMBIGUEDADES
1. «firmas públicas, efectos Git y cierre»: se enumera «efectos Git» como categoría de superficie, pero no se define qué efectos cuentan (commits, índice, refs, hooks, historial, etc.) ni cómo se comprueban. Obliga a inventar el universo y el criterio de fila/estado para esa categoría.

DRY-RUN
Un ejecutor futuro leería el brief/glosario de WS01 y el alcance/aceptación de WS02; inspeccionaría en deskops el árbol `desk/`, los comandos CLI y métodos de `DeskopsOperations` y, en solo lectura, `sldb models list` y el store local. Crearía `auditoria/deskops.md` con una fila por superficie, ubicación y lista completa de operaciones, más estado y evidencia; los datos pasivos con path/hash/listado; lo ausente como «no comprobado» con causa. Consumiría WS01; no usaría WS03/04 ni WS06. Validaría cobertura de categorías, ausencia de modelos inferidos, lista de operaciones no reducida y no inclusión de binarios ajenos. Si falta el store, registraría el hueco, no lo sustituiría.

FUTURO
WS06 y WS10 consumen la auditoría; la promoción sigue `not_authorized` y el TaskDoc/preflight fijarán archivos, pills, átomos y evidencia. La decisión de promover y el uso posterior corresponden al coordinador/humano, no a este nodo.
