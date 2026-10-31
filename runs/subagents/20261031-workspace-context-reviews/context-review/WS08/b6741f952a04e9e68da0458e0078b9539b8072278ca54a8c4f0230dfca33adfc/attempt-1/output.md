## REFORMULACION

**Propósito:** convertir los user-flows borrador en un mapa preciso y comprobable de UF01–UF10 como encargo de planificación, no como implementación.

**Resultado:** `desk/drawer/plans/workspace-documental/borradores/user-flows.md` actualizado: cada UF con entrada/salida, operación, error, nodo del DAG y gate humano; los huecos se marcan, no se inventan.

**Repo dueño:** `deskops`. **Límites:** no prometer funciones fuera de alcance, no habilitar Scion/G_EXEC, no mutar otro desk, no inventar operaciones ni contratos; G_PRODUCT ya está satisfecho. No se ejecuta nada.

## AMBIGUEDADES

1. **“cubrir manual, captura, revisión…”**  
   No se define qué es “manual” ni dónde se registra: ¿flujo dentro de `user-flows.md`, documento aparte, o solo referencia a pasos que validarán WS16/WS30? El `output_scope` solo admite `borradores/user-flows.md`. Obligaría a inventar el alcance y ubicación del manual.

2. **“cambios (UF07/WS29)”**  
   WS29 no figura en `depends_on` de WS08. Para mapear operaciones de cambios/impacto habría que asumir o inventar su contrato aún no producido; la aceptación exige operación por UF, aunque permite marcar hueco. Obligaría a decidir si se cita como hueco o como operación disponible.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (WS08 y vecinos), guía, brief, alcance, decisiones, cobertura, validación humana, `user-flows.md` y auditorías `deskops/infraestructura/ui` vía WS06/WS07.
- **Cambios previstos:** reescribir solo `borradores/user-flows.md`.
- **Dependencias:** WS07 concluido con registro P01–P09; G_PRODUCT satisfecho; operaciones desde auditorías transitivas. WS29 no es dependencia directa.
- **Validaciones futuras:** comprobar las 10 UF, campos exigidos, huecos con productor, gates correctos (WS16/30/37/39; WS29 como prueba técnica), delegación condicionada y ausencia de promesas fuera de alcance.

## FUTURO

WS09 consumirá estas UF para el catálogo de renderizaciones. WS11/WS12 producirán contratos y asignarán huecos. WS16/30/37/39 validarán con humano; WS29 tendrá prueba propia. La promoción y el TaskDoc fijarán archivos, textos y pruebas.
