REFORMULACION
Encargo: escribir plantillas Markdown authored de entradas/índices para el ejemplo, no generar el corpus. Resultado: archivos bajo `ejemplo/nav/` versionados en el paquete del plan y materializables por WS40. Repo dueño: deskops. Límites: solo texto curado y enlaces de recorrido; sin inventarios derivados, sin escribir repos reales, sin duplicar el registry; WS16 no depende, WS30 integra y WS43 reutiliza. Dependencias: contrato WS11 y generador/manifiesto WS40.

AMBIGUEDADES
1. "Verificar al regenerar que cada plantilla resuelve el root/store de procedencia de los dos desks" contradice "conjunto de plantillas cubre ambos desks, no cada plantilla individual". Obliga a inventar si cada plantilla debe enlazar ambos desks o solo el conjunto, y qué es la procedencia de una plantilla.
2. "conjunto de plantillas cubre ambos desks" no fija umbral: ¿un enlace por desk, todas las entradas clave del manifiesto, recorrido completo? Obliga a inventar el criterio de aceptación.
3. "Tras regenerar corpus WS40 con ejemplo/nav/" no nombra quién regenera ni autoriza a un nodo de deskops a ejecutar el generador y escribir el temp de graph_ui; tampoco fija evidencia. Obliga a inventar actor y límite de repo.

DRY-RUN
Lecturas: dag.yaml (WS17, WS11, WS40, WS30, WS43), brief.md, alcance.md, decisiones.md, cobertura.md y guía. Cambios previstos: crear plantillas Markdown en `desk/drawer/plans/workspace-documental/ejemplo/nav/`; no tocar corpus ni repos reales. Dependencias: contrato WS11; generador/manifiesto WS40; WS16 no requerido; WS30 y WS43 consumen. Validaciones futuras: regenerar corpus con plantillas, recorrer enlaces sin UI, resolver cada enlace contra WS11/manifiesto, comprobar no duplicación de registry y cobertura de ambos desks, y contrastar fuente/temporal. Sin ejecutar.

FUTURO
WS40 produce generador, manifiesto y corpus temporal; WS11, contrato de navegación; WS30 registra acta humana con plantillas/paths/hashes; WS43 publica en el desk real y registra correspondencia; el TaskDoc de promoción fija archivos, textos y casos de prueba.
