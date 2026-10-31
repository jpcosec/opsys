## REFORMULACION

**Propósito:** cerrar el contrato de operaciones y escritura del workspace documental: whitelist de lectura/mutación por campo/modelo, adaptador CLI/API público y política de coordinador, Git, campos workflow-protected, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI.

**Resultado:** `contratos/operaciones.md` y evidencia de `G_WRITE_CONTRACT`, `G_UI_WRITE` y, si aplica, `G_SLDB_WRITE`.

**Repo:** `deskops` (`output_base: deskops:desk/drawer/plans/workspace-documental/`).

**Límites:** no implementar WS20; no asumir que el lock UI protege escritores CLI; toda operación sin contrato queda no disponible; autoría/cierre bloqueados por `G_CLOSEOUT`; no aprobar gates por inferencia.

## AMBIGUEDADES

1. **«WS07 ya aprobó principios»** contradice `decisiones.md` («Estado general: PENDING_OWNER») y el gate `G_WRITE_POLICY` con `state: pending`. Obligaría a inventar una aprobación humana inexistente.

2. **«la capacidad raw-source faltante se diseña y queda gated por G_SOURCE»**: `G_SOURCE` no aparece definido en el bloque `gates` suministrado, sin resolver, evidencia ni repo dueño. Obligaría a inventar ese gate y su autoridad.

3. **«aceptar delta en sldb solo si source_mode=editable. Con read_only, G_SLDB_WRITE no es prerrequisito»**: `source_mode` vale `pending` y no hay rama para ese valor. Obligaría a inventar si en `pending` se bloquea, se omite o se acepta el delta sldb.

## DRY-RUN

- **Lecturas:** guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS12 y contratos de vecinos.
- **Cambios previstos:** redactar `contratos/operaciones.md` con whitelist por campo/modelo, clasificación de APIs existentes/comprobadas/faltantes, política de escritura y evidencia de gates; sin tocar implementación.
- **Dependencias:** salidas de WS11/WS08; `G_WRITE_POLICY` de WS07; valor de `source_mode` por P04/WS07; actas de responsables graph_ui/sldb.
- **Validaciones futuras:** comprobar gate aprobado; verificar `source_mode`; registrar capability exacta por acción; confirmar deltas aceptados; mantener autoría/cierre bloqueados por `G_CLOSEOUT`.

## FUTURO

WS07 resuelve P01 y P03–P06 y produce `G_WRITE_POLICY`. Un humano decide P04 (`source_mode`). Los responsables graph_ui/sldb aceptan deltas. WS20 aporta evidencia raw-source o el hueco `G_SOURCE`. WS19, WS25, WS26, WS28, WS39 y WS42 consumen el contrato.
