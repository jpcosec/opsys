## REFORMULACION
**Propósito:** precisar UF01–UF10 como encargo de planificación, mapeando cada paso a operaciones auditadas en WS02/03/04 y a criterios observables. **Resultado:** `borradores/user-flows.md` (repo deskops) con seis campos por UF —entrada, salida, operación, error, nodo, gate humano—, huecos marcados con dueño y productor, sin prometer funciones fuera de `alcance.md`. **Repo:** deskops. **Dependencias:** WS07 (registro de decisiones reutilizable) y G_PRODUCT ya satisfecho; auditorías disponibles por vía transitiva vía WS06/WS07. **Límites:** no implementa UI, no habilita mutaciones ni dispatch; delegación solo documentada como condicionada a G_SCION/G_EXEC; no inventa operaciones, actores ni productores; `promotion: not_authorized`.

## AMBIGUEDADES
ninguna

## DRY-RUN
Un ejecutor futuro leería: nodo WS08 en `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `validacion-humana.md`, `cobertura.md`, `context-review-guide.md`, el borrador actual de `user-flows.md` y las auditorías `auditoria/{deskops,infraestructura,ui}.md`. Consumiría el registro emitido por WS07 y daría G_PRODUCT por satisfecho sin volver a pedir firmas.

Cambios previstos: editar únicamente `deskops:desk/drawer/plans/workspace-documental/borradores/user-flows.md`, completando o corrigiendo por UF los seis campos, citando `archivo.md:línea` para cada operación, marcando como hueco lo no auditado con `owner_repo` del nodo productor y su ID (o «sin productor en el DAG»), y ajustando nodos/gates a `dag.yaml` y `validacion-humana.md`. No tocaría `dag.yaml`, contratos ni actas.

Errores esperados: cita de auditoría inexistente → marcar hueco, no inventar; operación auditada pero no expuesta en UI → declararla como operación, no como capacidad; contrato/dato faltante con productor nombrado → no es ambigüedad, se registra el hueco.

Validación esperada: las diez UF presentes con los seis campos; cada operación con cita; cada hueco con dueño y productor; ningún gate humano distinto de WS16/30/37/39; WS29 tratado como prueba técnica; ninguna promesa de cierre HTTP, ack disponible, captura UI ni mutación interdesk; delegación condicionada. Cierre: aceptación comprobable por inspección del archivo; la promoción queda fuera del nodo.

## FUTURO
WS09 consumirá estas UFs para el catálogo de renderizaciones; WS11 usará huecos y enlaces para el contrato de navegación; WS12 tomará los productores de huecos operativos; WS16/WS30 usarán los recorridos como guion. La promoción del nodo exige preflight task-only y autorización humana, hoy no otorgada.
