## REFORMULACION
PK07 es un paquete agregado no ejecutable que agrupa dos extensiones independientes con evidencia propia: WS29 (Changes e impacto comprobable) y WS39 (inspección/edición de modelos existentes). Su propósito es mantenerlas separadas del lector y manual básicos, sin convertirlas en prerrequisito. El resultado sustantivo del paquete es que ambos hijos cumplan sus aceptaciones y que el manual etiquete cada extensión según evidencia, sin presumir CST ni Kimun. Repo dueño de la agrupación: `deskops`; la implementación de ambos hijos pertenece a `graph_ui`. Límites: no ejecuta nada, no autoriza tareas ni añade aristas; su gate de revisión solo mide comprensión, no producto entregado.

## AMBIGUEDADES
Ninguna. Las dependencias y productores están nombrados: WS29 consume WS15/WS24; WS39 consume WS12/WS13. La ausencia de contrato o API se resuelve por las reglas comunes de alcance: detenerse y registrar el hueco, sin crear sustituto.

## DRY-RUN
Ejecución hipotética por hijos, sin orden entre ellos: no existe arista WS29–WS39, por lo que no se transfieren artefactos ni se suceden; pueden avanzar en paralelo al cumplirse sus prerrequisitos.

- WS29, tras WS15 y WS24: consume la lectura/vecindad y las rutas de integridad de WS11. Produce la vista Changes con documento afectado, relaciones entrantes y salientes a 1 hop y hallazgos agrupados por `sldb stores check`, `deskops doctor` y `deskops drift check`; enlaza al comando documentado, sin reparación automática. Valida con una mutación real sobre store temporal.
- WS39, tras WS12 y WS13: consume el contrato de operaciones y el panel Context del lector. Produce el punto de entrada desde documento activo al Schema/clase y al editor existente, y prueba inspección/mutación UF09 en store temporal, con acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`. No habilita promover si falta API/autoridad. Consume G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.
- Integración conjunta: el manual de WS31 etiqueta cada extensión según su evidencia; el capítulo 15 solo tras G_HUMAN_MODEL. PK07 cierra cuando ambos hijos aceptan; no hay validación ejecutable propia del agregado.

## FUTURO
WS31 publica y etiqueta el manual; el participante humano fijado por P08 firma el acta de WS39; G_HUMAN_MODEL se evalúa antes de marcar modelos disponibles. La promoción fija archivos y pruebas en TaskDoc. La recepción por delta corresponde al receptor P01 en el repo dueño.
