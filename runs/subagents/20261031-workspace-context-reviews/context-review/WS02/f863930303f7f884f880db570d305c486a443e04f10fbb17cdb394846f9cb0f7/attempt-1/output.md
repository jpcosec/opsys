## REFORMULACION
- **Propósito:** inventariar las superficies Deskops: archivos de las categorías enumeradas bajo `desk/`, comandos CLI, métodos de `DeskopsOperations` y modelos registrados en el store local `.sldb`.
- **Resultado:** `auditoria/deskops.md`, con una fila por superficie, su ubicación, todas sus operaciones públicas y estado comprobado.
- **Repo dueño:** `deskops`. Depende de WS01.
- **Límites:** no ejecutar; no inferir modelo por carpeta; no inventariar binarios ajenos; si falta el store, marcar «no comprobado» con causa.

## AMBIGUEDADES
1. «firmas públicas, efectos Git y cierre». La aceptación solo exige «ubicación» y «la operación expuesta (comando o método que la lee o muta, o “dato pasivo”)», sin definir cómo registrar los efectos Git ni qué efectos cuentan (commit, índice, hooks, push). Obliga a inventar columna, criterio y evidencia para un requisito del alcance que la aceptación no operacionaliza.
2. «modelos que sirven esas superficies». `sldb models list` enumera modelos, pero no establece qué modelo «sirve» a cada categoría enumerada; la aceptación solo prohíbe «inferir modelo por carpeta». Obliga a inventar el criterio de inclusión/exclusión de modelos.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml` (WS02/WS01), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, checkout `deskops`, store `.sldb`, salida read-only de `sldb models list` y código de CLI/`DeskopsOperations`.
- **Cambios previstos:** crear `auditoria/deskops.md`.
- **Dependencias:** WS01 (brief/glosario) y store local; si falta store, fila «no comprobado».
- **Validaciones futuras:** filas con `archivo:línea` o salida de solo lectura, sin duplicar por comando, revisión de contexto y promoción posterior. No se ejecuta nada.

## FUTURO
WS06 usará la auditoría para reconciliación y WS10 para el manual. La promoción fijará TaskDoc, archivos y pills; un humano decide la autorización. WS01 entrega el brief/glosario. No hay gate de aceptación propio en WS02.
