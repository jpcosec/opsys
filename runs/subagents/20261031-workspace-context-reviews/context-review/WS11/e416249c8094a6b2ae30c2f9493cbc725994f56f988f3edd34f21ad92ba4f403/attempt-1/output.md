REFORMULACION
Propósito: cerrar el contrato de navegación e identidad documental (identidad/ruta/modelo opcional, foco, enlaces/historia, resolución repo/store y lectura multidesk). Resultado: `contratos/navegacion.md` en `deskops`. Límites: es planificación; no implementa UI, no migra a Kimun, no crea sustitutos de API y no publica el contrato como cerrado sin recepción de graph_ui/spec2viz.

AMBIGUEDADES
1. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer» y «Clasificar huecos sin modelos hipotéticos». No se define el universo de huecos ni el criterio de completitud: WS08/WS09 aportan flujos y catálogo, pero no se exige que el contrato enumere todos los huecos derivados de ellos. El ejecutor tendría que inventar el inventario de huecos y cuándo queda “resuelto” cada uno.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, nodo WS11 y gates G_UI_READ/G_SPEC_VIEW. No reviso los bloques edge vecinos.
Cambios previstos: redactar `contratos/navegacion.md`; fijar identidad/ruta/modelo opcional, origen de nodos graph/code, foco, enlaces/historia, resolución repo/store y multidesk read-only; clasificar huecos. Sin código ni migración Kimun.
Dependencias: WS08, WS09 y G_PRODUCT (WS07); aceptación de graph_ui y spec2viz. G_UI_READ y G_SPEC_VIEW siguen pendientes.
Validaciones futuras: actas con sus `scope_nodes`; comprobar que cada hueco tenga tipo y dueño; confirmar ausencia de migración implícita; consumo posterior por WS12, WS13, WS18, WS40 y WS41.

FUTURO
WS07 designa responsables y registra P01/P07/P04; WS09 entrega catálogo; WS08 entrega flujos; graph_ui y spec2viz aceptan deltas; el humano decide las Pxx; WS12 fija la whitelist de operaciones; los nodos de implementación consumen el contrato. Los gates pendientes no son defecto de WS11.
