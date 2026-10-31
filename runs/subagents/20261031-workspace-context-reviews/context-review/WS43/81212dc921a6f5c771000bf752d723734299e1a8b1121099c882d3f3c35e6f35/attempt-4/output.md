## REFORMULACION
WS43 es un nodo de documentación cuyo propósito es publicar en el deskops real la navegación documental ya validada en Taller: entradas/índices authored, enlaces a repos conocidos por identidad/origen, sin tocar repos hermanos ni imponer modelos. Resultado esperado: `desk/README.md`, mapa/índices según P09 y WS11, y átomos de acuerdos durables. Repo dueño: `deskops`; base: `deskops:repository_root/`. Depende de WS17 y WS30; requiere `G_HUMAN_MANUAL`, `G_PRODUCT` y `G_WRITE_CONTRACT`. Límites: no publicar solo el ejemplo como ecosistema real; cada proyecto adicional exige tarea de repo y acuerdo de alcance.

## AMBIGUEDADES
1. «Persona designada recorre Markdown y UI real»: no se identifica quién designa ni qué persona acepta. Obligaría a inventar el actor de aceptación y quién firma/commitea el acta.
2. «Repos a enlazar = `deskops list repositories`» frente a «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: no queda claro si todos los repos listados pueden enlazarse en WS43 o solo los que ya tengan tarea/acuerdo. Obligaría a inventar el criterio de inclusión y si hay que abrir tareas antes.
3. «links/roots verificables»: no se define qué es un `root` ni qué hace verificable un enlace. Obligaría a inventar el criterio de aceptación y el método de comprobación.

## DRY-RUN
Lecturas previstas: contrato `contratos/navegacion.md` de WS11 (transitivo), plantillas WS17 materializadas por WS40 y validadas por WS30, P09, registry y salida de `deskops list repositories`. Cambios previstos: `desk/README.md`, mapa/índices autorizados y átomos de acuerdos durables. Dependencias: WS17 y WS30 terminados; gates pendientes; `output_base` indicado. Validaciones futuras: recorrido humano de Markdown/UI, comprobación de enlaces/roots, commit por `deskops closeout commit`, acta en `deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md` y confirmación de que no se publica solo el ejemplo. No se ejecuta nada.

## FUTURO
WS17/WS30 producen entradas validadas y aprobación humana; WS11 emite el contrato; WS07/WS12 resuelven `G_PRODUCT`/`G_WRITE_CONTRACT`; P09 y la persona designada los decide el humano.
