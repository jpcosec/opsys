# R4 — Dictamen final del delta (deepseek)

**Veredicto: REQUIERE CORRECCIONES.**

Verificado: `validate_plan.py --check` PASS y `build_plan.py --check` PASS (44 candidatas, 15 gates, sin ciclos; referencias con hash sin cambios). Los fixes R3 están presentes: WS41 depende de WS40; WS44 produce G_SCION y WS32 lo exige; WS30 incluye UF01/WS17; WS40 genera entrada mínima; `scope_nodes` de G_UI_READ cubre WS40/WS41; actas bajo `runs/acceptance`; `output_base` por nodo; G_SLDB_WRITE solo con fuente editable; UF02/UF08 sin envío interdesk.

## Bloqueante residual

**El operador Scion de WS44 no tiene tarea ni aceptación que lo designe.**  
`dag.yaml` WS44 exige “Responsable de instalación Scion, identificado por solicitante en WS07”, y `G_SCION` dice “resolver: WS44 por operador Scion designado en WS07”. Pero el alcance de WS07 solo designa responsables de graph_ui, sldb y spec2viz; su aceptación no exige la designación Scion, y `G_PRODUCT` solo requiere P01/P02/P07/P08/P09 y P04. `decisiones.md` añade una nota (“WS07 debe designar también al operador Scion”), pero no es un registro con actor/fecha ni condición de cierre. Consecuencia: WS07 puede cerrar y G_PRODUCT pasar sin operador Scion; WS44 llega a promoción sin el actor que su propio alcance exige y el ramal Scion queda bloqueado. Corrección: incluir la designación del operador Scion en el alcance y aceptación de WS07 y en la evidencia de G_PRODUCT (registro explícito de designación; puede ser P01 ampliado o P10), o crear un gate/tarea de designación que WS44 requiera.

## Sugerencias no bloqueantes

- `WS05` conserva “Comprobar API con probe read-only” aunque WS44 es el productor de G_SCION; aclarar que su intento es inventario y que solo el probe de WS44 cuenta, para evitar dos actas con autoridad distinta.
- `decisiones.md` afirma que los responsables de repo quedan identificados en P01, pero la fila P01 no lo menciona; alinear la nota con P01/P10 o con el alcance de WS07.

No detecto otro defecto que impida ejecutar una tarea cuando sus dependencias y gates estén satisfechos.
