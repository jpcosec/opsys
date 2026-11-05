# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. Ningún nodo tiene ejecución autorizada hasta que su revisión esté dispuesta.
- ROOT y PU son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional. Los gates `G_GC*`/`G_GO*` los producen otros planes (`gates-por-tipo` en deskops, `grafo-operable` en sldb); mientras no se cumplan, el elemento de UI correspondiente no se muestra (regla de alcance.md), y eso no es ambigüedad.
- Las decisiones DU1–DU6 de decisiones.md están tomadas.
- Las pantallas de Stitch son la referencia visual; sus datos son de ejemplo y nunca se copian.
- Los bloques `edge` son contratos de vecinos; no los revises.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance (en particular: mostrar un dato sin fuente real, o escribir sin pasar por las operaciones de deskops).

No cuentan: nombres exactos de archivos, funciones, clases CSS o tests que el TaskDoc fijará al promover; textos exactos de pantalla; detalles visuales que la pantalla de Stitch de referencia ya resuelve; trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.
