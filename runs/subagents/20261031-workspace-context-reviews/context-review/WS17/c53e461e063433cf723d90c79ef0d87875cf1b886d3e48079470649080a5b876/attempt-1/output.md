## REFORMULACION
**Propósito:** escribir las plantillas Markdown authored de entradas e índices para el corpus Taller.
**Resultado:** contenido versionado en `ejemplo/nav/`, bajo `deskops:desk/drawer/plans/workspace-documental/`.
**Repo dueño:** deskops.
**Límites:** no produce el corpus (WS40), no escribe repos reales ni el registry, no copia inventarios derivados y puede escribirse antes de WS16; WS30 las integra.

## AMBIGUEDADES
1. «el conjunto de plantillas cubre ambos desks, no cada plantilla individual»: no define qué entradas ni qué mínimo constituye cobertura; el ejecutor debe inventar el inventario de navegación y su alcance.
2. «plantillas temporales enlazan por roots/aliases del manifiesto WS40»: al ser plantillas estáticas, no se fija convención de sustitución ni layout para materializar esos roots; obligaría a inventar la sintaxis de enlace.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, nodo WS17, contrato WS11 y generador/manifiesto WS40 cuando existan.
**Cambios previstos:** crear plantillas en `ejemplo/nav/`; ninguna escritura en repos reales, registry ni corpus temporal.
**Dependencias:** contrato de navegación WS11 (identidad/roots/aliases) y generador WS40 (parámetro de plantillas y manifiesto). Regla común: si falta contrato, detenerse sin sustituto.
**Validaciones futuras:** regenerar el corpus con las plantillas, recorrer enlaces sin UI, comprobar resolución de roots/stores de ambos desks, ausencia de duplicación y de enlaces al checkout real; WS30 registra plantillas/paths/hashes y WS43 contrasta la publicación.

## FUTURO
WS40 debe aceptar la ruta de plantillas y materializarlas; WS11 debe exponer roots/aliases; WS30 valida los recorridos; WS43 publica en el deskops real; la promoción fija archivos exactos y TaskDoc. Nada autoriza ejecutar.
