REFORMULACION
WS11 es un encargo de planificación para cerrar el contrato de navegación e identidad documental. Debe producir `contratos/navegacion.md` en `deskops`, clasificando huecos y fijando resolución repo/store, foco, enlaces/historia y lectura multidesk. Depende de WS09 y WS08, y requiere G_PRODUCT. Límites: no implementa UI, no migra a Kimun, no modifica repos ajenos y no publica el contrato como cerrado sin aceptación de graph_ui y spec2viz; si falta recepción, queda pendiente.

AMBIGUEDADES
1. «Un documento Markdown mantiene identidad/ruta/modelo opcional». No se define qué compone la identidad —ruta, ID estable, hash o clave por store— ni cómo se resuelve entre repos. Obligaría a inventar la semántica de identidad que luego WS13.1 debe mostrar y WS41 usar en multidesk.
2. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer». Solo se definen instancia y vínculo; no hay criterio para distinguir consulta, API y renderer. Obligaría a inventar la taxonomía y, con ella, cuándo un hueco genera una dependencia nueva.
3. «si falta API abrir dependencia acotada del repo dueño antes de code». No se fija qué hace “acotada” ni cómo identificar al dueño si la API faltante no pertenece a un repo ya nombrado. Obligaría a inventar alcance y propietario de la dependencia.
4. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk». WS41 exige aliases/roots «explícitamente autorizados en contrato WS11», pero no se indica quién autoriza, con qué formato ni qué límites. Obligaría a inventar la política de autorización multidesk.

DRY-RUN
Sin ejecutar: lecturas de guía, brief, alcance, decisiones, cobertura y nodo/gates WS11. Cambios previstos: redactar `contratos/navegacion.md`, clasificar huecos, registrar dependencias API acotadas y preparar evidencia de G_UI_READ/G_SPEC_VIEW. Dependencias: catálogo WS09, flujos WS08, G_PRODUCT vía WS07 y responsables designados de graph_ui/spec2viz. Validaciones futuras: aceptación de ambos deltas, ausencia de migración Kimun implícita y contrato pendiente si falta recepción. Los gates pendientes son intencionales.

FUTURO
WS07 registra P01/P02/P07/P08/P09 y designa responsables; WS09 y WS08 entregan catálogo y flujos; graph_ui y spec2viz aceptan sus deltas; WS12 consume el contrato. WS13, WS17, WS18, WS33, WS40 y WS41 quedan condicionados por esas salidas.
