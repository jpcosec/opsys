REFORMULACION  
Propósito: publicar el manual documental básico ya demostrado. Resultado: `docs/workspace-user-manual.md`, `docs/assets/workspace-user-manual/` y átomos vinculados a decisiones/contratos vigentes. Repo dueño: `deskops`. Límites: no implementa UI ni modifica otros repos; no acredita Scion, permisos ni aceptación técnica inexistente; capítulos de personalización/impacto quedan propuestos si falta su evidencia; Scion solo como capítulo propuesto hasta WS38.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas previstas: `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, nodo WS31 de `dag.yaml` y, en promoción, `task-ws31.md` si existe. Cambios previstos: crear/actualizar el manual, sus assets y átomos enlazados; incorporar índice, capturas y limitaciones; marcar como propuesto lo no demostrado. Dependencias: WS30 aporta acta humana y recorridos; WS10 aporta índice/convención; WS43 aporta publicación real y acta; G_HUMAN_MANUAL debe estar resuelto por WS30. Validaciones futuras, sin ejecutar: que cada instrucción remita a acta WS30 o WS43; que etiquetas sean coherentes con actas/commits; que links resuelvan; que exista un átomo por Pxx vigente y por contrato inventariado, con fuente declarada y relación átomo→doc verificada; Tester independiente revisa antes del cierre.

FUTURO  
WS30 produce el acta de autoría/revisión manual y resuelve G_HUMAN_MANUAL. WS43 produce la publicación real, su acta y el mapa/índice validado. WS38 añadirá los capítulos verificados de delegación. WS29 y G_HUMAN_MODEL son evidencia opcional para capítulos de impacto/modelos; sin ella se mantiene etiqueta propuesta. La decisión humana sobre aceptación del manual corresponde al gate, no a este nodo.
