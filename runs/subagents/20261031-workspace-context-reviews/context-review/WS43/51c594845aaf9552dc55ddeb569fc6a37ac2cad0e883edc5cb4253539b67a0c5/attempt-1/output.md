REFORMULACION
Propósito: publicar en el deskops real la navegación documental validada en Taller, enlazando repos conocidos por identidad/origen sin escribir en ellos y registrando acuerdos durables en átomos antes de docs. Resultado: desk/README.md y mapa/índices de ecosistema según P09 y contrato WS11, átomos, acta de publicación y commit. Repo dueño: deskops. Límites: no modificar repos hermanos ni imponer modelos; escribir en otro repo exige su tarea y acuerdo; operaciones autorizadas; registry como inventario derivable; no publicar solo el ejemplo como ecosistema real.

AMBIGUEDADES
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» / «Repos a enlazar = todos los de `deskops list repositories`» / aceptación: «un enlace es verificable si resuelve a un path existente del repo enlazado». Si un repo listado carece de «entrada existente» o de path local, no se dice si omitirlo, enlazar su raíz o detenerse; el ejecutor tendría que inventar la excepción.

DRY-RUN
Lecturas previstas: dag.yaml/WS43 y gates; decisiones.md (P08/P09, P03–P06); alcance.md; brief.md; cobertura.md; contratos/navegacion.md (WS11); plantillas e índices de WS17; acta/manual de WS30; salida de `deskops list repositories`; README/registry actuales de deskops y validacion-humana.md.
Cambios previstos: escribir desk/README.md y mapa/índices de ecosistema según P09/WS11; crear átomos de acuerdos durables; enlazar repos por identidad/origen a paths existentes; guardar acta en deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md; commit vía `deskops closeout commit`. Sin tocar repos hermanos.
Dependencias: WS17 (plantillas), WS30 (G_HUMAN_MANUAL y validación), G_PRODUCT (WS07: P08/P09), G_WRITE_CONTRACT (WS12), contrato WS11 transitivo, corpus WS40 vía WS17/WS30.
Validaciones futuras: comprobar que cada enlace resuelve a path existente y root autorizado; recorrido humano Markdown+UI; acta con actor/versión/resultado y commit; verificar que no se publica solo el ejemplo y que registry no se duplica; confirmar gates resueltos antes de ejecutar.

FUTURO
WS07 resuelve P08/P09/P01 y designa actores (G_PRODUCT); WS12 produce G_WRITE_CONTRACT; WS30 produce G_HUMAN_MANUAL y su acta; WS17 entrega plantillas/índices; WS11 fija el contrato de navegación; el humano P08 recorre y firma el acta de publicación; `deskops closeout commit` materializa el commit. WS31 publicará el manual y los átomos vinculados.
