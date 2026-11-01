REFORMULACION
WS03 encarga una auditoría de solo lectura sobre sldb/pron/spec2viz: inventariar persistencia fuente/payload, control real de concurrencia, referencias documentales, búsquedas expuestas y alcance ViewDoc; Kimun solo como referencia. El resultado es `auditoria/infraestructura.md` en el repo dueño `deskops`. Límites: no modificar otros repos, no implementar, no promover; toda afirmación debe distinguir API comprobada, ausencia y hueco.

AMBIGUEDADES
1. «Inventariar persistencia, consultas y notaciones» (título) frente a «alcance real ViewDoc» (scope). No se define qué abarca «notaciones» ni si incluye layout/sintaxis de spec2viz además de ViewDoc. El ejecutor tendría que inventar el catálogo de notaciones y su profundidad.
2. «distinguir API comprobada (lectura citada del estado actual), ausencia y hueco» (acceptance). No hay criterio para separar «ausencia» de «hueco». El ejecutor tendría que inventar la clasificación y podría archivar de forma no uniforme una capacidad no encontrada.

DRY-RUN
Lecturas: `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `task-ws03.md` y código/documentación de sldb/pron/spec2viz en modo lectura. Cambios previstos: crear o actualizar `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`; ningún cambio de código ni interrepo. Dependencia: WS01 debe aportar brief/glosario; no hay gates propios ni promoción autorizada. Si falta un repo, API, dato o permiso, debe detenerse y registrar el hueco con repo dueño, sin crear sustituto. Validación esperada: salida documental única, citas verificables del estado actual, concurrencia real, búsquedas, ViewDoc y separación comprobado/ausente/hueco; sin cambios interrepo. WS06 consumirá esta auditoría para su matriz.

FUTURO
WS06 usa el inventario; WS11/WS12 y los receptores P01 deciden contratos y actas. La promoción, el TaskDoc, la aceptación humana y cualquier implementación corresponden a otros nodos o al solicitante, no a WS03.
