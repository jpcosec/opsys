## REFORMULACION

**Propósito:** inventariar, sin acceso vivo, la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos.

**Resultado:** `deskops:auditoria/scion.md`, con inventario, campos internos frente a API pública, capabilities y marca de las que requieren WS32/WS33.

**Repo dueño:** `deskops`; lee código y documentación de `deskops` y `../scion`.

**Límites:** solo lectura; no contacta endpoints vivos ni usa credenciales; no crea agentes, no envía mensajes ni modifica configuración; puede leer configuración sin secretos y no muestra tokens. No produce `G_SCION`; el probe es de WS44. Depende de WS01.

## AMBIGUEDADES

1. **«API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)»** y **«señalar los campos internos que no figuren en la API pública definida en el scope»**. El scope no fija precedencia ni criterio cuando documentación y exports difieren, ni aclara si un símbolo exportado pero no documentado cuenta como público. Obligaría a inventar la frontera público/interno que la aceptación exige aplicar.

2. **«puede leer configuración sin secretos»**. No acota repo, ruta ni tipo de configuración, ni define qué es «secreto» a efectos de redacción. Obligaría a inventar el perímetro de lectura y la regla de ocultación, con riesgo de exceder el alcance de solo leer `deskops` y `../scion`.

## DRY-RUN

- **Lecturas previstas:** brief/glosario de WS01; `runtime/templates/RunDoc` y documentación en `deskops`; código, documentación y exports públicos en `../scion`; configuración sin secretos.
- **Cambios previstos:** únicamente crear/editar `auditoria/scion.md`.
- **Dependencias:** WS01 como prerrequisito; WS32/WS33 solo como destino de la clasificación de capabilities.
- **Validaciones futuras:** revisar que no se usen tablas internas como interfaz; que el inventario separe las seis identidades y permisos; que marque campos internos y capabilities dependientes; que no exponga tokens. Nada se ejecuta aquí.

## FUTURO

- WS44 realizará el probe real y producirá `G_SCION`; requiere operador y acceso read-only registrados por el solicitante.
- WS32/WS33 consumirán el inventario para identidad de intento, dispatch, mensajes y decisiones.
- WS12 producirá el contrato del registro por intento que alimenta WS32.2.
