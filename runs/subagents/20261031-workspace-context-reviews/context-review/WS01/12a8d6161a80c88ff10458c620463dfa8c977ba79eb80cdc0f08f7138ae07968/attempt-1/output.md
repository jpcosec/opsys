REFORMULACION
Propósito: fijar y verificar el brief/glosario autosuficientes de WS01. Resultado: `brief.md` enlaza `decisiones.md` como registro Pxx completo, sin editar `decisiones.md`. Repo dueño: `deskops`. Límites: solo `brief.md`; no reescribir sin cambio real de decisión/contrato; no cerrar lifecycle ni autorizar producto.

AMBIGUEDADES
1. «Si cambia realmente el encargo» y «no reescribir si no cambió decisión/contrato»: no definen umbral ni fuente para decidir si un cambio es “real”. Obligaría a inventar cuándo reabrir y editar `brief.md`.
2. «Coordinator compara reformulación/dry-run de review barato aislado ritual-context-review con intención y explicita hallazgos/disposición; APTO no basta»: no fija dónde se registra esa disposición ni qué la hace suficiente. Obligaría a inventar evidencia o formato de aceptación.
3. «Acuerdos textuales tienen actor/fuente» frente a «La persona solicita» y «Extractos textuales que delimitan intención»: los extractos del brief no identifican fuente verificable por cita. Obligaría a inventar la fuente o dar por cumplido sin ella.

DRY-RUN
Lecturas previstas: guía de revisión, `brief.md`, `decisiones.md`, nodo WS01 de `dag.yaml` y documentos de alcance/cobertura/visión ya incluidos. Cambios previstos: ninguno por defecto; si el hash de `covered_work` coincide, no tocar `brief.md`; solo editarlo ante cambio real y sin tocar `decisiones.md`. Dependencias: `depends_on: []`, `requires: []`; sin gates propios. Validaciones futuras: SHA256 de `brief.md`, enlace al registro P01–P09, actor/fuente de acuerdos textuales, distinciones del glosario y comparación del coordinator.

FUTURO
El coordinator o humano registra la comparación y disposición; la promoción sigue `not_authorized` y su TaskDoc/preflight fijará archivos, pills y evidencia. Otros nodos producirán las auditorías y WS07 verificará/reutilizará decisiones. Nada de esto se ejecuta aquí.
