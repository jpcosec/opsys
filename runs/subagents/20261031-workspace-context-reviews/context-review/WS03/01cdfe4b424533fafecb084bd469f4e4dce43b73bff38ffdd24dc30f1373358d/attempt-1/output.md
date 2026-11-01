REFORMULACION
WS03 encarga una auditoría de solo lectura de sldb, pron y spec2viz sobre persistencia —fuente/payload, conflictos y locks reales—, consultas/índices expuestos, referencias documentales y alcance efectivo de ViewDoc; Kimun queda solo como referencia. El resultado es un documento en `auditoria/infraestructura.md`, con repo dueño `deskops` y sin cambios interrepo. Debe distinguir API comprobada mediante lectura citada del estado actual, ausencia y hueco. Es un nodo `delivery` de planificación, no un agregado; su promoción no está autorizada y no implementa ni decide producto.

AMBIGUEDADES
1. «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco». No define qué separa «ausencia» de «hueco» ni el criterio de clasificación; el ejecutor tendría que inventar la taxonomía y la aceptación quedaría dependiente de un criterio no fijado.
2. «referencias documentales». No delimita si son enlaces entre documentos, rutas de origen, identificadores, citas o relaciones de modelo; el ejecutor tendría que inventar qué universo inventariar y cuándo considerarlo cubierto.

DRY-RUN
Hipotéticamente, tras promoción y TaskDoc, el ejecutor leería `brief.md`, `decisiones.md`, `alcance.md` y `dag.yaml`, y en solo lectura el código, documentación y contratos públicos de sldb, pron y spec2viz, citando paths y commits. Crearía o actualizaría `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`. Consumiría el brief/glosario de WS01; no hay gates propios ni evaluación `per_delta`. No modificaría los repos auditados. Si falta acceso o evidencia, registraría la ausencia o el hueco con repo dueño, sin crear sustituto. Validaría que el documento separa API citada, ausencia y hueco, y que no hay cambios interrepo; la aceptación final la revisa el coordinador.

FUTURO
WS06 consume esta auditoría para su matriz de correspondencia por repo dueño; WS11/WS12 pueden citarla como estado actual. La autorización de promoción, el TaskDoc y la aceptación corresponden al coordinador humano, no a una aprobación automática.
