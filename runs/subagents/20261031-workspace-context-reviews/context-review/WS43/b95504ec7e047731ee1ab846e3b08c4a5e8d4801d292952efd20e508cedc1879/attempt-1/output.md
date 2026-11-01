REFORMULACION
Propósito: publicar en el repo deskops real la navegación documental validada antes en Taller. Resultado: README/mapa-índices authored aplicados, enlaces a todos los repos de `deskops list repositories` con roots/aliases verificables, átomos de acuerdos durables enlazados, acta en runs/.../publicacion/acta.md y commit por `deskops closeout commit`. Repo dueño: deskops. Límites: no escribir en repos hermanos sin tarea/acuerdo; registry se preserva como inventario derivable; no fabricar entradas interrepo; no publicar solo el ejemplo; gates G_HUMAN_MANUAL y G_WRITE_CONTRACT (per-delta) pendientes; G_PRODUCT satisfecho.

AMBIGUEDADES
1. Conjunto y granularidad de átomos. Cita: «los acuerdos durables aplicados al mapa (Pxx aceptadas y contratos navegacion.md/operaciones.md de WS11/WS12) quedan en átomos enlazados desde él» frente a «Regla durable de mapa = navegación/identidad/registry reusable P01/P02/P07/P09 vigentes…; P03–06 solo si mapa expone operaciones, P08 remite a protocolo». La primera admite todas las Pxx; la segunda las restringe. Obliga a inventar cuántos átomos y qué decisiones entran.

2. Descubrimiento e identidad de repos. Cita: «Repos a enlazar = todos los de `deskops list repositories`…» y «Enlazar repos conocidos por identidad/origen». No se nombra quién produce ese comando ni de dónde salen identidad/origen si no las trae; obliga a inventar el mecanismo (registry, git remote, etc.).

3. Superficie «UI real». Cita: «El participante que fija P08 recorre Markdown y UI real». No se define qué instancia de UI ni qué dependencia la produce apuntando al deskops real; WS43 solo depende de WS17/WS30, validados en Taller. Obliga a inventar el entorno.

DRY-RUN
Lecturas: WS43/WS17/WS30 y gates; brief, alcance, decisiones, cobertura; contratos/navegacion.md y operaciones.md cuando existan; acta WS30; plantillas WS17; `deskops list repositories`; desk/registry; desk/README.md; átomos; Board/reconciliacion.md.
Cambios previstos: desk/README.md, mapa/índices, átomos, acta, commit closeout; nada ejecutado.
Dependencias: WS17, WS30, WS11, WS12, G_HUMAN_MANUAL, G_PRODUCT.
Validaciones futuras: links resuelven a paths existentes con roots/aliases del contrato; correspondencia WS17↔acta WS30↔mapa; repos listados presentes o «entrada ausente»+follow-up; reutilización de átomo; acta/commit verificables; cero escrituras en hermanos.

FUTURO
WS11/WS12 producen contratos y el recibo G_WRITE_CONTRACT de WS43; WS30 su acta con paths/hashes; el humano aprueba G_HUMAN_MANUAL. La promoción fija archivos exactos, modelo del mapa y granularidad de átomos; el humano decide si el acta de publicación cierra el gate.
