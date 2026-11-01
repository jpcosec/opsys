REFORMULACION
Propósito: agrupar dos entregables independientes, Changes/impacto y modelos, con evidencia propia. Resultado: WS29 integra en graph_ui una vista de Changes con mutación real, relaciones a 1 hop y errores de `stores check`/`doctor`/`drift check`, sin reparación automática; WS39 integra inspección/edición del Schema existente desde el lector, con prueba UF09 y acta humana. Repo dueño: deskops; hijos en graph_ui. Límites: PK07 no ejecuta, no añade aristas ni autoriza tareas; no bloquea lector/manual básico; no presume CST/Kimun.

AMBIGUEDADES
1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun»: no nombra qué nodo o actor etiqueta ni dónde se registra; obligaría a inventar responsable y soporte del etiquetado.
2. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada»: «integración indicada» no define artefacto ni prueba conjunta; obligaría a inventar el criterio de integración del paquete.

DRY-RUN
PK07 es agregado no ejecutable: se cumple por sus hijos, sin orden único entre ellos. Hipotéticamente, WS29 parte de WS15 (errores/modo degradado) y WS24 (vista de grafo/vecindad), consume G_UI_READ y produce la vista Changes: documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos agrupados por comando, con enlaces a la documentación correspondiente; no repara. WS39 parte de WS12 (contrato de operaciones) y WS13 (lector/Context), consume G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT y produce el acceso desde documento activo a Schema/editor existente, pruebas UF09 en store temporal, acta humana y capítulo 15 del manual. Sin arista entre WS29 y WS39: pueden avanzar en paralelo al satisfacer sus prerrequisitos y no se transfieren artefactos. Integración conjunta: cada extensión se etiqueta por su evidencia y ninguna condiciona lector/manual básico. Validación: aceptación de cada hijo; si falta contrato/API, detener y registrar hueco con repo dueño.

FUTURO
WS15/WS24 y WS12/WS13 aportan entradas; WS31 publica el manual; el participante fijado por P08 firma el acta; G_HUMAN_MODEL decide disponibilidad.
