# Notas de promoción, revisión 9

Puntos que no son defectos del plan, pero que el TaskDoc de cada nodo debe fijar al promoverlo.

## WS05
- Fijar qué archivos de configuración sin secretos se leen y cómo se redactan los valores.

## WS08
- Fijar las columnas «entrada/salida» de cada UF y si «manual» lleva sección propia o se absorbe en las UF existentes; incluir los escenarios «navegación por teclado» y «conflicto en dos ventanas» que WS30 cita del guion (validacion-humana.md solo menciona los dos ventanas).

## WS11
- Nombrar el revisor y la evidencia del «contrato básico revisado».

## WS12
- Incluir el umbral de timeout de dispatch/reply: WS34.2 cita «el umbral del contrato WS12» y la aceptación de WS12 no lo nombra (WS34.1 depende de lo mismo). **Resuelto 2026-10-31:** WS12 asume esa sección por delta en su aceptación; una nota no cerraba la interfaz.
- Escribir el valor por defecto de la captura directa a drawer: sin prueba existente citada, la composición de llamadas es hueco con productor Deskops explícito antes de WS25.2, porque WS12 no ejecuta mutaciones.
- Decir quién ejecuta la «prueba real del canal de captura» (el dry-run del revisor la lista sin dueño).

## WS13.1
- Foco compartido: la aceptación dice que las demás representaciones comparten el foco y el scope lo limita a donde WS11 define correspondencia de origen; el TaskDoc debe probar solo esos pares y declarar el resto sin foco compartido.
- «No depender de conocer un ID»: probar abriendo por enlace o ruta WS11, sin el explorador WS13.2 (que depende de WS13.1).

## WS13.3
- Depende de WS11 y WS13.1, no de WS13.2: fijar cómo la prueba abre dos documentos (enlaces, rutas WS11 o catálogo base a1b2b22).
- Definir qué acciones apilan historia y si la pila es global o por división.

## WS15.1
- Fijar la señal y el texto del límite read-only visible (sin permiso o sin capacidad de edición).

## WS15.2
- Fijar el criterio de «sin desk» (ruta de lectura WS11) y qué es «refrescar» en la prueba.

## WS16
- Corpus: WS16 consume el manifiesto de WS40; el TaskDoc debe decir si ejecuta el comando del generador o recibe el corpus ya generado.
- Fijar repo y formato del registro de incidente cuando la causa no está aislada, y quién es el supervisor del repo receptor.

## WS17
- Fijar quién ejecuta el generador WS40 con `ejemplo/nav/` y cuántos enlaces por desk bastan para «cubre ambos desks».

## WS22
- Fijar qué campo del TaskDoc aporta las dependencias dibujadas y no tocar archivos del lector fuera de `board/`.

## WS24
- Fijar si el Markdown sin modelo se registra como caso de la vista genérica o llega solo por el lector WS13.

## WS26.1
- Fijar si un candidato sin evidencia o sin dependencias puede autorarse en la prueba UF04.

## WS26.2
- Citar la ruta y versión del ritual de fase usado para la capa lista; escribir como escenario que un TaskDoc sin `files` (o vacíos) es no comprobado.

## WS27.1
- Diff base con commits: decidir diff por commit o rango sobre `TaskDoc.references`; tratar rutas nuevas sin trackear y repos sin HEAD; orden del historial y caso de commits que no tocan `TaskDoc.files`.

## WS27.2
- Fijar el esquema de gates/summary de `closeout verify` y la correspondencia por tipo de evidencia (WS12), la base de resolución de artefactos (WS11) y la granularidad de «verificada».

## WS28
- Fijar qué evidencia lleva el handoff y que los endpoints son solo los que autorice WS12.

## WS30
- Alcanza WS08 solo de forma transitiva (WS08, WS11, WS12, WS19, WS30); el TaskDoc debe citar el guion de WS08.
- Aclarar si los hashes del acta son de las plantillas WS17 o también del corpus materializado.

## WS32.1
- Fijar la representación de `confirmed` cuando no hay observación y el contrato de integración con WS34/WS37.

