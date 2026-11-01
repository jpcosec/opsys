## REFORMULACION

**Propósito:** comprobar si sldb ya guarda de forma reversible un documento raw-source por API pública, con revisión y preservación de campos protegidos, y completar solo lo que falte.
**Resultado:** capacidad verificada o implementada en sldb (`src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`), con API pública y tests de roundtrip, conflicto, recuperación y campos protegidos; produce G_SOURCE.
**Repo:** sldb. No se toca UI ni se sobrescribe Markdown desde browser.
**Límites:** solo raw-source; la precondición de escritura de payload por campos es hueco separado de WS45; si la capacidad existe no se duplica código; al promoverse se convierte en tarea propia, hoy no autorizada.

## AMBIGUEDADES

1. Cita: «recuperación tras fallo» y, en decisiones, «buffer recuperable ante conflicto/fallo». Obliga a inventar dónde reside el buffer (servidor sldb o cliente), su canal y qué prueba demuestra recuperación.
2. Cita: «tests de roundtrip, conflicto, recuperación» frente a «la precondición de escritura de payload por campos es un hueco separado, producido por WS45». Obliga a decidir si WS20 prueba un conflicto de raw-source con precondición propia o espera WS45; ambas lecturas inventan alcance o prueba.
3. Cita: «conserva campos y secciones sin pérdida» y «se extrae/valida». El brief admite documentos sin contrato estructurado; obliga a inventar qué campos/secciones son la unidad de preservación y qué significa extraer en Markdown sin contrato.

## DRY-RUN

**Lecturas:** guía; brief; alcance; decisiones P04/G_SOURCE; dag.yaml (WS20 y contratos vecinos, sin revisarlos); `task-ws20.md`; en sldb `src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`; inventarios citados WS02–04/WS11.
**Cambios previstos:** primero verificar capacidad existente; si cumple la aceptación, solo añadir/linkar tests; si falta o es parcial, implementar o completar API pública y revalidar todo el contrato.
**Dependencias:** WS12/G_WRITE_CONTRACT; acta G_SLDB_WRITE; WS45 como productor separado de precondición de payload.
**Validaciones futuras:** roundtrip, conflicto, recuperación, campos protegidos; evidencia de G_SOURCE; verificación per_delta; convergencia con WS12.

## FUTURO

- El solicitante P01 emite el acta G_SLDB_WRITE en el repo sldb.
- WS12 verifica G_WRITE_CONTRACT para el delta WS20.
- WS45 publica la precondición de payload; WS21 queda bloqueado por G_SOURCE y G_PAYLOAD_PRECONDITION.
- La promoción fija TaskDoc, archivos, pills y preflight; la validación humana corresponde a WS30; la capacidad existente se constata en ejecución, no aquí.
