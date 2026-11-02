REFORMULACION
WS12 es un nodo de planificación en `deskops`: cerrar el contrato de operaciones y escritura. Su resultado es `contratos/operaciones.md`, con whitelist por operación/campo/canal/actor/revisión/Git/efectos, adapter público, política de coordinador, precondición de escritura, fallos parciales, permisos, closeout fuera del servidor UI, matriz de capacidades y huecos con dueño. Depende de WS11 y WS08, consume G_WRITE_POLICY ya satisfecho y produce G_WRITE_CONTRACT por delta. Límites: solo contrato y enlaces en deskops; no ejecuta mutaciones, no crea actas interrepo, API o modelos por reflejo.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería los inventarios WS02–04, el contrato WS11, los user-flows WS08, `decisiones.md`, `alcance.md` y las APIs/pruebas existentes citables. Redactaría `desk/drawer/plans/workspace-documental/contratos/operaciones.md` en deskops, añadiendo la matriz operación→canal→actor→revisión→efecto→prueba/recibo y registrando huecos con productor y repo. Consumiría WS11/WS08 y G_WRITE_POLICY; produciría G_WRITE_CONTRACT para los deltas de su `scope_nodes`, sin marcar `accepted_scope_nodes`. Validaría cada capacidad con path, símbolo y commit o prueba real; distinguiría contrato de acta receptora. Si falta API o conducta, se detendría, registraría el hueco y no crearía sustituto. No modificaría productos ni crearía actas.

FUTURO
P01/receptor del repo emite el acta por delta al prepararlo; WS45 verifica la precondición de payload; WS46 prueba o completa captura con origen; WS20 cubre raw-source; WS34.1/WS34.2 fijan después su política de timeout. La habilitación de mutaciones y la aceptación de cada delta quedan fuera de WS12.
