REFORMULACION

Propósito: cerrar en deskops el contrato técnico de operaciones y escritura del workspace como encargo de planificación. Resultado: `contratos/operaciones.md` con whitelist lectura/mutación por operación/campo/canal/actor/revisión/Git/efectos y estado comprobado/faltante; representación de la precondición; locks, fallos parciales, permisos y closeout; captura drawer/protoátomo; y, por delta Scion, política y umbral de timeout. Repo dueño: deskops. Límites: solo contrato y enlaces; no muta, no crea actas interrepo, API, modelo ni wrapper, no aprueba canales y no espera recibos de otros deltas. Depende de WS11 y WS08; G_WRITE_POLICY ya está satisfecho. No es agregado: produce un contrato.

AMBIGUEDADES

ninguna.

DRY-RUN

Lecturas: WS12 y aristas WS11/WS08 en `dag.yaml`; brief, alcance, decisiones y cobertura; contratos/inventarios WS02–04, WS11, WS08 y evidencia API/prueba citada. Cambios previstos: crear/actualizar `contratos/operaciones.md` y enlaces en deskops. Construir matriz por operación/campo/canal/actor/precondición/Git/efecto/estado; elegir y justificar la precondición; documentar captura comparando API/composición/wrapper; asignar huecos con productor nombrado (WS20/45/46/47/48, WS34) sin sustituirlos; incluir la sección de timeout por delta. Dependencias: consumir salidas WS11/WS08; no producir actas P01 ni mutaciones. Gates: G_WRITE_POLICY satisfecho; G_WRITE_CONTRACT `per_delta` queda pendiente y no exige aceptación conjunta. Errores: inventario, contrato o evidencia de API ausente → detener y registrar hueco con repo dueño, sin inventar sustituto. Validación esperada: contrato revisable con citas path/símbolo/commit, matriz completa, huecos asignados y límites explícitos; sin ejecutar pruebas de producto.

FUTURO

WS07 ya registró G_WRITE_POLICY. P01 y los repos receptores emitirán actas por delta; WS45 verificará la precondición; WS46–48 producirán captura, guarda y admisión; WS34.1/34.2 consumirán la política de timeout; WS19/25/26/28/39/42 consumirán la whitelist. G_WRITE_CONTRACT se aceptará por delta.
