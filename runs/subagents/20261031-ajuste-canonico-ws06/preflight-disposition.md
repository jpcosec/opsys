# Comparación del coordinador — consolidación canónica, aceptada para despacho

Preflight y cold en procesos Pi nuevos, sin herramientas y con stdin DEVNULL. Ambas reproducen objetivo, archivos permitidos, puntos A-F, roles y límites. Ninguna propone código, ni tocar P01-P09, ni activar WS07. La TaskDoc no cambia.

## Resoluciones, obligan a Executor y Tester
- Helper imprescindible: solo si build, validate o render no pueden expresar un cambio de A-E. Ninguno previsto; si hiciera falta, se reporta antes de tocarlo. Nunca se relaja una aserción.
- Proyecciones: `build_plan.py` regenera tabla, fichas y spec del diagrama; `render_diagram.py` regenera el diagrama; `validate_plan.py` sin --check regenera validation.txt. Se commitean junto al plan.
- WS45: owner sldb, output_base sldb:repository_root/, depends_on WS12, requires G_SLDB_WRITE y G_WRITE_CONTRACT, paquete coherente con WS20 según validate_plan. status candidate, estimate S o M, context_review pending. Su salida es un inventario y pruebas focalizadas primero; código solo si al ejecutarlo falta capacidad.
- Consumidores de WS45: los nodos que guardan payload por campos, identificados por su efecto en dag.yaml y citados uno a uno en result-summary.md. Ningún lector se conecta. Si se usa un gate técnico, lleva produced_by WS45, estado pending y evidencia concreta, sin satisfacerlo. Los nodos solo raw-source siguen con WS20 y G_SOURCE.
- Afectado = lo que liste `context_review.py status` tras congelar, incluidos pending, además de ROOT, PK* y agregados que el Supervisor corre aunque no cambien.
- Ejecutar context_review.py no es ejecución de producto: `execution_authorized=false` se mantiene.
- Tester: Pi deepseek-flash de solo lectura en Herdr, informe con `RESULTADO: PASS` o `FAIL` en última línea.
- Ruta de `git diff` de validación: desde la raíz del repo deskops, `deskops/` es el paquete de código.
