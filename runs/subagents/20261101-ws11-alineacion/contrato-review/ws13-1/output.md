REFORMULACION

Propósito: emitir un dictamen de revisión de contrato (contract-review) sobre `navegacion.md` (WS11) como fuente de WS13.1, verificando que fija identidad, fuente propia, enlaces, foco y errores sin obligar a WS13.1 a inventar. Resultado: informe con hallazgos y veredicto de aptitud, no implementación. Repo: solo lectura del input (`desk/drawer/plans/workspace-documental/`); no se toca `graph_ui` ni `sldb`. Límites: sin herramientas, sin historial, sin ejecutar; un solo documento de salida; no sustituye el PASS del Tester ni el acta de P01.

AMBIGUEDADES

1. «contrato-review/ws13-1/input.md»: el input no declara explícitamente el nodo revisado ni el formato del veredicto; obligaría a inventar alcance y criterio de PASS.
2. «Estado: borrador […] No está revisado» frente a «Corregido el 2026-11-01 tras la revisión root»: no se sabe si el contrato es fuente válida para WS13.1; obligaría a inventar si un borrador corregido puede consumirse.
3. «se devuelve en la respuesta: el de la configuración confiable si el operador lo incluyó y, si no, `local`» junto a «No existe `?alias=local`»: se devuelve un alias no aceptable como parámetro; obligaría a inventar la semántica de `local` en respuestas e historia.
4. «Sin configuración confiable la identidad de 2.2 y la clave de 5.3 usan `local`» frente a «viaja como ausencia del parámetro»: obligaría a inventar cómo se serializa la clave sin alias.
5. «Que `surface` reconstruya el texto íntegro no está verificado» y «El mecanismo es de WS13.1»: obligaría a inventar cómo se cumple «mismo origen» en la aceptación de WS13.1.
6. «una identidad física normalizada tiene un alias canónico» sin definir normalización (solo `resolve()`): obligaría a inventar el criterio ante mayúsculas o symlinks.
7. «el Executor de la corrección no repitió esa comparación»: la equivalencia `215bf624`↔`c19c6c0d` se apoya en texto de revisión; obligaría a inventar si la base citada es válida.

DRY-RUN

El nodo es un paquete no ejecutable: no hay archivos que cambiar, solo un informe. Un ejecutor futuro leería el contrato y los extractos, contrastaría cada cita con lo que WS13.1 declara necesitar y marcaría los huecos H-01…H-06, H-12, H-14 como dependencias, no como cambios. Hijos: WS13.1 transfiere lectura y foco; WS13.2, explorador y lista de permitidos; WS13.3, clave de sesión; WS41, alias y enlaces entre desks; WS15.1, estados E1-E9. Validación conjunta: recibos por delta con `G_UI_READ`, PASS de Tester y revisión root. Gates: ninguna petición implementa sin acta.

FUTURO

Deciden otros: P01 registra actas; el operador suministra aliases y roots; root/P01 fijan la selección de ViewDoc; el consumidor prepara stores fuera del request; si falta capacidad, intake en `sldb`.
