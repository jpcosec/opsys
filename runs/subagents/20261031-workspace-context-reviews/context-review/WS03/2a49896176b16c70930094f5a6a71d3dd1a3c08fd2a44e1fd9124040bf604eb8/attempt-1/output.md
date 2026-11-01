REFORMULACION  
El nodo encarga una auditoría de solo lectura sobre sldb/pron/spec2viz para inventariar fuente/payload, conflictos y límites reales de locks, referencias documentales, búsquedas y alcance ViewDoc. El resultado es una salida documental en `auditoria/infraestructura.md`, con repo dueño deskops. Límites: sin cambios interrepo, Kimun solo como referencia y distinción explícita entre API comprobada mediante lectura citada, ausencia y hueco. No implementa ni modifica los repos auditados.

AMBIGUEDADES  
1. «Auditoría de solo lectura de sldb/pron/spec2viz» y «alcance real ViewDoc»: el glosario sitúa el evaluador, las rutas de evaluación/guardado y el render de ViewDoc en graph_ui, fuera de los tres repos enumerados. Obliga a inventar si graph_ui entra en la lectura o si «alcance real ViewDoc» se limita a la proyección de spec2viz; sin decidirlo, el alcance del inventario queda indefinido.  
2. «referencias documentales»: no precisa qué relaciones deben inventariarse (enlaces, citas, referencias entre documentos, referencias API-documento) ni su profundidad. Obliga a inventar el universo y el criterio de cobertura, que luego sostendrá la aceptación.

DRY-RUN  
Un ejecutor futuro, tras promoción y TaskDoc, leería WS01 (brief/glosario aceptados), `decisiones.md`, `alcance.md`, `dag.yaml` y `task-ws03.md`; después inspeccionaría en solo lectura sldb, pron, spec2viz —y, si se resuelve la ambigüedad 1, graph_ui— citando path/símbolo/commit observado. Crearía o actualizaría únicamente `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`. No tocaría repos auditados ni el Board. Dependencia directa: WS01; sin gates propios; `promotion: not_authorized` impide ejecutar hasta autorización y preflight task-only. Validaría que cada API afirmada tenga lectura citada, que ausencia y hueco estén separados y que el diff solo contenga el artefacto. Si falta acceso o un repo, registraría el hueco con dueño, sin sustituirlo. No hay pruebas runtime.

FUTURO  
Un humano/coordinador decide la promoción y fija el TaskDoc con archivos, pills, átomos y evidencia. WS06 consume el inventario como prerrequisito para reconciliación. La aceptación del artefacto corresponde a revisión humana/coordinación; el nodo no produce gate.
