# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. Ningún nodo tiene ejecución autorizada.
- ROOT y PC son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional, no un defecto. Los gates `G_SLDB_*` los produce otro repo (sldb, plan `grafo-operable`, rev 9); lo que ese plan fija es contrato suministrado, no ambigüedad de este nodo.
- Las decisiones D2, D3, D4, D9 y D10 están tomadas por el dueño; las DC1–DC7 son propuestas de este plan y se leen como dadas. Los pendientes del dueño en decisiones.md no son ambigüedad del nodo salvo que el nodo dependa de uno sin decir qué hace mientras tanto.
- Los bloques `edge` son contratos de vecinos; no los revises.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance (en particular: escribir en sldb, o suplir con Python una regla que sldb debería evaluar).

No cuentan: nombres exactos de archivos, funciones o tests que el TaskDoc fijará al promover; contratos que produce una dependencia nombrada (un nodo GO de sldb o un GC de este plan); trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.
