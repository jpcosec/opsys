## REFORMULACION

Encargo de planificación (no de implementación): inventariar las superficies Deskops y sus operaciones públicas para producir `auditoria/deskops.md`. Resultado: una fila por superficie (archivo, comando público o modelo registrado) con ubicación, lista completa de operaciones que la leen/mutan —o «dato pasivo»— y estado comprobado con evidencia citada. Repo dueño: `deskops`. Límites: solo categorías enumeradas bajo `desk/` de este checkout y el store local `.sldb`; no inventariar binarios ajenos, no inferir modelo por carpeta; si falta store, informar «no comprobado» con causa.

## AMBIGUEDADES

1. «Superficie = cada archivo, comando público o modelo registrado concreto» frente a «Una fila por superficie con lista de todas sus operaciones públicas; no duplicar por comando». Obliga a inventar si cada comando/método público merece fila propia o solo aparece listado dentro de la fila de su archivo.
2. «archivos de categorías enumeradas bajo `desk/`» frente a la categoría «runs». En este checkout `runs/` está en la raíz, no bajo `desk/`; obliga a decidir si `runs` queda incluido, excluido o solo su posible `desk/runs`.

## DRY-RUN

Lecturas: `dag.yaml` (nodo y arista WS01), `brief.md`, `alcance.md`, `decisiones.md`; árbol read-only de `desk/`; `sldb models list`; código de comandos CLI y de `DeskopsOperations`; `deskops closeout verify|commit` como superficies. Consumo de WS01: verificar hash/alcance del brief ya authored; no reescribirlo. Sin gates (`requires: []`). Cambios previstos: crear/actualizar únicamente `auditoria/deskops.md` con filas ubicación/operaciones/estado. Errores esperados: store `.sldb` ausente o ruta de categoría inexistente → filas «no comprobado» con causa, sin abortar. Validación futura: toda categoría enumerada tiene filas, ninguna inferencia por carpeta, cada estado comprobado cita archivo:línea, hash/listado o salida read-only, y no hay binarios ajenos.

## FUTURO

WS06 consume esta auditoría para su matriz de correspondencia por repo dueño; WS10 la usa para el índice del manual. La promoción a TaskDoc (archivos exactos, pills, evidencia) la decide el coordinador humano; ninguna ejecución está autorizada.
