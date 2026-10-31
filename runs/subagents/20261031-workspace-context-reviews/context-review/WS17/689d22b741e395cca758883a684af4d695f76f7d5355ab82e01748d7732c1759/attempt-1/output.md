REFORMULACION
- Propósito: redactar entradas e índices authored del desk de ejemplo como plantillas Markdown versionadas; no generar el corpus.
- Resultado: fuentes Markdown bajo `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`, consumibles por WS40 para materializarlas en su root temporal.
- Repo dueño: deskops.
- Límites: no ser productor del corpus; no copiar inventarios derivados; no escribir repos reales; no duplicar registry; WS30 integra después y WS16 no es prerrequisito.

AMBIGUEDADES
ninguna.

DRY-RUN
- Lecturas: nodo WS17, guía, brief, alcance, decisiones y cobertura; WS11, WS40, WS30 y WS43 solo como dependencias/contexto, sin revisar sus contratos.
- Cambios previstos: crear plantillas de navegación authored en `ejemplo/nav/`, con enlaces Markdown que permitan resolver dos desks y su procedencia.
- Dependencias: WS11 aporta contrato de navegación/identidad; WS40 aporta generador, manifiesto, segundo desk y materialización temporal. WS16 no bloquea; WS30 valida; WS43 publica.
- Validaciones futuras: regenerar corpus WS40 con `ejemplo/nav/`, recorrer enlaces sin UI, comprobar dos desks/procedencia, no duplicar registry y que fuente versionada y destino temporal no sean registros independientes. Sin ejecutar.

FUTURO
- WS11 cierra el contrato de navegación/identidad; WS40 implementa el generador y su manifiesto; WS30 integra los índices en la validación manual; WS43 resuelve la publicación real según P09 y sus gates. La promoción de WS17 exige preflight y autorización, no se ejecuta aquí.
