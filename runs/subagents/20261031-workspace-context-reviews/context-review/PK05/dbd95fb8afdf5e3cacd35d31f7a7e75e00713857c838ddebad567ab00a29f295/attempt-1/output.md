REFORMULACION

Propósito: agrupar la revisión de los encargos de autoría y operación manual (entrega M), no ejecutarlos. Resultado: que cada hijo directo —WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30 y WS42— tenga `context_review` vigente con input y contrato actuales y disposición guardada; sin ambigüedad de encargo, o con bloqueo explícito que nombre responsable y dependencia. Repo dueño: no aplica a PK05, que es agrupación de revisión; cada hijo conserva el suyo. Límites: no es dependencia operativa ni entregable, no autoriza ejecución y no revisa las aristas de sus vecinos.

AMBIGUEDADES

ninguna.

DRY-RUN

Lecturas previstas: PK05; guía de context review; contratos de los nueve hijos; `decisiones.md` para P04 y gates; `cobertura.md` para el recorrido manual. Cambios previstos: ninguno; PK05 no se ejecuta ni modifica artefactos. Dependencias: `context_review.py status` y las disposiciones guardadas de cada hijo; vigencia de input y contrato de cada revisión. Validaciones futuras: comprobar que las nueve revisiones estén vigentes; que ninguna disposición reporte ambigüedad; que todo `status=blocked` incluya responsable y dependencia; no evaluar la calidad del producto ni el resultado de los hijos.

FUTURO

Las revisiones de los hijos producen sus disposiciones y el estado que PK05 consume. Los responsables nombrados en un bloqueo deciden cómo resolverlo. P04 (`source_mode`) y las aprobaciones P01–P09 corresponden a WS07/humanos y afectan a WS20/WS21, pero no son ambigüedad de PK05. La ejecución, promoción o aceptación de los hijos pertenece a otros nodos o al humano, no a esta agrupación.
