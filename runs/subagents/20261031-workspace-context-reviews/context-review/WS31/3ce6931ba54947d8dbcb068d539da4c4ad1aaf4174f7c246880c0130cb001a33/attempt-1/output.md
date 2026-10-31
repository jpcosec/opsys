REFORMULACION
Propósito: publicar un manual documental básico ya probado. Resultado: `docs/workspace-user-manual.md` y átomos vinculados, actualizando índice, capturas y limitaciones. Repo dueño: `deskops`. Límites: solo capacidades demostradas; Scion queda como capítulo propuesto hasta WS38; personalización/impacto no bloquean el manual básico y se etiquetan según gate/prueba.

AMBIGUEDADES
1. «actualizar índice/capturas/limitaciones» frente a `output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados`: el índice vive en `borradores/manual.md` (WS10) y no aparece en el scope; obligaría a inventar si se edita el archivo de WS10 o se duplica el índice.
2. «Cada instrucción tiene evidencia vigente»: no define vigencia, formato ni ubicación de la evidencia; obligaría a inventar el criterio de aceptación y dónde registrarlo.
3. «desk/atoms/ vinculados» y «atom->doc verificados»: no enumera átomos ni criterio de vinculación; obligaría a inventar qué conocimiento durable crear y cómo mapearlo.

DRY-RUN
Lecturas: `dag.yaml` WS31 y gates `G_HUMAN_MANUAL`/`G_HUMAN_MODEL`; guía; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `borradores/manual.md`; contratos vecinos WS30/WS10/WS43 como dependencias. Cambios previstos: redactar/actualizar el manual y su índice/capturas/limitaciones; crear/enlazar átomos; etiquetar Scion y capítulos de personalización/impacto como propuestos si falta gate o prueba. Dependencias: WS30 produce `G_HUMAN_MANUAL`; WS10 fija índice/convención; WS43 publica el desk real. Validaciones futuras: evidencia por instrucción, etiquetas disponible/propuesto/bloqueado, links y `atom->doc`. Sin ejecución.

FUTURO
WS30 produce el acta de `G_HUMAN_MANUAL` en `graph_ui`; WS43 publica navegación del desk real con acta y commit; WS38 añade capítulos Scion verificados; WS39 y WS29 habilitan modelos e impacto; el humano resuelve Pxx y autoriza promoción/preflight.
