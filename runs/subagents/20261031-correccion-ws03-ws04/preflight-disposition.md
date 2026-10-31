# Comparación del coordinador — corrección WS03/WS04, aceptada para despacho

Revisiones: preflight y cold v1–v3, cada una en proceso Pi nuevo, sin herramientas y con stdin DEVNULL. El alcance creció dos veces por hallazgos nuevos de la revisión independiente; por eso hubo tres rondas. `preflight.md` es la v1, conservada como historia; el insumo final es `preflight-v3-input.md` y `cold-v3-input.md`.

Las revisiones reproducen objetivo, seis puntos, límites y roles. Ninguna propuso tocar código ni WS06.

## Resoluciones sobre v3
- Los puntos se anclan por contenido, no por número de línea: ui.md:42 y similares son referencias a la versión previa.
- «Línea de encabezado» es la línea de corrección bajo el título; el párrafo de task.txt es otra cosa.
- WS18, WS19.2 y WS24 están definidos en dag.yaml. Puente demostrado = código que convierta lo editado en connect-dialog en una arista sin archivo físico, citado; si no aparece, se dice.
- De cada commit de ViewDoc se cita hash, fecha y asunto con `git log -1`, y sus archivos con `git show --stat`.
- Validaciones: las corre el Supervisor desde la raíz del repo deskops. La TaskDoc tocada por f16fcd1 se identifica por su stat.
- 35 nodos es el conteo de ui.md; WS18 se agrega como referencia sin cambiar ese conteo.
