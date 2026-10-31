REFORMULACION
Propósito: auditar en solo lectura sldb/pron/spec2viz para inventariar persistencia fuente/payload, concurrencia (conflictos y locks), referencias, búsquedas y alcance real de ViewDoc. Resultado: una salida documental en `auditoria/infraestructura.md` bajo el `output_base` de deskops, distinguiendo API comprobada, ausencia y hueco. Repo dueño: deskops; los repos auditados no se modifican. Límites: sin cambios interrepo, Kimun solo referencia, depende de WS01.

AMBIGUEDADES
1. «conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar)». No define qué es un «conflicto» (detección, resolución, solapamiento de escrituras) ni qué «límite» (timeout, granularidad, máximo, alcance). El ejecutor tendría que inventar las dimensiones del informe.
2. «referencias, búsquedas y alcance real ViewDoc». «Referencias» puede ser integridad referencial de DB, enlaces documentales o referencias de código; «búsquedas», API full-text, índices o consultas. Sin precisión, el ejecutor inventa qué inventariar y con qué evidencia.
3. «distinguir API comprobada, ausencia y hueco». No fija qué cuenta como comprobación (lectura de código, prueba ejecutada, documentación) ni qué revisión se audita; obliga a inventar el estándar de prueba y el snapshot de referencia.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, dag.yaml y, en solo lectura, código/config/docs de sldb/pron/spec2viz; salida de WS01. Cambios previstos: crear/actualizar únicamente `auditoria/infraestructura.md`; ningún cambio interrepo. Dependencias: WS01; acceso de lectura a los tres repos; no requiere WS05. Validaciones futuras: revisión de que el documento separa API comprobada/ausencia/hueco y de que no hay diff interrepo; WS06 consume el inventario; WS11/12 registran aceptación por repo.

FUTURO
WS07 designa responsables de repos y operador; el humano resuelve P01/P02/P04; WS06 usa esta auditoría para su matriz; WS11/12 aceptan por repo; WS12 fija la política de escritura a partir de los hallazgos. Nada de eso es ambigüedad de WS03.
