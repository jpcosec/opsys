## REFORMULACION
WS08 es un nodo de planificación, no un agregado ni un producto ejecutable: debe precisar en `deskops:borradores/user-flows.md` el encargo de UF01–UF10, mapeando cada flujo a operaciones auditadas, entradas/salidas, errores, nodos del DAG y gates humanos. Límites: no inventar operaciones; marcar huecos con dueño/productor; no prometer funciones fuera de alcance; UF02 local, UF08 solo lectura; delegación condicionada a G_SCION/G_EXEC; distinguir WS29 de gates humanos.

## AMBIGUEDADES
1. «cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado»: el manual no aparece en `output_scope` ni en la aceptación, que solo exige campos por UF. Obligaría a decidir si se redactan capítulos de manual o solo se mapean pasos que luego alimentarán otro nodo, con riesgo de exceder el alcance del archivo.
2. «operación/nodo/gate admiten listas completas, no elegir nodo principal»: no se define el universo de completitud ni si basta con las operaciones usadas por el flujo frente a todas las auditadas. Obligaría a inventar un criterio de inclusión y a decidir qué nodos de `cobertura.md` son obligatorios en cada UF.

## DRY-RUN
Un ejecutor futuro leería `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `validacion-humana.md`, `borradores/user-flows.md` y las auditorías `deskops.md`, `infraestructura.md`, `ui.md`; verificaría el estado de G_PRODUCT mediante WS07. Editaría solo `borradores/user-flows.md`: completaría para cada UF los seis campos, citaría operaciones con `archivo:línea`, marcaría huecos con repo dueño y productor o «sin productor en el DAG», y asignaría gates humanos/WS29 según el protocolo. No ejecutaría código ni mutaciones. Si falta una auditoría o una operación declarada como insumo, se detendría y registraría el hueco, sin sustituirla. Validaría por inspección: UF01–UF10 presentes, seis campos en cada una, ninguna operación inventada, nodos existentes en `dag.yaml`, gates coherentes con `validacion-humana.md`, y ausencia de promesas fuera de `alcance.md`.

## FUTURO
WS09 usará estos flujos para el catálogo de vistas y WS11 para navegación; WS40 aportará el corpus y WS16/30/37/39 ejecutarán validaciones humanas. La promoción sigue `not_authorized`: requiere TaskDoc, archivos/pills/evidencia y preflight; la autorización humana o del workflow decide, no este revisor.
