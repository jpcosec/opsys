## REFORMULACION
- **Propósito:** integrar la edición de campos con conflicto visible y el alta/baja de relaciones permitidas por contrato, reutilizando editores y API existentes.
- **Resultado:** nodo `aggregate`; no ejecutable por sí mismo. Se cumple cuando WS19.1 y WS19.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS19.
- **Repo dueño:** `graph_ui`.
- **Límites:** delta sobre ticket draft; no crear semántica de relaciones en el componente; `workflow-protected fields` no editables por este canal; mutación solo en desk y modo manual exclusivo; promoción no autorizada; no duplicar trabajo en paralelo.

## AMBIGUEDADES
Ninguna.

El nodo distingue propósito, hijos, repo, dependencias y aceptación agregada. Las puertas pendientes son intencionales y tienen productor/resolver identificado: `G_HUMAN_READ` por WS16; `G_UI_WRITE` y `G_WRITE_CONTRACT` por WS12. Los detalles de archivos, pruebas y textos quedan delegados a la promoción/TaskDoc, conforme a la guía.

## DRY-RUN
- **Lecturas:** nodo WS19 y guía; fuentes citadas (`brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, `dag.yaml`). Los bloques `edge` se tratan solo como contratos vecinos; no se revisan.
- **Cambios previstos:** ninguno. Es revisión de encargo, sin ejecución ni edición.
- **Dependencias:** WS12, WS16, WS19.1 y WS19.2. Gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT` pendientes.
- **Validaciones futuras:** comprobar aceptación de WS19.1/WS19.2 y evidencia de gates; verificar whitelist/canal de WS12; confirmar que no se añade semántica de relaciones en UI ni se habilitan campos protegidos.

## FUTURO
- **WS19.1/WS19.2:** implementan y evidencian edición de campos y relaciones.
- **WS12:** produce contrato y resuelve `G_UI_WRITE`/`G_WRITE_CONTRACT`.
- **WS16:** produce `G_HUMAN_READ` con acta humana.
- **Promoción:** otro paso fijará archivos, pruebas y TaskDoc; hoy no está autorizada.
- **Humano:** designa responsables y acepta deltas; ninguna propuesta Pxx se considera aprobada aquí.
