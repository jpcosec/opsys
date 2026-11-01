## REFORMULACION
- **Propósito**: inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, sin confundir interfaces internas con API pública.
- **Resultado**: `auditoria/scion.md`, con campos internos fuera de la API pública y capacidades que exigen API real, marcando las que requieren WS32 y WS33.
- **Repo dueño**: `deskops`; lectura también en `../scion`.
- **Límites**: solo código/documentación/configuración sin secretos; sin endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración. WS05 no produce `G_SCION`; eso corresponde a WS44.

## AMBIGUEDADES
Ninguna. El encargo define resultado, aceptación comprobable, repositorio, límites y dependencia WS01. Las rutas exactas y el TaskDoc corresponden a la promoción; la ausencia de API pública se resuelve señalando el hueco, no inventando capacidades.

## DRY-RUN
- **Lecturas previstas**: `brief.md`, `alcance.md`, `decisiones.md`, `dag.yaml`; en `deskops`, runtime/templates/RunDoc; en `../scion`, documentación y SDK/endpoints públicos.
- **Cambios previstos**: ninguno durante este review. El nodo planifica escribir únicamente `auditoria/scion.md` al promoverse.
- **Dependencias**: WS01 como prerrequisito; acceso de lectura a `../scion`; sin `G_SCION` ni probe vivo.
- **Validaciones futuras**: revisar que el inventario no use tablas internas como interfaz, que separe las identidades y permisos, y que marque capacidades de WS32/WS33.

## FUTURO
- WS44 realizará el probe read-only real y podrá satisfacer `G_SCION`; requiere operador y acceso registrados por el solicitante.
- WS32/WS33 consumirán el inventario para sus contratos e implementaciones.
- La promoción fijará archivos exactos, pills, átomos y evidencias; el humano decide autorización y recepción por delta.
