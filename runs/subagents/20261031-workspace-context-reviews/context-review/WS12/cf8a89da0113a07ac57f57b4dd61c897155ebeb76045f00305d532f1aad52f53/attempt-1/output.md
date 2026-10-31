REFORMULACION
Propósito: cerrar en WS12 el contrato de operaciones y escritura. Resultado: `contratos/operaciones.md` con whitelist, capabilities, canales, efectos, política de escritura y huecos. Repo dueño: `deskops`. Límites: no diseñar adapters inexistentes, no implementar WS20, no commit/closeout desde HTTP, no asumir que un lock UI protege escritores CLI y no habilitar operaciones sin contrato.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, `dag.yaml` (parameters, nodo WS12 y gates); los bloques edge se usan solo como contexto, no se revisan.

Cambios previstos: redactar whitelist por campo/modelo; registrar capability exacta —operación, canal, efectos— para las mutaciones y lecturas Git de WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS32, WS34, WS36, WS39 y WS42; clasificar APIs como existentes/comprobadas o faltantes; fijar política de coordinador, Git, campos protegidos, CAS/locks, fallos parciales, permisos y closeout; registrar aceptación de `graph_ui` y, solo si `source_mode=editable`, de `sldb`; mantener G_CLOSEOUT y G_SOURCE como puertas de las operaciones afectadas.

Dependencias: WS11 y WS08, con transitivas WS07/WS02–WS10; `G_WRITE_POLICY`; `source_mode`; WS12 produce `G_UI_WRITE` y `G_SLDB_WRITE`.

Validaciones futuras: cada nodo listado debe tener capability o hueco con repo dueño; ninguna operación sin contrato queda disponible; no se presume lock compartido; `source_mode` ya no vale `pending`; las actas de aceptación existen antes de cerrar; G_WRITE_CONTRACT queda verificable. Sin ejecutar nada.

FUTURO
WS07 humano resuelve P03–P06, P04/`source_mode` y designa responsables de repos; WS11/WS08 aportan navegación y user-flows; `graph_ui` y `sldb` aceptan sus deltas; G_CLOSEOUT externo y G_SOURCE/WS20 condicionan operaciones concretas. La promoción fija TaskDoc, archivos y pruebas.
