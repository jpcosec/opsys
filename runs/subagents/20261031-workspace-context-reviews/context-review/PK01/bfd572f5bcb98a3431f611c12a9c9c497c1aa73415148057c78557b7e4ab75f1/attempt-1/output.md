REFORMULACION
**Propósito:** fijar la base factual y una matriz de deltas verificables para no duplicar código. **Resultado sustantivo del paquete:** auditorías de superficies Deskops, infraestructura sldb/pron/spec2viz, UI graph_ui y API Scion, más `reconciliacion.md` con matriz por repo dueño (ya cubierto / extender ticket / nuevo delta), cobertura de los 64 nodos y atomización propuesta. **Repo dueño:** deskops; lecturas en `../UIs/graph_ui`, `../sldb`, `../spec2viz`, `../scion`. **Límites:** sin ejecución propia ni de producto, sin probes vivos, sin aceptar deltas ni tocar Boards ajenos, sin añadir aristas; PK01 termina cuando terminan sus hijos.

AMBIGUEDADES
1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada»: no define qué prueba el resultado integrado (¿basta WS06?, ¿hace falta consistencia cruzada entre auditorías?). Obligaría a inventar el criterio de validación del paquete.
2. «WS05 inventario Scion es independiente y alimenta E» frente a «salidas de sus hijos»: no aclara si `auditoria/scion.md` cuenta en la completitud del paquete o queda fuera de la integración. Obligaría a inventar el límite del paquete.

DRY-RUN
Hipotético: (1) WS01 verifica `brief.md` y lo deja como entrada; (2) WS02, WS03 y WS04, en paralelo tras WS01, leen `brief.md` y sus repos y producen `auditoria/deskops.md`, `infraestructura.md` y `ui.md`; (3) WS05, tras WS01, lee deskops y `../scion` y produce `auditoria/scion.md`, sin G_SCION; (4) WS06, tras WS02–WS04, integra evidencias en `reconciliacion.md`; (5) validación: cada fila con archivo:línea/commit o «no comprobado» con causa, clasificación y responsable, sin gates ni firmas. Dependencias: WS01→WS02/03/04/05; WS02/03/04→WS06.

FUTURO
WS05 alimenta el ramal E (WS32–WS34); P01/solicitante acepta deltas de graph_ui/sldb/spec2viz; WS11/WS12 enlazan actas por delta; WS44 produce G_SCION; WS07 reutiliza decisiones; WS16/WS30/WS37 validan producto.
