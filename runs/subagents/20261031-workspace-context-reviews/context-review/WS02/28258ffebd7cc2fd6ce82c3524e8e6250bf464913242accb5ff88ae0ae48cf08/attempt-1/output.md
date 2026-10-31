## REFORMULACION

Propósito: inventariar las superficies y operaciones públicas de Deskops en este checkout. Resultado: `auditoria/deskops.md`, con una fila por superficie, su ubicación, la lista completa de operaciones que la leen o mutan —o «dato pasivo»— y estado comprobado o «no comprobado» con causa. Repo dueño: `deskops`. Límites: solo categorías enumeradas bajo `desk/`, comandos CLI/`DeskopsOperations` y modelos del store local `.sldb`; no inventariar binarios ajenos; no inferir modelo por carpeta; sin mutaciones; depende de WS01; promoción no autorizada.

## AMBIGUEDADES

1. «cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» y «Universo: ... comandos Deskops». Obligaría a inventar si el inventario de comandos se limita a los que sirven las categorías enumeradas o abarca todos los comandos públicos de Deskops; el universo cambia según la lectura.

2. «firmas públicas, efectos Git y cierre». Obligaría a inventar qué es un «efecto Git» como superficie y cómo registrarlo/evidenciarlo, porque la definición previa de superficie solo admite archivo, comando público o modelo registrado.

3. «modelos que sirven esas superficies». Obligaría a inventar el criterio de pertenencia de un modelo a una superficie; sin él se puede omitir un modelo relevante o incluir uno que no corresponde.

## DRY-RUN

Lecturas previstas: brief/glosario de WS01; árbol `desk/` y archivos de las categorías enumeradas; definiciones de comandos CLI; clase `DeskopsOperations`; salida de solo lectura de `sldb models list`; store local `.sldb`. Cambios previstos: escribir `auditoria/deskops.md`. Dependencias: WS01 y store local; si falta el store, se registra «no comprobado» con causa. Validaciones futuras: una fila por superficie, lista completa de operaciones, evidencia `archivo:línea`, hash/listado o salida de comando de solo lectura; no inferir modelo por carpeta; no incluir binarios ajenos.

## FUTURO

WS06 consumirá esta auditoría para la correspondencia de alcance con repos dueños; WS10 la usará para el manual. La promoción de WS02 sigue `not_authorized`: el TaskDoc fijará archivos, pills y preflight. No hay ejecución ni aceptación de implementación en este nodo.
