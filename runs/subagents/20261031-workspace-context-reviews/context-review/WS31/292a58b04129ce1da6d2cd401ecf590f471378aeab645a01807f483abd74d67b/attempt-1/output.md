## REFORMULACION
Propósito: publicar el manual documental básico probado del workspace, integrando el índice y convención de WS10, capturas reales y limitaciones, con cada instrucción trazable a actas. Resultado: `docs/workspace-user-manual.md`, `docs/assets/workspace-user-manual/` y átomos vinculados en `desk/atoms/`. Repo dueño: deskops. Límites: solo lo demostrado por WS30/WS43; Scion queda propuesto hasta WS38; personalización/impacto propuestos salvo G_HUMAN_MODEL/WS29; no atomizar permisos ni aceptación inexistente; no bloquear el manual básico por extras.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: WS31 y vecinos en `dag.yaml`, `decisiones.md`, `borradores/manual.md`, acta WS30 en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md`, acta/commit de WS43 en `deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md`, `contratos/` del plan, manual y assets actuales, átomos existentes. Cambios previstos: redactar/actualizar el manual; añadir capturas reales; crear o enlazar átomos por cada Pxx vigente y cada contrato; etiquetar como propuestos Scion, personalización e impacto sin evidencia. Dependencias: G_HUMAN_MANUAL resuelto por WS30, índice de WS10 y publicación de WS43; contratos de WS11/WS12. Si falta un acta/contrato requerido, detenerse y registrar el hueco con repo dueño, sin sustituto. Validación esperada: links resolubles, etiquetas coherentes con actas/commits y atom→doc con fuente declarada; Tester independiente lo verifica antes del cierre. Errores: acta ausente, link roto o evidencia WS29/G_HUMAN_MODEL ausente; en extras se mantiene propuesto, en lo básico bloquea.

## FUTURO
WS30 ejecuta el protocolo humano y produce acta/G_HUMAN_MANUAL; WS10 entrega índice y convención; WS43 publica el mapa real con acta y commit; WS11/WS12 entregan `navegacion.md` y `operaciones.md`; WS39/WS29 aportan evidencia para capítulos extra y WS38 amplía Scion. La promoción de WS31 y su TaskDoc requieren autorización humana/ejecutora; no se hacen aquí.
