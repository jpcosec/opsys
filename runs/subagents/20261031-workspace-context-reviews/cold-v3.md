## Reformulación

**Objetivo**: revisar (no implementar) la calidad de los encargos del plan `desk/drawer/plans/workspace-documental/` — raíz, paquetes y candidatas WS01–WS44 — usando revisores baratos aislados que demuestren comprensión y produzcan dry-run, corrigiendo el texto de los briefs y descomponiendo nodos cuando corresponda.

**Resultado**: plan coherente (dag.yaml como fuente única), encargos corregidos/re-revisados, evidencia por nodo/intento bajo `runs/subagents/20261031-workspace-context-reviews/context-review/<node-id>/<sha>/attempt-<n>/` (input, manifest, output, stderr, receipt, disposition) y cierre por Tester independiente + supervisor. Sin producto ejecutado, sin decisiones Pxx inventadas, `execution_authorized=false`.

**Límites**: solo `plans/workspace-documental/`, `tasks/workspace-documental/` y la evidencia de esta tarea; helpers `.py` bajo ese plan; no `desk/rituals/`, `docs/`, skills; no tocar la otra tarea activa; no cerrar fase.

## Ambigüedades del encargo de revisión

1. **Esquema de jerarquía**: se exige escribir PK/ROOT/WSxx.n en dag.yaml "antes de revisión", pero no se da el esquema exacto ni quién lo define (¿coordinador, Executor, owner?). El encargo dice "el esquema se escribe" sin especificar forma ni validación previa.
2. **Criterio de corte para dividir**: "varias entregas separables" queda a juicio; no hay umbral verificable que distinga paquete legítimo de fragmentación innecesaria.
3. **Tester**: la tarea fija muestras obligatorias (WS01/07/11/12/…) pero no define formato de `validation.log` ni cómo computa "vigencia por hashes semánticos" más allá de la regla conservadora.
4. **"Guía breve de planificación"** se cita como fuente escrita, pero no se identifica ruta ni hash en el input.
5. **Input truncado**: el bloque `task-revisar-dag...` aparece sin cierre de comillas y con `files:`/`task_type`/`closeout_evidence` colgando; mi lectura asume el resto del TaskDoc fuera de este fragmento y no lo audito.

## Dry-run por roles (sin ejecutar)

- **Coordinador**: mapea raíz/paquetes/hojas; autora jerarquía en dag.yaml; por nodo arma input con brief+glosario+contratos de vecinos+fuentes (sin reviews previos); guarda contract.json canónico.
- **Executor**: lanza `pi --provider deepseek --model deepseek-flash --thinking low --offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools --system-prompt <rol> --print @input.md`; captura argv/versión/timestamps/hashes; compara reformulación con intención; dispone hallazgo (corregido / error reviewer / bloqueo).
- **Revisor barato** (cada proceso fresco): reformula propósito/resultado/límites, enumera ambigüedades, describe dry-run de lecturas/cambios/dependencias/validación; no ejecuta comandos ni edita.
- **Tester independiente**: verifica cobertura, vigencia por hashes, aislamiento y rúbrica en muestras; registra limitaciones.
- **Supervisor**: integración/cierre oficial; no cierra fase.

No ejecuté comandos ni edité archivos. No afirmo precio mínimo; el perfil flash es elección documentada, no medida global.
