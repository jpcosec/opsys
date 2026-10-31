## REFORMULACION
**Propósito:** producir plantillas Markdown authored de entradas e índices para el corpus Taller. **Resultado:** fuentes versionadas en `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`, materializadas por el generador WS40 en un root temporal. **Repo dueño:** deskops; el corpus lo produce graph_ui (WS40). **Límites:** no es productor del corpus, no escribe repos reales, no copia inventarios derivados ni duplica el registry; solo contenido authored y navegación posterior a la entrada mínima de WS40.

## AMBIGUEDADES
1. **Alcance del contenido y cobertura de repos.** El título dice «entradas e índices del desk ejemplo» (singular), la aceptación exige resolver «los dos desks del manifiesto WS40» y cobertura.md asigna a WS17 índices para UF10, cuyo corpus incluye «un tercer repo temporal sin desk». Obliga a inventar si las plantillas cubren uno, dos o tres repos y qué índices mínimos son exigibles.
2. **Criterio de éxito ante la referencia rota deliberada.** La aceptación pide «recorrer links Markdown sin UI», mientras WS40 incluye «referencia rota» como parte del corpus. Obliga a inventar si esa referencia debe quedar rota, excluirse del recorrido o documentarse como error esperado; sin ello, «recorrer links» no fija aceptación comprobable.
3. **Soporte de la procedencia.** «Mostrar el root/store de procedencia al resolver los dos desks» no dice si se muestra en las propias plantillas, en un acta o en la salida del generador. Obliga a inventar dónde y cómo se materializa ese requisito.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, nodo WS17 y contratos vecinos WS11/WS40/WS30/WS43. **Cambios previstos:** crear plantillas Markdown bajo `ejemplo/nav/` en deskops; ninguna escritura en repos reales ni en el generador. **Dependencias:** contrato de navegación WS11 y generador/manifiesto WS40; TaskDoc de promoción fijará archivos y textos. **Validaciones futuras:** regenerar corpus WS40 con la ruta de plantillas, recorrer links sin UI, comprobar roots/stores de los desks y no duplicación del registry; después WS16/WS30 y publicación WS43. Sin ejecución.

## FUTURO
WS40 materializa las plantillas y emite el manifiesto; WS11 cierra el contrato de resolución; el TaskDoc fija archivos, pills y evidencia; WS30 valida UF01/UF08 y WS43 publica en el desk real. P08/P09 y la aceptación de P01/P02/P07/P09 corresponden a decisión humana.
