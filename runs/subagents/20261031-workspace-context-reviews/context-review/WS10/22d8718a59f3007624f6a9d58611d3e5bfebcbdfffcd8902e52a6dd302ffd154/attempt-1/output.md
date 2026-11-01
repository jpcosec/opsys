REFORMULACION
Propósito: fijar en el manual el índice y el esquema conceptual de capítulos (propósito, entradas, salidas), las definiciones de disponibilidad y un ejemplo fijo, sin redactar el manual completo ni inventar pasos/capturas. Resultado: `borradores/manual.md` actualizado y contrastado con auditorías. Repo: `deskops`. Límites: solo ese output; reutiliza el manual CLI; Taller es corpus futuro hasta WS40; no implementa UI ni escribe pasos ficticios.

AMBIGUEDADES
ninguna

DRY-RUN
Un ejecutor futuro leería `borradores/manual.md`, `auditoria/deskops.md` (WS02), auditorías WS03/WS04 (`infraestructura.md`, `ui.md`), `decisiones.md` (WS07), la entrada WS40 y `docs/operator-manual.md`. Editaría solo `borradores/manual.md`: ordenaría índice y fichas por propósito/entradas/salidas; registraría las definiciones disponible/propuesto/bloqueado; mantendría Taller como `graph_ui:.tmp/workspace-documental-ejemplo/`, productor WS40 y corpus futuro; remitiría pruebas/actas a sus productores; conservaría referencias al manual CLI; ajustaría estados según auditorías sin crear pasos ni capturas. Dependencias: WS02 y WS07; WS03/WS04 transitivas; G_PRODUCT ya satisfecho. Validaría que las definiciones estén, que no haya pasos/capturas ficticios, que el ejemplo fijo conste y que el contraste actual cite auditorías. Si falta una auditoría o dependencia, se detendría y registraría el hueco; si WS40 no existe, mantendría “corpus futuro”. No ejecutaría nada.

FUTURO
WS40 produce Taller; WS30 aporta acta humana; WS31 publica el manual e incorpora el índice; WS09 consume los estados de disponibilidad. La promoción de WS10 requiere TaskDoc/preflight de otro nodo; no hay nueva firma humana ni aprobación de implementación.
