**Reformulación:** La tarea pide revisar recursivamente el plan `workspace-documental`: autorar en `dag.yaml` una jerarquía ROOT/PK, conservar WS01–WS44 y dividir en hijos WSxx.n cuando haya entregas separables; luego ejecutar reviews baratos aislados por nodo/intento, corregir encargos ambiguos y re-revisar, con evidencia hasheada. No se implementa producto, no se promueven candidatas, `execution_authorized=false`. Tester independiente valida muestras; supervisor integra/cierra. El reviewer barato solo reformula, señala ambigüedades y describe dry-run sin ejecutar.

**Ambigüedades que exigirían inventar (según input explícito):**
1. No está definida la partición exacta de WS01–WS44 en PK. “Agrupación por entregable/intención” no determina una asignación única; autorar PK/títulos/scopes requiere interpretar intención no escrita. Sin criterio verificable de agrupación, no puedo comprobar cobertura de paquetes.
2. En nodos partidos, “prerrequisitos originales pertinentes” no fija cómo repartir `depends_on`/`requires` entre hijos ni si un hijo puede depender de un hermano. Si la división es secuencial, falta regla explícita; inventarla alteraría contratos.
3. “Aceptación comprobable” y “brief autosuficiente” no tienen formato mínimo. Puede delegarse, pero el tester necesita estructura verificable para contrastar.

**Decisiones rutinarias delegadas / trabajo futuro (no ambigüedad):** redactar títulos/scopes/acceptance de ROOT/PK, `context-review-guide.md`, briefs por nodo, splits concretos, selección del modelo barato y disposición de hallazgos son decisiones delegadas al Executor/coordinador, documentables y revisables. Leer `dag.yaml`, `brief.md`, `decisiones.md`, etc.; ejecutar `build_plan.py --check`, `validate_plan.py --check`, reviews `pi`, tester y cierre son trabajo futuro explícito.

**Dry-run por roles, sin ejecutar:**
- **Executor:** leer fuentes explícitas; autorar jerarquía/guía/splits en `dag.yaml`; congelar esquema; construir inputs por nodo con fuentes/contratos y hashes; lanzar procesos `pi` aislados; registrar manifest/receipt; comparar, corregir y reintentar; regenerar proyecciones; no promover producto.
- **Reviewer barato:** recibir solo `input.md`; reformular propósito/resultado/límites; listar ambigüedades; describir lecturas, cambios propuestos, dependencias y validaciones futuras sin herramientas ni ejecución.
- **Coordinador:** comparar con intención escrita; aceptar/corregir/bloquear con cita; verificar vigencia por hashes; no aceptar “APTO”.
- **Tester:** subagente independiente; muestrear raíz, PK, hijos y WS indicadas; registrar `validation.log`; no editar plan/producto.
- **Supervisor:** integrar y cerrar; no cerrar fase.

No autorizo ejecución ni promoción; este dry-run solo prueba comprensión del encargo.
