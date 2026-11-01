## REFORMULACION

**Propósito:** separar identidad de intento y hechos de dispatch —intención local registrada frente a `confirmed` observado— en deskops, sin red, materializando el registro por intento que WS32.2 convertirá en manifiesto canónico.
**Resultado:** código y pruebas en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`; dos IDs locales distintos; registro intent/no confirmado; modelo registrado/validado por SLDB; RunDoc editado por API/CLI, no por Markdown ad hoc.
**Repo dueño:** deskops.
**Límites:** sin dispatch/reply de red ni evento Hub simulado; no inventa almacenamiento; contrato de registro según WS12; dependencias WS05/WS12; gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «Refinar el ticket de external_references.scion, sin segundo pipeline». El `output_scope` solo enumera código y tests, no el candidato del drawer. Obliga a decidir si el entregable es editar ese candidato —fuera del alcance y no autorizado— o implementar código; «sin segundo pipeline» no lo aclara.
2. «contrato de integración explícito». No indica productor ni si forma parte de la aceptación de WS32.1. Obliga a inventar quién lo redacta, cuándo y qué contiene.
3. «Dos intentos locales generan IDs distintos antes de dispatch» junto con «intento no es slug» y «SIN dispatch/reply de red». No define generación, formato ni alcance de unicidad del id, ni si «dispatch» debe modelarse como paso local pese a prohibirse la red. Obliga a inventar el esquema de identidad y el flujo.

## DRY-RUN

**Lecturas previstas:** nodo WS32.1, gates, `external_reference.scion`, guía, brief, alcance, decisiones, cobertura y reconciliación; contratos vecinos WS05, WS12, WS32 y WS32.2.
**Cambios previstos:** identidad de intento, registro local intent/no confirmado, modelo RunDoc y cierre en los archivos del `output_scope`; store temporal real; sin red.
**Dependencias:** WS05 aporta inventario Scion; WS12, contrato/ubicación del registro; WS32.2, manifiesto idempotente; WS34/37, correlación real. G_CLOSEOUT satisfecho; G_SCION no verificado; G_WRITE_CONTRACT pendiente por delta.
**Validaciones futuras:** dos IDs distintos; no etiquetar no confirmado como fallo/aceptado; registro/validación SLDB del modelo; sin simulación Hub ni dispatch de red.

## FUTURO

WS12 debe publicar el contrato/ubicación del registro por intento; WS05, el inventario de API; WS44 y el humano designado resolverán G_SCION. WS32.2 hará el manifiesto canónico; WS34/WS37 probarán dispatch real y correlación. La promoción de WS32.1 exige autorización humana y preflight task-only.
