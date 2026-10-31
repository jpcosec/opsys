# Catálogo inicial de vistas y renderizaciones

Estado: borrador. No es una lista de páginas a implementar ni una taxonomía de modelos aprobada. A4/B2 deben contrastar cada caso con documentos, consultas y renderizadores existentes.

| Fuente / selección | Representaciones candidatas | Operaciones / navegación |
|---|---|---|
| Entrada ecosistema/proyecto, índice o mapa | Markdown renderizado, lista enlazada, mapa de relaciones | Abrir destinos, explicar organización; resolver origen y proyecto |
| Cualquier documento del desk | Fuente Markdown, render estructurado, campos/propiedades | Leer, comparar, editar por contrato; referencias y backlinks |
| Board y sus referencias | Lista, tablero, dependencias | Abrir tareas/contexto/rituales; operaciones de enrutamiento |
| Task y documentos vinculados | Encargo, procedimiento aplicable, evidencia/cambios | Preparar, ejecutar, validar, revisar; acciones de workflow |
| Ritual, pasos y lifecycle | Procedimiento, relaciones/transiciones | Consultar obligaciones y condiciones; edición del contrato soportado |
| Átomos/protoátomos y fuentes | Documento, agrupación/consulta, relaciones | Capturar, clasificar, vincular, dividir/reunir, materializar |
| Inbox: entradas y consulta | Lista y mensaje/documento | Leer, responder, ack y triage según contrato |
| Drawer: candidatos y mapas | Documentos, lista/consulta, relaciones | Aclarar/organizar; autoría de trabajo explícita |
| MaterializationContractDoc y soportes | Contrato, origen/destino, impacto | Navegar procedencia, verificar vigencia y validación |
| Registro de repositorios | Directorio enlazado, relaciones de desks | Abrir desk, resolver identidad, comunicación autorizada |
| Roles, runtime profiles y RunDoc | Contrato, ejecución/evidencia, conversación vinculada | Preparar/delegar y revisar; estado operativo procede del runtime |
| Resultado de búsqueda o diagnóstico | Lista/tabla, documento en contexto, subgrafo | Afinar selección, abrir origen; no duplicar contenido |

## Reglas a precisar

- ViewDoc de Spec2viz ya expresa selección de modelos/predicados, relaciones y notación; verificar qué cubre antes de extenderlo. No confundir SurfaceDoc (documentación de subsistema CLI) con definición de una pantalla.
- Un Board contiene referencias, no una segunda copia de cada tarea.
- El renderer cambia representación; las operaciones semánticas mantienen su autoridad fuera del componente visual.
- Relaciones entrantes, inventarios y resultados derivables se calculan; documentos nuevos deben aportar organización/decisión authored real.
- El mismo documento puede abrirse en dos representaciones con selección e identidad comunes. Las composiciones señalan el documento/campo dueño de cada edición.
- No es necesario representar estado volátil del runtime ni preferencias privadas como documentos compartidos; fijar ese límite explícitamente.

## Ficha de cada vista (pendiente de completar)

Propósito humano; documento/consulta origen; identidad; contrato/modelo; campos y relaciones usados; renderer existente o requerido; navegación; acciones y dueño; destino de escritura; conflictos/errores; disponibilidad actual; aceptación mediante user-flow.
