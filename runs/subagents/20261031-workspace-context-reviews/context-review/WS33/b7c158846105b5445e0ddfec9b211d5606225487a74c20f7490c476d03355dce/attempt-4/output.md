# REFORMULACION

**Propósito:** dejar WS33 (agregado "Vincular mensajes, resultados y decisiones") bien planteado como encargo de planificación: que un ejecutor sepa qué debe existir al cerrarlo y qué no puede inventar.

**Resultado:** comportamiento comprobable del agregado —vínculo Hub/proyecto/conversación/mensaje/intento deduplicado y con procedencia, y decisión humana explícita con actor— sin duplicar tablas ni transporte de Scion.

**Repo dueño:** deskops (`output_base: deskops:repository_root/`).

**Límites:** no es ejecutable por sí mismo; termina cuando terminan WS33.1 y WS33.2. Backend documental, independiente de editor UI. `promotion: not_authorized`. `overlap_with: scion` con `never_parallel_duplicate`. No crear sustituto si falta contrato (alcance.md, reglas comunes).

# AMBIGUEDADES

Ninguna.

Comprobado y descartado como ambigüedad según la guía:
- G_SCION `unverified`: gate pendiente intencional; su productor (WS44, operador designado en WS07) está nombrado y alcance.md fija qué hacer si falta.
- Detalles de archivos/pills/TaskDoc: delegados a promoción (`task_file` nombrado).
- Dependencia de hijos en el propio agregado: patrón consistente con WS32/WS34; la aceptación declara explícitamente que los dependientes siguen colgando de este ID.
- Clave de deduplicación: definida en WS33.1 (Hub + proyecto + id de mensaje) y heredada por el agregado.

# DRY-RUN

**Lecturas (sin ejecutar):** nodos WS33, WS33.1, WS33.2, WS32, WS11 y gates G_SCION/G_WRITE_CONTRACT/G_CLOSEOUT en dag.yaml; brief.md, alcance.md, decisiones.md, cobertura.md (UF06), reconciliacion.md; al promover, `desk/drawer/tasks/workspace-documental/task-ws33.md`.

**Cambios previstos:** ninguno; esta revisión no muta el plan.

**Dependencias:** WS32 (identidad de intento/cierre) y WS11 (navegación e identidad) son prerrequisitos reales; WS33.1/WS33.2 producen el agregado. G_SCION bloquea hasta probe público de WS44.

**Validaciones futuras:** agregado no ejecutable; importación repetida no duplica ni atribuye conversación completa; decisión con actor ligada al intento; `completed` nunca equivale a aprobado; no tocar tablas Scion; preflight task-only y evidencia en promoción.

# FUTURO

- WS07 designa operador Scion; WS44 produce y puede revalidar G_SCION.
- WS06 aporta la matriz de reutilización de forma transitiva vía WS11/WS12.
- Salidas de WS33.1/WS33.2 alimentan WS34 (dispatch/reply) y WS35 (lectura en workspace, con G_UI_READ).
- Un humano autoriza la promoción (`deskops add task`); ninguna aprobación se infiere.
