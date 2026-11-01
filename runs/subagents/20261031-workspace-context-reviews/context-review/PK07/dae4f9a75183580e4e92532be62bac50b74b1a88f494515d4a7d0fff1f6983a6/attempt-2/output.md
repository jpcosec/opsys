## REFORMULACION

**Propósito:** agrupar dos extensiones independientes del workspace documental —Changes/impacto (WS29) y modelos/Schema (WS39)— sin convertirlas en prerrequisito del lector ni del manual básico.

**Resultado sustantivo del paquete:** evidencia propia de cada extensión: en WS29, una mutación real en store temporal que muestra documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos de los tres comandos, sin reparación automática; en WS39, inspección y edición de modelos existentes probada por API, con acta de aceptación humana. Integración: el manual etiqueta cada extensión según su evidencia, sin presumir CST/Kimun. WS29 y WS39 no se entregan artefactos entre sí.

**Repo dueño:** deskops (paquete); hijos en graph_ui.

**Límites:** agrupación no ejecutable, no autoriza tareas ni añade aristas; revisiones de comprensión ≠ producto entregado.

## AMBIGUEDADES

1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun» — el nodo no nombra qué manual ni quién lo produce ni qué hacer si no existe; obligaría a inventar si PK07 mantiene ese etiquetado o si depende de un productor externo.
2. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» — «integración indicada» no se concreta en el nodo (no hay arista WS29–WS39); obligaría a inventar qué validación conjunta se exige además de las aceptaciones individuales.

## DRY-RUN (hipotético, sin ejecutar)

WS29 y WS39 corren en paralelo: ninguna arista entre ellos.
- **WS29** consume WS15 (errores/modo degradado) y WS24 (grafo, panel Context); produce `frontends/mindmap/views/workspace/changes/` y tests; valida sobre store temporal real: mutación, afectados, 1 hop entrante/saliente y errores agrupados por comando, con enlace al comando documentado.
- **WS39** consume WS12 (whitelist/contrato) y WS13 (lector, panel Context); produce `shell/dialogs.js`, `views/models/`, `tests/` y `runs/.../modelos/acta.md`; valida UF09 sobre store temporal, contrastando efectos/errores con WS12; gates G_HUMAN_READ (solo uso de mutaciones), G_UI_WRITE, G_WRITE_CONTRACT; acta con participante P08.

Validación conjunta: ambas pruebas sobre el mismo corpus/store WS40; el manual publicado por WS31 solo etiqueta disponible lo que tenga evidencia; ninguna bloquea lector/manual.

## FUTURO

WS31 publica el capítulo 15 y el etiquetado; el humano fija el participante (P08) y pasa G_HUMAN_MODEL; los productores WS12/WS13/WS15/WS24 entregan sus contratos; el receptor registra actas.
