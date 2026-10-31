## REFORMULACION

**Propósito:** refinar el ticket existente de `external_references.scion` para unificar identidad de intento y cierre Scion, sin crear un segundo pipeline.

**Resultado:** nodo agregado no ejecutable. Se considera cumplido cuando WS32.1 y WS32.2 cumplen su aceptación; sus dependientes siguen apuntando a WS32.

**Repo y modo:** `owner_repo: deskops`, salida en `deskops:repository_root/`; solapamiento con `scion`; integración `delta_or_existing_ticket`, `never_parallel_duplicate`.

**Límites:** promoción no autorizada (`promotion: not_authorized`); no ejecutar; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; alcance acotado a identidad de intento, dispatch intent/confirmed, manifiesto/RunDoc/cierre consistentes e idempotentes.

## AMBIGUEDADES

Ninguna.

El agregado tiene aceptación comprobable por estado de hijos; repo, límites y gates están nombrados; las dependencias directas e indirectas son coherentes. La posible redundancia de WS05/WS12 en `depends_on` no obliga a inventar ni altera la aceptación del agregado.

## DRY-RUN

- **Lecturas previstas:** nodo WS32 en `dag.yaml`; contratos de WS32.1/WS32.2; ticket `external_references.scion`; inventario WS05; contrato WS12; definiciones de gates; `task_file` y reglas de promoción.
- **Cambios previstos:** ninguno en esta revisión; no se promueve ni edita código. Una promoción futura exigiría TaskDoc, archivos/pills/átomos/evidencia y preflight task-only.
- **Dependencias:** WS05 y WS12 aportan inventario y contrato; WS32.1 y WS32.2 materializan el resultado. G_CLOSEOUT está `blocked`; G_SCION `unverified`, producido por WS44; G_WRITE_CONTRACT `pending`, producido por WS12.
- **Validaciones futuras:** aceptación de ambos hijos; consistencia e idempotencia del manifiesto/RunDoc/cierre; ausencia de pipeline paralelo; gates satisfechos; autorización de promoción.

## FUTURO

WS44 produce G_SCION mediante probe real; el resolver externo cierra G_CLOSEOUT; WS12 produce G_WRITE_CONTRACT. Las decisiones Pxx y la autorización de promoción corresponden a actores humanos. WS33 y los nodos de UI/dependientes consumirán WS32 cuando sus propios gates y contratos estén listos.
