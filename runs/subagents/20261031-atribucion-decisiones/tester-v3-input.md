Eres un Tester independiente de una fuente documental, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes. No corrijas nada.

Decisión que autoriza el cambio: runs/subagents/20261031-atribucion-decisiones/root-decision-20261101.md. Criterio anterior de root, en review-source.md de esa carpeta: la afirmación humana conserva solo lo aceptado en pregunta+respuesta, sin exigir copia literal; deben mantenerse IDs, literal de preguntas/respuestas, source_tool_call, decisiones, baseline/source_mode, restricciones, actores, gates y contratos.

Archivos: desk/drawer/plans/workspace-documental/decisiones.md (actual), runs/subagents/20261031-atribucion-decisiones/decisiones-antes-7b045a6f.md (versión previa a toda la corrección), desk/drawer/plans/workspace-documental/context-review-guide.md, runs/subagents/20261031-atribucion-decisiones/fuente-diff-pendiente.txt, y attribution-map.md de la misma carpeta con sus adendas.

Importante: una revisión anterior miró solo si lo Humano afirmaba de más y no vio que se había borrado un actor. Compara TODAS las columnas.

1. Tabla P01-P09: para cada fila, compara cada columna entre la versión previa y la actual. Lista todo lo que desapareció, y di si reaparece en otra parte con su fuente. Busca actores, condiciones, restricciones o nodos perdidos o cambiados.
2. Secciones fuera de la tabla: ¿cambió alguna?
3. P07/P09: ¿el actor registrado está restituido? ¿Algún texto lo presenta como autor o aprobador histórico? ¿Dice que la autoría inicial sigue sin localizar?
4. T-P03.1: abre dag.yaml 735 y 1327. ¿La fila solo explicita un productor ya comprometido? ¿Atribuye algo a un humano o al ítem 1? ¿Crea API, gate o mecanismo? ¿Declara exclusividad por ausencia de señal? ¿Cambia P03?
5. Guía: ¿el texto nuevo evita inducir secuencia entre hermanos sin arista? ¿Añade requisito de producto? ¿Contradice a un nodo agregado cuyo scope pide «transferencia entre hijos»? ¿La frase P01-P06/P08 sigue haciendo pasar precisiones técnicas por humanas?
6. Adendas: ¿dicen algo que no coincida con los archivos?

Informe: tabla con objeto, evidencia real (archivo:línea leído), PASS o FAIL; hallazgos; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
