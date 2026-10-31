### WS17 [1]
1. «Registrar el root/store de procedencia al resolver los dos desks del manifiesto WS40; no duplicar el registry de deskops».
   Obliga a inventar el artefacto, formato y ubicación del registro: ¿va dentro de las plantillas versionadas, en un documento aparte o se relee del manifiesto WS40? Un root temporal no puede fijarse en plantillas reproducibles sin contradecir su materialización. La aceptación no define cómo comprobar ese registro ni quién lo produce.

### WS18 [2]
1. «no modificar su repo desde este plan» frente a «owner_repo: spec2viz» y «output_scope: sldb/views/ ... tests/». Obliga a inventar si la ejecución de WS18 puede escribir en spec2viz o solo preparar handoff; la frase puede leerse como prohibición de tocar el repo que el propio nodo declara como dueño.
2. «Vista portable (el mismo ViewDoc sin código específico del host) renderiza sobre un store real la selección declarada». No se nombra renderer ni harness, ni si WS18 debe construir uno; el scope solo habla de ViewDoc/NotationDoc y prohíbe UI pages. Obliga a inventar el medio de renderizado y el alcance del código de prueba.

### WS24 [3]
1. «Vecindad = hasta 2 hops.» No fija dirección ni tipos de arista: obliga a inventar si incluye relaciones entrantes, salientes o ambas, y si los backlinks cuentan dentro de la vecindad.
2. «es visible y navegable en la vista de documento genérica con su ruta de origen.» No define de dónde se obtiene esa ruta (ruta de archivo, identidad del store u origen declarado) ni qué mostrar si falta; obliga a inventar fuente y fallback.
3. «La vista muestra la clasificación (tipo y tags)» junto a «un soporte no modelado (Markdown sin modelo)», que no tiene tipo ni tags. No aclara si se muestra vacío, se omite o se etiqueta como no modelado; obliga a inventar ese estado.
