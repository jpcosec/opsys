---
id: WS17
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS11
- WS40
requires: []
---

# Escribir entradas e índices del desk ejemplo

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

ejemplo/nav/ (plantillas Markdown versionadas en el paquete del plan)

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Escribir solo entradas/índices authored como plantillas versionadas bajo el paquete del plan; no es el productor del corpus. El generador de WS40 acepta estas fuentes y las materializa bajo su root temporal, sin copiar inventarios derivados ni escribir repos reales. Puede escribirse antes de WS16: el lector no depende de estos índices nuevos; WS30 sí los integra. Índice authored = texto curado y enlaces de entrada elegidos para recorrido, sin copiar listados completos del store que debe resolver consulta. Registry = desk/registry/repo-*.md existente inventariado WS02. WS43 lo reutiliza en publicación real; plantillas temporales enlazan por roots/aliases del manifiesto WS40, sin copiar ni depender del registry real.

## Aceptación

Tras regenerar corpus WS40 con ejemplo/nav/, recorrer links Markdown sin UI; source versionado y destino temporal no son registros independientes. Verificar al regenerar que cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40; no duplicar el registry de deskops; el conjunto temporal usa solo manifiesto WS40, no enlaces al checkout real. Plantillas son fuente única: destino temporal se regenera desde ellas, no se edita/commitea como registro competidor. Resolver cada link según identidad/root/store/aliases contrato WS11 contra manifiesto WS40; conjunto de plantillas cubre ambos desks, no cada plantilla individual.

## Dependencias

Tareas: WS11, WS40. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS17/9878bea69f77150d5d210f342791c9726de2a2a44adf8a02dfbcff6b1310d878/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
