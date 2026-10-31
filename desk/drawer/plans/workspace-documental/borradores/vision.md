# Visión del workspace documental

Estado: borrador basado en brief.md; contrato por reconciliar en WS07. No describe funcionalidades ya entregadas ni reemplaza átomos/modelos del proyecto.

## Propósito

Permitir a una persona entender y operar un proyecto mediante sus documentos, relaciones y procedimientos. Un IDE para el desk: explorar, abrir, leer, editar, vincular y actuar sobre el mismo material, conservando contexto.

## Unidad de trabajo

Los documentos del desk son Markdown, modelados o no; un contrato estructurado es opcional según el soporte. Fuente y renderizado conservan la identidad y procedencia. Una representación puede mostrar un documento, componer documentos referenciados o evaluar una selección: no toda vista equivale a un único archivo ni toda relación requiere un documento nuevo. Código, eventos y estado de ejecución pueden tener otros soportes; no fingir que el runtime es Markdown.

## Superficies

Inbox, drawer, boards, tareas y fases, pills, rituales/lifecycle, átomos/protoátomos, materializaciones, registro de repositorios, roles/runtimes y ejecuciones. Su navegación debe mostrar relaciones y operaciones reales, con infraestructura documental como autoridad de lectura/escritura y Deskops como autoridad del workflow.

## Interacción propuesta

Explorador, documentos abiertos en pestañas y divisiones, búsqueda y panel contextual. Seleccionar un documento permite cambiar representación y seguir enlaces sin perder historia. La organización del ecosistema procede de documentos de entrada/índice, consultas y relaciones; el shell ofrece mecanismos genéricos de navegación. Disposición y preferencia local no necesitan convertirse automáticamente en documentos compartidos.

## Criterios de producto

- Trabajar sin agentes es un recorrido completo.
- Leer Markdown permite recorrer la estructura sin depender exclusivamente de la UI.
- Cada edición tiene destino y cada composición conserva origen.
- Una condición sintáctica satisfecha no se presenta como prueba de que tests o revisión humana pasaron.
- Un error o relación rota tiene diagnóstico; no se disfraza de colección vacía.
- El usuario puede comprender las consecuencias de una acción; no necesita conocer comandos internos para operaciones soportadas.

## Decisiones abiertas

Dónde viven y qué contratos usan las entradas e índices; alcance real de ViewDoc; backend inicial vs ruta Kimun; representación y persistencia de selección/disposición; política de edición fuente y sincronización; autoridad y compatibilidad de acciones; latencia aceptable. Resolver con WS02–WS04/WS07/WS11/WS12, no improvisar al dibujar pantallas.

## Superficies adicionales y material existente

CrossroadDoc y namespaces organizan dominios; issues Markdown deliberadamente no modelados son legibles y operables mediante contratos existentes. FAQ y StepDoc son documentos de orientación/procedimiento. Brainstorm, Schema/edición de clases y Specs ya existen en Mindmap: inventariar y conservar/integrar sus capacidades explícitamente. Carpetas legacy (features/primitives/logbook/materializers) se clasifican por soporte actual en WS02, no por nombre ni como modelo obligatorio nuevo. KGDB no es otro servicio nuevo: la capa de grafo actual vive en sldb; no reintroducir el proyecto retirado.

Vocabulario normativo de este borrador: brief.md. Alcance: alcance.md. Propuestas de host, backend y escritura: decisiones.md (pendientes). El workspace puede enfocar nodos no documentales, pero el documento no pierde su identidad al cambiar de representación.
