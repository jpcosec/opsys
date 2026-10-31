REFORMULACION
- Propósito: precisar el índice y la convención editorial del manual documental, con capítulos conceptuales, ejemplo fijo y etiquetas de disponibilidad.
- Resultado: `borradores/manual.md` actualizado con definiciones verificables de disponible/propuesto/bloqueado, sin pasos ni capturas ficticios.
- Repo dueño: `deskops`.
- Límites: nodo de planificación; solo `output_scope: borradores/manual.md`; no publica el manual final ni implementa UI; no escribe pasos/capturas ficticios; reutiliza el manual CLI; promoción no autorizada; depende de `G_PRODUCT`.

AMBIGUEDADES
1. Cita: «Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva por WS07.» El bloque suministrado de WS07 solo declara `depends_on: WS06`, no WS03/WS04. Esto contradice la afirmación del nodo y obliga al ejecutor a inventar de dónde obtiene las auditorías WS03/WS04, si debe esperarlas o si puede omitirlas.

DRY-RUN
- Lecturas previstas: guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, nodo WS10 y contratos WS02/WS07/gates; auditorías WS02–WS04 y `validacion-humana.md` si están disponibles; referencia al manual CLI existente.
- Cambios previstos: únicamente `borradores/manual.md`: fijar índice, convención, ejemplo y definiciones de etiquetas; no tocar `docs/workspace-user-manual.md`.
- Dependencias: WS02 aporta inventario comprobado; WS07/G_PRODUCT debe resolver decisiones; WS03/WS04 presentan la inconsistencia citada; WS31 consumirá este resultado.
- Validaciones futuras: comprobar que cada etiqueta remite a evidencia WS02, que no hay pasos/capturas ficticios, revisión del nodo y satisfacción de `G_PRODUCT` antes de ejecutar.

FUTURO
- WS07 y el actor humano resuelven P01–P09, incluido el ejemplo fijo y `source_mode`; `G_PRODUCT` queda registrado.
- WS31 publica el manual básico probado; el TaskDoc de promoción fijará archivos, evidencias y pills.
- Un humano debe aclarar la ruta de WS03/WS04 o corregir dependencias antes de ejecutar.
