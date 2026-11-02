REFORMULACION
WS12 es un encargo de planificación en `deskops`: cerrar el contrato de operaciones y escritura en `contratos/operaciones.md`. Debe fijar whitelist por campo/modelo/operación/canal/actor/revisión/Git/efectos, adaptador público existente, política de coordinador, campos protegidos, precondición de escritura de payload, fallos parciales, permisos y closeout fuera del servidor UI; además, matriz de capacidades/efectos/huecos y mapa de recibos por delta. Límites: solo contrato y enlaces en deskops; no implementa mutaciones, no crea API/modelo ni actas interrepo; si falta canal o conducta, registra hueco y dueño.

AMBIGUEDADES
1. «La duración no se elige ahora: esa sección del contrato WS12 la fija al preparar esos deltas, no WS34» junto con «asume producir... la política y el umbral de timeout». Obliga a inventar si el contrato se cierra con umbral vacío, quién lo fija después y con qué evidencia; no hay actor ni criterio de cierre para esa sección.

DRY-RUN
Lecturas: guía, `dag.yaml`, brief, alcance, decisiones, cobertura; `WS08 borradores/user-flows.md`, `WS11 contratos/navegacion.md`, auditorías WS02–04 y APIs/pruebas existentes citadas. Cambios: redactar `contratos/operaciones.md` con whitelist, adaptador, política, precondición, fallos, permisos, closeout, matriz y huecos; dejar constancia de secciones diferidas. Dependencias/gates: consumir `G_WRITE_POLICY` ya satisfecho; no declarar `G_WRITE_CONTRACT` globalmente satisfecho, solo contrato por delta; `G_UI_WRITE`/`G_SLDB_WRITE` quedan a recibos externos. Validación: cada capacidad con path/símbolo/commit o hueco con dueño; ninguna mutación marcada disponible; ninguna acta creada. Errores: falta WS08/WS11, auditoría o evidencia real → detener y registrar hueco, sin sustituto.

FUTURO
WS45 verifica la precondición; WS46 prueba captura; WS47 aplica la guarda; WS48 admite escrituras. Receptores P01 emiten actas por delta; WS34.1/WS34.2 fijan el umbral de timeout al prepararse. Humanos deciden recibos y habilitación de mutaciones.
