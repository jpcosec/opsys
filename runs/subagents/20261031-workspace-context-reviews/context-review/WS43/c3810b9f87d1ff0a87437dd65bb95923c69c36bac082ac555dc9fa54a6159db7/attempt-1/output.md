## REFORMULACION
**Propósito:** publicar en el desk real de deskops la navegación documental validada en Taller. **Resultado:** `desk/README.md`, mapa/índices, átomos de acuerdos durables, acta y commit. **Repo:** deskops (`output_base: deskops:repository_root/`). **Límites:** no publicar solo el ejemplo, no escribir en repos hermanos, no imponer modelos nuevos, enlazar todos los repos de `deskops list repositories` sin modificarlos; entradas en otros repos exigen tarea y acuerdo de alcance. Depende de WS17/WS30 y de gates pendientes; promoción no autorizada.

## AMBIGUEDADES
1. «átomos de acuerdos durables» (output_scope) frente a un acceptance que no menciona átomos: no se define qué acuerdos son durables, de qué fuente salen (P09, `contratos/navegacion.md`, acta de WS30) ni si su ausencia bloquea la aceptación. El ejecutor tendría que inventar el conjunto y el criterio de verificación.
2. «Aplicar entradas/índices authored validados en Taller al deskops real»: el acceptance exige recorrer Markdown/UI y comprobar links/roots, pero no exige comparar que el mapa/índices publicados sean exactamente los validados en Taller; «no publicar solo ejemplo» no cubre una publicación divergente. Obligaría a inventar el criterio de equivalencia.
3. «Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance»: «proyecto adicional» no se define frente a «todos los de `deskops list repositories`» y «repos hermanos». El ejecutor debe decidir si un repo enlazado es adicional y si enlazarlo o detenerse.

## DRY-RUN
**Lecturas previstas:** dag.yaml, P09/P08/P01, `contratos/navegacion.md` (WS11), entradas WS17 materializadas por WS40, acta/gate de WS30, `deskops list repositories`, registry y desk actual de deskops, contrato de escritura de WS12. **Cambios previstos:** `desk/README.md`, mapa/índices según P09/WS11, átomos, acta en `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`, commit por `deskops closeout commit`. **Dependencias:** WS17, WS30; G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT pendientes. **Validaciones futuras:** recorrido humano del participante P08, links/roots verificables, no ejemplo-only, no escritura en repos hermanos, acta y commit.

## FUTURO
WS07 resuelve P01/P08/P09 y G_PRODUCT; WS12 produce G_WRITE_CONTRACT; WS30 produce G_HUMAN_MANUAL y su acta. La promoción fijará paths, modelo/contrato y payload de átomos. La autorización de promoción y la aceptación humana no las decide este revisor.
