## REFORMULACION
WS43 es un nodo de entrega documental: publicar en el deskops real la navegación documental validada en Taller. Debe aplicar entradas/índices authored de WS17, contrastados con el acta de WS30, usando el contrato de navegación de WS11 (transitivo) y operaciones autorizadas de WS12. Repo dueño: `deskops`. Resultado: `desk/README.md`, mapa de ecosistema/índices, átomos de acuerdos durables, enlaces a repos conocidos y acta en `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`, con commit por `deskops closeout commit`. Límites: no escribir en repos hermanos sin tarea y acuerdo; no imponer modelos nuevos; reutilizar registry como inventario derivable; no publicar el ejemplo como ecosistema real; no omitir repos ni fabricar entradas interrepo.

## AMBIGUEDADES
1. «El participante que fija P08 recorre Markdown y UI real, links/roots verificables (...), commit por `deskops closeout commit`, acta deskops:runs/... y commit». No queda claro si el commit y el acta los produce el participante humano o el ejecutor del nodo, ni el orden entre acta y commit. Obligaría a inventar el actor responsable y la secuencia de evidencia.
2. «P08 remite a protocolo». No se nombra qué protocolo, dónde está ni quién lo produce. Obligaría a inventar el destino del enlace o el documento de protocolo.
3. «P03–06 solo si mapa expone operaciones». No hay criterio de qué significa que el mapa «exponga operaciones»; eso decide si deben crearse átomos de P03–P06. Obligaría a inventar el umbral.

## DRY-RUN
Lecturas: `dag.yaml` WS43, contrato `contratos/navegacion.md` de WS11, plantillas WS17, acta WS30, `decisiones.md`, `deskops list repositories`, registry y `desk/README.md` actual, átomos existentes. Cambios previstos: actualizar README, crear/reemplazar mapa según contrato, crear o reutilizar átomos de P01/P02/P07/P09 y contratos aplicables, enlazar cada repo por identidad/root autorizado, marcar entradas ausentes con follow-up del repo dueño, escribir acta y commit. Dependencias/gates: G_HUMAN_MANUAL, G_PRODUCT y G_WRITE_CONTRACT con WS43 en `per_delta`; si falta contrato, API, root o dato, detenerse y registrar el hueco sin sustituto. Validación esperada: enlaces resueltos a paths existentes, correspondencia con paths/hashes de WS17 validados por WS30, ausencia de escrituras en repos hermanos, acta y commit verificables.

## FUTURO
El participante humano ejecuta la revisión real; el responsable de recepción valida el delta de WS43; WS31 consume el acta de publicación para el manual.
