## REFORMULACION

Propósito: redactar entradas e índices authored del desk de ejemplo como plantillas Markdown versionadas que el generador WS40 materialice en su corpus temporal. Resultado: conjunto de plantillas bajo `ejemplo/nav/` que enlazan ambos desks del manifiesto y resuelven según el contrato WS11. Repo dueño: `deskops`. Límites: no produce el corpus, no escribe repos reales, no copia inventarios derivados ni sustituye el registry; puede escribirse antes de WS16 y WS30 lo integra.

## AMBIGUEDADES

1. «conjunto de plantillas cubre ambos desks, no cada plantilla individual». No se define qué entradas/índices ni qué amplitud constituyen cobertura; el ejecutor inventaría el conjunto mínimo y el criterio de aceptación.

2. «Registry = desk/registry/repo-*.md existente inventariado WS02; enlazarlo/reutilizarlo, no duplicar otro catálogo» y «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40; no duplicar el registry de deskops». El registry existente vive en el deskops real, mientras la aceptación exige resolver contra roots/stores del corpus temporal; WS40 no declara materializar registry. Obliga a inventar si se enlaza fuera del corpus o se crea una copia, que está prohibida.

## DRY-RUN

Lecturas: guía, brief, alcance, decisiones, cobertura; nodo WS17 y contratos vecinos WS11/WS40/WS30/WS43; registry WS02 referenciado. Cambios previstos: crear plantillas Markdown authored en `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`, sin editar el generador WS40, corpus ni repos reales, y sin commit (promotion no autorizada). Dependencias: contrato WS11 de identidad/root/store/aliases; generador y manifiesto WS40; registry existente inventariado WS02. Validaciones futuras: regenerar corpus WS40 con la ruta de plantillas; recorrer links Markdown sin UI; comprobar resolución contra el manifiesto para ambos desks y ausencia de registry duplicado; después WS30 y WS43. Nada ejecutado.

## FUTURO

WS11 produce el contrato de navegación; WS40 produce generador, manifiesto y parámetro de plantillas, y puede cerrar sin WS17; WS30 realiza validación humana y acta con paths/hashes; WS43 publica en el deskops real con closeout. La promoción fijará archivos/pills y el humano autoriza. WS16 no depende de estos índices.
