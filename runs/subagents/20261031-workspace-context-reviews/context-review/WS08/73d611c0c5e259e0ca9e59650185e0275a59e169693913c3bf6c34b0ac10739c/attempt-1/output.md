**REFORMULACION**  
Propósito: revisar WS08 como encargo de planificación para precisar user-flows y criterios observables. Resultado esperado: actualizar `borradores/user-flows.md` con cada UF y sus campos de entrada/salida, operación, error, nodo y gate humano, sin prometer funciones fuera de alcance. Repo dueño: `deskops`. Límites: nodo planning, sin implementación ni ejecución; depende de WS07 y `G_PRODUCT`; las operaciones salen de las auditorías vía WS06/WS07; `ack` local queda pendiente de WS12; UF08 es solo lectura; no se revisan los bloques edge.

**AMBIGUEDADES**  
1. «cubrir manual» junto con `output_scope: borradores/user-flows.md`. Obligaría a inventar qué “manual” debe cubrirse, si es un artefacto separado del user-flow, dónde se entrega y si WS08 puede escribir fuera de su `output_scope`. No hay nodo ni archivo de manual en el input.

**DRY-RUN**  
Lecturas: guía, brief, alcance, decisiones, cobertura, validación humana, borrador de user-flows y bloque WS08; los edge solo como contratos de contexto. Cambios previstos: ninguno ahora; al promover, solo `borradores/user-flows.md`. Dependencias: `G_PRODUCT` pendiente; operaciones por auditorías transitivas; `ack` local marcado como hueco hasta contrato WS12. Validaciones futuras: comprobar que cada UF tenga entrada/salida, operación, error, nodo y gate humano; que UF02 no dé `ack` por disponible; que UF08 no prometa envío interdesk; que UF03/UF06/UF07/UF09/UF10 no excedan alcance; que “manual” quede resuelto o registrado como hueco. Sin ejecutar.

**FUTURO**  
WS07 y el humano resuelven P01–P09, `G_PRODUCT` y `source_mode`; WS12 confirma o deja pendiente el contrato de `ack`; WS02/03/04 aportan operaciones auditadas; WS11/12 aceptan deltas; la promoción fija archivos y pruebas exactas; WS16/30/37/39 y WS29/39 aportan validaciones o pruebas propias. Nada de esto se ejecuta aquí.