## WS33
- Resolver en el preflight qué se reutiliza o extiende del candidato de drawer `external_references.scion` (`overlap_with: scion`).

## WS34.1
- Timeout: citar el umbral de WS12 (ver WS12); basta demostrar un caso rechazado o vencido.

## WS35
- Decidir si los mensajes sin intento (hueco de procedencia de WS33.1) se muestran en una sección propia o quedan fuera.

## WS36
- Alcanza WS33.2 solo a través del agregado WS33 (vía WS34 y WS35); nombrar WS33.2 en `depends_on` o `references` del TaskDoc.

## WS39
- El punto de entrada vive en el panel Context (`node/workspace-view.js`), fuera del `output_scope`: añadir el archivo al alcance o declarar el enganche por registro.
- Fijar el estado vacío cuando el documento no tiene Schema o clase origen, o tiene varias.

## WS45
- Decir si WS45 es la «tarea propia en sldb» cuando falte capacidad (como WS20) o si se abre otra; el output_scope ya acota el código a `src/sldb/...`.

## WS41
- Fijar la evidencia de «sin mutaciones cruzadas» (estado git, hash del store o ausencia de peticiones de escritura).

## WS43
- Fijar la granularidad y cantidad de átomos y cómo se arranca la UI contra el deskops real.

## WS44
- El solicitante designa al operador y registra su acceso en `autorizaciones/scion.md` antes del probe; fijar cómo se elige el Hub si hay varios.

## Añadido 2026-10-31 tras el Tester de la corrección

- WS22: fijar si «selección y links comunes con lector» exige tocar archivos fuera de board/, y cómo se abren pills y átomos.
- WS13.1: fijar la ruta de apertura sin ID, porque el explorador WS13.2 depende de este nodo.

## Añadido 2026-10-31 tras la revisión root de d9877e86

- WS35: decisión de presentación pendiente, no ambigüedad resuelta. La TaskDoc de WS35 fija si los mensajes sin intento resoluble se muestran como hueco de procedencia o se excluyen, y su aceptación, antes de ejecutar.

## Adenda 2026-11-01, corrección de procedencia

Lista completa en `runs/subagents/20261031-atribucion-decisiones/comparison-ledger.md`, sección «Para la promoción». Lo principal: el TaskDoc de WS12 debe citar T-P03.1, porque su aceptación no enumera la definición operativa de «modo manual exclusivo». Revisar además `output_scope` de WS36 y WS24, frontera de WS13.3 con `workspace.mjs`, y el caso de WS45.

## Adenda 2026-11-01, tanda sobre el parche de WS08

Lista en `runs/subagents/20261101-ws08-completitud/comparison-ledger.md`. Añade: WS09, productor por tipo cuando el campo diga «futura implementación»; WS13.1, foco en Code solo donde WS11 defina correspondencia; WS27.1, canal Git por WS12; WS39, documento sin Schema; WS31, «Pxx» son P01–P09 y T-Pxx se citan como fuente.

## Adenda 2026-11-01, decisión root sobre WS13.1 y WS12

Fuente: `runs/subagents/20261101-ws08-completitud/root-approval.md`.

- WS13.1: el scope limita el foco a la correspondencia real definida por WS11, y la aceptación circunscribe las representaciones soportadas a WS09/WS11. Seleccionar en Code, texto o graph se interpreta dentro de ese dominio. Sin mapeo, la operación se detiene y registra hueco, y eso no es aceptación satisfecha. No cerrar WS13.1 omitiendo en silencio un caso comprometido. Al promover: selecciones soportadas, correspondencias y pruebas explícitas; retirar un comportamiento comprometido exige cambio de alcance.
- WS12: T-P03.1 es obligatorio al preparar su TaskDoc. No autoriza asumir exclusividad ni inventar detección.
- Huecos declarados, sin productor en el DAG: bundle de delegación de UF06 y `Corpus.rank`. El ramal E resuelve el bundle con inventario, contrato y dueño real antes de consumirlo; no equivale a `create_task_bundle`. La semántica no se promete: WS14 admite capacidad degradada según la API real.
