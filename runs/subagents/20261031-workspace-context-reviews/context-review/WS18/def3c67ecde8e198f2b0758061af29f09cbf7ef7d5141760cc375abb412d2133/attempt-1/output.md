REFORMULACION
Propósito: revisar si WS18 se entiende como encargo de planificación para declarar ViewDoc y NotationDoc concretos, reutilizando el evaluador y las rutas existentes de graph_ui y la notación de spec2viz. Resultado: veredicto de claridad, sin ejecutar. Repo dueño: spec2viz; este paquete documental de deskops no escribe allí. Límites: no evaluar producto, no revisar contratos vecinos, no reabrir decisiones registradas, no inventar selección ni sustituir contratos; el gate pendiente es intencional.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS18, gate G_SPEC_VIEW e instrucción. Cambios previstos: ninguno; solo informe. Dependencias: WS09 y WS11 como fuentes de catálogo y contrato; capacidades WS03 contrastadas a través de esos contratos; G_SPEC_VIEW per_delta pendiente. Validaciones futuras: que los ViewDoc y NotationDoc se evalúen con el camino existente de graph_ui sobre un store real; que la selección coincida con la declarada; que el ViewDoc documente qué selecciona; que la TaskDoc se promueva y ejecute en spec2viz con recepción G_SPEC_VIEW del delta. No se alega que una prueba con dos stores demuestre el mismo payload completo.

FUTURO
WS09 debe fijar el catálogo y la selección mínima; WS11 debe cerrar el contrato de navegación e identidad y sus enlaces; WS03 aporta las capacidades contrastadas. Si falta la selección mínima, se detiene la promoción y se corrige el contrato, no se inventa. La TaskDoc, los archivos exactos, pills/atoms y el preflight los fija la promoción; el supervisor/Executor de spec2viz promueve y ejecuta. P01 o el receptor del repo emite el acta G_SPEC_VIEW por delta. El store real será el temporal de prueba o el corpus WS40 cuando exista.
