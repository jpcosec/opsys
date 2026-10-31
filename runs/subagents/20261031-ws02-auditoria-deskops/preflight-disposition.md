# Comparación del coordinador — WS02, aceptada para despacho

Revisiones: preflight y cold v1–v4, cada una en proceso Pi nuevo, sin herramientas y con stdin DEVNULL (recibos `*-receipt.json`). El insumo final es la TaskDoc vigente; `preflight.md` guarda la reformulación final, copia de `preflight-v4.md`.

Las cuatro rondas reproducen el objetivo, el entregable único, el repo y los límites: solo lectura, sin Scion, sin contratos nuevos, sin commits del Executor. Ningún revisor confundió la tarea con implementación ni propuso ejecutar fuera del alcance. v1–v3 detectaron lagunas reales (columnas, universo, hash, roles, atribución) y se corrigieron en la TaskDoc con `deskops edit task`. Los hallazgos de v4 son detalle o quedan resueltos aquí; estas resoluciones obligan al Executor y al Tester.

## Resoluciones sobre v4
- La columna efecto admite también «mutación store .sldb», y efecto Git incluye cualquier otra operación Git que el comando haga, nombrada tal cual; la lista de la TaskDoc no es cerrada.
- Comando y método son filas distintas. classmethod y staticmethod cuentan como método público.
- Fases: buscar también «fase». Un archivo no UTF-8 dentro del universo se lista y se marca «no comprobado» con esa causa.
- La carpeta de este run se excluye de runs-inventory.tsv y se dice.
