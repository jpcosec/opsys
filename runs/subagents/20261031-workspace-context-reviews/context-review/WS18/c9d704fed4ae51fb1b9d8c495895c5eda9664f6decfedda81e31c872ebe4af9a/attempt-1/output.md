## REFORMULACION
El encargo de WS18 es declarar ViewDoc y NotationDoc concretos, reutilizables, para selecciones y notación ya soportadas por spec2viz, y comprobarlos con el evaluador existente `evaluate_view` y las rutas `/api/views` de graph_ui, junto con `resolve_documents`. El resultado son datos authored y pruebas en `spec2viz`, dueño del repo, dentro de `sldb/views/` y `tests/`. Límites: no crear portabilidad genérica, servicio, CLI o runtime fuera de graph_ui; no extraer ni compartir el evaluador; no crear UI declarativa ficticia; no elegir selecciones por cuenta propia; deskops no escribe en spec2viz. La TaskDoc se promueve y ejecuta en spec2viz por su supervisor/Executor.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el nodo, el catálogo WS09, el contrato WS11, las capacidades WS03 y las filas C-37/C-49 de `reconciliacion.md`, además del código existente de `evaluate_view`, `resolve_documents` y `/api/views`. Crearía NotationDoc/ViewDoc concretos bajo la ruta y registro que confirme el contrato al promover, y pruebas en `tests/`; no modificaría el evaluador ni añadiría servicio o CLI. Consumiría de WS09 la selección mínima y de WS11 el contrato de navegación; si el catálogo no fija selección, se detendría y corregiría ese contrato, sin inventar una. Requiere el acta G_SPEC_VIEW `per_delta` del receptor P01 para ese alcance, con commit verificable; su ausencia impide promover/ejecutar ese delta, no los demás. Validaría sobre un store real que la selección evaluada coincide con WS09/WS11, que el ViewDoc documenta qué selecciona y que no se atribuye equivalencia de payload completo entre dos stores. Un fallo de evaluación o una selección no respaldada invalida la aceptación. La TaskDoc fijará archivos, escenarios y textos de prueba.

## FUTURO
WS09 debe fijar la selección mínima; WS11, el contrato y enlace; WS03, las capacidades contrastadas. P01/receptor del repo emite el acta G_SPEC_VIEW por delta. El supervisor/Executor de spec2viz promueve y ejecuta la TaskDoc; un humano autoriza la promoción.
