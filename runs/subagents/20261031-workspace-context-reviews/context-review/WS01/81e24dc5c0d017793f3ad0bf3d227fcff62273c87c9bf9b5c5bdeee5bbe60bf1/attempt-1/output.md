REFORMULACION

Propósito: fijar `brief.md` como base autosuficiente de planificación, con acuerdos textuales y glosario que no dependan de un chat invisible. Resultado: `brief.md` editado en sitio. Repo dueño: `deskops`. Límites: solo se edita `brief.md`; no se implementa UI/API, no se modifican tareas de otras sesiones y no se introduce ningún requisito que remita a historial no suministrado.

AMBIGUEDADES

ninguna

DRY-RUN

Lecturas previstas: guía de revisión, nodo WS01 de `dag.yaml`, `brief.md`, `decisiones.md` para el registro Pxx y `alcance.md` para límites. Cambios previstos: editar únicamente `brief.md` para conservar las citas de autorización atribuidas al solicitante, fijar las distinciones documento/nodo/vista/renderer/consulta/foco y asegurar que las propuestas Pxx remitan a `decisiones.md`. Dependencias: WS01 no tiene `depends_on`; WS02–WS05 dependen de WS01. Validaciones futuras: review barato sin historial que reformule el producto solo con `brief.md`; comprobar citas al solicitante y referencias Pxx; verificar que no aparece dependencia de chat invisible. No se ejecuta nada.

FUTURO

WS02–WS05 consumirán el brief como base de sus inventarios. WS07 verificará y reutilizará `decisiones.md` sin volver a pedir firmas. La promoción humana o el TaskDoc fijarán archivos exactos, pills, átomos, evidencia y preflight; el recibo se verificará al promover auditorías. Nada de esto autoriza implementación, contratos API ni permisos Scion.
