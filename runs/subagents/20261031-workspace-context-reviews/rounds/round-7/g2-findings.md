### WS13.1 [2]
1. «Markdown sin modelo legible»: no define qué evidencia demuestra “legible” ni la representación mínima exigida. Obligaría a inventar el criterio de aceptación y la prueba.
2. «La selección por documento/nodo fija el foco del documento abierto»: no precisa qué foco resulta al seleccionar el documento completo —frente a un nodo— ni cómo se refleja en texto/graph/code. Obligaría a inventar la semántica de foco a nivel documento.

### WS13.2 [1]
1. «al añadir un documento al store temporal de prueba, aparece sin cambiar código»
   No fija si «aparece» significa en el árbol ya abierto, tras recarga manual o por refresco automático, ni si el mismo criterio aplica a Markdown no modelado del desk. El ejecutor tendría que inventar la semántica de actualización y el alcance de esa comprobación.

### WS13.3 [4]
1. «Abrir, cambiar y cerrar pestañas» — no se define qué documento queda activo al cerrar la pestaña activa ni cómo se ajustan foco e historia. Obliga a inventar la semántica de cierre.
2. «Volver restaura documento, foco y origen. Volver sigue el orden inverso de navegación.» — no se especifica qué acciones crean entrada de historia (cambio de pestaña, apertura en división, seguir enlace) ni cómo tratar duplicados. Obliga a inventar el modelo de historia.
3. «Pestañas, dos documentos lado a lado» y «abrir dos documentos en divisiones» — no se fija si el máximo son dos divisiones o si pueden abrirse más. Obliga a inventar el límite de disposición.
4. «Disposición por sesión de navegador; no se exige persistir tras recargar.» — no aclara si el estado es en memoria o en almacenamiento de sesión, que sí sobrevive a recarga. Obliga a inventar la implementación del estado local.

### WS17 [2]
1. **No se define qué entradas/índices ni qué huecos de navegación cubrir.** Cita: «Escribir solo entradas/índices authored como plantillas versionadas bajo el paquete del plan» y «recorrer links Markdown sin UI». La aceptación solo comprueba que los links resuelven, no qué navegación debe existir; un conjunto mínimo pasaría. Obliga a inventar el contenido y la cobertura, salvo que se delegue explícitamente al TaskDoc.

2. **No se define cómo una plantilla referencia el root/store materializado.** Cita: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» y «el generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se fija si son rutas relativas al layout de WS40, marcadores sustituibles u otra convención. Obliga a inventar el mecanismo de vinculación; si no coincide con WS40, exigiría un cambio fuera de WS17.

### WS24 [2]
1. «Vecindad = hasta 2 hops.» No fija dirección ni si incluye backlinks. Obliga a inventar el conjunto exacto de nodos/relaciones que se muestra y se prueba.
2. «preservar Code local del ticket workspace en draft que identifique el acta WS11» no aparece en `acceptance` ni define cómo comprobar esa preservación o la identificación del acta. Obliga a inventar criterio y artefacto de verificación.

### WS40 [4]
1. **«los CLI reales de deskops/sldb verificados en WS02/WS03»**: el nodo solo declara `depends_on: WS11, WS08`; si WS02/WS03 no son ancestros, falta dependencia y el ejecutor tendría que inventar que esos CLI ya están verificados.
2. **«hace commits git reales en los repos temporales»**: no fija autor, email ni configuración git; obligaría a inventar identidad de commit o asumir una configuración global no declarada.
3. **«dos repos temporales bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)»** frente a **«Incluir un tercer repo temporal sin desk»**: no dice si el tercero vive bajo el mismo root ni cómo se limpian; obligaría a inventar ubicación y política de recreación.
4. **«bajo graph_ui:.tmp/...»**: no define exclusión git ni efecto sobre el worktree de `graph_ui`; obligaría a inventar si añadir `.gitignore` o asumir que los repos anidados no contaminan el repo real.

### WS41 [2]
1. **Dependencias contradictorias con cobertura.** El nodo declara `depends_on: WS13, WS11, WS40`, pero cobertura dice: «WS41 lectura multidesk, con WS13/14/15». Obliga a inventar si WS14 y WS15 son prerrequisitos reales —especialmente para búsqueda y errores honestos— o si sus funciones quedan fuera de la aceptación de WS41.
2. **Solapamiento de `tests/`.** WS41 incluye en su alcance «views/workspace/; tests/», mientras WS40 declara «tests/fixtures/workspace_documental/; script de seed; tests/». Obliga a decidir si WS41 puede modificar fixtures o el script de WS40, o solo añadir pruebas propias; es un límite que permite exceder el alcance del corpus ajeno.
