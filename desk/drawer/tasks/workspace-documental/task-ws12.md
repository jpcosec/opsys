---
id: WS12
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY
---

# Cerrar contrato de operaciones y escritura

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

contratos/operaciones.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy coordinador, Git, workflow-protected fields, precondición de escritura (before-image por valor, token publicado o CAS solo si el contrato lo fija)/locks, fallos parciales, permisos y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y dueño, no se diseña uno aquí. Whitelist incluye campos protegidos definidos por modelos/lifecycle auditados WS02 (status/current_node/history/closeout_evidence entre otros que determine modelo), por modelo/operación; no lista universal inventada.

## Aceptación

G_WRITE_POLICY registrado. Publicar whitelist por operación/campo/canal/actor/revisión/Git/efectos y estado existente comprobado/faltante. Mapear qué recibo receptor/prueba corresponde a cada delta; receptor P01 registra acta en su repo al preparar ese delta, no WS12: campos/intake no esperan Changes/modelos/Scion ni raw-source. G_WRITE_CONTRACT y G_UI_WRITE se evalúan por IDs/efecto, nunca como aceptación conjunta. Autoría de tareas/cierre esperan G_CLOSEOUT. Raw-source faltante tiene productor WS20 y G_SOURCE; recepción G_SLDB_WRITE antes de WS20, sin exigir API implementada para especificar contrato. Escritura de payload por campos: WS12 define la representación de la precondición, las operaciones y los escritores alcanzados, distinguiendo before-image por valor existente (`expected`, HTTP 409), token publicado (`version`/`content_hash`) y comparación o escritura pública con precondición compartida (aún no probada); no fuerza CAS en toda CLI ni un algoritmo, ni infiere frescura por CLI, y P03 no cambia. Su productor es WS45 (sldb, independiente de source_mode) y su gate G_PAYLOAD_PRECONDITION. Captura directa a drawer: WS12 compara API SLDB existente (`sldb.api.create_document`, DrawerService), composición de llamadas a esas API (no la Composición del glosario) y eventual wrapper Deskops, sin aprobar ninguna ni crear API o modelo por reflejo; `message send` más `promote` no queda aprobado (la promoción borra la nota y deja `why` apuntando a una ruta borrada). La captura a protoátomo entra en la whitelist con su canal o con su hueco y dueño. Solo si falta conducta de workflow se registra un productor Deskops explícito antes de WS25.2; si esa composición de llamadas cumple, se documenta prueba y contrato. Lock solo UI no coordina CLI/agentes: con otro coordinador escritor, read-only/handoff hasta API pública con autoridad compartida probada. WS12 solo escribe contrato y enlaces en deskops; no ejecuta mutaciones ni crea actas interrepo. Contrastar inventarios WS02–04 y contrato WS11, citar path/símbolo/commit observado; comprobado requiere evidencia real citada de API/prueba existente. Cierra con matriz de capacidades/efectos y huecos asignados, no requiere habilitar ninguna mutación. Receptor P01 en repo dueño produce acta por delta al prepararlo; G_WRITE_CONTRACT admite requisito de API faltante solo para el nodo productor de esa API (WS20 raw-source con G_SOURCE; WS45 precondición de payload con G_PAYLOAD_PRECONDITION), manteniendo consumidor WS21 bloqueado por G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE. Elegir la representación de la precondición es entregable de este contrato, justificado por operaciones y escritores alcanzados y reutilizando lo existente; WS45 la verifica. «Receptor P01» aplica a graph_ui, sldb y spec2viz: en deltas de deskops no se crea recepción nueva y rige la autorización de trabajo local. Falta conducta de workflow cuando ni la API ni su composición de llamadas pueden, con prueba real, preservar origen, no crear tarea activa y controlar colisiones. Para el ramal E, este contrato asume producir, como sección por delta de WS34.1 y WS34.2, la política y el umbral de timeout de dispatch y reply y su clasificación observable (al menos aceptado, rechazado y vencido sin confirmación). La duración no se elige ahora: esa sección del contrato WS12 la fija al preparar esos deltas, no WS34, y su ausencia no impide cerrar el contrato núcleo de las Entregas L y M.

## Dependencias

Tareas: WS11, WS08. Gates: G_WRITE_POLICY. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS12/bb6a2868ffb1980aadaa34e0156c15bb9cb624674ce040bdb1385ff9fd310ae4/attempt-3']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
