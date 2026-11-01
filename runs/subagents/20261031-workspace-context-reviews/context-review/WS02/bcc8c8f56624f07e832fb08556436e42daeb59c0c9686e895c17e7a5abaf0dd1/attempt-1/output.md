REFORMULACION
Propósito: inventariar superficies y operaciones públicas de Deskops como auditoría de planificación. Resultado: `auditoria/deskops.md`, una fila por superficie con ubicación, lista de operaciones y estado comprobado; datos pasivos con path/hash o listado; no inferir modelo por carpeta; lo no comprobado se marca con causa. Repo: `deskops`. Límites: solo categorías enumeradas bajo `desk/` de este checkout, comandos/métodos públicos y modelos del store local `.sldb`; cierre `verify|commit`; sin binarios ajenos, sin mutar ni implementar; depende de WS01; promoción no autorizada.

AMBIGUEDADES
1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas; una fila por superficie» frente a «Cada fila incluye ubicación (archivo o símbolo de código) y la operación expuesta (comando o método que la lee o muta...)». Si el comando es superficie, ¿es fila propia o la operación de una fila? Obliga a inventar el esquema de la tabla y si los comandos llevan fila; afecta completitud y «no duplicar por comando».
2. «modelos que sirven esas superficies». No define «servir». Obliga a inventar el criterio de inclusión/exclusión —referencia en código, nombre o relación en store— y puede producir filas de más o de menos.

DRY-RUN
Lecturas previstas: brief, alcance, decisiones, cobertura, `dag.yaml`, guía y fuentes Deskops (`desk/`, código CLI/`DeskopsOperations`, `.sldb` local); solo lectura con listados/hashes, `deskops --help`, `sldb models list`. Cambios previstos: crear únicamente `auditoria/deskops.md`. Dependencias: WS01 y store local; si falta store, registrar «no comprobado». Validaciones futuras: una fila por superficie, ubicación, lista completa de operaciones, evidencia archivo:línea/salida/hash, no inferir modelo por carpeta y preflight de promoción.

FUTURO
WS06 consumirá la auditoría para reconciliación; WS10 para el índice del manual. La promoción —TaskDoc, archivos, pills, átomos y evidencia— la fija otro nodo y la autoriza un humano; este nodo no aprueba implementación.
