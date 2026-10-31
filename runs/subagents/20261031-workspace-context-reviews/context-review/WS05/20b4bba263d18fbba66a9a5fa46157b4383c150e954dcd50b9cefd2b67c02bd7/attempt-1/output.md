## REFORMULACION

**Propósito:** inventariar la identidad y la API pública de Scion como encargo de planificación, no como integración.
**Resultado:** `auditoria/scion.md` en `deskops:desk/drawer/plans/workspace-documental/`, separando slug/agente/intento/dispatch/mensaje/conversación y permisos, distinguiendo API pública de tablas/funciones internas.
**Repo dueño:** deskops. Lectura permitida en deskops y `../scion`; sin modificar Scion.
**Límites:** sin endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración; configuración solo sin secretos y sin mostrar tokens. WS05 no produce G_SCION.

## AMBIGUEDADES

Ninguna. El nodo define resultado, aceptación comprobable, repo, límites y consumidores; los huecos de API pública se registran, no se suplen. La ausencia de contrato de hash o de acceso real queda cubierta por alcance/WS44, no obliga a inventar en WS05.

## DRY-RUN

**Lecturas previstas:** guía, `dag.yaml`, brief, alcance, decisiones, cobertura; código/documentación de deskops y `../scion`; configuración sin secretos; `runtime/templates/RunDoc` y API documentada/exportada.
**Cambios previstos:** crear el inventario en `auditoria/scion.md`, señalando campos internos fuera de la API pública, capabilities requeridas por WS32/WS33 y límites que exigen API real.
**Dependencias:** WS01 como prerrequisito; consumidores WS44, WS32 y WS33; WS12 aportará después el contrato de registro por intento.
**Validaciones futuras:** aceptación del inventario; separación de conceptos y permisos; no usar tablas internas como interfaz; ausencia de secretos; mapeo de capabilities por nodo; registrar hueco si no hay API pública. No se ejecuta nada.

## FUTURO

WS44 ejecutará el probe read-only y producirá G_SCION. WS32/WS33 consumirán el inventario y fijarán capabilities concretas; WS12 definirá el contrato del registro por intento. La promoción de WS05 requiere TaskDoc con archivos, pills y evidencia, y revisión humana del encargo; nada de eso corresponde decidirlo aquí.
