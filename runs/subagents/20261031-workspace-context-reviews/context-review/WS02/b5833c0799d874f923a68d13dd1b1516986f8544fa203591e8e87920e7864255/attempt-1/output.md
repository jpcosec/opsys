## REFORMULACION
Propósito: inventariar las superficies de Deskops y sus operaciones públicas como encargo de planificación. Resultado: `auditoria/deskops.md` con una fila por superficie —archivo, comando público o modelo registrado— que indique ubicación, operaciones que la leen o mutan, o «dato pasivo», y estado comprobado mediante archivo:línea, hash/listado read-only o salida de comando; lo no comprobado se marca con causa. Repo dueño: deskops. Límites: solo archivos de las categorías enumeradas bajo `desk/` de este checkout, comandos Deskops, métodos de `DeskopsOperations` y modelos que sirven esas superficies; store local `.sldb`; no inventariar binarios ajenos, no inferir modelo por carpeta, no ejecutar cambios ni implementar.

## AMBIGUEDADES
1. «firmas públicas, efectos Git y cierre»: no se define qué cuenta como «efectos Git» ni cómo registrarlos por superficie. Obligaría a inventar si son commits, staging, ramas u otra cosa, y si van en la misma fila o en filas aparte.
2. «modelos que sirven esas superficies»: falta el criterio para decidir qué modelo «sirve» a qué superficie. Obligaría a inventar el mapeo modelo-superficie.

## DRY-RUN
Un ejecutor futuro leería WS01 (brief/glosario), el nodo y el task file; listaría `desk/` y ejecutaría solo lecturas: `sldb models list`, ayuda/listado de comandos Deskops, inspección de símbolos de `DeskopsOperations` y comprobación del store `.sldb`. Crearía `auditoria/deskops.md` con la tabla. Consume la dependencia WS01; no hay `requires`. Si falta el store, marcaría «no comprobado» con causa; si un archivo es inaccesible, igual. Validación esperada: cada fila con ubicación y lista de operaciones, evidencia citada y sin inferir modelo por carpeta. WS06 y WS10 consumirían la auditoría.

## FUTURO
La promoción fijará archivos/pills exactos y el TaskDoc; el coordinador revisa el resultado y WS06/WS10 reutilizan la auditoría. Nada de eso es ambigüedad del nodo.
