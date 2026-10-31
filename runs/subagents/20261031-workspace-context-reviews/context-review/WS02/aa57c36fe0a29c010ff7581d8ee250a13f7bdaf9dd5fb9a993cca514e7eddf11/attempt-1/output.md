## REFORMULACION

**Propósito:** inventariar las superficies concretas de Deskops —archivos, comandos públicos y modelos registrados— con la operación que exponen y su estado comprobado.

**Resultado:** `auditoria/deskops.md`, con una fila por superficie.

**Repo dueño:** `deskops`.

**Límites:** solo lectura y evidencia citada; no inferir modelos por carpeta; lo no comprobado se marca con causa; no ejecutar cambios; respetar `output_scope`; depende de WS01.

## AMBIGUEDADES

1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» y «inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs»: no delimita si «archivo» incluye código fuente, planes, TaskDocs o solo datos runtime, ni la profundidad del inventario. Obliga a inventar el universo inventariable.

2. «Cada fila incluye ubicación (archivo o símbolo de código) y operación expuesta»: para un archivo Markdown o un dato no define qué cuenta como operación expuesta —lectura, comando que lo muta o método de API—. Obliga a inventar el vínculo archivo→operación.

3. «firmas públicas, efectos Git y cierre»: «efectos Git» no especifica qué efectos ni qué comandos entran; con aceptación de estado comprobado, obliga a decidir el alcance de esa comprobación sin ejecutar.

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, nodo WS02 y arista WS01 en `dag.yaml`.

**Cambios previstos:** crear `auditoria/deskops.md` con filas de superficies, ubicación, operación y estado.

**Dependencias:** WS01 debe aportar brief y glosario autosuficientes; no hay gate asociado a WS02.

**Validaciones futuras:** cada fila con ubicación y operación; estado respaldado por `archivo:línea` o salida de solo lectura; lo no comprobado con causa; ausencia de modelos inferidos por carpeta.

No se ejecuta ninguna lectura ni comando.

## FUTURO

WS06 consumirá la matriz para proponer correspondencias por repo; WS10 reutilizará las auditorías WS02–WS04. La promoción y el TaskDoc de WS02 requieren autorización humana y preflight específico. `G_PRODUCT` afecta a WS10, no a este nodo.
