## REFORMULACION

**Propósito:** verificar si sldb ya tiene guardado reversible de documentos raw-source y, si falta o está parcial, completarlo sin duplicar productor.

**Resultado:** API pública de guardado con revisión y preservación de campos protegidos, más pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos; eso constituye G_SOURCE.

**Repo dueño:** `sldb`. **Límites:** no sobrescribir Markdown desde browser; el alcance de archivos es `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; WS20 se convierte en la tarea propia de sldb al promoverse, con el mismo delta/recibo G_SLDB_WRITE.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS20 y gates en `dag.yaml`; `brief.md`; `alcance.md`; `decisiones.md` P04; contrato WS12 `contratos/operaciones.md` cuando exista; inventario real de capacidades y tests de sldb.

**Cambios previstos:**
- Si la capacidad satisface toda la aceptación: solo pruebas que prueben el contrato completo.
- Si es parcial: completar únicamente lo faltante y volver a probar todo.
- Si falta: implementar en API/CLI de sldb mediante la tarea propia aceptada.

**Dependencias:** WS12 produce G_WRITE_CONTRACT; G_SLDB_WRITE lo resuelve el receptor humano P01 por delta; G_SOURCE lo produce WS20.

**Validaciones futuras:** roundtrip guardar/extraer sin pérdida; conflicto; recuperación tras fallo; campos protegidos; revisión de contrato; pruebas sobre store temporal real o corpus WS40.

## FUTURO

- P01 emite el acta de recepción G_SLDB_WRITE en sldb.
- WS12 entrega el contrato técnico por delta.
- La promoción fija archivos, TaskDoc y pruebas concretas dentro de esta aceptación.
- WS21 consume G_SOURCE y permanece bloqueado hasta que WS20 lo produzca.
