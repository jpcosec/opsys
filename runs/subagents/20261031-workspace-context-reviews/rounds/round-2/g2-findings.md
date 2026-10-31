### WS13.1 [1]
1. «Code local con selección por documento/nodo». No define qué se selecciona ni qué efecto observable tiene. La aceptación solo exige «alternar entre texto/graph/code» y preservar origen, no comprobar la selección por documento/nodo. El ejecutor tendría que inventar si seleccionar un documento/nodo actualiza Code, si seleccionar Code cambia foco o si es solo estado visual, y cómo demostrarlo.


### WS13.3 [2]
1. **Cobertura de pestañas en la aceptación.** Cita: alcance “Pestañas, dos documentos lado a lado…” frente a aceptación “Abrir dos documentos en divisiones…”. Obliga a inventar si abrir/cambiar/cerrar pestañas es requisito verificable o si basta con dos divisiones; la aceptación no dice cómo comprobar la parte de pestañas.
2. **Significado operativo de “foco” y “origen”.** Cita: “alternar foco y volver conservando origen e historia” y “Foco es por documento; cambiar de pestaña cambia el documento activo, no el foco guardado…”. El glosario define foco como elemento seleccionado, pero aquí puede leerse como panel/documento activo. Obliga a inventar qué acción concreta demuestra “alternar foco” y qué estado observable prueba conservar el origen al volver.


### WS14 [2]
1. «según auditoria/infraestructura.md y contrato WS11»: no se identifica qué nodo o actor produce `auditoria/infraestructura.md` ni se aporta su contenido. El ejecutor tendría que inventar si ese documento existe, quién lo emite y qué criterio de infraestructura aplica, o asumir sin base que WS11 lo cubre.
2. «Sin resultados, error de backend y búsqueda degradada se ven como tres estados distintos»: no se define qué sigue funcionando en «búsqueda degradada» ni qué la diferencia funcionalmente del error de backend. Con «no parser propio», el ejecutor tendría que inventar un fallback o el criterio de distinción entre ambos estados.


### WS16 [1]
1. «Incluye UF10 arranque/ausencia de desk» junto a «sin crear corpus propio», frente a WS40 («Crear dos repos temporales… sus stores») y validacion-humana («Proyecto Taller… con su propio git y desk/store temporal»; «Segundo desk temporal para UF08»). El corpus descrito no contiene un proyecto sin desk. El ejecutor tendría que inventar/crear ese fixture —corpus propio— o decidir omitir UF10; ninguna de ambas está autorizada.


### WS18 [2]
1. «output_scope: sldb/views/ (nombres confirmados por contrato)» — no se identifica qué contrato ni quién confirma esos nombres. Obliga a inventar la ruta/archivo exacto o a asumir que el contrato es `contratos/navegacion.md` de WS11, que no los enumera.
2. «Vista portable evaluada sobre store real» — no fija resultado observable ni criterio de paso/fallo de esa evaluación. Obliga a inventar qué significa «evaluada» (¿render?, ¿selección correcta?, ¿ambas?). El TaskDoc puede fijar escenarios, pero solo dentro de una aceptación que aquí queda indefinida.


### WS23 [1]
1. Cita: “obligaciones, transiciones y fuentes navegables”. “Obligaciones” no está definido en el glosario ni en la aceptación. Obligaría a inventar qué obligaciones debe mostrar la vista, de qué campo/documento salen y cómo se comprueba que están bien representadas.


### WS24 [5]
1. **“crossroads”**: «Reutilizar gráfico actual y documento genérico para átomos/protoátomos/crossroads/materializaciones/pills». No aparece definido en brief.md ni en el glosario. Obligaría a inventar qué entidad es y cómo se representa.

2. **“documento genérico”**: «documento genérico para átomos/protoátomos…». El glosario define “Documento” y “Vista de trabajo”, pero no este componente. Obligaría a inventar qué contrato o componente existente se reutiliza.

3. **Referencia normativa ausente**: «Backlinks = relaciones entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md». Ese archivo no consta en el input ni se identifica nodo que lo produzca. Obligaría a inventar la semántica de backlinks y la capacidad real de la API.

4. **Aceptación no comprobable**: «soporte no modelado visible». No define qué cuenta como “soporte no modelado” ni qué evidencia demuestra “visible”. Obligaría a inventar el criterio de aceptación.

5. **“tarea actual”**: «preservar Code local de tarea actual» y «Code local = proyección Code del ticket workspace». No se identifica la tarea concreta entre las draft de graph_ui. Obligaría a inventar el destino de integración.


### WS40 [3]
1. «Crear dos repos temporales bajo .tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «nunca toca desk real». Falta la base de `.tmp`: si cuelga de graph_ui, del cwd o de un desk. Obliga a inventar dónde se escribe y si eso contradice el límite.
2. «entrada mínima ecosistema/proyecto con enlaces al Board/FAQ/conocimiento». No se define si Board/FAQ/conocimiento son documentos Markdown, datos reales de Deskops (tareas/Board) o vistas. Obliga a inventar qué se enlaza y qué se crea en el corpus.
3. «usar contratos/CLI reales» no nombra el contrato ni los comandos concretos. Aunque WS11 es dependencia, el nodo no explicita que su contrato de navegación sea el aplicable ni qué CLI crea stores/commits; obliga a elegir interfaz.

