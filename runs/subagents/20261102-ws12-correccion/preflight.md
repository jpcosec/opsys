## REFORMULACION

**Objetivo:** aplicar 8 hallazgos y decisiones A–E de la revisión root en `desk/drawer/plans/workspace-documental/contratos/operaciones.md` y proponer en `dag.yaml` productores, dependencias, aceptaciones y gates mínimos; congelar y entregar a root antes de renovar revisiones.

**Alcance:** superficies `contratos/operaciones.md`, `dag.yaml` (solo propuesta canónica mínima) y `runs/subagents/20261102-ws12-correccion/`. Autoridad: `review-source.md` sobre el resumen del TaskDoc.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`.

**Límites:** sin ejecutar productores, sin UI/SLDB/Scion/push, sin CAS universal, sin modelo/API/servicio de identidad nuevos, sin tocar helper/validadores/fuentes comunes, sin preguntar al solicitante, sin cerrar fase ni G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «Regenerar derivados» (Implementation Path §4): no enumera qué derivados ni comando. Obligaría a inventar artefactos y orden; Validation solo cita `build_plan.py --check` y `context_review.py status`.
2. «medición de invalidación» (Alcance/parada): sin métrica ni procedimiento. Inventar umbral y método.
3. Decisión B: «preferentemente dentro de WS45 solo si mantiene un entregable coherente… si requiere unidad separada, propón nodo atómico». Criterio no objetivo; obliga a inventar el umbral WS45 vs nodo.
4. Decisión C: «productor común explícito… sin ponerla exclusivamente dentro de WS19.1» no indica nodo ubicación. Inventar destino.
5. Decisión D: «primero probar composición pública… sin ejecutar productores»: tensión entre probar y no ejecutar. Inventar qué cuenta como prueba.
6. Hallazgo 2: «Captura el gap de SLDB en su inbox» sin ruta/formato de inbox. Inventar ubicación.
7. Matriz: no define valor cuando no hay productor (hallazgos 5/6). Inventar «N/A» o equivalente.
8. «dag.yaml y sus derivados»: «derivados» indefinido (¿navegacion.md?).

## DRY-RUN

Ejecutor futuro: (1) leer `review-source.md` y contrastar §§1–13 de `operaciones.md`; (2) parchear hallazgos 1–8 y A–E en `operaciones.md`; (3) editar `dag.yaml` añadiendo nodos productores/dependencias/aceptaciones/gates mínimos; (4) regenerar derivados (lista a fijar antes; si no, error de alcance); (5) medir invalidación (métrica a fijar); (6) generar matriz hallazgo→cambio→productor→consumidor; (7) escribir `tester-result-summary.md` vía Tester solo-lectura; (8) `git diff`, hashes y congelar sin commit de cierre ni renovación. Errores esperables: `build_plan.py --check` falla por referencias dag sin resolver; hueco de inbox SLDB sin ruta; discrepancia si productores alteran compromisos humanos (debe exponerse). Resultado esperado: contrato corregido, dag propuesto, matriz e invalidación medidas, G_WRITE_CONTRACT pendiente, entrega a root.
