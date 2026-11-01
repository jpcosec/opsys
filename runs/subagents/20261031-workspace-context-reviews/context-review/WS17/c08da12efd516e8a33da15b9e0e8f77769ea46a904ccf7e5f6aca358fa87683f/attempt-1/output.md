## REFORMULACION

WS17 encarga escribir entradas e índices authored del desk de ejemplo como plantillas Markdown versionadas en deskops, bajo `ejemplo/nav/` del paquete del plan, para que el generador de WS40 las materialice en el corpus temporal. Nodo documental, no agregado. Resultado: plantillas curadas que enlazan documentos de los dos desks con desk del manifiesto WS40, sin copiar inventarios derivados, sin duplicar `desk/registry/repo-*.md` y sin escribir repos reales. Repo dueño: deskops. Depende de WS11 (identidad/root/store/aliases) y WS40 (generador/manifiesto); no es productor del corpus. Aceptación: regenerar con `ejemplo/nav/`, recorrer links sin UI, resolver cada link contra el manifiesto y comprobar que el conjunto cubre ambos desks; plantillas como fuente única, destino temporal regenerado y no editado como registro competidor. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas: `dag.yaml` WS17; `contratos/navegacion.md` de WS11; generador, parámetro de plantillas y manifiesto JSON de WS40; documentos clave del corpus; `desk/registry/repo-*.md` solo para evitar duplicarlo; brief/alcance. Cambios: crear plantillas Markdown en `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`, con enlaces/aliases del manifiesto, texto curado y cobertura de ambos desks; commit de plantillas en deskops. No tocar generador, corpus fuente ni repos reales. Dependencias: WS11 aporta resolución de identidad; WS40 acepta la ruta y emite roots/stores/commits. Gates: WS17 no declara `requires`; WS40 requiere `G_UI_READ` para producir el manifiesto. Errores: si falta contrato o parámetro/manifiesto, detenerse y registrar hueco con repo dueño, sin sustituir; si un link no resuelve o apunta al checkout real, corregir; si se copia registry o listado completo, rechazar. Validación: regenerar, recorrer links sin UI, verificar resolución contra manifiesto, cobertura de ambos desks y no duplicación; confirmar que el destino temporal se reconstruye desde las plantillas.

## FUTURO

WS30 validará manualmente UF01 y enumerará plantillas/paths/hashes en acta; WS43 mapeará esas entradas a la publicación real en deskops y fijará el mapa definitivo con `G_HUMAN_MANUAL/G_PRODUCT/G_WRITE_CONTRACT`. WS40 mantiene generador y manifiesto; WS16 consume el corpus para lectura. Nada de eso corresponde a WS17.
