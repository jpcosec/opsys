## REFORMULACION
**Propósito:** revisar si PK04 se entiende como encargo de revisión agregada: qué agrupa, cuándo queda listo y con qué límites.
**Resultado:** PK04 es una agrupación de revisión, no una entrega ejecutable; queda verdadera cuando cada hijo directo —WS17, WS18, WS22, WS23, WS24— tiene revisión vigente sin ambigüedad o bloqueo explícito con responsable.
**Repo:** PK04 no declara `owner_repo`; agrupa hijos de `deskops` (WS17), `spec2viz` (WS18) y `graph_ui` (WS22–24). Es revisión, no ejecución.
**Límites:** no revisar los bloques edge; no ejecutar; no evaluar producto; no resolver Pxx; no promover nodos.

## AMBIGUEDADES
1. «input y contrato actuales»: no define qué es el “contrato” de un hijo ni qué versión lo hace actual. Obligaría a inventar si se compara contra `dag.yaml`, el input de review o la aceptación del hijo, y cuándo una revisión queda obsoleta.
2. «según `context_review.py status`»: no indica repo, ruta, propietario ni esquema de salida de la herramienta. Obligaría a inventar desde dónde ejecutarla y cómo interpretar sus estados.
3. «disposición guardada»: no fija ubicación, formato ni quién la guarda. Obligaría a inventar el registro de disposición y su criterio de vigencia.

## DRY-RUN
- **Lecturas:** PK04 y sus cinco hijos en `dag.yaml`; guía; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`. No leer edges como contratos a revisar.
- **Cambios previstos:** ninguno en archivos del plan; solo la disposición de review de PK04 si el proceso la exige, sin ejecutar.
- **Dependencias:** estado `context_review` de cada hijo, herramienta `context_review.py`, revisor con acceso a disposiciones.
- **Validaciones futuras:** confirmar los cinco hijos; revisión vigente o bloqueo con responsable; uso de input/contrato actuales.

## FUTURO
Otros revisores producen el `context_review` de WS17/WS18/WS22/WS23/WS24; WS07 designa responsables; los gates `G_UI_READ`/`G_SPEC_VIEW` y las salidas de WS11/WS40 condicionan a los hijos; un humano confirma las Pxx. Nada de eso se resuelve aquí.
