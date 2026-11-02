REFORMULACION
WS47 es un encargo de implementación en **sldb**: producir la guarda HO-07 (contrato WS12, sección 6.7) que impide que una edición por campos terminada en `save_document_payload` —POST `/save` update y update local de graph_ui— reescriba el archivo perdiendo contenido no declarado. Resultado: inventario con ruta, símbolo y commit de `refuse_structural_noise`, `refuse_undeclared_frontmatter` y la guarda de `deskops edit`; guarda que reutiliza ese criterio; pruebas focalizadas y declaración de pérdidas detectadas, no detectadas y casos deshabilitados. Repo dueño: **sldb**; `output_scope` limitado a `src/sldb/api/documents/`, `src/sldb/cli/serve/` solo para la guarda y `tests/`. Límites: no amplía WS45 ni cambia la creación; no resuelve el gap de prevalidación de update del inbox de sldb; sin merge ni restauración; no se sustituye con workaround de Deskops; no promete editar todo documento con ruido.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: contrato WS12 sección 6.7/HO-07; `save_document_payload`; `create_document` y `track_document_file`; funciones de rechazo; guarda de `deskops edit`; pruebas existentes. Cambios: añadir la guarda en API/CLI de sldb y tests; inventariar antes de crear un criterio propio. Dependencias: WS12; gates `G_WRITE_CONTRACT` y `G_SLDB_WRITE` por delta. Si faltan, detenerse y registrar el hueco, sin sustituto. Si toca el mismo código del gap de prevalidación, serializar. Validación: un update con `expected` vigente que perdería contenido no declarado se rechaza con error observable y sin cambios; un update seguro —incluido documento limpio— se aplica; un `expected` obsoleto sigue dando 409; la creación no cambia. Declarar alcance detectado/no detectado/deshabilitado. Hasta que pasen, WS19.1, WS19.2 y el recorrido directo de WS26.1 no habilitan edición de documentos con contenido no declarado.

FUTURO
WS12 fija la sección 6.7 y el canal; P01/receptor emite `G_SLDB_WRITE` por delta; WS12/`G_WRITE_CONTRACT` verifica el contrato; los consumidores deciden la habilitación. No hay aprobación de implementación ni acta de uso.
