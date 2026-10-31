REFORMULACION
Propósito: precisar el índice y la convención editorial del manual documental, fijando el ejemplo y las etiquetas de disponibilidad, y reutilizando el manual CLI. Resultado: `borradores/manual.md` actualizado como índice/convención, sin pasos ni capturas ficticias. Repo dueño: `deskops`; límites: solo capítulos conceptuales e índice, sin UI, implementación ni promoción; depende de WS02 y WS07/G_PRODUCT.

AMBIGUEDADES
1. Base de evidencia para “disponible”. Cita: «Las afirmaciones de capacidades se contrastan con WS02–WS04». El nodo solo declara `depends_on: WS02, WS07`; WS04 no está. Para cumplir «Definiciones verificables de disponible/propuesto/bloqueado», el ejecutor tendría que inventar si basta WS02 o si debe esperar/incorporar WS04. Es dependencia que falta y contradicción con la fuente suministrada.

DRY-RUN
Lecturas: `dag.yaml#WS10`; `manual.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; contratos WS02/WS07 solo como dependencias, sin revisarlos. Cambios previstos: editar únicamente `borradores/manual.md` — índice, convención por capítulo, referencia al ejemplo fijado, definiciones de etiquetas y enlaces al manual CLI. Dependencias: inventario WS02; decisiones WS07/G_PRODUCT, incluido P08; evidencia WS04 para disponibilidad; `docs/operator-manual.md`. Validaciones futuras: contraste de etiquetas con evidencia, ausencia de pasos/capturas ficticios; WS31 publicará el manual probado tras WS30/WS43. Sin ejecutar nada.

FUTURO
WS07/G_PRODUCT registra las decisiones humanas —P01/P02/P07/P08/P09 y `source_mode` P04— y fija el ejemplo; WS02 aporta el inventario; WS31 publica el manual probado; WS38 añade el capítulo Scion. Si se confirma WS04, un humano o WS07 debe reflejar su dependencia o retirar su mención antes de ejecutar WS10.
