# R2 — claude: workspace documental

## Veredicto: REQUIERE CORRECCIONES

La revisión 2 mejora mucho y la estructura es sólida. Quedan un ciclo real de gates, flujos prometidos sin implementador y un corpus de validación sin productor. Son correcciones locales; no hace falta rehacer el DAG.

[V] verificado en archivos o código. [I] inferencia.

## Bloqueantes del plan

**B1. Ciclo oculto G_WRITE ↔ WS12 [V].** `decisiones.md` exige para G_WRITE la "política de campos aprobada". Esa política es la salida de WS12 (`dag.yaml`: whitelist por campo/modelo), y WS12 requiere G_WRITE y lo verifica. El validador no lo detecta: `build_plan.py` fija `producers['G_WRITE']='WS07'`, aunque el resolver declarado es "WS07/WS12".
*Corrección:* partir en G_WRITE_POLICY (WS07, P03–P06, requerido por WS12) y G_WRITE_CONTRACT (WS12, requerido por implementaciones). Derivar los productores del YAML.

**B2. El lector perdió el explorador [V].** `vision.md` promete explorador y divisiones, y UF01 "abrir al lado". WS13 no los incluye (no aparecen en `dag.yaml`), aunque `reconciliacion.md` llama a explorer un delta. WS16 no exige índices, así que solo queda la búsqueda como punto de entrada.
*Corrección:* añadir a WS13 explorador sobre soporte real y dos documentos lado a lado, con aceptación observable.

**B3. UF08 lectura se valida sin implementador [V].** `cobertura.md` lo asigna a WS13/14/15 y `validacion-humana.md` lo prueba en WS16, pero ninguna aceptación cubre abrir otro desk. Mindmap abre un store por proceso (`SLDB_STORE`).
*Corrección:* nodo o aceptación explícita tras WS11 para resolver el segundo desk en lectura.

**B4. Corpus Taller sin productor y con destino contradictorio [V].** El protocolo lo ubica en `.tmp/workspace-documental-ejemplo/`, temporal. WS17 escribe `ejemplo/` "versionado". WS16 lo necesita, con un segundo desk, pero no depende de WS17, y el corpus "se escribe al preparar WS16/17".
*Corrección:* nodo propio (generador reproducible, repo y ruta únicos) como prerrequisito de WS16; WS17 añade solo índices sobre ese corpus.

**B5. UF03 promete operaciones sin nodo [V].** UF03 dice "vincular, dividir o reunir". WS19 edita campos, WS24 navega y WS30 solo prueba "edición". `atoms split|merge` existen. El ticket de edición también cubría relaciones, ausentes en WS19.
*Corrección:* ampliar WS19 o crear un nodo para operaciones de conocimiento, o recortar UF03 explícitamente.

**B6. WS16 no gobierna lo que dice gobernar [V].** `alcance.md`: "WS16 valida antes de continuar". WS25 y WS39 dependen de WS16 sin requerir G_HUMAN_READ, y solo WS19 lo requiere. Un rechazo humano no detiene esos nodos. WS22–24 y WS26–28 ni siquiera van después de WS16, y WS26/28 mutan.
*Corrección:* G_HUMAN_READ para toda mutación (WS19, 25, 26, 28, 39). Lo demás: dejarlo explícito como paralelo y ajustar `alcance.md`.

**B7. G_UI se resuelve antes de que existan los deltas [V/I].** WS06 pide aceptación "por cada delta", pero precede a P01 (host), WS09, WS11 y WS12, que los definen. No está claro si WS06 cierra con G_UI pendiente, y WS07 depende de WS06. "Responsable graph_ui" no es un actor verificable. WS18 (spec2viz) y WS20 (sldb) no tienen aceptación del repo receptor, pese al título de WS06.
*Corrección:* WS06 solo propone matriz. Crear aceptaciones posteriores: lector tras WS11, escritura tras WS12, por repo receptor y con actor nombrado por el humano.

