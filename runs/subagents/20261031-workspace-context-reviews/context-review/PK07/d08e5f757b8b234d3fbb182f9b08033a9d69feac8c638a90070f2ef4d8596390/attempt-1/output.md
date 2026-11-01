## REFORMULACION

**Propósito:** agrupar dos extensiones independientes del workspace documental —Changes/impacto y modelos— con evidencia propia, sin convertirlas en prerrequisito del lector ni del manual básico.

**Resultado:** paquete compuesto por WS29 (Changes con `stores check`, `doctor`, `drift check` e impacto a 1 hop sobre store temporal real) y WS39 (inspección/edición de Schema existente desde el lector, con draft/validate/promote y acta humana). PK07 no ejecuta: termina cuando ambos hijos cumplen.

**Repo:** agregado en `deskops`; hijos en `graph_ui`.

**Límites:** no añade aristas ni autoriza tareas; no presume CST/Kimun; WS29 no repara automáticamente; WS39 no reimplementa modelos ni habilita promover sin API/autoridad; ninguno bloquea lector/manual básico. La revisión de comprensión no acredita producto.

## AMBIGUEDADES

1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun.» No nombra qué manual ni qué nodo lo produce dentro de PK07. Obligaría a inventar el productor y el punto de verificación de esa etiqueta; WS39 cita WS31, pero PK07 no lo fija.

## DRY-RUN

PK07 es agregado no ejecutable. Un ejecutor futuro lanzaría sus hijos según sus propias aristas, sin orden entre sí: WS29 y WS39 son independientes y pueden avanzar en paralelo.

- **WS29:** consume WS15 (errores/modo degradado) y WS24 (grafo local/vecindad; a su vez WS13/WS09) y `G_UI_READ`. Crearía store temporal real, una mutación, consultaría la API de grafo de sldb para entrantes/salientes a 1 hop y ejecutaría los tres comandos. Cambios previstos en `frontends/mindmap/views/workspace/changes/` y `tests/`. Salida: vista de documento afectado, relaciones y hallazgos enlazados a comandos documentados, sin reparación.
- **WS39:** consume contrato WS12, lector WS13 y gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Cambios en `shell/dialogs.js`, `views/models/`, `tests/` y acta en `runs/subagents/workspace-documental-acceptance/modelos/`. Probaría el acceso desde Context del documento activo y UF09 en store temporal; salida: edición/validación y acta humana.

No hay artefacto de WS29 hacia WS39: solo comparten prerrequisitos. Integración: ambas pruebas sobre store temporal, manual que etiquete cada extensión según evidencia y comprobación de que ninguna bloquea WS13/WS16.

## FUTURO

WS31 publica el capítulo 15 del manual; el participante fijado por P08 firma el acta de WS39; `G_HUMAN_MODEL` decide disponibilidad en manual; la recepción P01 registra deltas.
