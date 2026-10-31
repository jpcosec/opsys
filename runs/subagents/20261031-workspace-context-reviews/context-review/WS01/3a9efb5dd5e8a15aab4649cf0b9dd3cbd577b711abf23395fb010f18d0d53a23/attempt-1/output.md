## REFORMULACION
WS01 fija en `desk/drawer/plans/workspace-documental/brief.md` un brief y glosario autosuficientes: acuerdos textuales del solicitante y distinciones documento/nodo/vista/renderer/consulta/foco, sin remitir a chats invisibles. Resultado: `brief.md` editado en sitio. Repo dueño: `deskops`; `output_scope: brief.md`. Límites: no implementa UI ni modifica tareas de otras sesiones; la promoción no está autorizada.

## AMBIGUEDADES
1. «cada propuesta del registro Pxx remite a decisiones.md» — el brief solo dice «Ver decisiones.md». Obliga a inventar si basta una referencia global o se exige remisión individual por Pxx, y qué propuestas quedan cubiertas.
2. Título «Fijar brief y glosario autosuficientes» frente a aceptación «Un review barato sin historial reformula el producto solo con brief.md» — no hay criterio comprobable para declarar suficiente el glosario ni para verificar las distinciones enumeradas en el scope. Obliga a inventar cómo se prueba esa parte.

## DRY-RUN
Lecturas previstas: `context-review-guide.md`, `brief.md`, `decisiones.md`, `alcance.md` y el nodo WS01 en `dag.yaml`. Cambios previstos: solo `brief.md`; previsiblemente remisiones explícitas a `decisiones.md` por Pxx y refuerzo del glosario. Dependencias: ninguna. Validaciones futuras: revisión sin historial que reformule el producto usando solo `brief.md`; comprobar que cada cita identifique al solicitante y que cada Pxx remita a `decisiones.md`; no ejecutar nada.

## FUTURO
WS07 resuelve y registra las propuestas Pxx y designa actores; el humano autoriza la promoción y el preflight de tarea. WS02–WS05 consumen el brief como dependencia. Nada de eso se decide en WS01.
