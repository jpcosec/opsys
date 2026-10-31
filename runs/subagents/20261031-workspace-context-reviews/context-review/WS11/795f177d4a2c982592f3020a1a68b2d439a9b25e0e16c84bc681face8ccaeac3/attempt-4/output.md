## REFORMULACION
**Propósito:** cerrar el contrato de navegación e identidad: resolver huecos como instancia, vínculo, consulta, API o renderer; fijar identidad/ruta/modelo opcional, resolución repo/store, foco, enlaces/historia y lectura multidesk read-only.
**Resultado:** `contratos/navegacion.md`.
**Repo:** `deskops`.
**Límites:** nodo de planificación; no implementa UI ni código; no introduce migración Kimun; no cierra sin aceptación de graph_ui y spec2viz; si falta recepción queda pendiente. Requiere `G_PRODUCT`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, definición WS11 y gates `G_PRODUCT`, `G_UI_READ`, `G_SPEC_VIEW`; WS08/WS09 solo como dependencias, sin revisar sus contratos.
**Cambios previstos:** redactar `contratos/navegacion.md`; si aparece API faltante, registrar hueco y dependencia acotada del repo dueño, sin implementar ni sustituirla.
**Dependencias:** WS08 y WS09 completos; `G_PRODUCT` resuelto por humano, con responsables de graph_ui/spec2viz designados en WS07 y P01/P07/P04 registrados.
**Validaciones futuras:** comprobar clasificación de cada hueco, resolución explícita repo/store, ausencia de migración Kimun implícita, cobertura de foco/enlaces/historia/multidesk y acta receptora con `scope_nodes` de `G_UI_READ`/`G_SPEC_VIEW`, incluidos WS40 y WS41 donde correspondan.

## FUTURO
WS07 debe producir la decisión humana y designar responsables; los dueños de graph_ui y spec2viz deben aceptar los deltas mediante acta verificable. WS12, WS13, WS18, WS40 y WS41 consumirán este contrato; una recepción ausente deja el cierre pendiente, no aprobado.
