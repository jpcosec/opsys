## REFORMULACION
**Propósito:** cerrar el contrato de navegación e identidad del workspace documental.  
**Resultado:** `contratos/navegacion.md`, con identidad/origen, foco, enlaces/historia, lectura multidesk y clasificación de huecos, más mapa de recepciones por delta.  
**Repo dueño:** `deskops`.  
**Límites:** nodo de planificación; no implementa, no escribe actas interrepo, no afirma recibos recibidos, no habilita mutaciones ni depende de Changes, Scion o ViewDoc opcional.

## AMBIGUEDADES
1. «Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales citadas por auditorías WS02–04»  
   Exige APIs reales también para foco/historia, pero P07 establece «Foco/historia/disposición locales». Obligaría a inventar si foco/historia requieren API de store o son estado local documentado.

2. «WS11 cierra con contrato básico revisado»  
   No define revisor, criterio ni evidencia de revisión. Obligaría a inventar quién revisa y cómo se acredita el cierre.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` WS11 y dependencias; `decisiones.md`; `alcance.md`; guía/brief; auditorías WS02–04 por dependencia transitiva; `borradores/user-flows.md` de WS08; `borradores/vistas.md` de WS09.  
**Cambios previstos:** crear/actualizar solo `deskops:desk/drawer/plans/workspace-documental/contratos/navegacion.md`; enlaces a actas externas solo si ya existen.  
**Dependencias:** WS09/WS08; G_PRODUCT satisfecho; G_UI_READ pendiente por delta, no bloquea contrato base; G_SPEC_VIEW opcional y separado para WS18.  
**Validaciones futuras:** citar API/evidencia con path/símbolo/commit; clasificar cada hueco como instancia/vínculo/consulta/API/renderer con productor; mapear deltas graph_ui con actor P01, IDs y efectos; no declarar recibos.

## FUTURO
El receptor P01 produce las actas por delta; WS18 obtiene G_SPEC_VIEW; WS13/40/41 y demás deltas implementan o prueban; la promoción fija TaskDoc, archivos y evidencias.
