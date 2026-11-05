# Brief: la UI de deskops

Fecha: 2026-11-04. Repos: deskops (dueño del contrato y de la vista de datos) y graph_ui (cliente que la sirve). Estado: plan en drawer.

## Encargo

El producto es la UI de deskops: la superficie donde una persona trabaja la fábrica. Ve sus desks, las tareas por etapa del ciclo de vida, qué gate bloquea cada una, qué evidencia falta, el drawer y el inbox, y los agentes que corren; y desde ahí hace las acciones del dominio (avanzar, diferir, promover, reconocer). sldb es el sustrato que no se ve; Scion ejecuta debajo.

No es un explorador del store. El visor "KIMUN Knowledge Workspace" de graph_ui (`frontends/workspace/`, puerto 8090) responde "¿qué es este nodo?" y queda como vista secundaria de inspección.

## Lenguaje visual (lo que el dueño pidió)

Las pantallas del proyecto Stitch "Software Factory Knowledge Hub" (projects/10031397220192998154) son la referencia visual. Lo que se toma de ellas:

- **Organización por trabajo, no por almacén:** columnas por etapa del ciclo de vida; el drawer como carril aparte; el inbox como buzón entre proyectos.
- **La tarjeta cuenta en qué está la tarea:** checklist de gates con estado (cumple / pendiente / falla), conteo "n de m", contexto bajo (pills) separado de conocimiento durable (atoms).
- **Panel de la tarea seleccionada:** objetivo, gates con detalle, pills (transitorias) con su "qué" y "cuándo", atoms (durables) con su respuesta, y las acciones del dominio con su condición visible.
- **Color con significado:** verde = cumple, ámbar = pendiente, rojo = falla; el acento solo para selección.
- **Densidad tranquila:** oscuro, bordes de 1 px, mono para ids y hashes.

Lo que no se toma: ningún número, gate, porcentaje, TTL, autor, versión ni nombre de ejemplo. Regla del plan: **un elemento de pantalla sin fuente real no se dibuja**; si la fuente llega con otro plan, el elemento aparece cuando ese plan cierra.

Pantallas de referencia (archivos HTML en Stitch, versión con el design system de graph_ui aplicado):

| Pantalla | Archivo Stitch |
|---|---|
| The Desk - Active Board | projects/10031397220192998154/files/10b9fa05c4624776bdf3c0c3a9958b71 |
| The Desk - Markdown Wiki Doc | projects/10031397220192998154/files/e9c1ec6a77464258b1f45ab27d099fa7 |
| The Desk - Tareas Concurrentes & Herencia | projects/10031397220192998154/files/3c1cfa2c9f2c41258dcefbf7d95e98d0 |
| Drawers - Cajón de Esbozos & Triage | projects/10031397220192998154/files/23e743b753d440998ea42fff169165a1 |
| Inbox - Buzón Inter-Proyecto | projects/10031397220192998154/files/8bdd66211c8f4c80b2ae7e0c1e98952b |

## Resultado esperado

1. Una vista de datos en deskops (`deskops view ... --format json` y la clase que la produce) que compone lo que la UI muestra desde operaciones reales: board por etapa, tarjeta y detalle de tarea con gates y evidencia, pills y atoms resueltos, drawer, inbox, agentes y corridas. Contrato escrito en `docs/deskops-ui.md`.
2. En graph_ui, un frontend nuevo `frontends/desk/` (servidor y shell) con el design system oscuro de graph_ui, que sirve esa vista: Board, Tarea, Drawer, Inbox, Agentes; y "Inspeccionar" enlaza al visor de nodos existente.
3. Acciones del dominio solo por operaciones de deskops, con confirmación y guarda de revisión: avanzar (ya existe en graph_ui), reconocer un mensaje y pasar un mensaje del inbox al drawer. El resto de verbos se muestran deshabilitados con el motivo y el nodo que los habilita.

## Fuera de alcance

Editar Markdown o YAML en el navegador; Spec Studio y diagramas (necesita vínculos por paso en spec2viz, plan aparte); autenticación y acceso remoto (solo loopback); lanzar agentes Scion desde la UI (llega con el dispatch de la fábrica); gates por tipo y recibos (los produce `gates-por-tipo`; la UI los muestra cuando existan).
