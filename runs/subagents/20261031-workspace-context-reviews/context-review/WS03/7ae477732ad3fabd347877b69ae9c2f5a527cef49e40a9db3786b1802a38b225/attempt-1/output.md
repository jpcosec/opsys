## REFORMULACION
**Propósito:** auditar en solo lectura la persistencia, consultas y notaciones reales de sldb/pron/spec2viz, incluyendo fuente/payload, conflictos y control de concurrencia (CAS por revisión/hash, locks de archivo o DB), referencias documentales, búsquedas/índices expuestos y alcance real de ViewDoc. Kimun queda solo como referencia.
**Resultado:** un documento en `deskops:desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` que distingue API comprobada con lectura citada del estado actual, ausencia y hueco.
**Repo dueño:** deskops. **Límites:** sin cambios interrepo; no implementa, no corrige código, no promueve ni ejecuta tareas.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** `brief.md`, `alcance.md`, `decisiones.md`, `context-review-guide.md`, nodo WS03 y su dependencia WS01; código y documentación de sldb/pron/spec2viz en solo lectura.
- **Cambios previstos:** únicamente redactar `auditoria/infraestructura.md`; ningún cambio en repos auditados ni en el Board.
- **Dependencias:** WS01 aporta brief/glosario; WS06 consumirá esta auditoría para la matriz de correspondencia. No se requieren permisos de escritura interrepo.
- **Validaciones futuras:** comprobar que el documento existe, que cada capacidad citada remite al estado actual, que separa comprobado/ausente/hueco y que no hubo modificaciones interrepo. La aceptación formal y la promoción quedan fuera de este nodo.

## FUTURO
- WS06 usará la auditoría para reconciliar capacidades con repos dueños.
- Un humano decidirá la aceptación del delta y autorizará, si procede, la promoción del nodo.
- El TaskDoc de promoción fijará archivos, pills y evidencia; la ejecución autorizada ocurrirá en otro nodo.
- Cualquier contrato o API faltante se registrará como hueco con repo dueño, sin crear sustituto.
