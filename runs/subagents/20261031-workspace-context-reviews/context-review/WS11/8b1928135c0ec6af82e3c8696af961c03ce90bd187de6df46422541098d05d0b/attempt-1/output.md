## REFORMULACION
Propósito: cerrar el contrato de navegación e identidad para documentos, nodos, foco, enlaces/historia y lectura multidesk. Resultado: `contratos/navegacion.md`, clasificación de huecos con productor y recibos por delta; `G_SPEC_VIEW` queda separado y opcional. Repo dueño: `deskops`. Límites: solo planificación; no implementar UI ni modificar otras sesiones; no inventar modelos ni APIs; usar APIs reales y registrar huecos; no aprobar Scion, Changes ni ViewDoc.

## AMBIGUEDADES
1. «Registrar recepción lector por delta en graph_ui (actor P01, IDs, efecto y evidencia)» junto a «cada delta sigue bloqueado hasta su propio recibo». No se identifica qué delta concreto debe recibirse al cerrar WS11 —solo WS13.1 menciona `a1b2b22`, pero WS11 no lo nombra— ni si puede cerrar sin ningún recibo. Obligaría a inventar un delta, un commit o un bloqueo de cierre.

2. «owner_repo: deskops» frente a `output_scope`: «recibos G_UI_READ por delta; recepción G_SPEC_VIEW separada y opcional» y la aceptación «en graph_ui». No queda claro si WS11 escribe/commitea actas en `graph_ui` o solo las describe en `deskops`. Obligaría a inventar autorización para escribir en otro repo o un actor que registre el acta.

3. «G_SPEC_VIEW se obtiene separadamente al preparar WS18, sin bloquear navegación base» contradice el gate suministrado: `resolver: WS11`, `produced_by: WS11`. Si WS11 cierra sin obtenerlo, no se sabe quién lo produce después ni si WS11 debe seguir abierto. Obligaría a inventar el productor o el momento de cierre.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo WS11/gates en `dag.yaml`; los bloques edge se usan solo como dependencias, no se revisan. Cambios previstos: redactar el contrato de navegación, clasificar cada hueco como instancia/vínculo/consulta/API/renderer con productor, y preparar los registros de recepción. Dependencias: WS09 y WS08; `G_PRODUCT` ya satisfecho; APIs reales vía auditorías/WS02–WS10. Validaciones futuras: revisión humana P01, recibos `G_UI_READ` por delta y `G_SPEC_VIEW` al preparar WS18. Sin ejecución.

## FUTURO
P01 acepta deltas concretos; WS18 obtiene `G_SPEC_VIEW`; WS13/WS40/WS41 consumen el contrato; WS12 usa la resolución de repo/store para operaciones. Nada de esto se decide aquí.
