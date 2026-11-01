REFORMULACION
Propósito: inventariar la UI de graph_ui y reconciliar el trabajo en curso —Board, tareas, git status y paneles herdr— mapeando cada nodo del plan que toque graph_ui a base reutilizada, delta, ticket o ausencia explícita.
Resultado: `auditoria/ui.md` con cada tarea externa (path, estado observado, SHA256 y alcance), cada solapamiento, la reconciliación del SPEC externo y del encargo aportado, y la tabla de mapeo por nodo.
Repo: dueño `deskops`; fuentes de lectura `../UIs/graph_ui` y `/home/jp/proyectos/softfactory_spec/SPEC.md`.
Límites: no cambiar tareas, Board ni sesiones; un commit solo prueba la base citada; las sesiones observadas son coordinación, no autoridad; promoción no autorizada.

AMBIGUEDADES
1. «registrando la correspondencia en auditoria/ui.md», mientras reconciliacion.md afirma que «auditorías WS02-WS04 ... aprobadas como inventario documental». Obliga a inventar si el ejecutor reescribe, amplía o solo verifica el ui.md ya aprobado, y cómo preserva su contenido y hash.
2. «reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan, con path y hash)». Obliga a inventar qué hacer si SPEC.md falta o no es legible, y si lo excluido expresamente en alcance.md cuenta como «ausencia» o como exclusión deliberada.
3. «ampliar historia solo si una referencia actual lo requiere». Obliga a inventar el criterio de suficiencia histórica y dónde termina la ampliación.

DRY-RUN
Lecturas previstas: dag.yaml, brief, alcance, decisiones, reconciliacion, cobertura y guía; Board, tareas, git status y código de graph_ui; commits a1b2b22/f16fcd1/134a665; SPEC.md; ui.md y approval.md existentes.
Cambios previstos: solo `auditoria/ui.md`; ningún cambio en tareas o Board de graph_ui.
Dependencias: WS01 y acceso de lectura a graph_ui/SPEC; SHA256 de cada archivo de tarea.
Validaciones futuras: tabla sin omisiones, tareas con path/estado/hash/alcance, solapamientos, SPEC con path/hash, encargo registrado o «no hubo».

FUTURO
WS06 consume el mapeo para reconciliacion.md; WS05 aporta el inventario Scion; el solicitante puede entregar el «encargo aportado»; la promoción exige preflight y autorización separada. Nada de esto se decide aquí.
