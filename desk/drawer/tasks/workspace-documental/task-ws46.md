---
id: WS46
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS12
requires:
- G_WRITE_CONTRACT
---

# Probar o completar la captura a drawer y protoátomo con origen

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

inventario y pruebas focalizadas; deskops/ (services/drawer.py, domain_tree.py, cli/commands/atoms.py) solo si al ejecutar falta conducta; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Productor Deskops explícito que WS12 exige antes de WS25.2 (HO-11 y HO-11b del contrato, sección 7). Primero probar la composición de llamadas públicas (por ejemplo POST /docs/create de sldb con el path fijado bajo desk/drawer/tasks/, o DrawerService) frente a las tres propiedades del contrato WS12; solo si no preservan origen, no crean tarea activa y controlan colisiones, completar la conducta que falte, con tarea propia en deskops. No se impone wrapper ni modelo nuevo antes de demostrar que hacen falta, y no se crea API ni modelo por reflejo. Candidato de drawer y protoátomo tienen pruebas separadas de origen y destino. Las pruebas usan un store temporal; no se muta el desk real ni se crea tarea activa.

## Aceptación

Inventario con ruta, símbolo y commit de la composición pública probada y, por separado para el candidato de drawer y para el protoátomo, una prueba real en tests/ de deskops que muestra origen (ruta y mensaje, con la representación del contrato WS12) persistido y visible tras recargar, ninguna tarea activa creada (ni en el Board ni en list tasks) y una colisión con un candidato o protoátomo existente rechazada sin sobrescribir, incluso si el archivo existe sin estar rastreado. Si la composición pública cumple, esas pruebas bastan y no se duplica código; si es parcial, se completa solo lo faltante y se vuelve a probar todo el contrato. WS25.2 depende de esta capacidad probada y no se cumple declarándola no disponible. Este nodo es plan; no afirma que exista ni que esté implementado o aceptado.

## Dependencias

Tareas: WS12. Gates: G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS46/6fa5dadbde672a72f8530b6a661a4ac3b75893ce8ff8d3aabbac0a27ff2fd997/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
