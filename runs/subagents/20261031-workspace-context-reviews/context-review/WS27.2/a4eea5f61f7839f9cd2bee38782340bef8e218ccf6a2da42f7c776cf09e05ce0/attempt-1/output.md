REFORMULACION
Propósito: revisar WS27.2 como encargo de planificación. Resultado: dictamen sobre claridad de propósito, resultado, repo, límites, dependencias y aceptación comprobable. Repo dueño: graph_ui; el plan vive en deskops. Límites: no ejecutar, no evaluar producto, no revisar contratos de nodos vecinos, no inventar aprobaciones ni sustituir contratos ausentes.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, nodo WS27.2 y gate G_UI_READ; los bloques edge se tratan como contratos vecinos, no se revisan. Cambios previstos: vista de evidencia en graph_ui bajo `frontends/mindmap/views/workspace/evidence/` y `tests/`, sin modelo de comentarios nuevo. Dependencias: WS13 y WS12; WS11 cuenta transitivamente para rutas de lectura; G_UI_READ es gate per_delta pendiente, no defecto. Validaciones futuras: mostrar declarada/encontrada/verificada y sus estados distintos; evidencia ausente como ausente; declarada sin artefacto, artefacto no declarado y verificación fallida sin colapsar; reporte ausente o fallo de comando como no verificable; abrir Markdown dentro del workspace y, fuera de ese caso, mostrar ruta y declarar no soportado; recibo G_UI_READ del delta; preflight y TaskDoc de promoción.

FUTURO
WS12 produce la correspondencia por tipo de evidencia, artefactos soporte y salida pública de `deskops closeout verify`. WS11 define rutas de lectura. WS13 entrega el lector integrado. El receptor P01/solicitante emite el acta G_UI_READ por delta concreto. La promoción fija archivos, pills, átomos y pruebas dentro de la aceptación. Si falta contrato, API, dato o permiso, rige la regla común: detenerse y registrar el hueco, sin crear sustituto.
