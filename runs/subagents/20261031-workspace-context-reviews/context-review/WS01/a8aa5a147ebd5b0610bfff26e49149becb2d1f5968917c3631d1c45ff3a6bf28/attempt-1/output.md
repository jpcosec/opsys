REFORMULACION  
Propósito: dejar `brief.md` autosuficiente, con acuerdos textuales y un glosario que permita entender el producto sin historial de chat. Resultado: `brief.md` editado en sitio con las distinciones documento/nodo/vista/renderer/consulta/foco y remisiones explícitas. Repo dueño: `deskops`. Límites: solo `output_scope: brief.md`; no implementar UI, no modificar tareas de otras sesiones, no resolver Pxx y no ejecutar nada.

AMBIGUEDADES  
1. «Un review barato sin historial reformula el producto solo con brief.md». No define qué debe contener esa reformulación ni qué umbral la hace aceptable; obligaría a inventar criterios de suficiencia (propósito, superficies, recorridos, límites) para decidir si pasa.  
2. «Cada acuerdo de la sección «Encargo y acuerdos explícitos» cita al solicitante». La sección mezcla citas textuales y prosa de autorización; no aclara si «acuerdo» incluye solo blockquotes o también afirmaciones como «Esto autoriza corregir el plan…». Obligaría a inventar la clasificación y la forma de cita.  
3. «cada propuesta del registro Pxx remite a decisiones.md». No precisa si basta un enlace general o hay que enumerar cada Pxx en `brief.md`; obligaría a inventar cobertura y formato de remisión.

DRY-RUN  
Lecturas previstas: `brief.md`, `decisiones.md`, `alcance.md`, guía de revisión y nodo `WS01`; no revisar bloques edge vecinos. Cambios previstos: editar solo `brief.md`; reforzar glosario, citas de acuerdos y remisiones a decisiones. Dependencias: ninguna declarada en `depends_on`/`requires`; la aceptación usa el registro de decisiones ya suministrado. Validaciones futuras: review sin historial, comprobación de citas y remisiones Pxx, y verificación de que no se tocó otro archivo.

FUTURO  
WS07 y el actor humano resuelven las Pxx; el TaskDoc de promoción fijará archivos, pills y evidencia; la autorización de promoción no corresponde a este nodo.
