REFORMULACION
El nodo encarga probar la composición pública de captura a drawer y protoátomo en deskops, verificando tres propiedades: origen preservado (ruta o mensaje), ninguna tarea activa y colisión controlada. Si la composición no cumple, debe completar solo la conducta faltante y volver a probar todo el contrato. Resultado: inventario con ruta/símbolo/commit y pruebas reales separadas para cada destino, con store temporal. Repo dueño: deskops. Límites: no mutar el desk real, no crear tarea activa, no imponer wrapper/API/modelo por reflejo; depende de WS12 y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «completar la conducta que falte, con tarea propia en deskops»: no identifica la tarea ni si debe existir antes, crearse o autorizarse. Obligaría a inventar su ID, canal de alta y si WS46 queda bloqueado hasta tenerla.
2. «No se impone wrapper ni modelo nuevo antes de demostrar que hacen falta»: no fija quién o cómo demuestra esa necesidad ni si, demostrada, WS46 puede crear API/modelo. Obligaría a inventar el criterio y el límite del cambio.
3. «incluso si el archivo existe sin estar rastreado»: se aplica al protoátomo, pero brief no establece que se persista como archivo. Obligaría a inventar la forma de almacenamiento y la condición de colisión del protoátomo.

DRY-RUN
Lecturas: contrato WS12 (sección 7, HO-11/HO-11b), estado de G_WRITE_CONTRACT, API SLDB (`/docs/create`, `create_document`), `DrawerService`, `deskops/services/drawer.py`, `domain_tree.py`, `cli/commands/atoms.py` y tests existentes. Cambios previstos: escribir inventario; añadir en `deskops/tests/` pruebas de candidato y protoátomo con store temporal; si falla alguna propiedad, editar mínimamente los archivos listados y repetir el contrato completo. Dependencias: WS12 y G_WRITE_CONTRACT per_delta con WS46 en `accepted_scope_nodes`; representación de origen y colisión del contrato. Errores: gate/contrato ausente o no aceptado para WS46 → detenerse y registrar hueco con dueño; composición parcial → completar solo lo faltante. Validación esperada: origen visible tras recargar, sin tarea en Board ni `list tasks`, colisión rechazada sin sobrescribir, inventario con commit; si hubo cambios, reejecutar todas las pruebas.

FUTURO
WS12 produce el contrato y la aceptación per_delta de G_WRITE_CONTRACT para WS46. La promoción sigue `not_authorized`: un humano debe autorizarla y el TaskDoc fijará archivos, casos y textos. WS25.2 consume la capacidad probada; no la produce.