**B8. "Workspace activo" no existe [V].** WS13 dice "delta sobre workspace activo", WS19 "ticket activo". Los tres tickets están en `draft` y `frontends/mindmap/views/workspace/` no existe. `reconciliacion.md` admite que no están implementados, pero luego dice "reutilizar lector/grafo/código/contexto". WS13 es la base, o falta una arista hacia el ticket.
*Corrección:* WS06 decide por ticket si se absorbe o es prerrequisito; corregir "activo" por "draft".

## Correcciones menores

**M1. G_CLOSEOUT en WS12 contagia [V].** Bloquea 17 nodos, incluida captura/ack (WS25), contra `alcance.md` ("cada acción espera solo su contrato"). La tarea de closeout sigue activa.
*Corrección:* quitarlo de WS12; WS26, WS28 y WS32 ya lo requieren.

**M2. WS27 usa "intento" [V].** "Diff scoped al repo e intento" depende de un concepto Scion (WS32) en el flujo manual.
*Corrección:* "repo y tarea"; WS12 define la derivación del diff.

**M3. La alternativa de P04 no tiene salida [V].** Con fuente solo lectura, WS21 no cierra y bloquea WS30/31.
*Corrección:* rama de aceptación en WS21 condicionada a P04.

**M4. UF10 [V].** `cobertura.md` lo acepta en WS16, pero el scope de WS16 y el protocolo lo omiten.
*Corrección:* incluirlo en ambos.

**M5. UF08 envío frente a P07 [V].** "Sin mutación cruzada" choca con `message send` en WS30, que además no lista UF08.
*Corrección:* decidir en P07 y alinear el protocolo.

**M6. UF04 [V].** "Enrutamiento en Board" y "capa lista" no aparecen en WS22/26.
*Corrección:* asignarlos o recortarlos en WS08.

**M7. WS10 [V].** Fija "ejemplo fijo" sin G_PRODUCT, aunque el ejemplo lo decide P08. `manual.md` §17 sigue en UF01–UF08.
*Corrección:* añadir WS07/G_PRODUCT y actualizar a UF10.

## Gates futuros bien modelados (no son defecto)

G_PRODUCT, G_SCION, G_EXEC, G_SOURCE, G_HUMAN_*, y G_CLOSEOUT como bloqueo externo con evidencia. Que sigan pendientes es correcto. `execution_authorized: false` y las propuestas P01–P08 distinguen bien intención de decisión.

## Sugerencia opcional

Una fuente privada de mi contexto (plan en el home del dueño), **pendiente de corroborar en fuente compartida**, describe `runtime dispatch`, `CommentDoc`, CDN vendorizado y `closeout` fuera de la UI. Solapa WS34/WS27 y la exclusión del CDN en `alcance.md`. No es autoridad. Conviene que el humano confirme en WS04/WS07 si sigue vigente. El código no tiene aún `runtime dispatch` ni `CommentDoc` [V].

## Hallazgos previos resueltos

- **Producto y autoridad:** unidad y host (P01), Kimun (P02), coordinador (P03), fuente y campos (P04), git y cierre (P05), promoción (P06). Todos quedan formulados como decisiones con actor, no resueltos por inferencia.
- **Identificadores y vocabulario:** glosario, colisión C2, ViewDoc acotado a grafo, `registry.js`, dependencia del chat.
- **Referencias:** rutas actuales con hash; tickets y planes reconciliados de forma explícita.
- **DAG:** A1 antes de flujos y vistas (WS02–05 preceden a WS08/09), B2+C1 fusionados en WS11, C2 fuera del lector, closeout como gate, F1 partido en WS15/WS29, validación temprana WS16, repo único por nodo, tamaños relativos, `output_scope`, tabla generada.
- **Omisiones:** búsqueda (WS14), diff y evidencia (WS27), delegación con acciones (WS34/36), arranque (UF10, salvo M4), filas de `vistas.md`, manual de modelos (UF09/WS39).

**Parciales:** H10 dueños (falta actor de G_UI, ver B7); UF08 (B3); H1, resuelto como propuesta, pero la tensión con los tickets draft sigue (B8).
