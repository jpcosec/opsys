REFORMULACION
WS09 es un encargo de planificación de deskops: precisar el catálogo de renderizaciones en `borradores/vistas.md`. Propósito: inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes, dejando ViewDoc como grafo y no como contrato universal de UI. Resultado: cada fila de las tablas de `vistas.md` y su ficha con origen, contrato, renderer, acción/dueño, error y estado; distinguir authored/derivado/preferencia local; estado según WS10, disponibilidad desde `auditoria/ui.md` (WS04) y error visible esperado. Límites: solo documentación de planificación; no ejecutar, implementar UI, promocionar ni revisar vecinos; depende de WS07/WS10/WS08 y G_PRODUCT. Repo: deskops.

AMBIGUEDADES
1. «Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado» exige "contrato" por fila, pero brief.md dice que un documento «puede tener contrato estructurado o no» y vistas.md incluye «Issue Markdown sin modelo». No se aclara si "contrato" admite "sin contrato/no aplica" o exige modelo/contrato a filas Markdown, Code, issue o FAQ. Obligaría a inventar un contrato o a incumplir la aceptación.
2. «error = fallo visible esperado para esa fila» no define clase ni fuente del fallo: ¿error de UI, operación no soportada, backend/CDN, contrato ausente? Obligaría a inventar el error esperado y haría desigual la comprobación.

DRY-RUN
Lecturas: WS09, vistas.md, brief/alcance/decisiones/cobertura, `auditoria/ui.md` (WS04), salidas de WS10 y WS08, registro de WS07. Cambios: completar `borradores/vistas.md`; ningún código. Dependencias: G_PRODUCT, WS07, WS10 y WS08; WS04 transitiva. Validaciones futuras: campos por fila, clasificación, estado, disponibilidad, error y ficha; sin ejecución.

FUTURO
WS07 debe registrar Pxx/G_PRODUCT y responsables; WS10 fija definiciones de estado; WS08 aporta user-flows; WS04 la auditoría. La promoción y el TaskDoc fijarán archivos, pruebas y textos; WS11/WS18 consumirán el catálogo. Autorización humana pendiente.
