## REFORMULACION
Propósito: revisar WS01 como encargo de planificación: fijar un brief y glosario autosuficientes. Resultado: `brief.md` enlazado a `decisiones.md` como registro Pxx, con acuerdos textuales con actor/fuente y vocabulario documento/nodo/vista/renderer/consulta/foco legible. Repo dueño: `deskops`; salida: `desk/drawer/plans/workspace-documental/brief.md`. Límites: no editar `decisiones.md`, no implementar, no cerrar lifecycle ni autorizar producto; solo reescribir brief si cambió realmente decisión/contrato; no revisar nodos vecinos.

## AMBIGUEDADES
1. «brief.md enlaza decisiones.md como registro Pxx completo»: no define si «enlaza» exige hipervínculo o basta mención, ni si «Pxx completo» requiere enumerar P01–P09 en el brief o solo remitir. Obliga a inventar formato y criterio de completitud.
2. «Acuerdos textuales tienen actor/fuente»: no aclara si «La persona» o «el solicitante» bastan como actor/fuente ni qué formato de fuente se admite. Obliga a inventar procedencia (nombre, ruta, tool call) no suministrada para las citas del brief.

## DRY-RUN
Lecturas previstas: nodo WS01, `brief.md`, `decisiones.md`, `alcance.md`, guía y hash de `covered_work`. Cambios previstos: ninguno por defecto; solo si se comprueba cambio de decisión/contrato, editar `brief.md` con acuerdos y vocabulario, sin tocar `decisiones.md`. Dependencias: sin `depends_on`; referencia interna a `decisiones.md`; la comparación del coordinator es externa; no se usan contratos de nodos vecinos. Validaciones futuras: coincidencia del SHA256 registrado, enlace/Pxx completo, términos del glosario legibles, actor/fuente de acuerdos y preflight de promoción.

## FUTURO
El coordinator compara reformulación/dry-run con la intención y explicita hallazgos/disposición; APTO no basta. La promoción y auditorías verifican hash/alcance con preflight task-only. Cualquier cambio real del encargo requiere registro/decisión y edición de `brief.md`; no produce autorización de producto ni lifecycle cerrado.
