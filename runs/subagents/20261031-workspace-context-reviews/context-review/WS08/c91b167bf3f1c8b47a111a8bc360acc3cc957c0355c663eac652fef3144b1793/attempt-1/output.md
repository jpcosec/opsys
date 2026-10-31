## REFORMULACION
- **Propósito:** revisar WS08 como encargo de planificación, no como implementación ni validación del producto.
- **Resultado:** precisar `borradores/user-flows.md` para que cada UF tenga entrada/salida, operación, error, nodo y gate humano; si falta una operación, marcarla como hueco.
- **Repo dueño:** `deskops`; `output_scope: borradores/user-flows.md`.
- **Límites:** no prometer funciones fuera de alcance, no inventar operaciones ni aprobaciones, no resolver Pxx, no modificar otros repos ni ejecutar. WS07 y `G_PRODUCT` siguen pendientes; el gate pendiente es intencional.

## AMBIGUEDADES
Ninguna.

El encargo nombra el resultado, el archivo de salida, la fuente de operaciones (`auditoria/{deskops,infraestructura,ui}.md`, vía WS06/WS07), la regla ante operaciones ausentes y los límites de UF02/UF08. La aceptación es comprobable por UF y el detalle exacto de formato queda para la promoción.

## DRY-RUN
- **Lecturas previstas:** guía de revisión; brief, alcance, decisiones, cobertura, validación humana; `borradores/user-flows.md`; nodo WS08 y contratos vecinos; auditorías cuando estén disponibles.
- **Cambios previstos:** solo `borradores/user-flows.md`. Completar/ajustar por UF los campos exigidos y marcar huecos; sin código, UI ni cambios en otros repos.
- **Dependencias:** WS07/`G_PRODUCT`; auditorías WS02/03/04 vía WS06/WS07; contratos WS11/WS12; corpus WS40; validaciones WS16/WS30/WS37/WS39; deltas futuros WS29/WS32–36/WS41/WS42; `source_mode` de P04.
- **Validaciones futuras:** comprobar que cada UF tiene los cinco campos, que ninguna operación ausente se inventa y que no se promete función fuera de alcance. WS11 consume el resultado; WS16/WS30 son gates humanos posteriores.

## FUTURO
WS07 debe obtener del humano el registro de P01–P09 y satisfacer `G_PRODUCT`. WS06/WS07 aportan las auditorías; WS11 y WS12 producen contratos de navegación y operaciones; WS40 genera el corpus; WS16/WS30/WS37/WS39 realizan validaciones humanas. WS29, WS32–36, WS41 y WS42 deben producir o confirmar sus operaciones y contratos. Ninguna de esas piezas se presume aprobada ni se sustituye desde WS08.
