REFORMULACION
Propósito: encargar a `graph_ui` la integración de una búsqueda navegable del workspace usando la API real, sin parser propio. Resultado: búsqueda por teclado que abre un documento con identidad y ruta de origen, conserva consulta y foco al volver, y distingue sin resultados, error de backend y degradación. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/`, `tests/`. Límites: solo lectura según API real; no cargar todo el grafo en cada tecla; no duplicar el ticket workspace; promoción no autorizada. Dependencias: WS13 y `G_UI_READ` pendiente.

AMBIGUEDADES
1. «Sin resultados/error/degradación diferenciados.» Esta frase del scope puede leerse como que esos estados no deben diferenciarse, mientras la aceptación exige que «se ven como tres estados distintos». Obligaría a decidir si el scope niega o enumera los tres estados.
2. «resultados abren el documento con su identidad y ruta de origen» no se comprueba en la aceptación, que solo exige abrir/volver y conservar consulta/foco. Obligaría a inventar dónde se muestran identidad y ruta, o si basta con abrir el documento.
3. «no cargar todo grafo en cada tecla» no fija umbral ni forma de comprobación. Obligaría a inventar qué cuenta como “todo grafo” y cómo demostrar que no se carga en cada pulsación.

DRY-RUN
Lecturas previstas: nodo WS14, guía, brief, alcance, decisiones, cobertura y reconciliación; WS13 y `G_UI_READ` solo como dependencias. Cambios previstos: integrar búsqueda en `graph_ui` reutilizando auditoría WS03 y contrato WS11; UI de tres estados y navegación por teclado; sin parser propio. Dependencias: WS13, `G_UI_READ` (WS11), auditoría WS03, contrato WS11 y matriz WS06 transitiva. Validaciones futuras: recorrido buscar-abrir-volver con consulta/foco; tres estados; no cargar grafo por tecla; identidad/ruta si se acepta. Sin ejecutar.

FUTURO
WS03 produce la auditoría; WS11 el contrato y `G_UI_READ`; WS13 el lector, historia y foco; WS06 la matriz vía WS11/WS12. La promoción fijará archivos, pills, átomos y preflight. WS07 designa al responsable de `graph_ui`; WS16 hará validación humana. Las decisiones Pxx y los gates humanos no se resuelven aquí.
