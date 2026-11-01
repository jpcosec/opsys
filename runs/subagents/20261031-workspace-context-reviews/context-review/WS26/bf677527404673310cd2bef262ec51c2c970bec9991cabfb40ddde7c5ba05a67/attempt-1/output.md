## REFORMULACION

**Propósito:** revisar WS26 como encargo de planificación, no como ejecución.
**Resultado:** un agregado no ejecutable que reúne autoría desde candidato, evidencia declarada, dependencias y binding de contexto/pills (WS26.1), más enrutamiento en Board y representación de capa lista (WS26.2), sin confundir ruta de Board con ejecución.
**Repo dueño:** `graph_ui`.
**Límites:** no implementa ni promociona por sí mismo; depende de WS12/WS22 y de sus hijos; sus gates son requisitos heredados, no aceptación conjunta; desarrollo/pruebas aisladas de API pueden avanzar, pero G_HUMAN_READ se exige antes de habilitar mutaciones en UI. La promoción queda supeditada al contrato y canal autorizado; no crea promoción nueva.

## AMBIGUEDADES

Ninguna.

El nodo es `aggregate` y su aceptación está definida como no ejecutable: se cumple cuando cumplen WS26.1 y WS26.2. Los detalles de autoría, evidencia, pills, enrutamiento y capa lista están delegados a hijos con aceptación propia. Las dependencias y gates pendientes son intencionales; WS12 es el productor del contrato y WS16/P01 los actores de los recibos humanos.

## DRY-RUN

**Lecturas previstas:** nodo WS26 y sus hijos en `dag.yaml`; vecinos WS12 y WS22; guía, brief, alcance, decisiones y cobertura.
**Cambios previstos:** ninguno; esta revisión no modifica DAG, contratos ni repos.
**Dependencias:** WS12 (contrato de operaciones/escritura), WS22 (Board navegable), WS26.1/WS26.2; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.
**Validaciones futuras:** aceptación de ambos hijos; recibos por delta en `graph_ui`; acta de lectura WS16; contrato WS12 por operación; verificación de que la capa lista separa dependencias pendientes y archivos solapados; WS30 valida el recorrido completo.

## FUTURO

- WS12 produce el contrato técnico por operación/delta y el canal autorizado.
- WS16 produce el acta de G_HUMAN_READ.
- El receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta concreto.
- WS26.1 y WS26.2 completan sus aceptaciones; entonces WS26 queda cumplido.
- WS30 ejecuta la validación humana de autoría y revisión.
