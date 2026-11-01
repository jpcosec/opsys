# Disposición WS15.2, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Orientación para proyecto sin desk con ruta absoluta y `deskops init <ruta>`, nunca init por GET, refresco muestra el desk real tras init externo, repo graph_ui, depende de WS13: coincide.

**Ambigüedades.**

1. cómo se detecta «sin desk». Clase: `detalle de promoción`. el criterio exacto (ausencia de `desk/`, respuesta de ruta WS11) es del contrato de lectura WS11 y del TaskDoc; la aceptación («tras ejecutar init fuera de la UI, refrescar muestra el desk real») es comprobable.
2. qué es «refrescar». Clase: `detalle de promoción`. caso de prueba: recarga o control; la aceptación solo exige que tras refrescar se vea el desk real.
3. «la ruta absoluta del proyecto como destino». Clase: `no es ambigüedad`. el scope lo liga al comando: «la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`»; destino = argumento `<ruta>` mostrado como texto.
