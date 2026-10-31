## REFORMULACION
**Propósito:** publicar en el deskops real la navegación documental validada, reutilizando el registry como inventario derivable.  
**Resultado:** `desk/README.md`, mapa/índices authored, átomos de acuerdos durables y acta de publicación en `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`, con commit por `deskops closeout commit`.  
**Repo:** `deskops`; no se escriben repos hermanos.  
**Límites:** enlazar todos los repos de `deskops list repositories` sin modificar sus repos; escribir en otro repo exige tarea y acuerdo de alcance; no imponer modelos nuevos; no publicar el ejemplo como ecosistema real; no atomizar permisos de sesión; P03–06 solo si el mapa expone operaciones.

## AMBIGUEDADES
Ninguna.

Las posibles dudas quedan resueltas por fuentes suministradas: P09 y el contrato de navegación fijan ubicación/modelo; WS30 enumera plantillas, paths y hashes; WS17 aporta las entradas; WS11/WS12 producen contratos; la ausencia de contrato se rige por «Reglas comunes de ejecución». Los detalles de archivos exactos, modelo definitivo, pills/átomos y preflight pertenecen a la promoción (`promotion: not_authorized`), no a este encargo.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS43, WS17, WS30, gates), guía, brief, alcance, decisiones y cobertura; contrato `contratos/navegacion.md` de WS11; contrato por delta de WS12; acta WS30; plantillas WS17; `desk/registry/repo-*.md`; átomos existentes.  
**Cambios previstos:** crear/actualizar `desk/README.md`; mapa/índices authored en deskops; átomos enlazados; acta de publicación; commit de cierre.  
**Dependencias:** WS17, WS30, WS11 (transitiva), G_HUMAN_MANUAL, G_PRODUCT satisfecho, G_WRITE_CONTRACT por delta para WS43.  
**Validaciones futuras:** resolver cada root/alias y enlace a path existente del repo enlazado; comprobar reutilización del registry; verificar átomos enlazados y correspondencia con paths/hashes del acta WS30; confirmar commit y acta; recorrido humano del participante P08. Los gates pendientes son intencionales.

## FUTURO
Producen otros nodos: WS17 las entradas/índices y sus paths; WS30 el acta con plantillas/paths/hashes validados; WS11 el contrato de navegación; WS12 el contrato técnico por delta; el humano P08 realiza el recorrido y la recepción. La promoción fijará archivos exactos, modelo/contrato, pills/átomos, evidencia y preflight en frío.
