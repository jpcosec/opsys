## REFORMULACION
- **Propósito:** cerrar, como encargo de planificación, el contrato de navegación e identidad del workspace documental.
- **Resultado:** `contratos/navegacion.md` con identidad/origen de documentos y nodos, foco, enlaces/historia, lectura multidesk read-only, clasificación de huecos (instancia/vínculo/consulta/API/renderer con productor dueño) y mapa de deltas que requieren recepción.
- **Repo:** `deskops`, bajo `desk/drawer/plans/workspace-documental/`.
- **Límites:** no implementar UI ni escribir actas interrepo; no aprobar Changes, Scion ni ViewDoc; el contrato básico puede cerrar sin acta receptora y cada delta queda bloqueado hasta su propio recibo.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodos WS11/WS09/WS08 y gates del `dag.yaml`; auditorías WS02–04 como dependencia transitiva.
- **Cambios previstos:** redactar `contratos/navegacion.md`; no tocar otros repos ni crear actas.
- **Dependencias:** WS09 aporta catálogo de renderizaciones; WS08, user-flows; WS02–04, APIs/evidencia vía cadena transitiva. `G_PRODUCT` figura satisfecho.
- **Validaciones futuras:** revisión de contexto; preflight de promoción y TaskDoc; recepción `G_UI_READ` por delta concreto; `G_SPEC_VIEW` solo al preparar WS18, sin bloquear navegación base.

## FUTURO
- El solicitante P01/receptor de `graph_ui` produce el acta de cada delta al prepararlo; WS11 solo enlaza actas ya registradas.
- WS18 obtiene `G_SPEC_VIEW` de forma separada.
- La promoción fijará archivos, pills y evidencia; nodos posteriores (WS13, WS40, WS41) consumen el contrato.
