**LECTURA PROPIA** (archivos del repo: `patch.diff`, `navegacion.md`, `review-source.md`, `sldb/.../open_store.py`)
**DATO DEL SUPERVISOR** (`tester-facts.log`): sha256 = `6a4f8518…62361e`, `status: all reviews current`, HEAD deskops `b30c24cf`.

| Objeto | Fuente | Evidencia archivo:línea | Resultado |
|---|---|---|---|
| Un solo cambio de cadena en §3.2 Validación | diff | `patch.diff:1-8` (un hunk, un `-`/`+`); `navegacion.md:93` | PASS |
| Texto exacto que da root | diff vs supervisor | `navegacion.md:93` = `review-source.md:15` (idéntico, incluidos «entrada ausente», «E-MD3 (8.5)», «antes de abrir el store, sin crearlo ni migrarlo y sin descubrimiento o fallback a otro store») | PASS |
| E-MD3 alcanzable ahora | contrato §3.2/§8.5 | `navegacion.md:93` + `navegacion.md:320` (fila E-MD3 «El alias autorizado no tiene store») | PASS |
| Alias autorizado + recurso ausente → E-MD3, no E-MD1 | contrato §3.2/§8.5 | `navegacion.md:93` y `navegacion.md:319` (E-MD1 solo «fuera del conjunto cerrado … o configuración ausente») | PASS |
| Alias fuera del conjunto sigue E-MD1 | contrato §3.2/§8.5 | `navegacion.md:94`, `navegacion.md:89` («No existe `?alias=local` … sigue dando E-MD1»), `:319` | PASS |
| Mismo caso con dos errores | contrato | `navegacion.md:94` (sin config → E-MD1) vs `:93`/`:320` (autorizado ausente → E-MD3): casos disjuntos | PASS |
| Frase no implica comprobación de arranque permanente | contrato vs decisión root | `navegacion.md:93` dice «se comprueba … antes de abrir el store» (por petición); no afirma permanencia ni check de arranque; `review-source.md:8` («tampoco deducir disponibilidad permanente de un check de arranque») | PASS |
| «Antes de abrir el store» compatible con no crear/no migrar/no fallback | contrato + código | `open_store.py:37-38` migra **solo si** `store_exists`; si falta store, la comprobación previa evita la llamada y con ella `_resolve_store_arg`/fallback (`open_store.py:32`) | PASS |
| Ninguna frase de 3.1/5.4/8.3/8.4 contradice el orden | contrato | `navegacion.md:80-82` (3.1 describe que `open_store` migra y resuelve alias), `:183-186` (5.4 obliga a no migrar como efecto de leer), `:304` (8.3), `:308` (8.4): descriptivas/obligación compatible | PASS |
| No regresión: unicidad `(root.resolve(), store.resolve())` y alias canónico | contrato | `navegacion.md:93` (texto intacto) | PASS |
| No regresión: `local` reservado y fuera del conjunto | contrato | `navegacion.md:92`, `:89`, `:94` | PASS |
| No regresión: ausencia del parámetro = desk del proceso | contrato | `navegacion.md:89` (Serialización) | PASS |
| No regresión: sin configuración no hay lectura cruzada | contrato | `navegacion.md:94` | PASS |
| No regresión: clave de sesión alias + identidad local | contrato | `navegacion.md:176` (5.3, texto intacto) | PASS |
| SHA256 resultante = aprobado | supervisor | `tester-facts.log:2` = `review-source.md:17` | PASS (dato del supervisor) |

**No pude verificar**
- Hash por cálculo propio: no hay herramienta de hash en este entorno; solo lo leo del log.
- Rutas `GU/…` y `DK/…` citadas en el contrato: `graph_ui` y el paquete `deskops` no existen en `/home/jp/proyectos`; no comprobé `workspace_routes.py:104` (503) ni los demás anclajes.
- Estado del repo, revisión fresca del consumidor y checks: solo el `status` del log, no ejecutados por mí.
- Que el archivo en disco sea el de los bytes del patch más allá de la comparación textual de la línea: verificado por lectura, no por diff calculado.

RESULTADO: PASS
