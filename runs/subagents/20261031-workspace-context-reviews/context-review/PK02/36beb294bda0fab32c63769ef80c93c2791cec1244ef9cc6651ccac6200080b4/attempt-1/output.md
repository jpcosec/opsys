REFORMULACION  
PK02 es un paquete de planificación, no una tarea ejecutable. Propósito: cerrar decisiones y contratos de producto, navegación y operaciones que permiten preparar cada delta del workspace documental. Resultado: registro P01–P09 reutilizado, UFs precisadas, catálogo de representaciones, convención de manual, contrato de navegación/identidad y contrato de operaciones/escritura. Repo dueño: deskops. Límites: no implementa UI/API, no ejecuta mutaciones, no crea actas interrepo, tareas ni aristas; no autoriza Scion; la edición sigue condicionada a G_SOURCE. PK02 termina cuando terminan sus hijos.

AMBIGUEDADES  
ninguna

DRY-RUN  
Al ser `aggregate`, no produce archivos propios: su ejecución hipotética es la de sus hijos y su integración. Lecturas: `dag.yaml`, `decisiones.md`, `brief.md`, `alcance.md`, `cobertura.md` y auditorías disponibles por WS02–WS04/WS06. Cambios previstos: solo los `output_scope` de los hijos.

Orden por aristas: WS07 reutiliza decisiones contra WS06 y deja registro P01–P09. WS08 consume WS07 y auditorías transitivas; produce `borradores/user-flows.md` con UF01–UF10, operaciones, errores, nodos y gates, marcando huecos. WS10, que además espera WS02, produce `borradores/manual.md` con índice, convención y disponibilidad; puede avanzar junto a WS08 tras WS07. WS09 consume WS07, WS08 y WS10; produce `borradores/vistas.md` con origen, contrato, renderer, acción/dueño, error y estado por fila. WS11 consume WS08/WS09; produce `contratos/navegacion.md` con identidad, origen, foco, enlaces, multidesk y clasificación de huecos. WS12 consume WS11/WS08; produce `contratos/operaciones.md` con whitelist, adapter, policy, precondición y efectos.

Validación integrada futura: revisar trazabilidad Pxx, que cada UF tenga operación/error/nodo/gate, cada vista origen/contrato/estado, cada hueco productor, y que operaciones/escrituras no supongan APIs ni permisos no probados. Si falta un insumo, el hijo afectado registra el hueco y se detiene; no se inventa sustituto.

FUTURO  
WS02–WS04/WS06 aportan auditorías y reconciliación; P01 decide y produce actas de recepción por delta; WS20 produce G_SOURCE; WS45 verifica la precondición de payload; WS40 aporta el corpus Taller. Las aceptaciones de producto y pruebas humanas corresponden a WS16/30/37/39 y al solicitante, no a PK02.
