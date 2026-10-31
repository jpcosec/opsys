## REFORMULACION
Propósito: convertir el borrador de user-flows en fichas verificables por UF: entrada/salida, operación real, error, nodo del DAG y gate humano, sin prometer funciones fuera de alcance ni inventar operaciones. Resultado: `borradores/user-flows.md` revisado. Repo dueño: deskops. Límites: no implementa ni ejecuta; las operaciones se extraen de auditoría vía WS06/WS07; UF08 es lectura; el ack de UF02 queda pendiente del contrato WS12; Scion/G_EXEC no se acreditan; promoción no autorizada.

## AMBIGUEDADES
1. «cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado» frente a «Cada UF tiene entrada/salida, operación, error, nodo y gate humano». La enumeración omite UF03 (conocimiento) y UF06 (delegar); obliga a decidir si el alcance es ese subconjunto o las diez UFs de `user-flows.md`, y en UF06 cómo mapear el ramal con G_EXEC/G_SCION pendientes.
2. «Nodo = ID del DAG», en singular. UF01, UF03–UF05 y UF07 tienen varios nodos y gates en `cobertura.md`/`validacion-humana.md`; obliga a inventar un nodo “principal” o un formato de lista no definido.
3. «…y gate humano» junto a «cambios (UF07/WS29)». Cobertura asigna a UF07 «prueba propia WS29» sin declararla humana; obliga a decidir si esa prueba cuenta como gate humano o a asignar uno que la fuente no nombra.

## DRY-RUN
Lecturas: brief, alcance, decisiones, cobertura, validacion-humana, `borradores/user-flows.md`, nodos WS02/03/04/07/29/39 y gates en `dag.yaml`, `auditoria/{deskops,infraestructura,ui}.md`. Cambios previstos: solo `borradores/user-flows.md`, una ficha por UF con entrada, salida, operación/nodo, error y gate, marcando huecos como tales. Dependencias: WS07 y G_PRODUCT satisfechos; auditorías por WS06 transitivo. Validaciones futuras: preflight task-only, consumo por WS09/WS11/WS12 y gates WS16/30/37/39.

## FUTURO
WS12 confirma la operación de ack de UF02; WS11 fija navegación e identidad; WS09 consume las fichas; WS29 produce su prueba de impacto; el promotor fija archivos/pills; el humano decide la promoción.
