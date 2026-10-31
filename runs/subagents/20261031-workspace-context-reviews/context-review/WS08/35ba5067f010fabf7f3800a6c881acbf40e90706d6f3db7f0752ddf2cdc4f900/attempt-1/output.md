## REFORMULACION

**Propósito:** precisar los user-flows UF01–UF10 como encargo de planificación, mapeando cada uno a operaciones reales de WS02/03/04 con entrada/salida, error, nodo y gate humano.
**Resultado:** `borradores/user-flows.md` precisado (no implementación ni UI).
**Repo dueño:** deskops.
**Límites:** no prometer función fuera de alcance; marcar hueco sin inventar; UF08 solo lectura, sin envío interdesk; ack local de UF02 pendiente del contrato WS12; no editar nodos del DAG; depende de WS07 y de G_PRODUCT.

## AMBIGUEDADES

1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: UF03/UF04/UF05 agrupan varios pasos con operaciones distintas; obligaría a inventar si se documenta una fila por UF o una por paso.
2. «nodo y gate humano» en singular: `cobertura.md` asigna varios («WS22/26», «WS16 diagnóstico; prueba propia WS29»); obligaría a inventar si se elige uno o se listan todos.
3. «cubrir manual»: no existe UF de manual en `user-flows.md`; obligaría a inventar un flujo nuevo o a reinterpretar UF05.
4. «Nodo = ID del DAG»: no aclara si es el nodo de implementación o el de validación; el campo separado «gate humano» sugiere lo primero, pero no lo fija.

## DRY-RUN

- **Lecturas:** guía, brief, alcance, decisiones, cobertura, validacion-humana, `borradores/user-flows.md`, `dag.yaml` y `auditoria/{deskops,infraestructura,ui}.md` vía WS06/WS07.
- **Cambios previstos:** únicamente `borradores/user-flows.md`.
- **Dependencias:** WS07/G_PRODUCT pendiente; operaciones por dependencia transitiva WS06/WS07; huecos de WS12 para ack.
- **Validaciones futuras:** WS09 depende de WS08; WS11/WS12 consumen el mapeo; WS16/WS30 lo verifican en recorrido.

## FUTURO

- WS07 registra P01–P09 y G_PRODUCT; el humano decide P08 y valida umbrales.
- La promoción fija TaskDoc, formato exacto de tabla y archivos.
- WS12 confirma o descarta la operación de ack local.
- WS29 aporta su prueba propia de impacto; WS09/WS11/WS12 heredan el mapeo.
