## REFORMULACION
**Propósito:** entregar el workspace documental de Deskops sobre Mindmap/SLDB/Deskops, cubriendo lector temprano, autoría/operación manual y manual publicado, con extensiones y Scion como ramales independientes.

**Resultado:** paquete integrado donde identidad/origen se conservan entre representaciones, las APIs y canales son públicos y verificables, las guardas de escritura están probadas, el manual queda trazado a versión y ningún extra opcional condiciona el núcleo.

**Repo:** `deskops` como dueño de la agrupación; receptores citados: graph_ui, SLDB y spec2viz.

**Límites:** no implementa UI, no modifica tareas de otras sesiones, no autoriza Scion ni dispatch, no convierte extras en prerrequisitos, no migra a Kimun ni promete colaboración multiusuario.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
ROOT es un agregado no ejecutable: termina cuando terminan sus hijos. Hipotéticamente:

- **PK01** produce auditorías por repo y matriz de deltas; WS01 alimenta WS02–WS04, WS06 integra evidencias y WS05 inventaria Scion. Entrega base factual a PK02/PK08.
- **PK02** consume WS06; WS07 reutiliza decisiones, WS08 define UFs, WS10 fija convención manual, WS09 cataloga vistas, WS11/W12 producen navegación y operaciones. Entrega contratos a PK03–PK05 y PK07.
- **PK03** consume WS11/WS08; WS13–WS15 implementan lector, búsqueda y errores; WS40 aporta Taller y WS41 lectura multidesk; WS16 integra el guion humano.
- **PK04** consume WS11/WS40 y WS13/WS09; WS17 publica índices, WS22/23/24 representan Board, procedimientos y conocimiento. WS18 ViewDoc queda opcional tras su gate.
- **PK05** consume WS12 y salidas de WS17/19/20/21/22/23/24/25/26/27/28/42; WS30 integra pruebas humanas de UF02–05 y navegación.
- **PK06** consume el acta WS30 y las entradas WS17; WS43 publica entradas reales y WS31 compone el manual versionado con fuentes.
- **PK07** consume WS15/24 y WS12; WS29 y WS39 se validan por sus pruebas propias, sin bloquear el manual básico.
- **PK08** consume WS05 y WS44; WS32–WS36 construyen el ramal y WS37/38 lo aceptan/publican tras permisos reales.

**Validación conjunta:** actas WS16/WS30, publicación WS43/WS31, pruebas propias de PK07 y acta WS37/WS38. Se comprueba integración de identidad/origen, APIs, guardas/canales y ausencia de dependencias opcionales sobre núcleo.

## FUTURO
Deciden o producen otros nodos: actas humanas WS16/30/37, publicación WS43/31, permisos Scion, contratos G_SOURCE/G_PAYLOAD/G_SPEC_VIEW y recibos técnicos por delta.
