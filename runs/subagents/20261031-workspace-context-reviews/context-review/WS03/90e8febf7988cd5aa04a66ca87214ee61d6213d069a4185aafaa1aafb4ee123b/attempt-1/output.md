## REFORMULACION
- **Propósito:** auditar en solo lectura `sldb/pron/spec2viz` para inventariar persistencia (fuente/payload), conflictos y límites de locks, referencias, búsquedas y alcance real de ViewDoc; Kimun solo como referencia.
- **Resultado:** un documento `auditoria/infraestructura.md` que distingue API comprobada, ausencia y hueco.
- **Repo dueño:** `deskops`.
- **Límites:** solo lectura, sin cambios interrepo ni implementación; depende de WS01. La promoción no está autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** `brief.md`, `alcance.md`, `decisiones.md` y el contrato del nodo; `task-ws03.md` al promoverse; repos `sldb`, `pron` y `spec2viz` en solo lectura; Kimun solo como referencia.
- **Cambios previstos:** producir/actualizar `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`; ningún cambio en los repos auditados.
- **Dependencias:** WS01 debe estar disponible para fijar vocabulario y acuerdos. WS06 consumirá esta auditoría. No hay gate propio en el nodo.
- **Validaciones futuras:** comprobar que la salida distinga API comprobada, ausencia y hueco; que no haya cambios interrepo; y que sea coherente con brief, alcance y decisiones. Sin ejecución.

## FUTURO
WS06 usará esta auditoría para registrar acuerdos de alcance con repos dueños; WS11/12 obtendrán aceptación específica. WS07 resolverá P01/P02/P04, entre otras, y un humano autorizará o rechazará las propuestas. Esas decisiones y la promoción de WS03 no son ambigüedades de este nodo.
