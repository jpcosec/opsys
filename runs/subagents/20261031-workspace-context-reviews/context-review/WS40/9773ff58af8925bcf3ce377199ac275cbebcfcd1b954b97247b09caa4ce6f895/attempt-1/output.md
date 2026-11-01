REFORMULACION
WS40 es un encargo de implementación en graph_ui, no un agregado: versionar un generador reproducible que, con el contrato WS11 y los CLI reales de deskops/sldb, cree un corpus Taller aislado —dos repos/desks temporales y un tercer repo sin desk— con Markdown no modelado, Code local, referencia rota, entrada mínima, FAQ, README de arranque, enlaces entre desks y manifiesto JSON. Debe hacer commits reales solo en repos temporales y nunca tocar un desk real. Límites: no produce el contenido authored de WS17 ni sustituye la validación de WS16; las plantillas WS17 son opcionales; no implementa UI. Repo dueño: graph_ui; alcance: tests/fixtures/workspace_documental/, script de seed y tests/. Depende de WS11, WS08 y G_UI_READ.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: dag.yaml, guía, brief/alcance/decisiones, contrato WS11, user-flows WS08, TaskDoc promovido, repo graph_ui y disponibilidad de CLI deskops/sldb verificados en WS02/WS03.
Cambios: crear script generador y fixtures/tests; en ejecución, crear directorios temporales aislados, inicializar git, usar CLI reales para stores/documentos, generar dos desks con Board/FAQ/conocimiento, tercer repo sin desk, Markdown no modelado, Code local, referencia rota y enlaces entre desks; aceptar opcionalmente plantillas WS17; escribir README/instrucciones; imprimir manifiesto JSON con roots, stores, commits y documentos clave; hacer commits solo en temporales.
Dependencias: contrato WS11 para identidad/enlaces; WS08 para recorridos; CLI verificados; G_UI_READ por delta.
Errores esperados: falta de contrato/CLI, ruta de plantillas inválida, fallo de git, intento de escribir fuera de tmp, referencia rota no declarada.
Validación: ejecutar el comando desde cero dos veces, comprobar manifiesto, commits git, árboles temporales, enlaces, ausencia de escritura en desk real y de servidor fake; tests reproducibles.

FUTURO
WS17 aportará plantillas authored y regenerará el corpus; WS16 validará lectura con humano; WS30 usará el corpus para edición; WS41 consumirá los enlaces entre desks; el solicitante P01/receptor de graph_ui emitirá el recibo G_UI_READ del delta. Nada de esto se decide aquí.
